#!/usr/bin/env python3
"""
Doc Updater - Automatically updates all project documentation
Every agent action triggers doc updates
"""

import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional

class DocUpdater:
    """Automatically updates project documentation"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.docs = {
            'PROJECT': self.project_dir / 'PROJECT.md',
            'ARCHITECTURE': self.project_dir / 'ARCHITECTURE.md',
            'CHANGELOG': self.project_dir / 'CHANGELOG.md',
            'DECISIONS': self.project_dir / '.buildmate' / 'decisions.md',
            'RESEARCH': self.project_dir / '.buildmate' / 'research.md'
        }
        
        # Ensure .buildmate dir exists
        (self.project_dir / '.buildmate').mkdir(parents=True, exist_ok=True)
    
    # ============ PROJECT.md Updates ============
    
    def create_project_doc(self, name: str, description: str, answers: Dict[str, str]):
        """Create initial PROJECT.md"""
        content = f"""# {name}

## Goal
{description}

## In Scope
<!-- Coder updates this as features are implemented -->
- [ ] Initial setup

## Out of Scope
<!-- Architect defines boundaries -->
- [ ] Future features not in MVP

## Constraints
<!-- Based on user answers -->
- Audience: {answers.get('audience', 'Unknown')}
- Tech: {answers.get('tech', 'Not specified')}
- Timeline: {answers.get('timeline', 'Not specified')}

## Current Status
**Phase:** Planning  
**Last Updated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}

## Completed
<!-- Auto-updated by Coder -->
_None yet_

## Blockers
<!-- Auto-updated when issues found -->
_None_

## Key Decisions
<!-- Links to DECISIONS.md -->
See [decisions.md](.buildmate/decisions.md)
"""
        self._write_file(self.docs['PROJECT'], content)
    
    def update_project_status(self, phase: str, completed_items: list = None, blockers: list = None):
        """Update PROJECT.md status section"""
        if not self.docs['PROJECT'].exists():
            return
        
        content = self.docs['PROJECT'].read_text()
        
        # Update phase
        content = re.sub(
            r'\*\*Phase:\*\* \w+',
            f'**Phase:** {phase}',
            content
        )
        
        # Update timestamp
        content = re.sub(
            r'\*\*Last Updated:\*\* .+',
            f"**Last Updated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}",
            content
        )
        
        # Update completed items
        if completed_items:
            completed_section = "\n".join([f"- [x] {item}" for item in completed_items])
            content = re.sub(
                r'## Completed\n<!--[^>]+-->\n.+?(?=\n## |$)',
                f'## Completed\n<!-- Auto-updated by Coder -->\n{completed_section}\n',
                content,
                flags=re.DOTALL
            )
        
        # Update blockers
        if blockers:
            blockers_section = "\n".join([f"- ⚠️ {b}" for b in blockers])
            content = re.sub(
                r'## Blockers\n<!--[^>]+-->\n.+?(?=\n## |$)',
                f'## Blockers\n<!-- Auto-updated when issues found -->\n{blockers_section}\n',
                content,
                flags=re.DOTALL
            )
        
        self._write_file(self.docs['PROJECT'], content)
    
    def add_to_scope(self, item: str):
        """Add item to In Scope section"""
        if not self.docs['PROJECT'].exists():
            return
        
        content = self.docs['PROJECT'].read_text()
        
        # Find In Scope section and add item
        if '## In Scope' in content:
            content = content.replace(
                '## In Scope\n<!-- Coder updates this as features are implemented -->',
                f'## In Scope\n<!-- Coder updates this as features are implemented -->\n- [x] {item}'
            )
            self._write_file(self.docs['PROJECT'], content)
    
    # ============ ARCHITECTURE.md Updates ============
    
    def create_architecture_doc(self, tech_stack: list, structure: str):
        """Create initial ARCHITECTURE.md"""
        content = f"""# Architecture

## Tech Stack
<!-- Auto-updated by Architect -->
{chr(10).join(['- ' + t for t in tech_stack])}

## Folder Structure
```
{structure}
```

## Data Flow
<!-- Architect updates this -->
_TBD_

## API Design
<!-- Architect updates this -->
_TBD_

## Decisions
<!-- Links to DECISIONS.md -->
See [decisions.md](.buildmate/decisions.md)

Last Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}
"""
        self._write_file(self.docs['ARCHITECTURE'], content)
    
    def update_architecture_section(self, section: str, content_update: str):
        """Update a specific section of ARCHITECTURE.md"""
        if not self.docs['ARCHITECTURE'].exists():
            return
        
        content = self.docs['ARCHITECTURE'].read_text()
        
        # Update specific section
        pattern = rf'(## {section}\n<!--[^>]+-->\n).+?(?=\n## |Last Updated|$)'
        replacement = rf'\1{content_update}\n'
        
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Update timestamp
        content = re.sub(
            r'Last Updated: .+',
            f"Last Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}",
            content
        )
        
        self._write_file(self.docs['ARCHITECTURE'], content)
    
    # ============ CHANGELOG.md Updates ============
    
    def create_changelog(self):
        """Create initial CHANGELOG.md"""
        content = f"""# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - {datetime.now(timezone.utc).strftime('%Y-%m-%d')}

### Added
<!-- Auto-updated by Coder -->

### Changed
<!-- Auto-updated by Coder -->

### Fixed
<!-- Auto-updated by Coder -->

"""
        self._write_file(self.docs['CHANGELOG'], content)
    
    def add_changelog_entry(self, entry: str, category: str = "Added"):
        """Add entry to CHANGELOG.md"""
        if not self.docs['CHANGELOG'].exists():
            self.create_changelog()
        
        content = self.docs['CHANGELOG'].read_text()
        
        # Find the right section and add entry
        section_pattern = rf'(### {category}\n<!--[^>]+-->)(\n)'
        replacement = rf'\1\n- {entry}\2'
        
        content = re.sub(section_pattern, replacement, content)
        
        self._write_file(self.docs['CHANGELOG'], content)
    
    # ============ DECISIONS.md Updates ============
    
    def create_decisions_doc(self):
        """Create initial decisions.md"""
        content = f"""# Decisions

This log tracks key architectural and implementation decisions.

## Format
- Date: YYYY-MM-DD
- Decision: What was decided
- Context: Why this choice
- Consequences: Impact

---

## Decision Log

"""
        self._write_file(self.docs['DECISIONS'], content)
    
    def log_decision(self, decision: str, context: str, consequences: str = ""):
        """Log a new decision"""
        if not self.docs['DECISIONS'].exists():
            self.create_decisions_doc()
        
        date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        entry = f"""### {date}: {decision}

**Context:** {context}

**Decision:** {decision}

**Consequences:** {consequences or 'TBD'}

---

"""
        
        content = self.docs['DECISIONS'].read_text()
        
        # Insert after "## Decision Log"
        content = content.replace(
            '## Decision Log\n\n',
            f'## Decision Log\n\n{entry}'
        )
        
        self._write_file(self.docs['DECISIONS'], content)
    
    # ============ RESEARCH.md Updates ============
    
    def create_research_doc(self, topic: str):
        """Create research.md for a topic"""
        content = f"""# Research: {topic}

Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}

## Summary
<!-- Researcher fills this -->

## Options Considered
<!-- Researcher lists options -->

### Option 1: 
- Pros: 
- Cons: 

## Recommendation
<!-- Researcher's pick -->

"""
        self._write_file(self.docs['RESEARCH'], content)
    
    def update_research_section(self, section: str, content_update: str):
        """Update a section of research.md"""
        if not self.docs['RESEARCH'].exists():
            return
        
        doc_content = self.docs['RESEARCH'].read_text()
        
        # Simple section replacement
        pattern = rf'(## {section}\n).+?(?=\n## |$)'
        replacement = rf'\1{content_update}\n'
        
        doc_content = re.sub(pattern, replacement, doc_content, flags=re.DOTALL)
        
        self._write_file(self.docs['RESEARCH'], doc_content)
    
    # ============ Utility ============
    
    def _write_file(self, filepath: Path, content: str):
        """Write content to file"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
    
    def agent_completed(self, agent: str, task: str, outputs: Dict[str, Any]):
        """
        Called when an agent completes a task
        Auto-updates all relevant docs
        
        Args:
            agent: Which agent (researcher/architect/coder)
            task: What they did
            outputs: Dict of outputs from the agent
        """
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')
        
        if agent == "researcher":
            # Update research doc
            if 'findings' in outputs:
                self.update_research_section('Summary', outputs['findings'])
            
            # Log decision if recommendation made
            if 'recommendation' in outputs:
                self.log_decision(
                    outputs['recommendation'],
                    f"Based on research: {task}",
                    outputs.get('consequences', '')
                )
        
        elif agent == "architect":
            # Update architecture doc
            if 'structure' in outputs:
                self.update_architecture_section('Folder Structure', outputs['structure'])
            if 'data_flow' in outputs:
                self.update_architecture_section('Data Flow', outputs['data_flow'])
            if 'tech_stack' in outputs:
                tech_list = outputs['tech_stack'] if isinstance(outputs['tech_stack'], list) else [outputs['tech_stack']]
                # Recreate with new stack
                self.create_architecture_doc(tech_list, outputs.get('structure', 'TBD'))
            
            # Log decisions
            if 'decisions' in outputs:
                for decision in outputs['decisions']:
                    self.log_decision(
                        decision.get('what', ''),
                        decision.get('why', ''),
                        decision.get('impact', '')
                    )
        
        elif agent == "coder":
            # Update changelog
            self.add_changelog_entry(f"{task} ({agent})", category="Added")
            
            # Update project.md completed section
            self.update_project_status(
                phase="coding",
                completed_items=[task]
            )
            
            # Add to scope
            self.add_to_scope(task)


if __name__ == "__main__":
    # Test doc updater
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        updater = DocUpdater(tmpdir)
        
        # Create initial docs
        updater.create_project_doc(
            name="Test Bot",
            description="A test trading bot",
            answers={"tech": "Python", "audience": "Just me"}
        )
        
        updater.create_architecture_doc(
            tech_stack=["Python", "FastAPI", "SQLite"],
            structure="bot/\n├── main.py\n└── config.py"
        )
        
        updater.create_changelog()
        
        # Simulate coder completing task
        updater.agent_completed(
            agent="coder",
            task="Implemented auth middleware",
            outputs={}
        )
        
        print("PROJECT.md:")
        print(updater.docs['PROJECT'].read_text()[:500])
        print("\n...\n")
        
        print("CHANGELOG.md:")
        print(updater.docs['CHANGELOG'].read_text())

#!/usr/bin/env python3
"""
Architect Agent - Designs system structure

NOW WITH INLINE RESEARCH:
- Quick survey of options (2-3 alternatives)
- Recommendation with rationale
- Designs architecture based on research
"""

from pathlib import Path
from typing import Dict, Any

class ArchitectAgent:
    """Background agent that designs system architecture + does quick research"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.architecture_file = self.project_dir / "ARCHITECTURE.md"
        self.decisions_file = self.project_dir / ".blitz" / "decisions.md"
    
    def design(self, requirements: str, tech_preference: str = None, features: str = None) -> Dict[str, Any]:
        """
        Design system architecture with inline research
        
        Args:
            requirements: What needs to be built
            tech_preference: User's tech preference (if any)
            features: Key features needed
            
        Returns:
            Agent info with prompt
        """
        return {
            'prompt': self._generate_prompt(requirements, tech_preference, features),
            'output_files': [
                str(self.architecture_file),
                str(self.decisions_file)
            ],
            'estimated_time': '8-12 minutes'
        }
    
    def _generate_prompt(self, requirements: str, tech_preference: str, features: str) -> str:
        """Generate the architecture + research prompt"""
        
        tech_context = ""
        if tech_preference and tech_preference != "No preference":
            tech_context = f"\nUser prefers: {tech_preference}\nUse this unless there's a compelling reason not to."
        
        features_context = ""
        if features:
            features_context = f"\nKey features needed: {features}"
        
        return f"""You are the Architect agent for Blitz.

Design system architecture for:
{requirements}
{features_context}
{tech_context}

## YOUR JOB (8-12 minutes total):

### Step 1: Quick Research (3-4 min)
Survey the landscape for each major decision:
- Language/Framework: Compare 2-3 options
- Database: Compare 2-3 options  
- Key libraries: What are the popular choices?

For each comparison:
- Option A: [name] - best for [X], pros/cons
- Option B: [name] - best for [Y], pros/cons
- **Recommendation**: [your pick] + why

### Step 2: Architecture Design (5-8 min)
Create ARCHITECTURE.md at: {self.architecture_file}

Structure:
# Architecture

## Tech Stack
For each choice, include WHY:
- Language/Framework: [choice] - [one-line rationale]
- Database: [choice] - [one-line rationale]
- Key Libraries: [list with purpose]

## Folder Structure
```
project/
├── [folder]/       # [purpose]
├── [folder]/       # [purpose]
└── [entry point]   # [purpose]
```

## Data Flow
1. [User action] → [System response] → [Result]
2. ...

## API/Interface
[Key functions or endpoints]

## Key Decisions
See [decisions.md](.blitz/decisions.md)

### Step 3: Log Decisions
Write to: {self.decisions_file}

For each major decision, add:
### YYYY-MM-DD: [Decision title]
**Context:** [What problem we're solving]
**Decision:** [What we chose]
**Rationale:** [Why this choice]
**Consequences:** [Trade-offs, limitations]

## PRINCIPLES:
- MVP-focused: What's the SIMPLEST thing that works?
- Prefer boring technology: Battle-tested > bleeding edge
- Plan for change: Design so parts can be swapped later
- Document WHY, not just WHAT

Keep it practical. This is MVP architecture, not enterprise over-engineering.
"""


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: architect.py <project_dir> [requirements]")
        sys.exit(1)
    
    project_dir = Path(sys.argv[1])
    requirements = sys.argv[2] if len(sys.argv) > 2 else "Build the project"
    tech_pref = sys.argv[3] if len(sys.argv) > 3 else None
    features = sys.argv[4] if len(sys.argv) > 4 else None
    
    agent = ArchitectAgent(project_dir)
    result = agent.design(requirements, tech_pref, features)
    
    print(result['prompt'])

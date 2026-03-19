#!/usr/bin/env python3
"""
Architect Agent - Designs system structure and tech stack
"""

from pathlib import Path
from typing import Dict, Any

class ArchitectAgent:
    """Background agent that designs system architecture"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.architecture_file = self.project_dir / "ARCHITECTURE.md"
        self.decisions_file = self.project_dir / ".buildmate" / "decisions.md"
    
    def design(self, requirements: str, research_findings: str = None) -> Dict[str, Any]:
        """
        Design system architecture
        
        Returns prompt for Claude to execute
        """
        return {
            'prompt': self._generate_prompt(requirements, research_findings),
            'output_files': [
                str(self.architecture_file),
                str(self.decisions_file)
            ]
        }
    
    def _generate_prompt(self, requirements: str, research_findings: str = None) -> str:
        """Generate the architecture prompt"""
        research_section = ""
        if research_findings:
            research_section = f"""
Research findings to consider:
{research_findings}
"""
        
        return f"""Design system architecture for:

{requirements}

{research_section}

Create ARCHITECTURE.md at: {self.architecture_file}

Structure:
# Architecture

## Tech Stack
- Language/Framework: [choice + why]
- Database: [choice + why]  
- Key Libraries: [list with purpose]

## Folder Structure
```
project/
├── [folder]/       # Purpose
├── [folder]/       # Purpose
└── README.md       # Entry point
```

## Data Flow
1. User does X → System does Y → Result Z
2. ...

## API/Interface Design
[If applicable - key endpoints or functions]

## Key Decisions
[Log each major decision with rationale]

Also log decisions to: {self.decisions_file}

Format each decision:
### YYYY-MM-DD: [Decision title]
**Context:** [What problem we're solving]
**Decision:** [What we chose]
**Consequences:** [Impact, trade-offs]

Keep it simple - this is MVP architecture. No over-engineering.
"""


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: architect.py <project_dir> [requirements]")
        sys.exit(1)
    
    project_dir = Path(sys.argv[1])
    requirements = sys.argv[2] if len(sys.argv) > 2 else "Build the project"
    
    agent = ArchitectAgent(project_dir)
    result = agent.design(requirements)
    
    print(result['prompt'])

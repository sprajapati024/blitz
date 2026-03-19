#!/usr/bin/env python3
"""
Researcher Agent - Finds best tech options, APIs, patterns
"""

from pathlib import Path
from typing import Dict, Any

class ResearcherAgent:
    """Background agent that researches tech choices"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.output_file = self.project_dir / ".blitz" / "research.md"
    
    def research(self, topic: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Research a topic and return findings
        
        In real implementation, this would:
        1. Search web for current best practices
        2. Compare libraries/frameworks
        3. Check GitHub for popular patterns
        
        For MVP, returns structured prompt for Claude to execute
        """
        return {
            'prompt': self._generate_prompt(topic, context),
            'output_file': str(self.output_file),
            'expected_sections': [
                'Summary',
                'Options Considered', 
                'Recommendation',
                'Pitfalls to Avoid'
            ]
        }
    
    def _generate_prompt(self, topic: str, context: Dict[str, Any]) -> str:
        """Generate the research prompt"""
        features = context.get('features', '')
        tech_pref = context.get('tech_preference', 'No preference')
        
        return f"""Research: {topic}

Context:
- Features needed: {features}
- Tech preference: {tech_pref}

Research and write to: {self.output_file}

Structure:
## Summary
2-3 sentences on best approach

## Options Considered
For each major component (API, database, framework, etc.):

### Option 1: [Name]
- Best for: [use case]
- Pros: 
- Cons: 
- Setup complexity: Easy/Medium/Hard

### Option 2: [Name]
...

## Recommendation
What to use and why (match to tech preference if specified)

## Pitfalls to Avoid
Common mistakes with this stack

Be practical. Recommend battle-tested options over bleeding edge.
"""


# Command-line interface
if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 3:
        print("Usage: researcher.py <project_dir> <topic>")
        sys.exit(1)
    
    project_dir = Path(sys.argv[1])
    topic = sys.argv[2]
    
    context = {}
    if len(sys.argv) > 3:
        context = json.loads(sys.argv[3])
    
    agent = ResearcherAgent(project_dir)
    result = agent.research(topic, context)
    
    print(result['prompt'])

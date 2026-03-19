#!/usr/bin/env python3
"""
Agent Spawner - Spawns and manages the 3 background agents
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timezone

class AgentSpawner:
    """Spawns and manages researcher, architect, and coder agents"""
    
    def __init__(self, project_dir: Path, callbacks: Dict[str, Callable] = None):
        self.project_dir = Path(project_dir)
        self.agents_dir = Path(__file__).parent.parent / "agents"
        self.callbacks = callbacks or {}
        
        # Track running agents
        self.running_agents = {}
    
    def spawn_researcher(self, topic: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Spawn researcher agent to investigate a topic
        
        Args:
            topic: What to research
            context: Additional context (tech preferences, constraints)
            
        Returns:
            Agent info dict with process details
        """
        agent_id = f"researcher_{datetime.now(timezone.utc).strftime('%H%M%S')}"
        
        # Build the prompt for the researcher
        prompt = self._build_researcher_prompt(topic, context)
        
        # In real implementation, this would spawn a subprocess or use Task tool
        # For now, return the prompt that Claude would use
        agent_info = {
            'id': agent_id,
            'type': 'researcher',
            'topic': topic,
            'status': 'spawned',
            'prompt': prompt,
            'outputs': {
                'research_file': str(self.project_dir / '.buildmate' / 'research.md')
            }
        }
        
        self.running_agents[agent_id] = agent_info
        
        # Trigger callback if registered
        if 'on_spawn' in self.callbacks:
            self.callbacks['on_spawn'](agent_info)
        
        return agent_info
    
    def spawn_architect(self, requirements: str, research_findings: str = None) -> Dict[str, Any]:
        """
        Spawn architect agent to design system
        
        Args:
            requirements: What needs to be built
            research_findings: Output from researcher (optional)
            
        Returns:
            Agent info dict
        """
        agent_id = f"architect_{datetime.now(timezone.utc).strftime('%H%M%S')}"
        
        prompt = self._build_architect_prompt(requirements, research_findings)
        
        agent_info = {
            'id': agent_id,
            'type': 'architect',
            'status': 'spawned',
            'prompt': prompt,
            'outputs': {
                'architecture_file': str(self.project_dir / 'ARCHITECTURE.md')
            }
        }
        
        self.running_agents[agent_id] = agent_info
        
        if 'on_spawn' in self.callbacks:
            self.callbacks['on_spawn'](agent_info)
        
        return agent_info
    
    def spawn_coder(self, architecture: str, task: str = "Implement MVP") -> Dict[str, Any]:
        """
        Spawn coder agent to implement features
        
        Args:
            architecture: Path to or content of ARCHITECTURE.md
            task: Specific task to implement
            
        Returns:
            Agent info dict
        """
        agent_id = f"coder_{datetime.now(timezone.utc).strftime('%H%M%S')}"
        
        prompt = self._build_coder_prompt(architecture, task)
        
        agent_info = {
            'id': agent_id,
            'type': 'coder',
            'task': task,
            'status': 'spawned',
            'prompt': prompt,
            'outputs': {
                'code_dir': str(self.project_dir),
                'changelog': str(self.project_dir / 'CHANGELOG.md')
            }
        }
        
        self.running_agents[agent_id] = agent_info
        
        if 'on_spawn' in self.callbacks:
            self.callbacks['on_spawn'](agent_info)
        
        return agent_info
    
    def spawn_all_for_project(self, project_name: str, description: str, answers: Dict[str, str]):
        """
        Spawn all 3 agents in sequence for a new project
        
        Returns dict with all agent infos
        """
        agents = {}
        
        # 1. Spawn researcher (parallel - quick)
        research_topic = f"{project_name}: {description}"
        context = {
            'tech_preference': answers.get('tech', 'No preference'),
            'timeline': answers.get('timeline', 'Not specified'),
            'features': answers.get('features', '')
        }
        agents['researcher'] = self.spawn_researcher(research_topic, context)
        
        # 2. Spawn architect (after research or parallel)
        requirements = f"Build {project_name}: {description}\n\nKey features: {answers.get('features', 'TBD')}"
        agents['architect'] = self.spawn_architect(requirements)
        
        # 3. Spawn coder (after architecture)
        # In real implementation, this would wait for architect to complete
        agents['coder'] = self.spawn_coder(
            architecture=str(self.project_dir / 'ARCHITECTURE.md'),
            task=f"Implement {project_name} MVP"
        )
        
        return agents
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a running agent"""
        return self.running_agents.get(agent_id)
    
    def get_all_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            'running': len(self.running_agents),
            'agents': self.running_agents
        }
    
    def _build_researcher_prompt(self, topic: str, context: Dict[str, Any] = None) -> str:
        """Build the prompt for researcher agent"""
        context_str = ""
        if context:
            context_str = f"""
Context:
- Tech preference: {context.get('tech_preference', 'None')}
- Timeline: {context.get('timeline', 'Not specified')}
- Features needed: {context.get('features', 'TBD')}
"""
        
        return f"""You are the Researcher agent for Buildmate.

Research this topic thoroughly: {topic}

{context_str}

Your job:
1. Find the best libraries/frameworks for this use case
2. Compare at least 3 options for each major decision
3. Check for common pitfalls and how to avoid them
4. Look for existing patterns/templates

Output format:
Write findings to: {self.project_dir}/.buildmate/research.md

Include:
- ## Summary (2-3 sentences)
- ## Options Considered (with pros/cons)
- ## Recommendation (what to use and why)
- ## Pitfalls to Avoid

Be thorough but concise. This is background research - user will see summary only.
"""
    
    def _build_architect_prompt(self, requirements: str, research_findings: str = None) -> str:
        """Build the prompt for architect agent"""
        research_section = ""
        if research_findings:
            research_section = f"""
Research Findings:
{research_findings}

Use these findings to inform your architecture decisions.
"""
        
        return f"""You are the Architect agent for Buildmate.

Design the system architecture for:
{requirements}

{research_section}

Your job:
1. Design clean folder structure
2. Choose tech stack (justify each choice)
3. Plan data flow
4. Design API/contracts
5. Log all architectural decisions

Output files:
1. {self.project_dir}/ARCHITECTURE.md - Full architecture doc
2. Update {self.project_dir}/PROJECT.md - Tech stack section
3. Log decisions to {self.project_dir}/.buildmate/decisions.md

Architecture.md structure:
- ## Tech Stack (with justification)
- ## Folder Structure (tree diagram)
- ## Data Flow (how data moves)
- ## API Design (if applicable)
- ## Key Decisions (links to decisions.md)

Keep it practical. This is MVP architecture, not enterprise over-engineering.
"""
    
    def _build_coder_prompt(self, architecture: str, task: str) -> str:
        """Build the prompt for coder agent"""
        return f"""You are the Coder agent for Buildmate.

Your task: {task}

Architecture (follow this exactly):
{architecture}

Your job:
1. Implement the feature following the architecture
2. Write clean, documented code
3. Include basic tests
4. Update docs as you go

Rules:
- Follow the architecture - don't deviate without logging a decision
- Keep it simple - MVP quality, not gold-plated
- Test your code works
- Update CHANGELOG.md with what you built

Output:
- Working code in the project directory
- Updated PROJECT.md (mark features complete)
- Updated CHANGELOG.md (what was added)
- Tests that verify the core functionality

After completing:
1. Test the code actually runs
2. Verify it meets the architecture
3. Update all docs
4. Report what you built

Build it like you're shipping it today.
"""


# Helper functions for integration
def spawn_agents_for_project(project_dir: Path, name: str, description: str, answers: Dict[str, str]):
    """
    Convenience function to spawn all agents for a new project
    
    Returns:
        Dict with agent information
    """
    spawner = AgentSpawner(project_dir)
    return spawner.spawn_all_for_project(name, description, answers)


if __name__ == "__main__":
    # Test agent spawner
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        spawner = AgentSpawner(tmpdir)
        
        # Spawn all agents
        agents = spawner.spawn_all_for_project(
            project_name="Trading Bot",
            description="A paper trading bot for stocks",
            answers={
                "tech": "Python",
                "features": "paper trading, price alerts",
                "timeline": "This week"
            }
        )
        
        print("Spawned agents:")
        for agent_type, info in agents.items():
            print(f"\n{agent_type.upper()}:")
            print(f"  ID: {info['id']}")
            print(f"  Status: {info['status']}")
            print(f"  Prompt length: {len(info['prompt'])} chars")

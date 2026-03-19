#!/usr/bin/env python3
"""
Agent Spawner - Spawns and manages the 2 background agents

v3.1: Simplified to 2 agents (removed researcher - architect does inline research)
v3.2: Added checkpoint integration for smart interruptions
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timezone

from .checkpoint_manager import CheckpointManager, InterruptHandler

class AgentSpawner:
    """Spawns and manages architect and coder agents with checkpoint support"""
    
    def __init__(self, project_dir: Path, callbacks: Dict[str, Callable] = None):
        self.project_dir = Path(project_dir)
        self.agents_dir = Path(__file__).parent.parent / "agents"
        self.callbacks = callbacks or {}
        
        # Checkpoint support
        self.checkpoint_manager = CheckpointManager(project_dir)
        self.interrupt_handler = InterruptHandler(project_dir, self.checkpoint_manager)
        
        # Track running agents
        self.running_agents = {}
        self._current_task = None
        self._current_phase = None
    
    def spawn_architect(self, requirements: str, tech_preference: str = None, features: str = None) -> Dict[str, Any]:
        """
        Spawn architect agent (now includes inline research)
        
        Args:
            requirements: What to build
            tech_preference: User's tech preference
            features: Key features
            
        Returns:
            Agent info
        """
        self._current_phase = 'designing'
        self._current_task = f"Architecture for: {requirements[:50]}..."
        
        agent_id = f"architect_{datetime.now(timezone.utc).strftime('%H%M%S')}"
        
        prompt = self._build_architect_prompt(requirements, tech_preference, features)
        
        agent_info = {
            'id': agent_id,
            'type': 'architect',
            'status': 'spawned',
            'prompt': prompt,
            'outputs': {
                'architecture_file': str(self.project_dir / 'ARCHITECTURE.md'),
                'decisions_file': str(self.project_dir / '.blitz' / 'decisions.md')
            },
            'estimated_time': '8-12 minutes'
        }
        
        self.running_agents[agent_id] = agent_info
        
        if 'on_spawn' in self.callbacks:
            self.callbacks['on_spawn'](agent_info)
        
        return agent_info
    
    def spawn_coder(self, architecture_path: str, task: str = "Implement MVP", progress_callback: Callable = None) -> Dict[str, Any]:
        """
        Spawn coder agent to implement features
        
        Args:
            architecture_path: Path to ARCHITECTURE.md
            task: Specific task to implement
            progress_callback: Function to call with progress updates
            
        Returns:
            Agent info
        """
        self._current_phase = 'coding'
        self._current_task = task
        
        # Create checkpoint before starting coder
        checkpoint = self.checkpoint_manager.create_checkpoint(
            name="before_coding",
            description=f"Before starting: {task}",
            agent_status={k: v.get('status', 'idle') for k, v in self.running_agents.items()},
            current_tasks=[task],
            completed_tasks=[],
            phase='coding'
        )
        
        agent_id = f"coder_{datetime.now(timezone.utc).strftime('%H%M%S')}"
        
        prompt = self._build_coder_prompt(architecture_path, task, progress_callback)
        
        agent_info = {
            'id': agent_id,
            'type': 'coder',
            'task': task,
            'status': 'spawned',
            'prompt': prompt,
            'outputs': {
                'code_dir': str(self.project_dir),
                'changelog': str(self.project_dir / 'CHANGELOG.md')
            },
            'progress_callback': progress_callback,
            'estimated_time': '20-30 minutes',
            'checkpoint_id': checkpoint.id
        }
        
        self.running_agents[agent_id] = agent_info
        
        if 'on_spawn' in self.callbacks:
            self.callbacks['on_spawn'](agent_info)
        
        return agent_info
    
    def spawn_all_for_project(self, project_name: str, description: str, answers: Dict[str, str]):
        """
        Spawn both agents in sequence for a new project
        
        Returns dict with both agent infos
        """
        agents = {}
        
        tech_pref = answers.get('tech', 'No preference')
        features = answers.get('features', '')
        
        # 1. Spawn architect (includes inline research)
        requirements = f"Build {project_name}: {description}"
        agents['architect'] = self.spawn_architect(requirements, tech_pref, features)
        
        # 2. Spawn coder (after architect or parallel with dependency)
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
    
    # ===== Checkpoint/Interruption Methods =====
    
    def handle_user_interrupt(self, user_request: str) -> Dict[str, Any]:
        """
        Handle user interruption mid-build.
        
        Args:
            user_request: What the user wants to change
            
        Returns:
            Dict with options and context
        """
        agent_status = {k: v.get('status', 'idle') for k, v in self.running_agents.items()}
        
        return self.interrupt_handler.handle_interrupt(
            user_request=user_request,
            current_phase=self._current_phase or 'unknown',
            current_task=self._current_task or 'unknown',
            agent_status=agent_status,
            completed_tasks=[]  # Would track from state manager
        )
    
    def execute_interrupt_option(self, option_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute chosen interruption option.
        
        Args:
            option_id: Option chosen by user
            context: Additional context from handle_user_interrupt
            
        Returns:
            Result of the action
        """
        return self.interrupt_handler.execute_option(option_id, context)
    
    def create_manual_checkpoint(self, name: str, description: str) -> Dict[str, Any]:
        """Create a checkpoint on demand"""
        agent_status = {k: v.get('status', 'idle') for k, v in self.running_agents.items()}
        
        checkpoint = self.checkpoint_manager.create_checkpoint(
            name=name,
            description=description,
            agent_status=agent_status,
            current_tasks=[self._current_task] if self._current_task else [],
            completed_tasks=[],
            phase=self._current_phase or 'unknown'
        )
        
        return {
            'success': True,
            'checkpoint_id': checkpoint.id,
            'files_count': checkpoint.files_count,
            'timestamp': checkpoint.timestamp
        }
    
    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """List all available checkpoints"""
        checkpoints = self.checkpoint_manager.list_checkpoints()
        return [cp.to_dict() for cp in checkpoints]
    
    def restore_checkpoint(self, checkpoint_id: str, dry_run: bool = False) -> Dict[str, Any]:
        """Restore to a checkpoint"""
        return self.checkpoint_manager.restore_checkpoint(checkpoint_id, dry_run)
    
    def compare_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        """Compare current state to checkpoint"""
        return self.checkpoint_manager.compare_checkpoint(checkpoint_id)
    
    def _build_architect_prompt(self, requirements: str, tech_preference: str, features: str) -> str:
        """Build prompt for architect (with inline research)"""
        tech_context = f"\nTech preference: {tech_preference}" if tech_preference else ""
        features_context = f"\nFeatures: {features}" if features else ""
        
        return f"""You are the Architect agent for Blitz.

Design system architecture for:
{requirements}
{features_context}
{tech_context}

## YOUR JOB (8-12 minutes):

### Step 1: Quick Research (3-4 min)
Compare 2-3 options for:
- Language/Framework
- Database  
- Key libraries

**Recommendation**: Pick one, explain why

### Step 2: Architecture (5-8 min)
Create ARCHITECTURE.md:
- Tech Stack (with WHY for each)
- Folder Structure (tree)
- Data Flow
- API/Interface design

### Step 3: Log Decisions
Write to .blitz/decisions.md

## PRINCIPLES:
- MVP-focused: Simplest thing that works
- Prefer boring technology
- Design for change

Keep it practical. Not enterprise over-engineering.
"""
    
    def _build_coder_prompt(self, architecture: str, task: str, progress_callback: str = None) -> str:
        """Build prompt for coder with progress streaming"""
        
        progress_instructions = ""
        if progress_callback:
            progress_instructions = """
## PROGRESS STREAMING:
As you work, update progress at key milestones:

After each major component, write a brief update to .blitz/progress.json:
```json
{
  "timestamp": "2024-03-19T10:30:00Z",
  "component": "auth middleware",
  "status": "complete",
  "next": "user API endpoints",
  "percent_complete": 35
}
```

Key milestones to report:
- Project structure created
- Core modules implemented
- Auth working
- Main features done
- Tests passing
- MVP complete
"""
        
        return f"""You are the Coder agent for Blitz.

Your task: {task}

Architecture: {architecture}

## RULES:
1. Write WORKING code - test that it runs
2. Follow the architecture
3. Keep it simple - MVP quality
4. Include basic error handling
5. Write tests

## DOC UPDATES:
- Update CHANGELOG.md with what you add
- Update PROJECT.md to mark features complete
{progress_instructions}

## ERROR HANDLING:
If you hit a problem:
1. Try alternative approach
2. If stuck, document in .blitz/errors.json:
```json
{
  "error": "description",
  "component": "where it happened",
  "suggestions": ["option 1", "option 2"],
  "recommendation": "what you think we should do"
}
```

Build like you're shipping today.
"""


# Helper functions
def spawn_agents_for_project(project_dir: Path, name: str, description: str, answers: Dict[str, str]):
    """Convenience function to spawn both agents"""
    spawner = AgentSpawner(project_dir)
    return spawner.spawn_all_for_project(name, description, answers)


if __name__ == "__main__":
    import sys
    
    with tempfile.TemporaryDirectory() as tmpdir:
        spawner = AgentSpawner(tmpdir)
        
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
            print(f"\n{agent_type.upper()}: {info['id']}")
            print(f"  Est. time: {info.get('estimated_time', 'unknown')}")

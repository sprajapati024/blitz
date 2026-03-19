#!/usr/bin/env python3
"""
State Manager - Tracks project state across sessions
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from enum import Enum

class ProjectPhase(Enum):
    PLANNING = "planning"
    RESEARCHING = "researching"
    DESIGNING = "designing"
    CODING = "coding"
    TESTING = "testing"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    PAUSED = "paused"

class StateManager:
    """Manages project state persistence"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.buildmate_dir = self.project_dir / ".buildmate"
        self.state_file = self.buildmate_dir / "state.json"
        
        # Ensure buildmate directory exists
        self.buildmate_dir.mkdir(parents=True, exist_ok=True)
    
    def initialize_project(self, name: str, description: str, answers: Dict[str, str]) -> Dict[str, Any]:
        """
        Initialize a new project with state
        
        Args:
            name: Project name
            description: Brief description
            answers: Dict of clarifying question answers
            
        Returns:
            Initial state dict
        """
        state = {
            "version": "3.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "project": {
                "name": name,
                "description": description,
                "phase": ProjectPhase.PLANNING.value,
                "status": "active"
            },
            "answers": answers,
            "progress": {
                "research_complete": False,
                "architecture_complete": False,
                "coding_complete": False,
                "testing_complete": False
            },
            "agents": {
                "researcher": {"status": "idle", "last_run": None},
                "architect": {"status": "idle", "last_run": None},
                "coder": {"status": "idle", "last_run": None}
            },
            "completed_tasks": [],
            "current_tasks": [],
            "blockers": []
        }
        
        self._save_state(state)
        return state
    
    def get_state(self) -> Optional[Dict[str, Any]]:
        """Load current project state"""
        if not self.state_file.exists():
            return None
        
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def update_state(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update project state with new values
        
        Args:
            updates: Dict of fields to update
            
        Returns:
            Updated state
        """
        state = self.get_state() or {}
        
        # Deep merge updates
        self._deep_merge(state, updates)
        
        # Always update timestamp
        state['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        self._save_state(state)
        return state
    
    def update_phase(self, phase: ProjectPhase) -> Dict[str, Any]:
        """Update project phase"""
        return self.update_state({
            'project': {
                'phase': phase.value
            }
        })
    
    def update_agent_status(self, agent: str, status: str, task: str = None) -> Dict[str, Any]:
        """Update agent status"""
        update = {
            'agents': {
                agent: {
                    'status': status,
                    'last_run': datetime.now(timezone.utc).isoformat()
                }
            }
        }
        if task:
            update['agents'][agent]['current_task'] = task
        
        return self.update_state(update)
    
    def add_completed_task(self, task: str, agent: str) -> Dict[str, Any]:
        """Add a completed task"""
        state = self.get_state() or {}
        
        completed = state.get('completed_tasks', [])
        completed.append({
            'task': task,
            'agent': agent,
            'completed_at': datetime.now(timezone.utc).isoformat()
        })
        
        return self.update_state({'completed_tasks': completed})
    
    def add_blocker(self, blocker: str) -> Dict[str, Any]:
        """Add a blocker that needs user attention"""
        state = self.get_state() or {}
        
        blockers = state.get('blockers', [])
        blockers.append({
            'description': blocker,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'resolved': False
        })
        
        return self.update_state({'blockers': blockers})
    
    def resolve_blocker(self, index: int) -> Dict[str, Any]:
        """Mark a blocker as resolved"""
        state = self.get_state() or {}
        
        blockers = state.get('blockers', [])
        if 0 <= index < len(blockers):
            blockers[index]['resolved'] = True
            blockers[index]['resolved_at'] = datetime.now(timezone.utc).isoformat()
        
        return self.update_state({'blockers': blockers})
    
    def get_status_summary(self) -> str:
        """Get a human-readable status summary"""
        state = self.get_state()
        
        if not state:
            return "No active project."
        
        project = state.get('project', {})
        agents = state.get('agents', {})
        progress = state.get('progress', {})
        blockers = [b for b in state.get('blockers', []) if not b.get('resolved')]
        
        lines = [
            f"📁 {project.get('name', 'Unnamed')}",
            f"Phase: {project.get('phase', 'unknown')}",
            "",
            "Progress:"
        ]
        
        # Progress checklist
        if progress.get('research_complete'):
            lines.append("  ✅ Research")
        else:
            lines.append("  ⏳ Research")
            
        if progress.get('architecture_complete'):
            lines.append("  ✅ Architecture")
        else:
            lines.append("  ⏳ Architecture")
            
        if progress.get('coding_complete'):
            lines.append("  ✅ Implementation")
        else:
            lines.append("  ⏳ Implementation")
        
        # Current agent activity
        active_agents = [
            name for name, info in agents.items()
            if info.get('status') == 'running'
        ]
        
        if active_agents:
            lines.append(f"\n🔧 Active: {', '.join(active_agents)}")
        
        # Blockers
        if blockers:
            lines.append(f"\n⚠️  Blockers ({len(blockers)}):")
            for b in blockers:
                lines.append(f"   - {b['description']}")
        
        return "\n".join(lines)
    
    def _save_state(self, state: Dict[str, Any]):
        """Save state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def _deep_merge(self, base: Dict, updates: Dict):
        """Deep merge updates into base dict"""
        for key, value in updates.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value


if __name__ == "__main__":
    # Test state manager
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = StateManager(tmpdir)
        
        # Initialize project
        state = manager.initialize_project(
            name="test-bot",
            description="A test trading bot",
            answers={
                "audience": "Just me",
                "features": "paper trading, alerts",
                "tech": "Python",
                "timeline": "This week"
            }
        )
        print("Initialized:")
        print(json.dumps(state, indent=2))
        
        # Update agent status
        manager.update_agent_status("researcher", "running", "Finding APIs")
        
        # Complete research
        manager.update_state({
            'progress': {'research_complete': True}
        })
        manager.update_agent_status("researcher", "idle")
        manager.add_completed_task("Researched trading APIs", "researcher")
        
        # Print summary
        print("\n" + manager.get_status_summary())

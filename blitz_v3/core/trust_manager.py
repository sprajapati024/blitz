#!/usr/bin/env python3
"""
Trust Manager - Manages trust modes for Blitz

Three modes:
- NOTIFY: Default, ask before doing, frequent updates
- AUTO: Do it, then tell user, fewer updates  
- GHOST: Silent execution, daily summary only

Unlock criteria:
- AUTO: 3+ successful projects
- GHOST: 10+ successful projects
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from enum import Enum


class TrustMode(Enum):
    """Trust levels for Blitz operation"""
    NOTIFY = "notify"    # Ask before doing
    AUTO = "auto"        # Do it, then tell
    GHOST = "ghost"      # Silent, daily summary


class TrustManager:
    """
    Manages trust modes and project history.
    
    Tracks:
    - Current trust mode
    - Successful project count (for unlocks)
    - Project history
    - Daily summaries (for ghost mode)
    """
    
    # Unlock thresholds
    AUTO_THRESHOLD = 3
    GHOST_THRESHOLD = 10
    
    def __init__(self, blitz_home: Path = None):
        """
        Initialize trust manager
        
        Args:
            blitz_home: Path to .blitz directory (default: ~/.blitz)
        """
        if blitz_home is None:
            blitz_home = Path.home() / ".blitz"
        
        self.blitz_home = Path(blitz_home)
        self.preferences_file = self.blitz_home / "preferences.json"
        self.history_file = self.blitz_home / "history.json"
        self.summaries_dir = self.blitz_home / "summaries"
        
        # Ensure directories exist
        self.blitz_home.mkdir(parents=True, exist_ok=True)
        self.summaries_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or init preferences
        self._preferences = self._load_preferences()
        self._history = self._load_history()
    
    def _load_preferences(self) -> Dict[str, Any]:
        """Load user preferences"""
        if not self.preferences_file.exists():
            return self._default_preferences()
        
        try:
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._default_preferences()
    
    def _default_preferences(self) -> Dict[str, Any]:
        """Default preferences for new users"""
        return {
            "trust_mode": TrustMode.NOTIFY.value,
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "settings": {
                "auto_switch_threshold": True,  # Auto suggest mode upgrades
                "ghost_summary_time": "09:00",  # Daily summary time
                "progress_update_interval": 300  # 5 minutes (notify mode)
            }
        }
    
    def _load_history(self) -> Dict[str, Any]:
        """Load project history"""
        if not self.history_file.exists():
            return {"projects": []}
        
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"projects": []}
    
    def _save_preferences(self):
        """Save preferences to file"""
        with open(self.preferences_file, 'w') as f:
            json.dump(self._preferences, f, indent=2)
    
    def _save_history(self):
        """Save history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(self._history, f, indent=2)
    
    # ==================== Mode Management ====================
    
    def get_current_mode(self) -> TrustMode:
        """Get current trust mode"""
        mode_str = self._preferences.get("trust_mode", TrustMode.NOTIFY.value)
        return TrustMode(mode_str)
    
    def get_tone(self) -> str:
        """Get user's preferred tone/personality"""
        return self._preferences.get("tone", "sassy")  # Default to sassy for personality
    
    def set_mode(self, mode: TrustMode, force: bool = False) -> Dict[str, Any]:
        """
        Set trust mode
        
        Args:
            mode: Mode to switch to
            force: Skip unlock checks
            
        Returns:
            Dict with result and message
        """
        current = self.get_current_mode()
        
        if current == mode:
            return {
                "success": True,
                "changed": False,
                "message": f"Already in {mode.value} mode"
            }
        
        # Check unlock requirements
        if not force:
            unlock_check = self._check_unlock(mode)
            if not unlock_check["unlocked"]:
                return {
                    "success": False,
                    "changed": False,
                    "message": unlock_check["message"],
                    "required": unlock_check["required"],
                    "current": unlock_check["current"]
                }
        
        # Update mode
        self._preferences["trust_mode"] = mode.value
        self._preferences["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._save_preferences()
        
        return {
            "success": True,
            "changed": True,
            "message": f"Switched to {mode.value} mode",
            "previous": current.value,
            "current": mode.value
        }
    
    def _check_unlock(self, mode: TrustMode) -> Dict[str, Any]:
        """Check if mode is unlocked"""
        successful = self.get_successful_project_count()
        
        if mode == TrustMode.NOTIFY:
            return {"unlocked": True}
        
        elif mode == TrustMode.AUTO:
            if successful >= self.AUTO_THRESHOLD:
                return {"unlocked": True}
            return {
                "unlocked": False,
                "message": f"AUTO mode unlocks after {self.AUTO_THRESHOLD} successful projects",
                "required": self.AUTO_THRESHOLD,
                "current": successful
            }
        
        elif mode == TrustMode.GHOST:
            if successful >= self.GHOST_THRESHOLD:
                return {"unlocked": True}
            return {
                "unlocked": False,
                "message": f"GHOST mode unlocks after {self.GHOST_THRESHOLD} successful projects",
                "required": self.GHOST_THRESHOLD,
                "current": successful
            }
        
        return {"unlocked": False, "message": "Unknown mode"}
    
    def get_available_modes(self) -> List[Dict[str, Any]]:
        """Get all modes with unlock status"""
        successful = self.get_successful_project_count()
        
        modes = []
        for mode in TrustMode:
            unlock_info = self._check_unlock(mode)
            modes.append({
                "mode": mode.value,
                "name": self._get_mode_name(mode),
                "description": self._get_mode_description(mode),
                "unlocked": unlock_info["unlocked"],
                "required": unlock_info.get("required"),
                "current": successful if unlock_info.get("required") else None
            })
        
        return modes
    
    def _get_mode_name(self, mode: TrustMode) -> str:
        """Get human-readable mode name"""
        names = {
            TrustMode.NOTIFY: "Notify Mode",
            TrustMode.AUTO: "Auto Mode",
            TrustMode.GHOST: "Ghost Mode"
        }
        return names.get(mode, mode.value)
    
    def _get_mode_description(self, mode: TrustMode) -> str:
        """Get mode description"""
        descriptions = {
            TrustMode.NOTIFY: "Ask before acting. Frequent updates. Full transparency.",
            TrustMode.AUTO: "Act first, notify after. Fewer updates. For power users.",
            TrustMode.GHOST: "Silent execution. Daily summary only. Maximum trust."
        }
        return descriptions.get(mode, "")
    
    # ==================== Project History ====================
    
    def record_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record a completed project
        
        Args:
            project_data: Project info (name, type, duration, success, etc.)
            
        Returns:
            Updated stats
        """
        project_record = {
            "id": project_data.get("id") or f"proj_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
            "name": project_data.get("name", "Unnamed"),
            "type": project_data.get("type", "unknown"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "duration_minutes": project_data.get("duration_minutes"),
            "success": project_data.get("success", True),
            "tech_stack": project_data.get("tech_stack", []),
            "features": project_data.get("features", [])
        }
        
        self._history["projects"].append(project_record)
        self._save_history()
        
        # Check for unlock notifications
        unlocks = self._check_new_unlocks()
        
        return {
            "recorded": True,
            "project_id": project_record["id"],
            "total_projects": len(self._history["projects"]),
            "successful_projects": self.get_successful_project_count(),
            "new_unlocks": unlocks
        }
    
    def _check_new_unlocks(self) -> List[Dict[str, Any]]:
        """Check if this project unlocked new modes"""
        successful = self.get_successful_project_count()
        unlocks = []
        
        if successful == self.AUTO_THRESHOLD:
            unlocks.append({
                "mode": TrustMode.AUTO.value,
                "message": f"🎉 Auto Mode unlocked! ({successful} successful projects)"
            })
        
        if successful == self.GHOST_THRESHOLD:
            unlocks.append({
                "mode": TrustMode.GHOST.value,
                "message": f"👻 Ghost Mode unlocked! ({successful} successful projects)"
            })
        
        return unlocks
    
    def get_successful_project_count(self) -> int:
        """Get number of successful projects"""
        return sum(1 for p in self._history["projects"] if p.get("success", True))
    
    def get_project_stats(self) -> Dict[str, Any]:
        """Get project statistics"""
        projects = self._history["projects"]
        successful = [p for p in projects if p.get("success", True)]
        
        return {
            "total": len(projects),
            "successful": len(successful),
            "failed": len(projects) - len(successful),
            "by_type": self._count_by_field(projects, "type"),
            "by_tech": self._count_tech_stacks(projects),
            "recent": projects[-5:] if projects else []
        }
    
    def _count_by_field(self, projects: List[Dict], field: str) -> Dict[str, int]:
        """Count projects by field value"""
        counts = {}
        for p in projects:
            value = p.get(field, "unknown")
            counts[value] = counts.get(value, 0) + 1
        return counts
    
    def _count_tech_stacks(self, projects: List[Dict]) -> Dict[str, int]:
        """Count tech stack usage"""
        counts = {}
        for p in projects:
            for tech in p.get("tech_stack", []):
                counts[tech] = counts.get(tech, 0) + 1
        return counts
    
    # ==================== Mode-Specific Behavior ====================
    
    def should_ask_before_action(self, action_type: str = "default") -> bool:
        """
        Check if Blitz should ask user before acting
        
        Args:
            action_type: Type of action (spawn_agents, make_decision, etc.)
            
        Returns:
            True if should ask, False if should proceed
        """
        mode = self.get_current_mode()
        
        if mode == TrustMode.NOTIFY:
            return True
        
        if mode == TrustMode.AUTO:
            # Only ask for major decisions
            major_actions = ["change_tech_stack", "rewind_checkpoint", "delete_project"]
            return action_type in major_actions
        
        if mode == TrustMode.GHOST:
            # Almost never ask
            critical_actions = ["delete_project", "security_risk"]
            return action_type in critical_actions
        
        return True
    
    def get_progress_update_frequency(self) -> int:
        """Get how often to send progress updates (seconds)"""
        mode = self.get_current_mode()
        
        if mode == TrustMode.NOTIFY:
            return 300  # 5 minutes
        
        if mode == TrustMode.AUTO:
            return 600  # 10 minutes
        
        if mode == TrustMode.GHOST:
            return 3600  # 1 hour (or never, use daily summary)
        
        return 300
    
    def should_send_completion_notice(self) -> bool:
        """Check if should notify on completion"""
        mode = self.get_current_mode()
        return mode in [TrustMode.NOTIFY, TrustMode.AUTO]
    
    def format_user_message(self, message_type: str, data: Dict[str, Any] = None) -> Optional[str]:
        """
        Format message based on trust mode
        
        Args:
            message_type: Type of message (starting, progress, complete, etc.)
            data: Message data
            
        Returns:
            Formatted message or None if shouldn't send
        """
        mode = self.get_current_mode()
        data = data or {}
        
        if mode == TrustMode.NOTIFY:
            return self._format_notify_message(message_type, data)
        
        elif mode == TrustMode.AUTO:
            return self._format_auto_message(message_type, data)
        
        elif mode == TrustMode.GHOST:
            # Ghost mode logs to summary, doesn't send immediate messages
            self._log_to_summary(message_type, data)
            return None
        
        return None
    
    def _format_notify_message(self, message_type: str, data: Dict[str, Any]) -> str:
        """Format message for notify mode"""
        if message_type == "starting":
            return f"Building {data.get('project_name', 'project')} now. I'll keep you updated."
        
        elif message_type == "progress":
            return f"{data.get('component', 'Working')} {data.get('status', 'in progress')}..."
        
        elif message_type == "complete":
            features = data.get('features', [])
            features_text = "\n".join([f"✓ {f}" for f in features]) if features else ""
            return f"Done! {data.get('project_name', 'Project')} ready.\n\n{features_text}\n\nTry it: {data.get('run_command', '')}"
        
        elif message_type == "error":
            return f"Hit a snag: {data.get('error', 'Unknown error')}\n\nOptions:\n{data.get('options', '1. Retry')}\n\nWhat do you want to do?"
        
        return ""
    
    def _format_auto_message(self, message_type: str, data: Dict[str, Any]) -> Optional[str]:
        """Format message for auto mode (fewer messages)"""
        if message_type == "starting":
            # Don't message on start
            return None
        
        elif message_type == "progress":
            # Only major milestones
            if data.get('milestone'):
                return f"{data.get('component', 'Progress')} {data.get('status', 'done')}."
            return None
        
        elif message_type == "complete":
            features = data.get('features', [])
            return f"Done! {data.get('project_name')} built ({len(features)} features).\n\n{data.get('run_command', '')}"
        
        elif message_type == "error":
            # Still notify on errors
            return f"Issue: {data.get('error')}\n\n{data.get('recommendation', '')}"
        
        return None
    
    def _log_to_summary(self, message_type: str, data: Dict[str, Any]):
        """Log to daily summary (ghost mode)"""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        summary_file = self.summaries_dir / f"{today}.json"
        
        summary = {"entries": []}
        if summary_file.exists():
            try:
                with open(summary_file, 'r') as f:
                    summary = json.load(f)
            except:
                pass
        
        summary["entries"].append({
            "type": message_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        })
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
    
    def get_daily_summary(self, date: str = None) -> Optional[str]:
        """
        Get formatted daily summary for ghost mode
        
        Args:
            date: Date string (YYYY-MM-DD), default today
            
        Returns:
            Formatted summary or None
        """
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        summary_file = self.summaries_dir / f"{date}.json"
        if not summary_file.exists():
            return None
        
        try:
            with open(summary_file, 'r') as f:
                summary = json.load(f)
        except:
            return None
        
        # Format summary
        entries = summary.get("entries", [])
        
        completed = []
        in_progress = []
        
        for entry in entries:
            if entry["type"] == "complete":
                completed.append(entry["data"].get("project_name", "Unknown"))
            elif entry["type"] == "progress" and entry["data"].get("milestone"):
                in_progress.append(entry["data"].get("component", "Work"))
        
        lines = [f"📅 {date} Summary"]
        
        if completed:
            lines.append("\n✅ Completed:")
            for c in completed:
                lines.append(f"   • {c}")
        
        if in_progress:
            lines.append("\n⏳ In Progress:")
            for ip in in_progress:
                lines.append(f"   • {ip}")
        
        if not completed and not in_progress:
            lines.append("\nNo activity today.")
        
        lines.append("\nType 'status' for details.")
        
        return "\n".join(lines)


# ==================== Convenience Functions ====================

def get_trust_manager() -> TrustManager:
    """Get global trust manager instance"""
    return TrustManager()


def can_use_mode(mode: str) -> bool:
    """Quick check if mode is available"""
    tm = get_trust_manager()
    
    try:
        trust_mode = TrustMode(mode.lower())
        result = tm._check_unlock(trust_mode)
        return result["unlocked"]
    except ValueError:
        return False


if __name__ == "__main__":
    # Test trust manager
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tm = TrustManager(tmpdir)
        
        print("=== Initial State ===")
        print(f"Current mode: {tm.get_current_mode().value}")
        print(f"Available modes: {[m['mode'] for m in tm.get_available_modes()]}")
        
        print("\n=== Trying to set AUTO (should fail) ===")
        result = tm.set_mode(TrustMode.AUTO)
        print(f"Result: {result}")
        
        print("\n=== Recording 3 successful projects ===")
        for i in range(3):
            result = tm.record_project({
                "name": f"Test Project {i+1}",
                "type": "cli-tool",
                "success": True,
                "tech_stack": ["Python", "Typer"],
                "duration_minutes": 30
            })
            print(f"Project {i+1}: {result['successful_projects']} successful")
            if result['new_unlocks']:
                for unlock in result['new_unlocks']:
                    print(f"  🎉 {unlock['message']}")
        
        print("\n=== Now AUTO should work ===")
        result = tm.set_mode(TrustMode.AUTO)
        print(f"Result: {result}")
        
        print(f"\nCurrent mode: {tm.get_current_mode().value}")
        
        print("\n=== Testing message formatting ===")
        print("NOTIFY mode:")
        msg = tm.format_user_message("starting", {"project_name": "My App"})
        print(f"  {msg}")
        
        tm.set_mode(TrustMode.AUTO, force=True)
        print("\nAUTO mode:")
        msg = tm.format_user_message("complete", {
            "project_name": "My App",
            "features": ["Auth", "API", "UI"],
            "run_command": "python app.py"
        })
        print(f"  {msg}")

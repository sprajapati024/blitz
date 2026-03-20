#!/usr/bin/env python3
"""
Progress Streamer - Streams casual progress updates every 5-10 minutes

Converts technical progress into human-friendly updates.
Supports Telegram notifications if Claude Code Telegram plugin is active.
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Callable

# Telegram notification helpers
def send_telegram_notification(message: str) -> bool:
    """
    Send notification via Telegram if available.
    Returns True if sent, False if no Telegram or failed.
    """
    # Check if Telegram plugin is available (set by Claude Code environment)
    telegram_available = os.environ.get('CLAUDE_TELEGRAM_AVAILABLE', 'false').lower() == 'true'
    telegram_chat_id = os.environ.get('CLAUDE_TELEGRAM_CHAT_ID')
    
    if not telegram_available or not telegram_chat_id:
        return False
    
    # Note: Actual sending is handled by Claude Code via the telegram:reply tool
    # This function just signals that a notification should be sent
    # The message will be printed and Claude will route it to Telegram if plugin is active
    return True

def notify_user(message: str, console_callback: Callable = None):
    """
    Notify user via console and/or Telegram.
    Falls back to console if Telegram not available.
    """
    # Always print to console
    if console_callback:
        console_callback(message)
    else:
        print(message)
    
    # Signal Telegram availability (Claude handles actual routing)
    if send_telegram_notification(message):
        # Telegram plugin is active - message will be routed there too
        pass

class ProgressStreamer:
    """Streams natural language progress updates"""
    
    def __init__(self, project_dir: Path, update_callback: Callable = None):
        self.project_dir = Path(project_dir)
        self.progress_file = self.project_dir / ".blitz" / "progress.json"
        self.update_callback = update_callback or print
        self.last_update = None
        self.update_interval = 300  # 5 minutes minimum between updates
    
    def check_and_report(self, force: bool = False) -> Optional[str]:
        """
        Check progress and return natural language update if enough time passed
        Sends to both console and Telegram if available.
        
        Args:
            force: Report even if not enough time passed
            
        Returns:
            Natural language progress message or None
        """
        if not self.progress_file.exists():
            return None
        
        try:
            progress = json.loads(self.progress_file.read_text())
        except (json.JSONDecodeError, IOError):
            return None
        
        # Check if enough time passed
        if not force and self.last_update:
            elapsed = time.time() - self.last_update
            if elapsed < self.update_interval:
                return None
        
        # Generate natural language update
        message = self._generate_update(progress)
        
        if message:
            self.last_update = time.time()
            # Send to both console and Telegram
            notify_user(message, self.update_callback)
        
        return message
    
    def _generate_update(self, progress: Dict[str, Any]) -> Optional[str]:
        """Convert progress data to natural language"""
        
        component = progress.get('component', '')
        status = progress.get('status', '')
        next_step = progress.get('next', '')
        percent = progress.get('percent_complete', 0)
        
        # Don't report same component twice
        if hasattr(self, '_last_component') and self._last_component == component:
            return None
        self._last_component = component
        
        # Generate casual update based on component (vibes edition)
        updates = {
            'project structure': f"Structure's locked in. On to the fun stuff...",
            'auth': f"Auth's behaving. Now building the features you actually care about...",
            'database': f"Database layer: crushed it. Connecting the pipes...",
            'api': f"API endpoints: fresh and clean. Making it pretty now...",
            'ui': f"UI coming together nicely. Writing tests so it doesn't break...",
            'tests': f"Tests passing. Just polishing the rough edges...",
            'mvp': f"MVP complete! Your baby is ready for the world 🚀"
        }
        
        # Find matching update or generate generic
        for key, message in updates.items():
            if key.lower() in component.lower():
                return message
        
        # Generic progress
        if percent > 0:
            return f"{component} {status}. About {percent}% done."
        
        return f"{component} {status}."
    
    def report_completion(self, component: str, next_component: str = None) -> str:
        """Report component completion"""
        
        completions = {
            'research': f"Research done - going with the recommended stack.",
            'architecture': f"Architecture set - {next_component or 'starting implementation'}...",
            'data layer': f"Data layer finished. Working on {next_component or 'next part'}...",
            'api': f"API working. Moving to {next_component or 'frontend'}...",
            'frontend': f"UI renders. Adding polish now...",
            'tests': f"Tests pass. Almost done...",
        }
        
        for key, message in completions.items():
            if key.lower() in component.lower():
                return message
        
        return f"{component} complete. {next_component or 'Continuing...'}"
    
    def report_error(self, error: str, suggestions: list, recommendation: str) -> str:
        """Report error with recovery options (vibes edition)"""

        suggestion_text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(suggestions)])

        return f"""Plot twist — hit a little snag with {error}

No stress, we got options:
{suggestion_text}

My gut says: {recommendation}

What feels right?"""


class ErrorRecovery:
    """Handles agent errors with recovery options"""
    
    COMMON_ERRORS = {
        'api_rate_limit': {
            'pattern': ['rate limit', '429', 'too many requests'],
            'suggestions': [
                'Add caching to reduce API calls',
                'Switch to alternative API',
                'Use mock data for development'
            ],
            'recommendation': 'Add caching - keeps us on the real API'
        },
        'api_down': {
            'pattern': ['unavailable', '503', 'timeout', 'connection error'],
            'suggestions': [
                'Switch to backup API',
                'Use mock data temporarily',
                'Add retry logic with backoff'
            ],
            'recommendation': 'Use mock data for now, fix later'
        },
        'dependency_conflict': {
            'pattern': ['conflict', 'incompatible', 'version', 'dependency'],
            'suggestions': [
                'Pin to compatible versions',
                'Switch to alternative library',
                'Create isolated environment'
            ],
            'recommendation': 'Pin versions - most reliable'
        },
        'permission_denied': {
            'pattern': ['permission', 'access denied', 'unauthorized', '403'],
            'suggestions': [
                'Fix file permissions',
                'Run with elevated privileges',
                'Change output directory'
            ],
            'recommendation': 'Fix permissions - proper solution'
        }
    }
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.errors_file = self.project_dir / ".blitz" / "errors.json"
    
    def handle_error(self, error_message: str, component: str) -> Dict[str, Any]:
        """
        Analyze error and return recovery options
        
        Returns:
            {
                'error': str,
                'component': str,
                'suggestions': list,
                'recommendation': str,
                'can_auto_recover': bool
            }
        """
        error_lower = error_message.lower()
        
        # Match against known errors
        for error_type, info in self.COMMON_ERRORS.items():
            for pattern in info['pattern']:
                if pattern in error_lower:
                    return {
                        'error': error_message,
                        'component': component,
                        'suggestions': info['suggestions'],
                        'recommendation': info['recommendation'],
                        'can_auto_recover': False,  # Always ask user
                        'error_type': error_type
                    }
        
        # Unknown error - generic response
        return {
            'error': error_message,
            'component': component,
            'suggestions': [
                'Try alternative approach',
                'Simplify the implementation',
                'Skip this feature for now'
            ],
            'recommendation': 'Try alternative approach',
            'can_auto_recover': False,
            'error_type': 'unknown'
        }
    
    def log_error(self, error_info: Dict[str, Any]):
        """Log error to errors.json"""
        errors = []
        if self.errors_file.exists():
            try:
                errors = json.loads(self.errors_file.read_text())
            except:
                pass
        
        errors.append({
            **error_info,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'resolved': False
        })
        
        self.errors_file.parent.mkdir(parents=True, exist_ok=True)
        self.errors_file.write_text(json.dumps(errors, indent=2))
    
    def mark_resolved(self, error_index: int, resolution: str):
        """Mark error as resolved"""
        if not self.errors_file.exists():
            return
        
        try:
            errors = json.loads(self.errors_file.read_text())
            if 0 <= error_index < len(errors):
                errors[error_index]['resolved'] = True
                errors[error_index]['resolution'] = resolution
                errors[error_index]['resolved_at'] = datetime.now(timezone.utc).isoformat()
                self.errors_file.write_text(json.dumps(errors, indent=2))
        except:
            pass


if __name__ == "__main__":
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test progress streamer
        streamer = ProgressStreamer(tmpdir)
        
        # Simulate progress updates
        progress_file = Path(tmpdir) / ".blitz" / "progress.json"
        progress_file.parent.mkdir(parents=True, exist_ok=True)
        
        progress_file.write_text(json.dumps({
            'component': 'auth middleware',
            'status': 'complete',
            'percent_complete': 35,
            'next': 'user API'
        }))
        
        message = streamer.check_and_report(force=True)
        print(f"Progress update: {message}")
        
        # Test error recovery
        recovery = ErrorRecovery(tmpdir)
        error_info = recovery.handle_error(
            "API rate limit exceeded (429)",
            "data fetching"
        )
        print(f"\nError handled: {error_info}")

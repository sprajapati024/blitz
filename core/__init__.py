"""
Blitz v3 - Autonomous Development Team
Core module for intent detection, agent spawning, and doc management.
"""

from .intent_detector import IntentDetector
from .state_manager import StateManager
from .doc_updater import DocUpdater
from .agent_spawner import AgentSpawner

__all__ = ['IntentDetector', 'StateManager', 'DocUpdater', 'AgentSpawner']

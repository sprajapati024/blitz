#!/usr/bin/env python3
"""
Intent Detector - Identifies when user wants to build/fix/update
"""

import re
from enum import Enum
from typing import Optional, Dict, Any

class IntentType(Enum):
    BUILD = "build"      # Create new project/feature
    FIX = "fix"          # Fix bug/issue
    UPDATE = "update"    # Update existing feature
    REFACTOR = "refactor" # Restructure code
    RESEARCH = "research" # Research topic
    UNKNOWN = "unknown"  # No clear intent

class IntentDetector:
    """Detects user intent from natural language"""
    
    # Patterns that indicate BUILD intent
    BUILD_PATTERNS = [
        r"build me\s+(?:a|an)?\s*(.+)",
        r"create\s+(?:a|an)?\s*(.+)",
        r"make\s+(?:a|an)?\s*(.+)",
        r"i want\s+(?:a|an)?\s*(.+)",
        r"i need\s+(?:a|an)?\s*(.+)",
        r"can you\s+(?:build|create|make)\s+(?:a|an)?\s*(.+)",
        r"let's\s+(?:build|create|make)\s+(?:a|an)?\s*(.+)",
        r"start\s+(?:a|an)?\s*(.+\s+project)",
        r"new\s+(?:project|app|tool|bot|system)",
    ]
    
    # Patterns that indicate FIX intent
    FIX_PATTERNS = [
        r"fix\s+(.+)",
        r"debug\s+(.+)",
        r"repair\s+(.+)",
        r"it's\s+broken",
        r"not\s+working",
        r"there's\s+a\s+bug",
        r"crashing",
        r"error\s+in",
    ]
    
    # Patterns that indicate UPDATE intent
    UPDATE_PATTERNS = [
        r"add\s+(.+)",
        r"update\s+(.+)",
        r"change\s+(.+)",
        r"modify\s+(.+)",
        r"implement\s+(.+)",
        r"support\s+(.+)",
        r"enable\s+(.+)",
    ]
    
    # Patterns that indicate REFACTOR intent
    REFACTOR_PATTERNS = [
        r"refactor\s+(.+)",
        r"restructure\s+(.+)",
        r"rewrite\s+(.+)",
        r"clean\s+up\s+(.+)",
        r"simplify\s+(.+)",
        r"optimize\s+(.+)",
    ]
    
    # Patterns that indicate RESEARCH intent
    RESEARCH_PATTERNS = [
        r"research\s+(.+)",
        r"find\s+(?:out\s+)?(?:about\s+)?(.+)",
        r"what\s+(?:is|are)\s+(.+)",
        r"compare\s+(.+)",
        r"best\s+way\s+to",
        r"should\s+i\s+use",
    ]
    
    def detect(self, message: str) -> Dict[str, Any]:
        """
        Detect intent from user message
        
        Returns:
            {
                'intent': IntentType,
                'confidence': float (0-1),
                'subject': str (what they want to build/fix/etc),
                'raw_message': str
            }
        """
        message_lower = message.lower().strip()
        
        # Check each intent type in order of priority
        for intent_type, patterns in [
            (IntentType.BUILD, self.BUILD_PATTERNS),
            (IntentType.FIX, self.FIX_PATTERNS),
            (IntentType.UPDATE, self.UPDATE_PATTERNS),
            (IntentType.REFACTOR, self.REFACTOR_PATTERNS),
            (IntentType.RESEARCH, self.RESEARCH_PATTERNS),
        ]:
            for pattern in patterns:
                match = re.search(pattern, message_lower)
                if match:
                    subject = match.group(1).strip() if match.groups() else ""
                    confidence = self._calculate_confidence(message_lower, pattern)
                    return {
                        'intent': intent_type,
                        'confidence': confidence,
                        'subject': subject,
                        'raw_message': message
                    }
        
        # No intent detected
        return {
            'intent': IntentType.UNKNOWN,
            'confidence': 0.0,
            'subject': "",
            'raw_message': message
        }
    
    def _calculate_confidence(self, message: str, matched_pattern: str) -> float:
        """Calculate confidence score based on match quality"""
        # Start with base confidence
        confidence = 0.7
        
        # Boost for longer, more specific messages
        words = len(message.split())
        if words > 5:
            confidence += 0.1
        if words > 10:
            confidence += 0.1
        
        # Cap at 0.95
        return min(confidence, 0.95)
    
    def should_intercept(self, message: str, threshold: float = 0.6) -> bool:
        """
        Decide if Blitz should take over the conversation
        
        Args:
            message: User's message
            threshold: Minimum confidence to intercept
            
        Returns:
            True if Blitz should manage this request
        """
        result = self.detect(message)
        return result['confidence'] >= threshold and result['intent'] != IntentType.UNKNOWN
    
    def get_clarifying_questions(self, intent: IntentType, subject: str) -> list:
        """
        Get the 3-4 clarifying questions based on intent
        
        Returns list of question dicts with id, question, and options
        """
        if intent == IntentType.BUILD:
            return [
                {
                    'id': 'audience',
                    'question': 'Who will use this?',
                    'options': ['Just me', 'My team', 'Public users', 'Enterprise'],
                    'type': 'select'
                },
                {
                    'id': 'features',
                    'question': 'What are the must-have features?',
                    'help': 'List 2-3 core features (comma separated)',
                    'type': 'text'
                },
                {
                    'id': 'tech',
                    'question': 'Any tech preference?',
                    'options': ['No preference', 'Python', 'JavaScript/TypeScript', 'Go', 'Other'],
                    'type': 'select'
                },
                {
                    'id': 'timeline',
                    'question': 'Timeline?',
                    'options': ['This week', 'This month', 'No rush'],
                    'type': 'select'
                }
            ]
        elif intent == IntentType.FIX:
            return [
                {
                    'id': 'issue',
                    'question': 'What exactly is broken?',
                    'type': 'text'
                },
                {
                    'id': 'reproduce',
                    'question': 'How can I reproduce it?',
                    'type': 'text'
                }
            ]
        elif intent == IntentType.UPDATE:
            return [
                {
                    'id': 'what',
                    'question': f'What should I add to {subject}?',
                    'type': 'text'
                },
                {
                    'id': 'priority',
                    'question': 'How important is this?',
                    'options': ['Critical - blocking', 'Important - needed soon', 'Nice to have'],
                    'type': 'select'
                }
            ]
        else:
            return [
                {
                    'id': 'details',
                    'question': 'Tell me more about what you need:',
                    'type': 'text'
                }
            ]


# Singleton instance
_detector = None

def get_detector() -> IntentDetector:
    """Get singleton intent detector"""
    global _detector
    if _detector is None:
        _detector = IntentDetector()
    return _detector


if __name__ == "__main__":
    # Test the detector
    detector = IntentDetector()
    
    test_messages = [
        "Build me a trading bot for stocks",
        "I need a habit tracker app",
        "Fix the login bug",
        "Add push notifications",
        "Research best auth libraries",
        "How's the weather today?",  # Should be unknown
    ]
    
    for msg in test_messages:
        result = detector.detect(msg)
        should_intercept = detector.should_intercept(msg)
        print(f"\nMessage: {msg}")
        print(f"  Intent: {result['intent'].value}")
        print(f"  Subject: {result['subject']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Intercept: {should_intercept}")

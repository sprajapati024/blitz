#!/usr/bin/env python3
"""
Tests for Intent Detector (0% coverage target)

Tests:
- All BUILD patterns (8 patterns)
- All FIX patterns (8 patterns)
- All UPDATE patterns (7 patterns)
- All REFACTOR patterns (6 patterns)
- All RESEARCH patterns (6 patterns)
- Confidence calculation edge cases
- should_intercept with different thresholds
- get_clarifying_questions for each intent type
- Unknown falls through
- Singleton get_detector() thread safety
"""

import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.intent_detector import IntentDetector, IntentType, get_detector


class TestIntentPatterns:
    """Test intent detection patterns"""

    def test_build_patterns(self):
        """Test all BUILD patterns"""
        detector = IntentDetector()

        build_messages = [
            ("build me a trading bot", "trading bot"),
            ("create a web app", "web app"),
            ("make an api", "api"),
            ("i want a chatbot", "chatbot"),
            ("i need a dashboard", "dashboard"),
            ("can you build a calculator", "calculator"),
            ("can you create a tool", "tool"),
            ("can you make an app", "app"),
            ("let's build a bot", "bot"),
            ("let's create a system", "system"),
            ("start a new project", "new project"),
        ]

        for msg, expected_subject in build_messages:
            result = detector.detect(msg)
            assert result["intent"] == IntentType.BUILD, f"Failed for: {msg}"
            if expected_subject:
                assert expected_subject in result["subject"], (
                    f"Subject mismatch for {msg}: got '{result['subject']}'"
                )

        print("✅ All BUILD patterns detected correctly")
        return True

    def test_fix_patterns(self):
        """Test all FIX patterns"""
        detector = IntentDetector()

        fix_messages = [
            ("fix the login bug", "the login bug"),
            ("debug the api", "the api"),
            ("repair the database", "the database"),
            ("it's broken", ""),
            ("not working", ""),
            ("there's a bug", ""),
            ("crashing", ""),
            ("error in the code", "the code"),
            ("error in production", "production"),
        ]

        for msg, expected_subject in fix_messages:
            result = detector.detect(msg)
            assert result["intent"] == IntentType.FIX, f"Failed for: {msg}"

        print("✅ All FIX patterns detected correctly")
        return True

    def test_update_patterns(self):
        """Test all UPDATE patterns"""
        detector = IntentDetector()

        update_messages = [
            ("add user authentication", "user authentication"),
            ("update the dashboard", "the dashboard"),
            ("change the layout", "the layout"),
            ("modify the settings", "the settings"),
            ("implement notifications", "notifications"),
            ("support dark mode", "dark mode"),
            ("enable caching", "caching"),
        ]

        for msg, expected_subject in update_messages:
            result = detector.detect(msg)
            assert result["intent"] == IntentType.UPDATE, f"Failed for: {msg}"
            assert expected_subject in result["subject"], f"Subject mismatch for {msg}"

        print("✅ All UPDATE patterns detected correctly")
        return True

    def test_refactor_patterns(self):
        """Test all REFACTOR patterns"""
        detector = IntentDetector()

        refactor_messages = [
            ("refactor the auth module", "the auth module"),
            ("restructure the codebase", "the codebase"),
            ("rewrite the parser", "the parser"),
            ("clean up the utils", "the utils"),
            ("simplify the logic", "the logic"),
            ("optimize the database queries", "the database queries"),
        ]

        for msg, expected_subject in refactor_messages:
            result = detector.detect(msg)
            assert result["intent"] == IntentType.REFACTOR, f"Failed for: {msg}"
            assert expected_subject in result["subject"], f"Subject mismatch for {msg}"

        print("✅ All REFACTOR patterns detected correctly")
        return True

    def test_research_patterns(self):
        """Test all RESEARCH patterns"""
        detector = IntentDetector()

        research_messages = [
            ("research authentication libraries", "authentication libraries"),
            ("find out about react", "react"),
            ("find about vuejs", "vuejs"),
            ("what is docker", "docker"),
            ("what are the best frameworks", "the best frameworks"),
            ("compare python and go", "python and go"),
            ("best way to learn rust", "rust"),
            ("should i use typescript", "typescript"),
        ]

        for msg, expected_subject in research_messages:
            result = detector.detect(msg)
            assert result["intent"] == IntentType.RESEARCH, f"Failed for: {msg}"

        print("✅ All RESEARCH patterns detected correctly")
        return True

    def test_priority_order(self):
        """Test that BUILD takes priority over other patterns"""
        detector = IntentDetector()

        result = detector.detect("build me a bot and fix the bug")
        assert result["intent"] == IntentType.BUILD

        result = detector.detect("create an api and add caching")
        assert result["intent"] == IntentType.BUILD

        print("✅ Priority order correct")
        return True

    def test_unknown_falls_through(self):
        """Test that unknown messages return UNKNOWN intent"""
        detector = IntentDetector()

        unknown_messages = [
            "hello there",
            "how's the weather today?",
            "what did you eat for lunch?",
            "random text with no clear intent",
            "",
            "   ",
        ]

        for msg in unknown_messages:
            result = detector.detect(msg)
            assert result["intent"] == IntentType.UNKNOWN, f"Should be UNKNOWN: {msg}"
            assert result["confidence"] == 0.0, f"Confidence should be 0.0: {msg}"
            assert result["subject"] == "", f"Subject should be empty: {msg}"

        print("✅ Unknown falls through correctly")
        return True


class TestConfidenceCalculation:
    """Test confidence score calculation"""

    def test_base_confidence(self):
        """Test base confidence is 0.7"""
        detector = IntentDetector()
        result = detector.detect("build me a bot")
        assert result["confidence"] == 0.7
        print("✅ Base confidence is 0.7")
        return True

    def test_longer_message_boost(self):
        """Test confidence boost for longer messages"""
        detector = IntentDetector()

        short = detector.detect("build me a bot")
        assert short["confidence"] == 0.7

        medium = detector.detect("build me a trading bot with portfolio tracking")
        assert abs(medium["confidence"] - 0.8) < 0.001

        long_msg = "build me a sophisticated trading bot with portfolio tracking and real-time market analysis"
        long_result = detector.detect(long_msg)
        assert abs(long_result["confidence"] - 0.9) < 0.001

        print("✅ Confidence boost for longer messages")
        return True

    def test_confidence_cap(self):
        """Test confidence is capped at 0.95"""
        detector = IntentDetector()

        very_long = "build me " + "a really " * 50 + "complex trading bot"
        result = detector.detect(very_long)
        assert result["confidence"] <= 0.95

        print("✅ Confidence capped at 0.95")
        return True


class TestShouldIntercept:
    """Test should_intercept method"""

    def test_default_threshold(self):
        """Test default threshold of 0.6"""
        detector = IntentDetector()

        low_confidence = detector.should_intercept("build")
        assert low_confidence is False

        normal = detector.should_intercept("build me a trading bot")
        assert normal is True

        print("✅ Default threshold works")
        return True

    def test_custom_threshold(self):
        """Test custom threshold values"""
        detector = IntentDetector()

        msg = "build me a bot"
        assert detector.should_intercept(msg, threshold=0.5) is True
        assert detector.should_intercept(msg, threshold=0.7) is True
        assert detector.should_intercept(msg, threshold=0.8) is False

        high_conf = "build me a sophisticated trading bot with portfolio tracking and real-time market analysis"
        assert detector.should_intercept(high_conf, threshold=0.85) is True

        print("✅ Custom thresholds work")
        return True

    def test_unknown_never_intercepts(self):
        """Test that UNKNOWN intent never intercepts regardless of confidence"""
        detector = IntentDetector()

        result = detector.detect("hello there")
        assert result["intent"] == IntentType.UNKNOWN

        assert detector.should_intercept("hello there") is False
        assert detector.should_intercept("hello there", threshold=0.0) is False

        print("✅ UNKNOWN never intercepts")
        return True


class TestClarifyingQuestions:
    """Test get_clarifying_questions method"""

    def test_build_questions(self):
        """Test BUILD clarifying questions"""
        detector = IntentDetector()

        questions = detector.get_clarifying_questions(IntentType.BUILD, "chatbot")

        assert len(questions) == 4

        ids = [q["id"] for q in questions]
        assert "audience" in ids
        assert "features" in ids
        assert "tech" in ids
        assert "timeline" in ids

        audience_q = next(q for q in questions if q["id"] == "audience")
        assert audience_q["type"] == "select"
        assert "Just me" in audience_q["options"]

        features_q = next(q for q in questions if q["id"] == "features")
        assert features_q["type"] == "text"

        print("✅ BUILD clarifying questions correct")
        return True

    def test_fix_questions(self):
        """Test FIX clarifying questions"""
        detector = IntentDetector()

        questions = detector.get_clarifying_questions(IntentType.FIX, "")

        assert len(questions) == 2

        ids = [q["id"] for q in questions]
        assert "issue" in ids
        assert "reproduce" in ids

        issue_q = next(q for q in questions if q["id"] == "issue")
        assert issue_q["type"] == "text"

        print("✅ FIX clarifying questions correct")
        return True

    def test_update_questions(self):
        """Test UPDATE clarifying questions"""
        detector = IntentDetector()

        questions = detector.get_clarifying_questions(IntentType.UPDATE, "auth")

        assert len(questions) == 2

        ids = [q["id"] for q in questions]
        assert "what" in ids
        assert "priority" in ids

        what_q = next(q for q in questions if q["id"] == "what")
        assert "auth" in what_q["question"]

        print("✅ UPDATE clarifying questions correct")
        return True

    def test_unknown_questions(self):
        """Test default questions for unknown/other intents"""
        detector = IntentDetector()

        questions = detector.get_clarifying_questions(IntentType.RESEARCH, "")

        assert len(questions) == 1

        q = questions[0]
        assert q["id"] == "details"
        assert q["type"] == "text"

        questions = detector.get_clarifying_questions(IntentType.REFACTOR, "")
        assert len(questions) == 1

        print("✅ Default questions for other intents correct")
        return True


class TestSingletonThreadSafety:
    """Test get_detector() singleton thread safety"""

    def test_singleton_returns_same_instance(self):
        """Test that get_detector returns the same instance"""
        detector1 = get_detector()
        detector2 = get_detector()

        assert detector1 is detector2

        print("✅ Singleton returns same instance")
        return True

    def test_concurrent_access(self):
        """Test concurrent access to get_detector"""
        results = []
        errors = []

        def get_detector_twice():
            try:
                d1 = get_detector()
                d2 = get_detector()
                results.append(d1 is d2)
            except Exception as e:
                errors.append(str(e))

        threads = [threading.Thread(target=get_detector_twice) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert all(results), "Not all results were True"

        print("✅ Concurrent access thread-safe")
        return True


def run_all_tests():
    """Run all intent detector tests"""
    print("\n" + "=" * 60)
    print("TESTS: Intent Detector (0% coverage target)")
    print("=" * 60 + "\n")

    test_patterns = TestIntentPatterns()
    test_confidence = TestConfidenceCalculation()
    test_intercept = TestShouldIntercept()
    test_questions = TestClarifyingQuestions()
    test_singleton = TestSingletonThreadSafety()

    tests = [
        ("BUILD patterns", test_patterns.test_build_patterns),
        ("FIX patterns", test_patterns.test_fix_patterns),
        ("UPDATE patterns", test_patterns.test_update_patterns),
        ("REFACTOR patterns", test_patterns.test_refactor_patterns),
        ("RESEARCH patterns", test_patterns.test_research_patterns),
        ("Priority order", test_patterns.test_priority_order),
        ("Unknown falls through", test_patterns.test_unknown_falls_through),
        ("Base confidence", test_confidence.test_base_confidence),
        ("Longer message boost", test_confidence.test_longer_message_boost),
        ("Confidence cap", test_confidence.test_confidence_cap),
        ("Default threshold", test_intercept.test_default_threshold),
        ("Custom threshold", test_intercept.test_custom_threshold),
        ("UNKNOWN never intercepts", test_intercept.test_unknown_never_intercepts),
        ("BUILD questions", test_questions.test_build_questions),
        ("FIX questions", test_questions.test_fix_questions),
        ("UPDATE questions", test_questions.test_update_questions),
        ("Unknown questions", test_questions.test_unknown_questions),
        ("Singleton returns same", test_singleton.test_singleton_returns_same_instance),
        ("Concurrent access", test_singleton.test_concurrent_access),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            print(f"❌ FAILED: {name}")
            print(f"   Error: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

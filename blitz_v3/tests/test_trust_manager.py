#!/usr/bin/env python3
"""
Integration tests for Trust Manager (Phase 3)

Tests:
- Mode switching with unlock requirements
- Project history tracking
- Message formatting per mode
- Daily summaries
"""

import sys
import tempfile
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.trust_manager import TrustManager, TrustMode


class TestTrustManager:
    """Test trust manager functionality"""
    
    def test_default_mode_is_notify(self):
        """Verify default mode is NOTIFY"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            assert tm.get_current_mode() == TrustMode.NOTIFY
            print("✅ Default mode is NOTIFY")
            return True
    
    def test_auto_mode_locked_initially(self):
        """Verify AUTO mode is locked with 0 projects"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            result = tm._check_unlock(TrustMode.AUTO)
            assert not result["unlocked"]
            assert result["required"] == 3
            print("✅ AUTO mode locked initially")
            return True
    
    def test_ghost_mode_locked_initially(self):
        """Verify GHOST mode is locked with 0 projects"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            result = tm._check_unlock(TrustMode.GHOST)
            assert not result["unlocked"]
            assert result["required"] == 10
            print("✅ GHOST mode locked initially")
            return True
    
    def test_cannot_switch_to_locked_mode(self):
        """Verify cannot switch to locked mode"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            result = tm.set_mode(TrustMode.AUTO)
            assert not result["success"]
            assert "3 successful projects" in result["message"]
            print("✅ Cannot switch to locked mode")
            return True
    
    def test_auto_unlocks_after_3_projects(self):
        """Verify AUTO unlocks after 3 successful projects"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            
            # Record 2 projects
            for i in range(2):
                tm.record_project({
                    "name": f"Project {i+1}",
                    "success": True
                })
            
            # Should still be locked
            result = tm.set_mode(TrustMode.AUTO)
            assert not result["success"]
            
            # Record 3rd project
            result = tm.record_project({
                "name": "Project 3",
                "success": True
            })
            
            # Should have unlocked AUTO
            assert len(result["new_unlocks"]) == 1
            assert result["new_unlocks"][0]["mode"] == "auto"
            
            # Should now be able to switch
            result = tm.set_mode(TrustMode.AUTO)
            assert result["success"]
            assert tm.get_current_mode() == TrustMode.AUTO
            
            print("✅ AUTO unlocks after 3 projects")
            return True
    
    def test_project_stats_tracking(self):
        """Verify project stats are tracked correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            
            # Record some projects
            tm.record_project({"name": "CLI Tool", "type": "cli", "success": True, "tech_stack": ["Python"]})
            tm.record_project({"name": "Web App", "type": "web", "success": True, "tech_stack": ["Python", "React"]})
            tm.record_project({"name": "Failed Bot", "type": "bot", "success": False})
            
            stats = tm.get_project_stats()
            
            assert stats["total"] == 3
            assert stats["successful"] == 2
            assert stats["failed"] == 1
            assert stats["by_type"]["cli"] == 1
            assert stats["by_type"]["web"] == 1
            
            print("✅ Project stats tracked correctly")
            return True
    
    def test_notify_mode_messages(self):
        """Verify NOTIFY mode formats all messages"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            
            # All messages should be formatted
            start_msg = tm.format_user_message("starting", {"project_name": "Test"})
            assert start_msg is not None
            assert "Building" in start_msg
            
            progress_msg = tm.format_user_message("progress", {"component": "Auth", "status": "done"})
            assert progress_msg is not None
            
            complete_msg = tm.format_user_message("complete", {
                "project_name": "Test",
                "features": ["Auth"],
                "run_command": "python app.py"
            })
            assert complete_msg is not None
            assert "Done!" in complete_msg
            
            print("✅ NOTIFY mode formats all messages")
            return True
    
    def test_auto_mode_suppresses_starting_message(self):
        """Verify AUTO mode suppresses 'starting' message"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            tm.set_mode(TrustMode.AUTO, force=True)
            
            # Starting message should be suppressed
            start_msg = tm.format_user_message("starting", {"project_name": "Test"})
            assert start_msg is None
            
            # But complete should still show
            complete_msg = tm.format_user_message("complete", {
                "project_name": "Test",
                "features": ["Auth"],
                "run_command": "python app.py"
            })
            assert complete_msg is not None
            
            print("✅ AUTO mode suppresses starting message")
            return True
    
    def test_ghost_mode_logs_to_summary(self):
        """Verify GHOST mode logs to summary instead of sending"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            tm.set_mode(TrustMode.GHOST, force=True)
            
            # Message should be logged, not returned
            result = tm.format_user_message("complete", {
                "project_name": "Test",
                "features": ["Auth"]
            })
            assert result is None
            
            # But should be in daily summary
            summary = tm.get_daily_summary()
            assert summary is not None
            assert "Test" in summary
            
            print("✅ GHOST mode logs to summary")
            return True
    
    def test_should_ask_before_action(self):
        """Verify should_ask logic per mode"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            
            # NOTIFY: ask for everything
            assert tm.should_ask_before_action("spawn_agents")
            assert tm.should_ask_before_action("make_decision")
            
            # AUTO: only ask for major decisions
            tm.set_mode(TrustMode.AUTO, force=True)
            assert not tm.should_ask_before_action("spawn_agents")
            assert tm.should_ask_before_action("change_tech_stack")
            
            # GHOST: almost never ask
            tm.set_mode(TrustMode.GHOST, force=True)
            assert not tm.should_ask_before_action("spawn_agents")
            assert not tm.should_ask_before_action("change_tech_stack")
            assert tm.should_ask_before_action("delete_project")
            
            print("✅ should_ask logic works per mode")
            return True
    
    def test_get_available_modes(self):
        """Verify get_available_modes returns all modes with status"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tm = TrustManager(tmpdir)
            
            modes = tm.get_available_modes()
            
            assert len(modes) == 3
            
            # NOTIFY should be unlocked
            notify = [m for m in modes if m["mode"] == "notify"][0]
            assert notify["unlocked"]
            
            # AUTO should be locked
            auto = [m for m in modes if m["mode"] == "auto"][0]
            assert not auto["unlocked"]
            assert auto["required"] == 3
            
            print("✅ get_available_modes works")
            return True
    
    def test_persistence(self):
        """Verify preferences persist across instances"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # First instance
            tm1 = TrustManager(tmpdir)
            tm1.set_mode(TrustMode.AUTO, force=True)
            
            # Second instance
            tm2 = TrustManager(tmpdir)
            assert tm2.get_current_mode() == TrustMode.AUTO
            
            # History should persist too
            tm1.record_project({"name": "Test", "success": True})
            tm3 = TrustManager(tmpdir)
            assert tm3.get_successful_project_count() == 1
            
            print("✅ Preferences and history persist")
            return True


def run_all_tests():
    """Run all trust manager tests"""
    print("\n" + "="*60)
    print("INTEGRATION TESTS: Trust Manager (Phase 3)")
    print("="*60 + "\n")
    
    test = TestTrustManager()
    
    tests = [
        ("Default mode is NOTIFY", test.test_default_mode_is_notify),
        ("AUTO mode locked initially", test.test_auto_mode_locked_initially),
        ("GHOST mode locked initially", test.test_ghost_mode_locked_initially),
        ("Cannot switch to locked mode", test.test_cannot_switch_to_locked_mode),
        ("AUTO unlocks after 3 projects", test.test_auto_unlocks_after_3_projects),
        ("Project stats tracking", test.test_project_stats_tracking),
        ("NOTIFY mode messages", test.test_notify_mode_messages),
        ("AUTO mode suppresses starting", test.test_auto_mode_suppresses_starting_message),
        ("GHOST mode logs to summary", test.test_ghost_mode_logs_to_summary),
        ("should_ask before action", test.test_should_ask_before_action),
        ("get_available_modes", test.test_get_available_modes),
        ("Persistence", test.test_persistence),
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
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Tests for Agent Spawner (0% coverage target)

Tests:
- spawn_architect creates correct info dict
- spawn_coder creates checkpoint before coding
- spawn_all_for_project sequence
- handle_user_interrupt delegates to InterruptHandler
- trust mode integration methods
- message formatting methods
- record_project_completion flow
- get_available_trust_modes
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent_spawner import AgentSpawner
from core.checkpoint_manager import CheckpointManager, InterruptHandler
from core.trust_manager import TrustManager, TrustMode


class TestSpawnArchitect:
    """Test spawn_architect method"""

    def setup_spawner(self, tmpdir):
        """Create a spawner with minimal project"""
        project_dir = Path(tmpdir) / "test_project"
        project_dir.mkdir()
        return AgentSpawner(project_dir)

    def test_creates_correct_info_dict(self):
        """Test spawn_architect returns correct info dict"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = self.setup_spawner(tmpdir)

            info = spawner.spawn_architect(
                requirements="Build a trading bot",
                tech_preference="Python",
                features="paper trading, alerts",
            )

            assert "id" in info
            assert info["type"] == "architect"
            assert info["status"] == "spawned"
            assert "prompt" in info
            assert "outputs" in info
            assert "architecture_file" in info["outputs"]
            assert "decisions_file" in info["outputs"]
            assert "estimated_time" in info

            assert "Design system architecture for:" in info["prompt"]
            assert "Python" in info["prompt"]
            assert "paper trading, alerts" in info["prompt"]

            print("✅ spawn_architect creates correct info dict")
            return True

    def test_tracks_running_agent(self):
        """Test spawn_architect tracks the agent"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = self.setup_spawner(tmpdir)

            assert len(spawner.running_agents) == 0

            info = spawner.spawn_architect("Build a bot")

            assert len(spawner.running_agents) == 1
            assert info["id"] in spawner.running_agents

            print("✅ spawn_architect tracks running agent")
            return True

    def test_calls_on_spawn_callback(self):
        """Test spawn_architect calls on_spawn callback"""
        with tempfile.TemporaryDirectory() as tmpdir:
            callback_called = []

            def on_spawn(info):
                callback_called.append(info)

            spawner = AgentSpawner(
                Path(tmpdir) / "test", callbacks={"on_spawn": on_spawn}
            )

            info = spawner.spawn_architect("Build a bot")

            assert len(callback_called) == 1
            assert callback_called[0]["id"] == info["id"]

            print("✅ spawn_architect calls on_spawn callback")
            return True


class TestSpawnCoder:
    """Test spawn_coder method"""

    def setup_spawner(self, tmpdir):
        """Create a spawner with minimal project"""
        project_dir = Path(tmpdir) / "test_project"
        project_dir.mkdir()
        return AgentSpawner(project_dir)

    def test_creates_checkpoint_before_coding(self):
        """Test spawn_coder creates checkpoint before coding"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = self.setup_spawner(tmpdir)

            (Path(tmpdir) / "test_project" / "ARCHITECTURE.md").write_text(
                "# Architecture"
            )

            info = spawner.spawn_coder(
                architecture_path=str(
                    Path(tmpdir) / "test_project" / "ARCHITECTURE.md"
                ),
                task="Implement MVP",
            )

            assert "checkpoint_id" in info
            assert info["checkpoint_id"] is not None

            cp_manager = CheckpointManager(Path(tmpdir) / "test_project")
            checkpoints = cp_manager.list_checkpoints()
            assert len(checkpoints) == 1
            assert checkpoints[0].id == info["checkpoint_id"]

            print("✅ spawn_coder creates checkpoint before coding")
            return True

    def test_returns_correct_info_dict(self):
        """Test spawn_coder returns correct info dict"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = self.setup_spawner(tmpdir)

            (Path(tmpdir) / "test_project" / "ARCHITECTURE.md").write_text(
                "# Architecture"
            )

            info = spawner.spawn_coder(
                architecture_path=str(
                    Path(tmpdir) / "test_project" / "ARCHITECTURE.md"
                ),
                task="Implement auth",
            )

            assert "id" in info
            assert info["type"] == "coder"
            assert info["task"] == "Implement auth"
            assert info["status"] == "spawned"
            assert "prompt" in info
            assert "outputs" in info
            assert "code_dir" in info["outputs"]
            assert "changelog" in info["outputs"]
            assert "estimated_time" in info

            print("✅ spawn_coder returns correct info dict")
            return True


class TestHandleUserInterrupt:
    """Test handle_user_interrupt method"""

    def test_delegates_to_interrupt_handler(self):
        """Test handle_user_interrupt delegates to InterruptHandler"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            project_dir.mkdir()

            spawner = AgentSpawner(project_dir)

            result = spawner.handle_user_interrupt("Use PostgreSQL instead")

            assert "options" in result
            assert "interruption_checkpoint" in result

            print("✅ handle_user_interrupt delegates to InterruptHandler")
            return True


class TestTrustModeIntegration:
    """Test trust mode integration methods"""

    def test_get_trust_mode(self):
        """Test get_trust_mode returns current mode"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = AgentSpawner(Path(tmpdir) / "test")

            mode = spawner.get_trust_mode()
            assert mode in [TrustMode.NOTIFY, TrustMode.AUTO, TrustMode.GHOST]

            print("✅ get_trust_mode works")
            return True

    def test_set_trust_mode_valid(self):
        """Test set_trust_mode with valid mode"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = AgentSpawner(Path(tmpdir) / "test")

            result = spawner.set_trust_mode("auto", force=True)
            assert result["success"] is True

            assert spawner.get_trust_mode() == TrustMode.AUTO

            print("✅ set_trust_mode with valid mode works")
            return True

    def test_set_trust_mode_invalid(self):
        """Test set_trust_mode with invalid mode"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = AgentSpawner(Path(tmpdir) / "test")

            result = spawner.set_trust_mode("invalid_mode")
            assert result["success"] is False
            assert "Invalid mode" in result["message"]

            print("✅ set_trust_mode with invalid mode returns error")
            return True


class TestMessageFormatting:
    """Test message formatting methods"""

    def test_format_progress_message(self):
        """Test format_progress_message"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = AgentSpawner(Path(tmpdir) / "test")

            msg = spawner.format_progress_message("Auth module", "done", milestone=True)
            assert msg is not None

            print("✅ format_progress_message works")
            return True

    def test_format_completion_message(self):
        """Test format_completion_message"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = AgentSpawner(Path(tmpdir) / "test")

            msg = spawner.format_completion_message(
                project_name="Trading Bot",
                features=["paper trading", "alerts"],
                run_command="python bot.py",
            )
            assert msg is not None

            print("✅ format_completion_message works")
            return True

    def test_format_error_message(self):
        """Test format_error_message"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = AgentSpawner(Path(tmpdir) / "test")

            msg = spawner.format_error_message(
                error="Database connection failed",
                options=["Check credentials", "Use SQLite instead"],
                recommendation="Use SQLite",
            )
            assert msg is not None
            assert "Database connection failed" in msg

            print("✅ format_error_message works")
            return True


class TestRecordProjectCompletion:
    """Test record_project_completion method"""

    def test_records_completion(self):
        """Test record_project_completion"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = AgentSpawner(Path(tmpdir) / "test")
            spawner._project_start_time = None

            result = spawner.record_project_completion(
                success=True, features=["Auth", "API"], tech_stack=["Python", "Flask"]
            )

            assert "recorded" in result
            assert result["recorded"] is True

            print("✅ record_project_completion works")
            return True


class TestGetAvailableTrustModes:
    """Test get_available_trust_modes method"""

    def test_returns_all_modes(self):
        """Test get_available_trust_modes returns all modes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = AgentSpawner(Path(tmpdir) / "test")

            modes = spawner.get_available_trust_modes()

            assert len(modes) == 3

            mode_names = [m["mode"] for m in modes]
            assert "notify" in mode_names
            assert "auto" in mode_names
            assert "ghost" in mode_names

            print("✅ get_available_trust_modes returns all modes")
            return True


class TestGetAgentStatus:
    """Test agent status methods"""

    def test_get_agent_status(self):
        """Test get_agent_status returns correct status"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            project_dir.mkdir()

            spawner = AgentSpawner(project_dir)
            (project_dir / "ARCHITECTURE.md").write_text("# Arch")

            info = spawner.spawn_architect("Build a bot")

            status = spawner.get_agent_status(info["id"])
            assert status is not None
            assert status["id"] == info["id"]

            print("✅ get_agent_status works")
            return True

    def test_get_agent_status_not_found(self):
        """Test get_agent_status returns None for unknown agent"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = AgentSpawner(Path(tmpdir) / "test")

            status = spawner.get_agent_status("nonexistent_id")
            assert status is None

            print("✅ get_agent_status returns None for unknown")
            return True

    def test_get_all_status(self):
        """Test get_all_status returns all agents"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            project_dir.mkdir()

            spawner = AgentSpawner(project_dir)
            (project_dir / "ARCHITECTURE.md").write_text("# Arch")

            spawner.spawn_architect("Build a bot")
            spawner.spawn_coder(str(project_dir / "ARCHITECTURE.md"), "Implement")

            status = spawner.get_all_status()
            assert status["running"] == 2
            assert len(status["agents"]) == 2

            print("✅ get_all_status works")
            return True


class TestCheckpointMethods:
    """Test checkpoint-related methods"""

    def test_create_manual_checkpoint(self):
        """Test create_manual_checkpoint"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spawner = AgentSpawner(Path(tmpdir) / "test")

            result = spawner.create_manual_checkpoint(
                name="before refactor", description="Before refactoring auth"
            )

            assert result["success"] is True
            assert "checkpoint_id" in result
            assert "timestamp" in result

            print("✅ create_manual_checkpoint works")
            return True

    def test_list_checkpoints(self):
        """Test list_checkpoints"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            project_dir.mkdir()

            spawner = AgentSpawner(project_dir)
            (project_dir / "ARCHITECTURE.md").write_text("# Arch")

            spawner.spawn_coder(str(project_dir / "ARCHITECTURE.md"), "Task 1")
            spawner.create_manual_checkpoint("manual", "desc")

            checkpoints = spawner.list_checkpoints()
            assert len(checkpoints) == 2

            print("✅ list_checkpoints works")
            return True

    def test_compare_checkpoint(self):
        """Test compare_checkpoint"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            project_dir.mkdir()

            spawner = AgentSpawner(project_dir)
            (project_dir / "ARCHITECTURE.md").write_text("# Arch")

            cp = spawner.spawn_coder(str(project_dir / "ARCHITECTURE.md"), "Task")

            comparison = spawner.compare_checkpoint(cp["checkpoint_id"])
            assert "success" in comparison

            print("✅ compare_checkpoint works")
            return True

    def test_restore_checkpoint_dry_run(self):
        """Test restore_checkpoint dry run"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            project_dir.mkdir()

            spawner = AgentSpawner(project_dir)
            (project_dir / "ARCHITECTURE.md").write_text("# Arch")

            cp = spawner.spawn_coder(str(project_dir / "ARCHITECTURE.md"), "Task")

            result = spawner.restore_checkpoint(cp["checkpoint_id"], dry_run=True)
            assert result["success"] is True

            print("✅ restore_checkpoint dry run works")
            return True


def run_all_tests():
    """Run all agent spawner tests"""
    print("\n" + "=" * 60)
    print("TESTS: Agent Spawner (0% coverage target)")
    print("=" * 60 + "\n")

    tests = [
        (
            "spawn_architect creates correct info dict",
            TestSpawnArchitect().test_creates_correct_info_dict,
        ),
        (
            "spawn_architect tracks running agent",
            TestSpawnArchitect().test_tracks_running_agent,
        ),
        (
            "spawn_architect calls on_spawn callback",
            TestSpawnArchitect().test_calls_on_spawn_callback,
        ),
        (
            "spawn_coder creates checkpoint before coding",
            TestSpawnCoder().test_creates_checkpoint_before_coding,
        ),
        (
            "spawn_coder returns correct info dict",
            TestSpawnCoder().test_returns_correct_info_dict,
        ),
        (
            "handle_user_interrupt delegates",
            TestHandleUserInterrupt().test_delegates_to_interrupt_handler,
        ),
        ("get_trust_mode works", TestTrustModeIntegration().test_get_trust_mode),
        ("set_trust_mode valid", TestTrustModeIntegration().test_set_trust_mode_valid),
        (
            "set_trust_mode invalid",
            TestTrustModeIntegration().test_set_trust_mode_invalid,
        ),
        (
            "format_progress_message",
            TestMessageFormatting().test_format_progress_message,
        ),
        (
            "format_completion_message",
            TestMessageFormatting().test_format_completion_message,
        ),
        ("format_error_message", TestMessageFormatting().test_format_error_message),
        (
            "record_project_completion",
            TestRecordProjectCompletion().test_records_completion,
        ),
        (
            "get_available_trust_modes",
            TestGetAvailableTrustModes().test_returns_all_modes,
        ),
        ("get_agent_status works", TestGetAgentStatus().test_get_agent_status),
        (
            "get_agent_status not found",
            TestGetAgentStatus().test_get_agent_status_not_found,
        ),
        ("get_all_status works", TestGetAgentStatus().test_get_all_status),
        (
            "create_manual_checkpoint",
            TestCheckpointMethods().test_create_manual_checkpoint,
        ),
        ("list_checkpoints", TestCheckpointMethods().test_list_checkpoints),
        ("compare_checkpoint", TestCheckpointMethods().test_compare_checkpoint),
        (
            "restore_checkpoint dry run",
            TestCheckpointMethods().test_restore_checkpoint_dry_run,
        ),
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

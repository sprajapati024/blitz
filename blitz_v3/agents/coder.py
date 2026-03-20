#!/usr/bin/env python3
"""
Coder Agent - Implements features and writes code
"""

from pathlib import Path
from typing import Dict, Any
from core.test_runner import TestRunner


class CoderAgent:
    """Background agent that implements features"""

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.test_runner = TestRunner(project_dir)

    def implement(self, task: str, architecture_path: str = None) -> Dict[str, Any]:
        """
        Implement a feature/task

        Returns prompt for Claude to execute
        """
        arch_section = ""
        if architecture_path and Path(architecture_path).exists():
            arch_content = Path(architecture_path).read_text()
            arch_section = f"""
Follow this architecture exactly:
```
{arch_content[:2000]}  # First 2000 chars
```
"""

        return {
            "prompt": self._generate_prompt(task, arch_section),
            "output_dir": str(self.project_dir),
            "docs_to_update": [
                str(self.project_dir / "CHANGELOG.md"),
                str(self.project_dir / "PROJECT.md"),
            ],
        }

    def _generate_prompt(self, task: str, architecture: str = "") -> str:
        """Generate the coding prompt"""
        return f"""Implement: {task}

{architecture}

Rules:
1. Write working code - test that it runs
2. Follow the architecture - don't deviate without good reason
3. Keep it simple - MVP quality
4. Include basic error handling
5. Add docstrings/comments for clarity

As you code:
- Update CHANGELOG.md with what you add
- Update PROJECT.md to mark features complete
- Test your code actually works

Deliverables:
- Working code in the project directory
- Updated documentation
- Basic tests verifying core functionality

Build like you're shipping today.
"""

    def _run_tests(self) -> Dict[str, Any]:
        """Run tests after coding is complete"""
        results = self.test_runner.run_tests()

        test_count = (
            results.get("passed", 0)
            + results.get("failed", 0)
            + results.get("errors", 0)
        )
        status = "PASSED" if results.get("success") else "FAILED"

        message = f"Tests {status}: {results.get('passed', 0)} passed, {results.get('failed', 0)} failed, {results.get('errors', 0)} errors"
        if test_count == 0:
            message = "No tests found or run"

        return {
            "test_results": results,
            "message": message,
            "framework": self.test_runner.framework,
            "test_files": [str(f) for f in self.test_runner.get_test_files()],
        }

    def implement_with_tests(
        self, task: str, architecture_path: str = None
    ) -> Dict[str, Any]:
        """
        Implement a feature/task and run tests automatically
        """
        result = self.implement(task, architecture_path)
        test_results = self._run_tests()

        result["test_info"] = test_results

        if test_results["test_results"].get("success"):
            result["prompt"] += f"\n\nTest Results: {test_results['message']}"
        else:
            result["prompt"] += f"\n\nWARNING - {test_results['message']}"

        return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: coder.py <project_dir> [task]")
        sys.exit(1)

    project_dir = Path(sys.argv[1])
    task = sys.argv[2] if len(sys.argv) > 2 else "Implement MVP"
    architecture = sys.argv[3] if len(sys.argv) > 3 else None

    agent = CoderAgent(project_dir)
    result = agent.implement(task, architecture)

    print(result["prompt"])

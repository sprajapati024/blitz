#!/usr/bin/env python3
"""
Test Runner - Detects and runs tests across frameworks
"""

import subprocess
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class TestRunner:
    FRAMEWORKS = {
        "pytest": {
            "config_files": ["pytest.ini", "pyproject.toml", "setup.cfg"],
            "test_patterns": ["test_*.py", "*_test.py"],
            "command": ["pytest", "-v", "--tb=short"],
            "coverage_cmd": ["pytest", "--cov", "--cov-report=json"],
        },
        "unittest": {
            "config_files": [],
            "test_patterns": ["test_*.py"],
            "command": ["python", "-m", "unittest", "discover", "-v"],
            "coverage_cmd": None,
        },
        "jest": {
            "config_files": ["package.json"],
            "test_patterns": ["*.test.js", "*.spec.js"],
            "command": ["npm", "test", "--", "--passWithNoTests"],
            "coverage_cmd": [
                "npm",
                "test",
                "--",
                "--coverage",
                "--coverageReporters=json",
            ],
        },
        "go": {
            "config_files": ["go.mod"],
            "test_patterns": ["*_test.go"],
            "command": ["go", "test", "-v", "./..."],
            "coverage_cmd": ["go", "test", "-v", "-coverprofile=coverage.out", "./..."],
        },
        "cargo": {
            "config_files": ["Cargo.toml"],
            "test_patterns": ["*_test.rs"],
            "command": ["cargo", "test", "--", "--nocapture"],
            "coverage_cmd": ["cargo", "tarpaulin", "--output-dir", ".coverage"],
        },
    }

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.framework = self._detect_framework()
        self._test_files: Optional[List[Path]] = None

    def _detect_framework(self) -> str:
        """Detect test framework based on project files"""
        for framework, info in self.FRAMEWORKS.items():
            for config_file in info["config_files"]:
                if (self.project_dir / config_file).exists():
                    if (
                        framework == "unittest"
                        and (self.project_dir / "pyproject.toml").exists()
                    ):
                        continue
                    return framework
                    for pattern in info["test_patterns"]:
                        if list(self.project_dir.glob(f"**/{pattern}")):
                            return framework
        return "pytest"

    def _find_test_files(self) -> List[Path]:
        """Find all test files in project"""
        if self.framework not in self.FRAMEWORKS:
            return []
        patterns = self.FRAMEWORKS[self.framework]["test_patterns"]
        test_files = []
        for pattern in patterns:
            test_files.extend(self.project_dir.glob(f"**/{pattern}"))
        return sorted(set(test_files))

    def has_tests(self) -> bool:
        """Check if test files exist"""
        if self._test_files is None:
            self._test_files = self._find_test_files()
        return len(self._test_files) > 0

    def get_test_files(self) -> List[Path]:
        """Return list of test file paths"""
        if self._test_files is None:
            self._test_files = self._find_test_files()
        return self._test_files

    def _parse_pytest_output(self, output: str) -> Dict[str, Any]:
        """Parse pytest output"""
        result = {
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "duration": 0.0,
            "output": output,
            "raw": {},
        }

        passed = re.findall(r"PASSED", output)
        failed = re.findall(r"FAILED", output)
        errors = re.findall(r"ERROR", output)
        skipped = re.findall(r"SKIPPED", output)

        result["passed"] = len(passed)
        result["failed"] = len(failed)
        result["errors"] = len(errors)
        result["skipped"] = len(skipped)

        duration_match = re.search(r"(\d+\.\d+)s", output)
        if duration_match:
            result["duration"] = float(duration_match.group(1))

        summary_match = re.search(r"(\d+) passed.*?(\d+) failed", output)
        if summary_match:
            result["raw"]["summary"] = (
                f"{summary_match.group(1)} passed, {summary_match.group(2)} failed"
            )

        return result

    def _parse_jest_output(self, output: str) -> Dict[str, Any]:
        """Parse jest output"""
        result = {
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "duration": 0.0,
            "output": output,
            "raw": {},
        }

        suites_match = re.search(
            r"Test Suites:\s*(\d+)\s*total.*?(\d+)\s*passed.*?(\d+)\s*failed",
            output,
            re.DOTALL,
        )
        if suites_match:
            result["raw"]["suites"] = (
                f"{suites_match.group(2)} passed, {suites_match.group(3)} failed"
            )

        tests_match = re.search(
            r"Tests:\s*(\d+)\s*passed.*?(\d+)\s*failed", output, re.DOTALL
        )
        if tests_match:
            result["passed"] = int(tests_match.group(1))
            result["failed"] = int(tests_match.group(2))

        time_match = re.search(r"Time:\s*([\d.]+)s", output)
        if time_match:
            result["duration"] = float(time_match.group(1))

        return result

    def _parse_go_output(self, output: str) -> Dict[str, Any]:
        """Parse go test output"""
        result = {
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "duration": 0.0,
            "output": output,
            "raw": {},
        }

        ok_match = re.findall(r"^--- PASS:", output, re.MULTILINE)
        fail_match = re.findall(r"^--- FAIL:", output, re.MULTILINE)

        result["passed"] = len(ok_match)
        result["failed"] = len(fail_match)

        coverage_match = re.search(r"coverage:\s*([\d.]+)%", output)
        if coverage_match:
            result["raw"]["coverage"] = float(coverage_match.group(1))

        return result

    def _parse_cargo_output(self, output: str) -> Dict[str, Any]:
        """Parse cargo test output"""
        result = {
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "duration": 0.0,
            "output": output,
            "raw": {},
        }

        passed = re.findall(r"test result: ok", output)
        failed = re.findall(r"test result: FAILED", output)

        result["passed"] = len(passed)
        result["failed"] = len(failed)

        return result

    def _parse_unittest_output(self, output: str) -> Dict[str, Any]:
        """Parse unittest output"""
        result = {
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "duration": 0.0,
            "output": output,
            "raw": {},
        }

        Ran_match = re.search(r"Ran (\d+) test", output)
        if Ran_match:
            total = int(Ran_match.group(1))

        fail_match = re.search(r"FAIL:", output)
        err_match = re.search(r"ERROR:", output)
        ok_match = re.search(r"OK \((\d+)\) \(", output)

        if ok_match:
            result["passed"] = int(ok_match.group(1))
        if fail_match:
            result["failed"] = 1
        if err_match:
            result["errors"] = 1

        return result

    def run_tests(self, verbose: bool = True) -> Dict[str, Any]:
        """Run tests with appropriate command"""
        if not self.has_tests():
            return {
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "duration": 0.0,
                "output": "No test files found",
                "success": True,
                "message": "No tests to run",
            }

        framework_info = self.FRAMEWORKS.get(self.framework, {})
        cmd = framework_info.get("command", ["pytest", "-v"]).copy()

        if not verbose:
            if self.framework == "pytest":
                cmd = ["pytest", "-q"]
            elif self.framework == "jest":
                cmd = ["npm", "test", "--", "--silent"]

        try:
            result = subprocess.run(
                cmd, cwd=self.project_dir, capture_output=True, text=True, timeout=300
            )

            output = result.stdout + result.stderr

            if self.framework == "pytest":
                parsed = self._parse_pytest_output(output)
            elif self.framework == "jest":
                parsed = self._parse_jest_output(output)
            elif self.framework == "go":
                parsed = self._parse_go_output(output)
            elif self.framework == "cargo":
                parsed = self._parse_cargo_output(output)
            elif self.framework == "unittest":
                parsed = self._parse_unittest_output(output)
            else:
                parsed = {
                    "passed": 0,
                    "failed": 0,
                    "errors": 0,
                    "skipped": 0,
                    "duration": 0.0,
                    "output": output,
                }

            parsed["success"] = result.returncode == 0
            parsed["returncode"] = result.returncode

            return parsed

        except subprocess.TimeoutExpired:
            return {
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "duration": 300.0,
                "output": "Test run timed out after 300 seconds",
                "success": False,
                "error": "timeout",
            }
        except Exception as e:
            return {
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "duration": 0.0,
                "output": str(e),
                "success": False,
                "error": str(e),
            }

    def get_coverage(self) -> Optional[Dict[str, Any]]:
        """Get test coverage if available"""
        coverage_file = self.project_dir / "coverage" / "coverage-final.json"

        if self.framework == "pytest":
            if coverage_file.exists():
                try:
                    with open(coverage_file) as f:
                        data = json.load(f)
                    total_lines = sum(data.values()) if data else 0
                    return {
                        "available": True,
                        "format": "pytest-cov",
                        "files_covered": len(data),
                    }
                except:
                    pass
        elif self.framework == "jest":
            coverage_dir = self.project_dir / "coverage"
            if coverage_dir.exists():
                return {
                    "available": True,
                    "format": "jest",
                    "directory": str(coverage_dir),
                }
        elif self.framework == "go":
            coverage_out = self.project_dir / "coverage.out"
            if coverage_out.exists():
                return {"available": True, "format": "go", "file": str(coverage_out)}

        return {"available": False}

    def _format_results(self, results: Dict[str, Any]) -> str:
        """Format test results for display"""
        if "message" in results and "No tests" in results["message"]:
            return results["message"]

        lines = []
        lines.append(f"Framework: {self.framework}")

        if results.get("success"):
            lines.append("All tests passed!")
        else:
            lines.append("Tests failed:")

        lines.append(f"  Passed: {results.get('passed', 0)}")
        lines.append(f"  Failed: {results.get('failed', 0)}")
        lines.append(f"  Errors: {results.get('errors', 0)}")
        lines.append(f"  Duration: {results.get('duration', 0):.2f}s")

        if results.get("output"):
            lines.append(f"\nOutput:\n{results['output'][:1000]}")

        return "\n".join(lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: test_runner.py <project_dir>")
        sys.exit(1)

    project_dir = Path(sys.argv[1])
    runner = TestRunner(project_dir)

    print(f"Detected framework: {runner.framework}")
    print(f"Test files found: {len(runner.get_test_files())}")

    results = runner.run_tests()
    print(runner._format_results(results))

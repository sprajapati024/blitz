#!/usr/bin/env python3
"""
GitManager - Git integration for Blitz v3

Provides branch creation, smart commits, status checks, and PR hints.
"""

import subprocess
import re
from pathlib import Path
from typing import Dict, Any, List, Optional


class GitManager:
    """Manages Git operations for Blitz projects"""

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)

    def _run_git(
        self, args: List[str], capture_output: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a git command"""
        return subprocess.run(
            ["git"] + args,
            cwd=self.project_dir,
            capture_output=capture_output,
            text=True,
        )

    def is_repo(self) -> bool:
        """Check if project is a git repository"""
        result = self._run_git(["rev-parse", "--git-dir"])
        return result.returncode == 0

    def get_status(self) -> Dict[str, Any]:
        """
        Get git status

        Returns:
            Dict with is_repo, branch, has_changes, staged, unstaged
        """
        if not self.is_repo():
            return {
                "is_repo": False,
                "branch": None,
                "has_changes": False,
                "staged": [],
                "unstaged": [],
                "untracked": [],
            }

        status_result = self._run_git(["status", "--porcelain=v1"])
        lines = (
            status_result.stdout.strip().split("\n")
            if status_result.stdout.strip()
            else []
        )

        staged = []
        unstaged = []
        untracked = []

        for line in lines:
            if not line:
                continue
            index_status = line[:2]
            filename = line[3:]

            if index_status == "??":
                untracked.append(filename)
            elif index_status[0] in ("M", "A", "D", "R", "C"):
                staged.append(filename)
            elif index_status[1] in ("M", "D"):
                unstaged.append(filename)
            else:
                unstaged.append(filename)

        branch_result = self._run_git(["branch", "--show-current"])
        branch = branch_result.stdout.strip()

        return {
            "is_repo": True,
            "branch": branch,
            "has_changes": len(staged) > 0 or len(unstaged) > 0 or len(untracked) > 0,
            "staged": staged,
            "unstaged": unstaged,
            "untracked": untracked,
        }

    def create_feature_branch(self, branch_name: str) -> Dict[str, Any]:
        """
        Create and switch to a feature branch

        Args:
            branch_name: Name of the feature branch

        Returns:
            Dict with success status and branch name
        """
        if not self.is_repo():
            return {
                "success": False,
                "error": "Not a git repository. Run 'git init' first.",
                "branch": None,
            }

        safe_branch_name = re.sub(r"[^a-zA-Z0-9_\-/]", "-", branch_name)
        safe_branch_name = re.sub(r"-+", "-", safe_branch_name).strip("-")

        if not safe_branch_name.startswith("feature/"):
            safe_branch_name = f"feature/{safe_branch_name}"

        result = self._run_git(["checkout", "-b", safe_branch_name])

        if result.returncode == 0:
            return {
                "success": True,
                "branch": safe_branch_name,
                "message": f"Created and switched to branch: {safe_branch_name}",
            }
        else:
            return {
                "success": False,
                "error": result.stderr.strip(),
                "branch": None,
            }

    def commit_changes(
        self, message: str, files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Commit changes with auto-detected files or specified files

        Args:
            message: Commit message
            files: Specific files to commit (None for auto-detect)

        Returns:
            Dict with success status and commit info
        """
        if not self.is_repo():
            return {
                "success": False,
                "error": "Not a git repository",
                "commit": None,
            }

        if files is None:
            result = self._run_git(["add", "-A"])
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": result.stderr.strip(),
                    "commit": None,
                }
        else:
            for f in files:
                result = self._run_git(["add", f])
                if result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"Failed to add {f}: {result.stderr.strip()}",
                        "commit": None,
                    }

        status = self.get_status()
        if not status["has_changes"]:
            return {
                "success": False,
                "error": "No changes to commit",
                "commit": None,
            }

        commit_result = self._run_git(["commit", "-m", message])

        if commit_result.returncode == 0:
            commit_hash = "unknown"
            for line in commit_result.stdout.split("\n"):
                match = re.search(r"\b([0-9a-f]{7,40})\b", line)
                if match:
                    commit_hash = match.group(1)[:7]
                    break
            return {
                "success": True,
                "message": f"Committed: {message}",
                "commit": commit_hash,
                "files_count": len(status["staged"])
                + len(status["unstaged"])
                + len(status["untracked"]),
            }
        else:
            return {
                "success": False,
                "error": commit_result.stderr.strip(),
                "commit": None,
            }

    def generate_commit_message(self, changelog_path: Path) -> str:
        """
        Generate commit message from changelog

        Args:
            changelog_path: Path to CHANGELOG.md

        Returns:
            Generated commit message
        """
        if not changelog_path.exists():
            return "Update project"

        content = changelog_path.read_text()

        sections = []
        current_section = []

        for line in content.split("\n"):
            if line.startswith("## "):
                if current_section and sections:
                    sections.append("\n".join(current_section))
                current_section = []
                sections.append(line)
            elif line.startswith("- ") or line.startswith("* "):
                current_section.append(line)

        if current_section:
            sections.append("\n".join(current_section))

        meaningful_changes = []
        skip_patterns = ("unreleased", "change", "update", "modify")

        for section in sections:
            if not section.strip():
                continue
            if any(p in section.lower() for p in skip_patterns):
                continue
            if section.startswith("## "):
                continue

            for line in section.split("\n"):
                line = line.strip()
                if line.startswith("- ") or line.startswith("* "):
                    change = line[2:].strip()
                    if change and len(change) > 3:
                        meaningful_changes.append(change)

        if meaningful_changes:
            unique_changes = list(dict.fromkeys(meaningful_changes))[:5]
            message = "feat: " + unique_changes[0]
            if len(unique_changes) > 1:
                message += "\n\nChanges:\n" + "\n".join(
                    f"- {c}" for c in unique_changes[1:]
                )
            return message

        return "Update project"

    def get_pr_command(self, branch: Optional[str] = None) -> str:
        """
        Return command to create PR

        Args:
            branch: Target branch (defaults to main/master)

        Returns:
            PR creation command
        """
        if not self.is_repo():
            return "git init && git add . && git commit -m 'Initial commit'"

        remotes = self._run_git(["remote", "-v"])
        if "github.com" in remotes.stdout:
            target = branch if branch else "main"
            return f"gh pr create --base {target} --fill"
        elif "gitlab.com" in remotes.stdout:
            return "glab mr create --fill"
        else:
            return f"git push -u origin {branch if branch else 'HEAD'}"

    def get_current_branch(self) -> Optional[str]:
        """Get current branch name"""
        if not self.is_repo():
            return None
        result = self._run_git(["branch", "--show-current"])
        return result.stdout.strip() if result.returncode == 0 else None

    def has_uncommitted_changes(self) -> bool:
        """Check if there are uncommitted changes"""
        status = self.get_status()
        return status["has_changes"]

    def get_diff_summary(self) -> str:
        """Get a summary of changes"""
        if not self.is_repo():
            return "Not a git repository"

        status = self.get_status()
        if not status["has_changes"]:
            return "No changes"

        parts = []
        if status["staged"]:
            parts.append(f"{len(status['staged'])} staged")
        if status["unstaged"]:
            parts.append(f"{len(status['unstaged'])} modified")
        if status["untracked"]:
            parts.append(f"{len(status['untracked'])} untracked")

        return ", ".join(parts)

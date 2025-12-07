#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevAgent - Git Operations

Handles git operations including:
- Creating branches
- Committing changes
- Generating commit messages
"""

import subprocess
from pathlib import Path
from typing import Optional


class GitOperations:
    """
    Manages git operations for a project.
    """
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self._verify_git_repo()
    
    def _verify_git_repo(self):
        """Verify that we're in a git repository."""
        if not (self.project_path / ".git").exists():
            raise ValueError(f"Not a git repository: {self.project_path}")
    
    def _run_git(self, *args) -> tuple[bool, str]:
        """Run a git command and return (success, output)."""
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout.strip() or result.stderr.strip()
        except Exception as e:
            return False, str(e)
    
    def get_current_branch(self) -> str:
        """Get the name of the current branch."""
        success, output = self._run_git("branch", "--show-current")
        return output if success else "unknown"
    
    def has_uncommitted_changes(self) -> bool:
        """Check if there are uncommitted changes."""
        success, output = self._run_git("status", "--porcelain")
        return bool(output)
    
    def create_branch(self, branch_name: str) -> bool:
        """
        Create and checkout a new branch.
        
        If there are uncommitted changes, stash them first.
        """
        # Check for uncommitted changes
        had_changes = self.has_uncommitted_changes()
        
        if had_changes:
            # Stash changes
            self._run_git("stash", "push", "-m", "DevAgent: auto-stash before branch")
        
        # Create and checkout new branch
        success, output = self._run_git("checkout", "-b", branch_name)
        
        if not success:
            # Branch might already exist, try to checkout
            success, output = self._run_git("checkout", branch_name)
        
        if had_changes and success:
            # Restore stashed changes
            self._run_git("stash", "pop")
        
        return success
    
    def commit_all(self, message: str) -> Optional[str]:
        """
        Stage all changes and commit.
        
        Returns the commit hash if successful, None otherwise.
        """
        # Stage all changes
        success, _ = self._run_git("add", "-A")
        if not success:
            return None
        
        # Check if there's anything to commit
        if not self.has_uncommitted_changes():
            return None
        
        # Commit
        success, output = self._run_git("commit", "-m", message)
        if not success:
            return None
        
        # Get commit hash
        success, commit_hash = self._run_git("rev-parse", "HEAD")
        return commit_hash if success else None
    
    def get_diff(self, staged: bool = False) -> str:
        """Get the current diff."""
        args = ["diff"]
        if staged:
            args.append("--staged")
        
        success, output = self._run_git(*args)
        return output if success else ""
    
    def checkout_branch(self, branch_name: str) -> bool:
        """Checkout an existing branch."""
        success, _ = self._run_git("checkout", branch_name)
        return success
    
    def merge_branch(self, branch_name: str, message: str = None) -> bool:
        """Merge a branch into the current branch."""
        args = ["merge", branch_name]
        if message:
            args.extend(["-m", message])
        
        success, _ = self._run_git(*args)
        return success
    
    def delete_branch(self, branch_name: str, force: bool = False) -> bool:
        """Delete a branch."""
        flag = "-D" if force else "-d"
        success, _ = self._run_git("branch", flag, branch_name)
        return success

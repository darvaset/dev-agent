#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevAgent - File Operations

Handles file system operations including:
- Creating files
- Modifying files
- Deleting files
- Reading files
"""

from pathlib import Path
from typing import Optional


class FileOperations:
    """
    Manages file operations for a project.
    
    All paths are relative to the project root.
    """
    
    def __init__(self, project_path: Path):
        self.project_path = project_path.resolve()
    
    def _resolve_path(self, relative_path: str) -> Path:
        """Resolve a relative path to an absolute path within the project."""
        # Clean up the path
        relative_path = relative_path.strip().lstrip("/")
        
        full_path = (self.project_path / relative_path).resolve()
        
        # Security check: ensure we're still within the project
        if not str(full_path).startswith(str(self.project_path)):
            raise ValueError(f"Path escapes project directory: {relative_path}")
        
        return full_path
    
    def read_file(self, relative_path: str) -> Optional[str]:
        """Read a file's contents."""
        try:
            path = self._resolve_path(relative_path)
            if path.exists():
                return path.read_text(encoding="utf-8")
            return None
        except Exception:
            return None
    
    def create_file(self, relative_path: str, content: str) -> bool:
        """
        Create a new file with the given content.
        
        Creates parent directories if needed.
        Raises error if file already exists.
        """
        path = self._resolve_path(relative_path)
        
        if path.exists():
            raise FileExistsError(f"File already exists: {relative_path}")
        
        # Create parent directories
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        path.write_text(content, encoding="utf-8")
        
        return True
    
    def write_file(self, relative_path: str, content: str) -> bool:
        """
        Write content to a file, creating or overwriting as needed.
        
        Creates parent directories if needed.
        """
        path = self._resolve_path(relative_path)
        
        # Create parent directories
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        path.write_text(content, encoding="utf-8")
        
        return True
    
    def delete_file(self, relative_path: str) -> bool:
        """Delete a file."""
        path = self._resolve_path(relative_path)
        
        if not path.exists():
            return False
        
        if path.is_dir():
            raise IsADirectoryError(f"Cannot delete directory: {relative_path}")
        
        path.unlink()
        return True
    
    def exists(self, relative_path: str) -> bool:
        """Check if a file exists."""
        try:
            path = self._resolve_path(relative_path)
            return path.exists()
        except Exception:
            return False
    
    def list_directory(self, relative_path: str = ".") -> list[str]:
        """List contents of a directory."""
        path = self._resolve_path(relative_path)
        
        if not path.exists():
            return []
        
        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {relative_path}")
        
        return [item.name for item in path.iterdir()]
    
    def ensure_directory(self, relative_path: str) -> bool:
        """Ensure a directory exists, creating it if needed."""
        path = self._resolve_path(relative_path)
        path.mkdir(parents=True, exist_ok=True)
        return True

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevAgent - Project Context Management

Handles detection and caching of project context including:
- Tech stack detection
- Project structure
- Key files identification
- Task history
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional

from devagent.config import GLOBAL_CONFIG_DIR


class ProjectContext:
    """
    Manages context for a specific project.
    
    Context is cached in ~/.devagent/projects/{project_hash}/
    """
    
    def __init__(self, project_path: Path):
        self.project_path = project_path.resolve()
        self.project_name = self.project_path.name
        self.project_hash = self._hash_path(str(self.project_path))
        
        self.context_dir = GLOBAL_CONFIG_DIR / "projects" / self.project_hash
        self.context_file = self.context_dir / "context.json"
        self.history_file = self.context_dir / "history.json"
        
        # Ensure directory exists
        self.context_dir.mkdir(parents=True, exist_ok=True)
    
    def _hash_path(self, path: str) -> str:
        """Create a short hash of the project path for directory naming."""
        return hashlib.md5(path.encode()).hexdigest()[:12]
    
    def get_context(self) -> dict:
        """
        Get the project context, loading from cache or detecting fresh.
        """
        # Try to load cached context
        if self.context_file.exists():
            try:
                with open(self.context_file, "r") as f:
                    cached = json.load(f)
                
                # Check if cache is still valid (less than 1 hour old)
                cached_time = datetime.fromisoformat(cached.get("_cached_at", "2000-01-01"))
                if (datetime.now() - cached_time).seconds < 3600:
                    return cached
            except Exception:
                pass
        
        # Detect fresh context
        return self.refresh()
    
    def refresh(self) -> dict:
        """Detect and cache fresh project context."""
        context = {
            "name": self.project_name,
            "path": str(self.project_path),
            "tech_stack": [],
            "primary_language": None,
            "framework": None,
            "key_files": {},
            "structure_summary": "",
            "_cached_at": datetime.now().isoformat()
        }
        
        # Detect tech stack based on files present
        context["tech_stack"], context["key_files"] = self._detect_tech_stack()
        
        # Determine primary language and framework
        context["primary_language"] = self._detect_primary_language(context["tech_stack"])
        context["framework"] = self._detect_framework(context["tech_stack"])
        
        # Generate structure summary
        context["structure_summary"] = self._generate_structure_summary()
        
        # Cache the context
        with open(self.context_file, "w") as f:
            json.dump(context, f, indent=2)
        
        return context
    
    def _detect_tech_stack(self) -> tuple[list[str], dict]:
        """Detect technologies used in the project."""
        tech_stack = []
        key_files = {}
        
        # Check for various config files
        detectors = {
            # JavaScript/TypeScript ecosystem
            "package.json": ("nodejs", "package.json"),
            "tsconfig.json": ("typescript", "tsconfig.json"),
            "next.config.ts": ("nextjs", "next.config.ts"),
            "next.config.js": ("nextjs", "next.config.js"),
            "next.config.mjs": ("nextjs", "next.config.mjs"),
            "vite.config.ts": ("vite", "vite.config.ts"),
            "vite.config.js": ("vite", "vite.config.js"),
            "tailwind.config.js": ("tailwind", "tailwind.config.js"),
            "tailwind.config.ts": ("tailwind", "tailwind.config.ts"),
            
            # Python ecosystem
            "requirements.txt": ("python", "requirements.txt"),
            "pyproject.toml": ("python", "pyproject.toml"),
            "setup.py": ("python", "setup.py"),
            "Pipfile": ("python", "Pipfile"),
            
            # Database
            "prisma/schema.prisma": ("prisma", "prisma/schema.prisma"),
            
            # Docker
            "Dockerfile": ("docker", "Dockerfile"),
            "docker-compose.yml": ("docker", "docker-compose.yml"),
            "docker-compose.yaml": ("docker", "docker-compose.yaml"),
            
            # Git
            ".git": ("git", None),
        }
        
        for file_path, (tech, key_file_name) in detectors.items():
            if (self.project_path / file_path).exists():
                if tech not in tech_stack:
                    tech_stack.append(tech)
                if key_file_name:
                    key_files[tech] = file_path
        
        # Additional detection from package.json
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json, "r") as f:
                    pkg = json.load(f)
                
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                
                if "react" in deps:
                    tech_stack.append("react")
                if "vue" in deps:
                    tech_stack.append("vue")
                if "express" in deps:
                    tech_stack.append("express")
                if "@supabase/supabase-js" in deps:
                    tech_stack.append("supabase")
                if "neo4j-driver" in deps:
                    tech_stack.append("neo4j")
                    
            except Exception:
                pass
        
        return tech_stack, key_files
    
    def _detect_primary_language(self, tech_stack: list[str]) -> str:
        """Determine the primary programming language."""
        if "typescript" in tech_stack:
            return "TypeScript"
        elif "nodejs" in tech_stack:
            return "JavaScript"
        elif "python" in tech_stack:
            return "Python"
        return "Unknown"
    
    def _detect_framework(self, tech_stack: list[str]) -> Optional[str]:
        """Determine the primary framework."""
        frameworks = ["nextjs", "vite", "express", "vue", "react"]
        for fw in frameworks:
            if fw in tech_stack:
                return fw.title() if fw != "nextjs" else "Next.js"
        return None
    
    def _generate_structure_summary(self, max_depth: int = 2) -> str:
        """Generate a summary of the project structure."""
        lines = []
        
        def walk(path: Path, prefix: str = "", depth: int = 0):
            if depth > max_depth:
                return
            
            # Skip certain directories
            skip_dirs = {".git", "node_modules", "__pycache__", ".next", "venv", ".venv", "dist", "build"}
            
            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
            except PermissionError:
                return
            
            for i, item in enumerate(items):
                if item.name.startswith(".") and item.name not in [".env.example", ".gitignore"]:
                    continue
                if item.name in skip_dirs:
                    continue
                
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                lines.append(f"{prefix}{current_prefix}{item.name}")
                
                if item.is_dir():
                    extension = "    " if is_last else "│   "
                    walk(item, prefix + extension, depth + 1)
        
        walk(self.project_path)
        
        # Limit output
        if len(lines) > 50:
            lines = lines[:50]
            lines.append("... (truncated)")
        
        return "\n".join(lines)
    
    def get_history(self, limit: int = 10) -> list[dict]:
        """Get recent task history for this project."""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, "r") as f:
                history = json.load(f)
            return history[-limit:]
        except Exception:
            return []
    
    def add_history_entry(self, prompt_name: str, result: dict):
        """Add an entry to the task history."""
        history = self.get_history(limit=100)  # Keep last 100
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt_name": prompt_name,
            "status": result.get("status", "unknown"),
            "files_changed": len(result.get("files_created", [])) + len(result.get("files_modified", [])),
            "git_branch": result.get("git", {}).get("branch"),
            "git_commit": result.get("git", {}).get("commit"),
        }
        
        history.append(entry)
        
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=2)

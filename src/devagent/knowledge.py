#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevAgent - Knowledge Base Management

Handles loading and managing knowledge files including:
- Rules (coding standards, best practices)
- Patterns (code templates, common structures)
- Personas (developer preferences)
"""

from pathlib import Path
from typing import Optional
import re


# Knowledge base is stored alongside the package
KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "knowledge"


class KnowledgeBase:
    """
    Manages the knowledge base of rules, patterns, and personas.
    """
    
    def __init__(self, knowledge_dir: Path = None):
        self.knowledge_dir = knowledge_dir or KNOWLEDGE_DIR
        
        # Create directories if they don't exist
        (self.knowledge_dir / "rules").mkdir(parents=True, exist_ok=True)
        (self.knowledge_dir / "patterns").mkdir(parents=True, exist_ok=True)
        (self.knowledge_dir / "personas").mkdir(parents=True, exist_ok=True)
    
    def list_rules(self) -> dict[str, list[dict]]:
        """
        List all available rules organized by category.
        
        Returns:
            {
                "rules": [{"name": "typescript", "description": "..."}],
                "patterns": [...],
                "personas": [...]
            }
        """
        result = {
            "rules": [],
            "patterns": [],
            "personas": []
        }
        
        for category in result.keys():
            category_dir = self.knowledge_dir / category
            if category_dir.exists():
                for file in category_dir.glob("*.md"):
                    if file.name.startswith("_"):
                        continue
                    
                    # Try to extract description from first line
                    description = ""
                    try:
                        content = file.read_text(encoding="utf-8")
                        first_line = content.split("\n")[0]
                        if first_line.startswith("# "):
                            description = first_line[2:].strip()
                    except Exception:
                        pass
                    
                    result[category].append({
                        "name": file.stem,
                        "description": description,
                        "path": str(file)
                    })
        
        return result
    
    def get_rule(self, name: str) -> Optional[str]:
        """
        Get the content of a specific rule by name.
        
        Searches in rules/, patterns/, and personas/ directories.
        """
        for category in ["rules", "patterns", "personas"]:
            file_path = self.knowledge_dir / category / f"{name}.md"
            if file_path.exists():
                return file_path.read_text(encoding="utf-8")
        
        return None
    
    def get_rules_for_stack(self, tech_stack: list[str]) -> list[str]:
        """
        Get all relevant rules for a given tech stack.
        
        Always includes the base rules, then adds tech-specific ones.
        """
        rules = []
        
        # Always include base rules if they exist
        base_rule = self.get_rule("_base")
        if base_rule:
            rules.append(base_rule)
        
        # Map tech stack items to rule names
        tech_to_rules = {
            "typescript": ["typescript"],
            "javascript": ["javascript"],
            "nodejs": ["nodejs"],
            "nextjs": ["nextjs", "react"],
            "react": ["react"],
            "python": ["python"],
            "prisma": ["prisma"],
            "tailwind": ["tailwind"],
            "supabase": ["supabase"],
            "neo4j": ["neo4j"],
        }
        
        # Collect relevant rules
        added_rules = set()
        for tech in tech_stack:
            tech_lower = tech.lower()
            if tech_lower in tech_to_rules:
                for rule_name in tech_to_rules[tech_lower]:
                    if rule_name not in added_rules:
                        rule_content = self.get_rule(rule_name)
                        if rule_content:
                            rules.append(rule_content)
                            added_rules.add(rule_name)
        
        return rules
    
    def get_persona(self, name: str) -> Optional[str]:
        """Get a persona configuration."""
        file_path = self.knowledge_dir / "personas" / f"{name}.md"
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return None
    
    def get_pattern(self, name: str) -> Optional[str]:
        """Get a code pattern template."""
        file_path = self.knowledge_dir / "patterns" / f"{name}.md"
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return None

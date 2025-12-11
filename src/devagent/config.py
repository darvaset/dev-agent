#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevAgent - Configuration Management

Handles global configuration including API keys and defaults.
Configuration is stored in ~/.devagent/
"""

import os
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


GLOBAL_CONFIG_DIR = Path.home() / ".devagent"
GLOBAL_CONFIG_FILE = GLOBAL_CONFIG_DIR / "config.yaml"
GLOBAL_ENV_FILE = GLOBAL_CONFIG_DIR / ".env"


# Available models mapped by use case
AVAILABLE_MODELS = {
    # Best quality (use for complex tasks)
    "pro": "models/gemini-2.5-pro",
    
    # Balanced (default - good quality, reasonable speed)
    "flash": "models/gemini-2.5-flash",
    
    # Experimental
    "gemini-3-pro": "models/gemini-3-pro-preview",
}

# Default model for DevAgent
DEFAULT_MODEL = "models/gemini-2.5-flash"


@dataclass
class Config:
    """DevAgent configuration."""
    
    gemini_api_key: Optional[str] = None
    default_model: str = DEFAULT_MODEL
    debug: bool = False
    auto_commit: bool = True
    create_branch: bool = True
    default_validation: Optional[str] = None
    
    # Paths
    config_dir: Path = field(default_factory=lambda: GLOBAL_CONFIG_DIR)
    projects_dir: Path = field(default_factory=lambda: GLOBAL_CONFIG_DIR / "projects")
    logs_dir: Path = field(default_factory=lambda: GLOBAL_CONFIG_DIR / "logs")
    
    @classmethod
    def load(cls) -> "Config":
        """Load configuration from global config file and environment."""
        config = cls()
        
        # Load from config file if exists
        if GLOBAL_CONFIG_FILE.exists():
            try:
                with open(GLOBAL_CONFIG_FILE, "r") as f:
                    data = yaml.safe_load(f) or {}
                
                config.default_model = data.get("default_model", config.default_model)
                config.debug = data.get("debug", config.debug)
                config.auto_commit = data.get("auto_commit", config.auto_commit)
                config.create_branch = data.get("create_branch", config.create_branch)
                config.default_validation = data.get("default_validation")
                
            except Exception:
                pass  # Use defaults if config file is invalid
        
        # Load API key from environment or .env file
        config.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        
        if not config.gemini_api_key and GLOBAL_ENV_FILE.exists():
            try:
                with open(GLOBAL_ENV_FILE, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY="):
                            config.gemini_api_key = line.split("=", 1)[1].strip().strip('"\'')
                            break
            except Exception:
                pass
        
        return config
    
    @staticmethod
    def resolve_model(model_name: str) -> str:
        """
        Resolve a model shorthand to the full model path.
        
        Examples:
            "pro" -> "models/gemini-2.5-pro"
            "flash" -> "models/gemini-2.5-flash"
            "models/gemini-2.5-pro" -> "models/gemini-2.5-pro" (unchanged)
        """
        # If it's already a full path, return as-is
        if model_name.startswith("models/"):
            return model_name
        
        # Check if it's a shorthand
        if model_name in AVAILABLE_MODELS:
            return AVAILABLE_MODELS[model_name]
        
        # Try adding models/ prefix
        return f"models/{model_name}"
    
    def save(self):
        """Save configuration to global config file."""
        ensure_global_config()
        
        data = {
            "default_model": self.default_model,
            "debug": self.debug,
            "auto_commit": self.auto_commit,
            "create_branch": self.create_branch,
        }
        
        if self.default_validation:
            data["default_validation"] = self.default_validation
        
        with open(GLOBAL_CONFIG_FILE, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
    
    def set_api_key(self, api_key: str):
        """Save API key to the global .env file."""
        ensure_global_config()
        
        self.gemini_api_key = api_key
        
        # Write to .env file
        with open(GLOBAL_ENV_FILE, "w") as f:
            f.write(f'GEMINI_API_KEY="{api_key}"\n')
        
        # Set restrictive permissions
        GLOBAL_ENV_FILE.chmod(0o600)


def ensure_global_config() -> Path:
    """
    Ensure the global config directory and files exist.
    Returns the path to the config directory.
    """
    # Create main config directory
    GLOBAL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (GLOBAL_CONFIG_DIR / "projects").mkdir(exist_ok=True)
    (GLOBAL_CONFIG_DIR / "logs").mkdir(exist_ok=True)
    
    # Create default config file if it doesn't exist
    if not GLOBAL_CONFIG_FILE.exists():
        default_config = {
            "default_model": DEFAULT_MODEL,
            "debug": False,
            "auto_commit": True,
            "create_branch": True,
        }
        
        with open(GLOBAL_CONFIG_FILE, "w") as f:
            yaml.dump(default_config, f, default_flow_style=False)
            f.write("\n# Model shortcuts available:\n")
            for shortcut, full_name in AVAILABLE_MODELS.items():
                f.write(f"# - {shortcut}: {full_name}\n")
    
    # Create .env template if it doesn't exist
    if not GLOBAL_ENV_FILE.exists():
        with open(GLOBAL_ENV_FILE, "w") as f:
            f.write('# DevAgent Environment Variables\n')
            f.write('GEMINI_API_KEY="your-api-key-here"\n')
        GLOBAL_ENV_FILE.chmod(0o600)
    
    return GLOBAL_CONFIG_DIR

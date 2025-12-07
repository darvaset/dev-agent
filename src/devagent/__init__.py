"""
DevAgent - AI-powered development agent using Gemini API

A reusable development assistant that can be installed via pip and used
across multiple projects. It leverages Google's Gemini API to execute
development tasks based on detailed prompts.
"""

__version__ = "0.1.0"
__author__ = "Diego"

from devagent.agent import DevAgent

__all__ = ["DevAgent"]

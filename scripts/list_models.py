#!/usr/bin/env python3
"""
Quick script to list available Gemini models.
Run: python scripts/list_models.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from ~/.devagent/.env
env_path = Path.home() / ".devagent" / ".env"
if env_path.exists():
    load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found")
    exit(1)

genai.configure(api_key=api_key)

print("📋 Available Gemini Models:\n")
print("-" * 80)

for model in genai.list_models():
    # Only show models that support generateContent
    if "generateContent" in model.supported_generation_methods:
        print(f"🤖 {model.name}")
        print(f"   Display Name: {model.display_name}")
        desc = model.description[:100] + "..." if len(model.description) > 100 else model.description
        print(f"   Description: {desc}")
        print(f"   Input Token Limit: {model.input_token_limit:,}")
        print(f"   Output Token Limit: {model.output_token_limit:,}")
        print("-" * 80)

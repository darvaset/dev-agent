#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevAgent - Main Agent Logic

Orchestrates the execution of development tasks using Gemini API.
"""

import json
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

import google.generativeai as genai
from rich.console import Console

from devagent.config import Config
from devagent.context import ProjectContext
from devagent.knowledge import KnowledgeBase
from devagent.git_ops import GitOperations
from devagent.file_ops import FileOperations

console = Console()


class DevAgent:
    """
    Main agent that executes development tasks.
    
    Workflow:
    1. Load prompt file
    2. Gather project context
    3. Load relevant knowledge/rules
    4. Build enriched prompt
    5. Call Gemini API
    6. Parse structured response
    7. Execute file operations
    8. Run validation (optional)
    9. Git commit (optional)
    """
    
    def __init__(
        self, 
        config: Config, 
        use_git: bool = True,
        model_override: Optional[str] = None
    ):
        self.config = config
        self.use_git = use_git
        
        # Resolve model name (handle shortcuts like "pro", "flash")
        raw_model = model_override or config.default_model
        self.model_name = Config.resolve_model(raw_model)
        
        self.project_ctx = ProjectContext(Path.cwd())
        self.knowledge = KnowledgeBase()
        self.git_ops = GitOperations(Path.cwd()) if use_git else None
        self.file_ops = FileOperations(Path.cwd())
        
        self._setup_gemini()
    
    def _setup_gemini(self):
        """Configure the Gemini API client."""
        if not self.config.gemini_api_key:
            raise ValueError(
                "Gemini API key not configured. Run 'devagent init' to set it up."
            )
        
        genai.configure(api_key=self.config.gemini_api_key)
        
        # Configure generation to return JSON
        self.generation_config = genai.GenerationConfig(
            response_mime_type="application/json"
        )
        self.model = genai.GenerativeModel(
            self.model_name,
            generation_config=self.generation_config
        )
        console.print(f"[dim]Using model: {self.model_name}[/dim]")
    
    def execute(self, prompt_path: Path, extra_rules: list[str] = None) -> dict:
        """
        Execute a development task from a prompt file.
        
        Args:
            prompt_path: Path to the prompt markdown file
            extra_rules: Additional rules to include
            
        Returns:
            Result dictionary with status, files changed, etc.
        """
        result = {
            "status": "pending",
            "files_created": [],
            "files_modified": [],
            "files_deleted": [],
            "git": {},
            "validation": {},
            "errors": [],
            "summary": ""
        }
        
        try:
            # 1. Read the prompt
            console.print("[dim]📄 Reading prompt...[/dim]")
            prompt_content = prompt_path.read_text(encoding="utf-8")
            
            # 2. Create git branch if enabled
            if self.use_git and self.git_ops:
                branch_name = self._generate_branch_name(prompt_path.stem)
                console.print(f"[dim]🔀 Creating branch: {branch_name}[/dim]")
                self.git_ops.create_branch(branch_name)
                result["git"]["branch"] = branch_name
            
            # 3. Build enriched prompt
            console.print("[dim]🧠 Building context...[/dim]")
            enriched_prompt = self._build_prompt(prompt_content, extra_rules)
            
            # 4. Call Gemini
            console.print("[dim]🤖 Calling Gemini API...[/dim]")
            response = self._call_gemini(enriched_prompt)
            
            # 5. Parse response
            console.print("[dim]📋 Parsing response...[/dim]")
            actions = self._parse_response(response)
            
            # 6. Execute file operations
            console.print("[dim]📝 Executing file operations...[/dim]")
            file_results = self._execute_file_actions(actions)
            result["files_created"] = file_results["created"]
            result["files_modified"] = file_results["modified"]
            result["files_deleted"] = file_results["deleted"]
            
            # 7. Run validation if specified
            if actions.get("validation_command"):
                console.print("[dim]🧪 Running validation...[/dim]")
                result["validation"] = self._run_validation(actions["validation_command"])
            
            # 8. Git commit if successful
            if self.use_git and self.git_ops and result["validation"].get("success", True):
                commit_msg = actions.get("commit_message", f"DevAgent: {prompt_path.stem}")
                console.print(f"[dim]💾 Committing changes...[/dim]")
                commit_hash = self.git_ops.commit_all(commit_msg)
                result["git"]["commit"] = commit_hash
            
            # 9. Save to history
            result["status"] = "success"
            result["summary"] = actions.get("summary", "Task completed")
            self.project_ctx.add_history_entry(
                prompt_name=prompt_path.name,
                result=result,
                full_prompt_content=enriched_prompt,
                full_gemini_response=response.text
            )
            
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            console.print(f"[red]Error: {e}[/red]")
        
        return result
    
    def preview(self, prompt_path: Path, extra_rules: list[str] = None) -> dict:
        """
        Preview what would be done without executing.
        
        Returns the parsed actions from Gemini without applying them.
        """
        prompt_content = prompt_path.read_text(encoding="utf-8")
        enriched_prompt = self._build_prompt(prompt_content, extra_rules, dry_run=True)
        
        response = self._call_gemini(enriched_prompt)
        actions = self._parse_response(response)
        
        return {
            "status": "preview",
            "files_to_create": [f["path"] for f in actions.get("files_to_create", [])],
            "files_to_modify": [f["path"] for f in actions.get("files_to_modify", [])],
            "files_to_delete": actions.get("files_to_delete", []),
            "validation_command": actions.get("validation_command"),
            "summary": actions.get("summary", ""),
            "raw_response": response[:2000] + "..." if len(response) > 2000 else response
        }
    
    def _build_prompt(
        self, 
        user_prompt: str, 
        extra_rules: list[str] = None,
        dry_run: bool = False
    ) -> str:
        """Build the complete prompt with context and rules."""
        
        # Get project context
        ctx = self.project_ctx.get_context()
        
        # Get relevant rules based on project tech stack
        rules = self.knowledge.get_rules_for_stack(ctx.get("tech_stack", []))
        
        # Add extra rules if specified
        if extra_rules:
            for rule_name in extra_rules:
                rule_content = self.knowledge.get_rule(rule_name)
                if rule_content:
                    rules.append(rule_content)
        
        # Get persona
        persona = self.knowledge.get_persona("diego")
        
        # Build the system prompt
        system_prompt = self._build_system_prompt(ctx, rules, persona, dry_run)
        
        # Combine everything
        full_prompt = f"""{system_prompt}

---

# USER TASK

{user_prompt}

---

# RESPONSE FORMAT

You MUST respond with a valid JSON object. The response will be parsed directly as JSON.

CRITICAL JSON RULES:
1. All string content must have proper JSON escaping
2. Use \\n for newlines inside strings
3. Use \\\\ for backslashes
4. Use \\" for quotes inside strings
5. Do NOT include markdown code blocks - respond with raw JSON only

Structure:
{{
    "summary": "Brief description of what was done",
    "files_to_create": [
        {{
            "path": "relative/path/to/file.ts",
            "content": "file content with proper escaping for newlines (\\n) and quotes (\\")",
            "description": "why this file was created"
        }}
    ],
    "files_to_modify": [
        {{
            "path": "relative/path/to/existing/file.ts",
            "content": "complete new content of the file",
            "description": "what was changed and why"
        }}
    ],
    "files_to_delete": ["path/to/delete.ts"],
    "validation_command": "npm run build",
    "commit_message": "feat: description of changes"
}}

IMPORTANT:
- For files_to_modify, provide the COMPLETE new content, not a diff
- All paths are relative to the project root
- Use appropriate commit message prefixes: feat, fix, refactor, docs, chore
- validation_command should be a command that verifies the changes work
- Respond ONLY with valid JSON, no explanation before or after
"""
        
        return full_prompt
    
    def _build_system_prompt(
        self, 
        ctx: dict, 
        rules: list[str], 
        persona: str,
        dry_run: bool
    ) -> str:
        """Build the system/context portion of the prompt."""
        
        mode = "PREVIEW MODE - Describe what you would do" if dry_run else "EXECUTE MODE - Generate actual file contents"
        
        prompt = f"""# DEVAGENT SYSTEM PROMPT

You are DevAgent, an AI development assistant. You execute development tasks by generating file contents.

## MODE: {mode}

## PROJECT CONTEXT

- **Name**: {ctx.get('name', 'Unknown')}
- **Path**: {ctx.get('path', 'Unknown')}
- **Tech Stack**: {', '.join(ctx.get('tech_stack', ['Unknown']))}
- **Primary Language**: {ctx.get('primary_language', 'Unknown')}
- **Framework**: {ctx.get('framework', 'Unknown')}

### Project Structure
```
{ctx.get('structure_summary', 'Not available')}
```

### Key Files
{self._format_key_files(ctx.get('key_files', {}))}

## CODING RULES AND GUIDELINES

{chr(10).join(rules) if rules else 'No specific rules loaded.'}

## DEVELOPER PREFERENCES

{persona if persona else 'No specific preferences loaded.'}
"""
        return prompt
    
    def _format_key_files(self, key_files: dict) -> str:
        """Format key files for the prompt."""
        if not key_files:
            return "No key files detected."
        
        lines = []
        for file_type, file_path in key_files.items():
            lines.append(f"- **{file_type}**: `{file_path}`")
        return "\n".join(lines)
    
    def _call_gemini(self, prompt: str) -> str:
        """Call the Gemini API and return the response text."""
        try:
            response = self.model.generate_content(prompt)
            return response
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {e}")
    
    def _parse_response(self, response: str) -> dict:
        """Parse the JSON response from Gemini."""
        # Clean up the response
        text = response.text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        
        # Try to parse directly
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            console.print(f"[yellow]Warning: Initial JSON parse failed, attempting repair...[/yellow]")
            
            # Try to fix common escape issues
            try:
                # Fix invalid escape sequences by escaping backslashes that aren't part of valid escapes
                fixed_text = self._fix_json_escapes(text)
                return json.loads(fixed_text)
            except json.JSONDecodeError:
                pass
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                try:
                    extracted = json_match.group()
                    fixed_extracted = self._fix_json_escapes(extracted)
                    return json.loads(fixed_extracted)
                except json.JSONDecodeError:
                    pass
            
            raise ValueError(f"Failed to parse Gemini response as JSON: {e}\nResponse: {text[:500]}")
    
    def _fix_json_escapes(self, text: str) -> str:
        """
        Fix common JSON escape issues in LLM responses.
        
        LLMs often produce invalid escape sequences like \\x, \\p, etc.
        This method attempts to fix them while preserving valid escapes.
        """
        # Valid JSON escape sequences
        valid_escapes = {'\\n', '\\r', '\\t', '\\b', '\\f', '\\"', '\\\\', '\\/'}
        
        result = []
        i = 0
        while i < len(text):
            if text[i] == '\\' and i + 1 < len(text):
                two_char = text[i:i+2]
                if two_char in valid_escapes:
                    result.append(two_char)
                    i += 2
                elif text[i+1] == 'u' and i + 5 < len(text):
                    # Unicode escape \uXXXX
                    result.append(text[i:i+6])
                    i += 6
                else:
                    # Invalid escape - escape the backslash
                    result.append('\\\\')
                    i += 1
            else:
                result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    def _execute_file_actions(self, actions: dict) -> dict:
        """Execute the file operations from the parsed response."""
        results = {"created": [], "modified": [], "deleted": []}
        
        # Create files
        for file_info in actions.get("files_to_create", []):
            path = file_info["path"]
            content = file_info["content"]
            self.file_ops.create_file(path, content)
            results["created"].append(path)
            console.print(f"   [green]+ Created: {path}[/green]")
        
        # Modify files
        for file_info in actions.get("files_to_modify", []):
            path = file_info["path"]
            content = file_info["content"]
            self.file_ops.write_file(path, content)
            results["modified"].append(path)
            console.print(f"   [yellow]~ Modified: {path}[/yellow]")
        
        # Delete files
        for path in actions.get("files_to_delete", []):
            self.file_ops.delete_file(path)
            results["deleted"].append(path)
            console.print(f"   [red]- Deleted: {path}[/red]")
        
        return results
    
    def _run_validation(self, command: str) -> dict:
        """Run a validation command and return the result."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=Path.cwd()
            )
            
            return {
                "command": command,
                "success": result.returncode == 0,
                "output": result.stdout if result.returncode == 0 else result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "command": command,
                "success": False,
                "output": "Command timed out after 120 seconds",
                "return_code": -1
            }
        except Exception as e:
            return {
                "command": command,
                "success": False,
                "output": str(e),
                "return_code": -1
            }
    
    def _generate_branch_name(self, prompt_name: str) -> str:
        """Generate a git branch name from the prompt name."""
        # Clean the prompt name
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '-', prompt_name.lower())
        clean_name = re.sub(r'-+', '-', clean_name).strip('-')
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        
        return f"devagent/{clean_name}-{timestamp}"

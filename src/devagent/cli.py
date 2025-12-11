#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevAgent CLI - Command Line Interface

Entry point for the devagent command.

Usage:
    devagent run <prompt_file>          Execute a prompt file
    devagent run <prompt_file> --dry    Preview without executing
    devagent context                    Show current project context
    devagent context --refresh          Refresh project context
    devagent rules                      List available rules
    devagent init                       Initialize devagent config
    devagent history                    Show task history for current project
"""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
import json
import sys

from devagent.agent import DevAgent
from devagent.context import ProjectContext
from devagent.knowledge import KnowledgeBase
from devagent.config import Config, ensure_global_config

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="devagent")
def main():
    """
    🤖 DevAgent - AI-powered development assistant
    
    Execute development tasks using Google's Gemini API.
    Designed to work with detailed prompts from Claude or other AI assistants.
    """
    pass


@main.command()
@click.argument("prompt_file", type=click.Path(exists=True))
@click.option("--dry", "-d", is_flag=True, help="Dry run - preview without executing")
@click.option("--rules", "-r", multiple=True, help="Additional rules to include")
@click.option("--no-git", is_flag=True, help="Skip git operations")
@click.option("--model", "-m", default=None, help="Specify the Gemini model to use (e.g., 'gemini-1.5-pro', 'flash'). Overrides the default.")
def run(prompt_file: str, dry: bool, rules: tuple, no_git: bool, model: str):
    """
    Execute a prompt file.
    
    The prompt file should be a markdown file with detailed instructions
    for the development task to perform.
    
    Example:
        devagent run prompts/UPDATE_SCHEMA.md
        devagent run task.md --dry
        devagent run task.md --rules typescript,nextjs
    """
    try:
        config = Config.load()
        agent = DevAgent(config, use_git=not no_git, model_override=model)
        
        prompt_path = Path(prompt_file).resolve()
        
        console.print(Panel(
            f"[bold blue]📄 Prompt:[/] {prompt_path.name}\n"
            f"[bold blue]📁 Project:[/] {Path.cwd().name}\n"
            f"[bold blue]🔧 Mode:[/] {'Dry Run' if dry else 'Execute'}\n"
            f"[bold blue]📚 Extra Rules:[/] {', '.join(rules) if rules else 'None'}",
            title="🤖 DevAgent",
            border_style="blue"
        ))
        
        if dry:
            console.print("\n[yellow]⚠️  DRY RUN - No changes will be made[/yellow]\n")
            result = agent.preview(prompt_path, extra_rules=list(rules))
        else:
            result = agent.execute(prompt_path, extra_rules=list(rules))
        
        _display_result(result)
        
    except FileNotFoundError as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        if config and config.debug:
            console.print_exception()
        sys.exit(1)


@main.command()
@click.option("--refresh", "-r", is_flag=True, help="Refresh context from project files")
def context(refresh: bool):
    """
    Show or refresh context for the current project.
    
    DevAgent automatically detects your project's tech stack,
    structure, and relevant files to provide better assistance.
    """
    try:
        project_ctx = ProjectContext(Path.cwd())
        
        if refresh:
            console.print("[yellow]🔄 Refreshing project context...[/yellow]")
            project_ctx.refresh()
            console.print("[green]✅ Context refreshed[/green]\n")
        
        ctx = project_ctx.get_context()
        
        console.print(Panel(
            f"[bold]Project:[/] {ctx['name']}\n"
            f"[bold]Path:[/] {ctx['path']}\n"
            f"[bold]Tech Stack:[/] {', '.join(ctx.get('tech_stack', ['Unknown']))}\n"
            f"[bold]Language:[/] {ctx.get('primary_language', 'Unknown')}\n"
            f"[bold]Framework:[/] {ctx.get('framework', 'Unknown')}",
            title="📁 Project Context",
            border_style="cyan"
        ))
        
        if ctx.get("key_files"):
            table = Table(title="Key Files Detected")
            table.add_column("Type", style="cyan")
            table.add_column("File", style="green")
            
            for file_type, file_path in ctx["key_files"].items():
                table.add_row(file_type, file_path)
            
            console.print(table)
            
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option("--category", "-c", help="Filter by category (rules, patterns, personas)")
def rules(category: str):
    """
    List available knowledge base rules.
    
    Rules are markdown files that provide context and guidelines
    for different technologies, patterns, and coding styles.
    """
    try:
        kb = KnowledgeBase()
        all_rules = kb.list_rules()
        
        if category:
            all_rules = {k: v for k, v in all_rules.items() if k == category}
        
        for cat, items in all_rules.items():
            table = Table(title=f"📚 {cat.title()}")
            table.add_column("Name", style="cyan")
            table.add_column("Description", style="white")
            
            for item in items:
                table.add_row(item["name"], item.get("description", ""))
            
            console.print(table)
            console.print()
            
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        sys.exit(1)


@main.command()
def init():
    """
    Initialize DevAgent configuration.
    
    Creates the global config directory and files if they don't exist.
    Prompts for API key if not configured.
    """
    try:
        config_path = ensure_global_config()
        console.print(f"[green]✅ Config initialized at:[/green] {config_path}")
        
        config = Config.load()
        if not config.gemini_api_key:
            api_key = click.prompt(
                "Enter your Gemini API key",
                hide_input=True
            )
            config.set_api_key(api_key)
            console.print("[green]✅ API key saved[/green]")
        else:
            console.print("[green]✅ API key already configured[/green]")
            
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option("--limit", "-n", default=10, help="Number of entries to show")
def history(limit: int):
    """
    Show task execution history for the current project.
    """
    try:
        project_ctx = ProjectContext(Path.cwd())
        hist = project_ctx.get_history(limit=limit)
        
        if not hist:
            console.print("[yellow]No history found for this project[/yellow]")
            return
        
        table = Table(title=f"📜 Task History - {Path.cwd().name}")
        table.add_column("Date", style="cyan")
        table.add_column("Prompt", style="white")
        table.add_column("Status", style="green")
        table.add_column("Files Changed", style="yellow")
        
        for entry in hist:
            status_icon = "✅" if entry["status"] == "success" else "❌"
            table.add_row(
                entry["timestamp"],
                entry["prompt_name"][:40],
                f"{status_icon} {entry['status']}",
                str(entry.get("files_changed", 0))
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        sys.exit(1)


def _display_result(result: dict):
    """Display the execution result in a nice format."""
    
    status = result.get("status", "unknown")
    
    if status == "success":
        console.print("\n[bold green]✅ Task completed successfully![/bold green]\n")
    elif status == "partial":
        console.print("\n[bold yellow]⚠️  Task completed with warnings[/bold yellow]\n")
    else:
        console.print("\n[bold red]❌ Task failed[/bold red]\n")
    
    # Files created
    if result.get("files_created"):
        console.print("[bold]📄 Files Created:[/bold]")
        for f in result["files_created"]:
            console.print(f"   [green]+ {f}[/green]")
    
    # Files modified
    if result.get("files_modified"):
        console.print("[bold]📝 Files Modified:[/bold]")
        for f in result["files_modified"]:
            console.print(f"   [yellow]~ {f}[/yellow]")
    
    # Git info
    if result.get("git"):
        git_info = result["git"]
        console.print(f"\n[bold]🔀 Git:[/bold]")
        if git_info.get("branch"):
            console.print(f"   Branch: [cyan]{git_info['branch']}[/cyan]")
        if git_info.get("commit"):
            console.print(f"   Commit: [cyan]{git_info['commit'][:8]}[/cyan]")
    
    # Validation
    if result.get("validation"):
        val = result["validation"]
        val_status = "✅" if val.get("success") else "❌"
        console.print(f"\n[bold]🧪 Validation:[/bold] {val_status}")
        if val.get("command"):
            console.print(f"   Command: [dim]{val['command']}[/dim]")
        if val.get("output") and not val.get("success"):
            console.print(f"   [red]{val['output'][:500]}[/red]")
    
    # Summary
    if result.get("summary"):
        console.print(f"\n[bold]📋 Summary:[/bold]")
        console.print(f"   {result['summary']}")
    
    # Errors
    if result.get("errors"):
        console.print(f"\n[bold red]Errors:[/bold red]")
        for err in result["errors"]:
            console.print(f"   [red]• {err}[/red]")


if __name__ == "__main__":
    main()

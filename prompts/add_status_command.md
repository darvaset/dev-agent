# Task: Add 'devagent status' command

## Context
To improve usability and help users verify their setup, we need a new command that displays the current configuration status of DevAgent. This aligns with "Phase 1: Usability & Documentation" in the `ROADMAP.md`.

## Requirements
1.  **Modify `src/devagent/cli.py`**: Add a new command function decorated with `@main.command()`.
2.  **Command Name**: The command should be named `status`.
3.  **Functionality**:
    *   Load the `Config` from `devagent.config`.
    *   Check if the `GEMINI_API_KEY` is configured.
    *   Get the `default_model` from the configuration.
    *   Get the path to the global config directory.
4.  **Output Formatting**:
    *   Use `rich.panel.Panel` to display the information in a style consistent with other commands (like `devagent context`).
    *   The panel should display:
        *   **Config Directory**: The path to `~/.devagent`.
        *   **API Key Status**: "✅ Configured" if the key exists, "❌ Not Found" otherwise.
        *   **Default Model**: The value of `default_model` from the config.

## Files to Modify
- `src/devagent/cli.py`

## Example Implementation (to guide the agent)
```python
# This is an example to be placed in src/devagent/cli.py

@main.command()
def status():
    """Display current configuration status."""
    try:
        config = Config.load()
        
        api_key_status = "✅ Configured" if config.gemini_api_key else "❌ Not Found"
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_row("[bold]Config Directory[/]:", str(config.config_dir))
        table.add_row("[bold]API Key Status[/]:", api_key_status)
        table.add_row("[bold]Default Model[/]:", config.default_model)
        
        console.print(Panel(
            table,
            title="⚙️ DevAgent Status",
            border_style="yellow"
        ))
            
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        sys.exit(1)
```

## Validation
After the command is added, running `devagent status` in the terminal should display the configuration panel without errors.

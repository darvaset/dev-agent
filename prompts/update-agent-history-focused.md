# Task: Update DevAgent's Agent Logic for Enhanced History Saving

## Context

The `ProjectContext.add_history_entry` method is now capable of storing the full original prompt and the complete Gemini API response. This task is to update the `DevAgent` class to utilize this enhanced functionality.

## Requirements

1.  **Locate the `execute` method in `src/devagent/agent.py`.**
2.  **Identify the line where `self.project_ctx.add_history_entry` is called.**
3.  **Modify this call to pass the following arguments:**
    *   `full_prompt_content=enriched_prompt`
    *   `full_gemini_response=response.text`

    *   Ensure `enriched_prompt` (the complete prompt sent to Gemini) is correctly used.
    *   Ensure `response.text` (the full text response from Gemini's `model.generate_content`) is correctly used.

    The call should now look like this (preserving existing arguments):
    ```python
    self.project_ctx.add_history_entry(
        prompt_name=prompt_path.name,
        result=result,
        full_prompt_content=enriched_prompt,
        full_gemini_response=response.text
    )
    ```

## Files to Modify

- `src/devagent/agent.py`

## Validation

After running DevAgent with this prompt, we will validate the implementation by:

1.  **Running a test task:** Execute `devagent run prompts/implement-enhanced-history.md`. (This is a dummy prompt to trigger DevAgent's execution).
2.  **Inspecting `history.json`**: Check the file `~/.devagent/projects/{project_hash}/history.json`. A new entry should appear for the executed task, and it should contain `task_id`, `full_prompt_path`, and `full_gemini_response_path` fields.
3.  **Verifying saved files**: Navigate to the task-specific history directory (e.g., `~/.devagent/projects/{project_hash}/history/{task_id}/`). Confirm that `prompt.md` and `response.json` files exist and contain the expected full content.

## Important Notes

-   **DO NOT** modify `src/devagent/context.py` or any other file.
-   Only modify the specified line in `src/devagent/agent.py`.
-   Ensure no new imports are introduced unless strictly necessary and directly related to the modification.

# Task: Add a new coding rule for 'testing'

## Context
Add a basic coding rule to the knowledge base focused on best practices for writing tests. This will expand DevAgent's internal knowledge base.

## Requirements
1.  Create a new markdown file: `knowledge/rules/testing.md`.
2.  The content of this file should be:

    ```markdown
    # Testing Best Practices

    ## General Guidelines
    - Write clear and concise test names.
    - Test one specific piece of functionality per test.
    - Use descriptive assertion messages.
    - Keep tests independent and repeatable.
    ```
    Ensure the markdown formatting is correct.

## Files to Create
- `knowledge/rules/testing.md`

## Validation
- Verify that the file `knowledge/rules/testing.md` exists.
- Verify its content matches the specified guidelines.
- Run `devagent rules` and confirm 'testing' appears in the list of rules.

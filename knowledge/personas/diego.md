# Diego's Development Preferences

## Communication Style

- **Spanish for discussions**, English for code and documentation
- Explain the reasoning before implementing
- Ask clarifying questions when requirements are ambiguous
- Provide options when there are multiple valid approaches

## Code Philosophy

1. **Explicit over implicit** - Code should clearly show intent
2. **Design for the future** - Consider extensibility, but don't over-engineer
3. **Document decisions** - Comments should explain WHY, not WHAT
4. **Fail fast, fail loud** - Errors should be visible and actionable

## Quality Standards

1. Code must compile/build without errors
2. Must pass existing tests (don't break what works)
3. Include basic error handling
4. Use typed languages/strict mode when available
5. Follow existing patterns in the codebase

## Formatting Preferences

- 2 spaces for indentation in TypeScript/JavaScript
- 4 spaces for Python
- 100 character line limit
- Trailing commas in multi-line structures
- Single quotes for strings (TypeScript)
- Double quotes for Python

## Project Organization

- Keep related code together
- Separate concerns (UI, business logic, data access)
- Use index files for cleaner imports
- Maintain a clear folder structure

## Git Workflow

- Feature branches for new work
- Descriptive commit messages using conventional commits
- Squash commits before merging when appropriate
- Keep PRs focused and reasonably sized

## Testing Philosophy

- Test behavior, not implementation
- Focus on critical paths first
- Integration tests over unit tests for APIs
- Don't test third-party code

## When Stuck

- Search for existing patterns in the codebase first
- Check official documentation
- Consider if the approach is too complex
- Ask for clarification rather than assume

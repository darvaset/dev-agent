# Base Rules - Always Applied

These rules apply to ALL projects regardless of tech stack.

## Code Quality

1. **Explicit over Implicit** - Always prefer explicit code that clearly shows intent
2. **Error Handling** - Never swallow errors silently; always handle or propagate them
3. **Comments** - Write comments for WHY, not WHAT. Code should be self-documenting for WHAT

## File Organization

1. Keep files focused on a single responsibility
2. Use descriptive file names that indicate purpose
3. Group related files in directories
4. Keep imports organized: external deps first, then internal modules, then types

## Git Practices

1. Use conventional commit messages: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, `test:`
2. One logical change per commit
3. Branch names should be descriptive: `feature/add-user-auth`, `fix/login-bug`

## Documentation

1. Every public function should have a docstring/JSDoc
2. README should explain what the project does, how to set it up, and how to run it
3. Document environment variables in `.env.example`

## Security

1. Never commit secrets or API keys
2. Validate all user input
3. Use parameterized queries for databases
4. Sanitize output to prevent XSS

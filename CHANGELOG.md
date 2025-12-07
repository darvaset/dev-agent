# Changelog

All notable changes to DevAgent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-06

### Added
- Initial release of DevAgent
- CLI tool installable via pip (`devagent` command)
- Gemini API integration with support for multiple models
- Automatic project context detection (tech stack, structure, key files)
- Knowledge base system with rules, patterns, and personas
- Built-in rules for: TypeScript, Python, Next.js, React, Prisma, Tailwind, Neo4j
- Git integration (auto-create branch, auto-commit)
- File operations (create, modify, delete)
- Commands:
  - `devagent run <prompt>` - Execute a development task
  - `devagent run <prompt> --dry` - Preview without executing
  - `devagent context` - Show project context
  - `devagent rules` - List available rules
  - `devagent init` - Initialize configuration
  - `devagent history` - Show task history
- Model shortcuts (pro, flash, flash-lite)
- Script to list available Gemini models
- Configuration stored in `~/.devagent/`

### Technical
- Python 3.10+ required
- Dependencies: google-generativeai, rich, click, gitpython, pyyaml

---

## [Unreleased]

### Planned for 0.2.0 (Phase 1)
- Enhanced history with full prompt/response storage
- Feedback system (good/bad marking)
- Project learnings file
- Detailed history command

See [ROADMAP.md](ROADMAP.md) for full development plan.

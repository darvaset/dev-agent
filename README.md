# 🤖 DevAgent

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange.svg)]()

AI-powered development assistant that executes coding tasks using Google's Gemini API. Designed to work with detailed prompts from Claude or other AI assistants.

## ✨ Features

- **🔍 Auto-Detection** - Automatically detects your project's tech stack and structure
- **📚 Knowledge Base** - Built-in coding rules for TypeScript, Python, Next.js, React, Prisma, and more
- **🔀 Git Integration** - Auto-creates branches and commits for each task
- **🎯 Multiple Models** - Support for Gemini 2.5 Pro, Flash, and experimental models
- **📋 Dry Run** - Preview changes before executing
- **👤 Personas** - Customize coding style and preferences

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/YOUR_USERNAME/dev-agent.git
cd dev-agent
pip install -e .

# Initialize (enter your Gemini API key)
devagent init

# Use in any project
cd /path/to/your/project
devagent run prompts/your-task.md
```

## 📋 Usage

### Execute a Task

```bash
# Run a prompt
devagent run prompts/ADD_USER_AUTH.md

# Preview without executing
devagent run prompts/UPDATE_SCHEMA.md --dry

# Use specific model
devagent run task.md --model pro

# Add extra rules
devagent run task.md --rules typescript,nextjs

# Skip git operations
devagent run task.md --no-git
```

### Other Commands

```bash
devagent context          # Show detected project context
devagent context --refresh # Refresh context cache
devagent rules            # List available rules
devagent history          # Show task history
devagent init             # Initialize/reset configuration
```

### Model Shortcuts

| Shortcut | Model | Use Case |
|----------|-------|----------|
| `pro` | gemini-2.5-pro | Complex tasks, best quality |
| `flash` | gemini-2.5-flash | Balanced (default) |
| `flash-lite` | gemini-2.5-flash-lite | Simple tasks, fast/cheap |
| `gemini-3-pro` | gemini-3-pro-preview | Experimental |

## 📁 Project Structure

```
dev-agent/
├── src/devagent/          # Main package
│   ├── cli.py             # CLI commands
│   ├── agent.py           # Core agent logic
│   ├── context.py         # Project detection
│   ├── knowledge.py       # Rules & patterns
│   ├── config.py          # Configuration
│   ├── git_ops.py         # Git operations
│   └── file_ops.py        # File operations
├── knowledge/             # Knowledge base
│   ├── rules/             # Coding standards
│   ├── patterns/          # Code templates
│   └── personas/          # Developer preferences
├── scripts/               # Utility scripts
└── pyproject.toml         # Package config
```

## 📚 Knowledge Base

### Built-in Rules

| Rule | Description |
|------|-------------|
| `_base` | Universal coding standards |
| `typescript` | TypeScript best practices |
| `python` | Python/PEP8 guidelines |
| `nextjs` | Next.js App Router patterns |
| `react` | React component patterns |
| `prisma` | Prisma schema & queries |
| `tailwind` | Tailwind CSS organization |
| `neo4j` | Neo4j/Cypher patterns |

### Adding Custom Rules

Create a markdown file in `knowledge/rules/`:

```markdown
# My Custom Rule

## Section 1
- Guideline 1
- Guideline 2
```

## ⚙️ Configuration

Configuration is stored in `~/.devagent/`:

```yaml
# ~/.devagent/config.yaml
default_model: models/gemini-2.5-flash
debug: false
auto_commit: true
create_branch: true
```

```bash
# ~/.devagent/.env
GEMINI_API_KEY="your-api-key-here"
```

## 📝 Writing Prompts

DevAgent works best with detailed, structured prompts:

```markdown
# Task: Add User Authentication

## Context
This project needs user authentication using Supabase Auth.

## Requirements
1. Add login/signup pages
2. Create auth context provider
3. Protect dashboard routes

## Files to Create
- src/app/login/page.tsx
- src/contexts/AuthContext.tsx

## Validation
Run: npm run build
```

## 🤝 Workflow with Claude

1. **Claude** designs the solution and creates detailed prompts
2. **DevAgent** executes the prompts using Gemini
3. **You** review and iterate

## 🛣️ Roadmap

See [ROADMAP.md](ROADMAP.md) for the full development plan.

**Next up (Phase 1):**
- Enhanced history with full prompt/response storage
- Feedback system for learning
- Project-specific learnings

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built by Diego** | QA Engineering Manager @ Bethink Labs

*"Automating development, one prompt at a time"*

# 🤖 DevAgent

AI-powered development assistant using Google's Gemini API. Execute development tasks from detailed prompts, with automatic context detection, git integration, and coding standards enforcement.

## 🎯 What It Does

DevAgent bridges the gap between AI design (Claude) and execution (Gemini):

1. **Reads** detailed prompt files (markdown)
2. **Detects** your project's tech stack and structure
3. **Applies** relevant coding rules and your preferences
4. **Generates** code using Gemini API
5. **Writes** files to your project
6. **Validates** changes (build/test)
7. **Commits** with proper git workflow

## 🚀 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/dev-agent.git
cd dev-agent

# Install in editable mode
pip install -e .

# Initialize configuration
devagent init
# Enter your Gemini API key when prompted
```

## 📋 Usage

### Execute a Prompt

```bash
cd /path/to/your/project

# Run a prompt file
devagent run prompts/ADD_USER_AUTH.md

# Preview without executing
devagent run prompts/UPDATE_SCHEMA.md --dry

# Use specific rules
devagent run task.md --rules typescript,nextjs

# Skip git operations
devagent run task.md --no-git
```

### Other Commands

```bash
# Show current project context
devagent context

# Refresh project context
devagent context --refresh

# List available rules
devagent rules

# Show task history
devagent history
```

## 📁 Project Structure

```
dev-agent/
├── src/devagent/          # Main package
│   ├── cli.py             # CLI entry point
│   ├── agent.py           # Main agent logic
│   ├── context.py         # Project detection
│   ├── knowledge.py       # Rules management
│   ├── config.py          # Configuration
│   ├── git_ops.py         # Git operations
│   └── file_ops.py        # File operations
├── knowledge/             # Knowledge base
│   ├── rules/             # Coding standards
│   ├── patterns/          # Code templates
│   └── personas/          # Developer preferences
└── pyproject.toml         # Package config
```

## 📚 Knowledge Base

DevAgent uses a knowledge base to provide context:

### Rules (`knowledge/rules/`)
- `_base.md` - Always applied
- `typescript.md` - TypeScript projects
- `python.md` - Python projects
- `nextjs.md` - Next.js projects
- `prisma.md` - Prisma ORM
- `react.md` - React components

### Personas (`knowledge/personas/`)
- `diego.md` - Your coding preferences

### Adding New Rules

Create a markdown file in `knowledge/rules/`:

```markdown
# My Custom Rule

## Section 1
- Rule 1
- Rule 2

## Section 2
...
```

## ⚙️ Configuration

Configuration is stored in `~/.devagent/`:

```
~/.devagent/
├── config.yaml       # Settings
├── .env              # API keys (chmod 600)
├── projects/         # Per-project context cache
└── logs/             # Execution logs
```

### config.yaml

```yaml
default_model: gemini-1.5-pro
debug: false
auto_commit: true
create_branch: true
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
4. Add logout functionality

## Files to Create
- src/app/login/page.tsx
- src/app/signup/page.tsx
- src/contexts/AuthContext.tsx
- src/middleware.ts

## Validation
Run: npm run build
```

## 🔧 Troubleshooting

### "API key not configured"
```bash
devagent init
# Or manually edit ~/.devagent/.env
```

### "Not a git repository"
Use `--no-git` flag or initialize git:
```bash
git init
```

### "Failed to parse response"
The model returned invalid JSON. Try:
- Simplifying your prompt
- Using a different model: `--model gemini-1.5-flash`

## 🤝 Workflow with Claude

1. **Claude** designs the solution and creates detailed prompts
2. **DevAgent** executes the prompts using Gemini
3. **You** review and iterate

Example prompt from Claude → DevAgent:

```markdown
# Update Database Schema

## Task
Update the Prisma schema to use Person instead of Player.

## Changes Required
1. Rename `Player` model to `Person`
2. Add `isRetired` field
3. Update all relations
...
```

## 📄 License

MIT

---

**Built by Diego** | QA Engineering Manager
*"Automating development, one prompt at a time"*

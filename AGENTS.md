# Repository Guidelines

## Project Structure & Module Organization
This repo packages Manus skill definitions.
- `skills/<skill-name>/SKILL.md`: core instruction set for each skill.
- `README.md`: sync and usage workflow.
- `manus-skills.json`: generated metadata manifest.

Keep skills self-contained so each folder can be copied or indexed independently.

## Build, Test, and Development Commands
This repository is generated; validate content and metadata after sync.

```bash
# List skill definitions
find skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort

# Check required frontmatter keys
rg -n "^(name|description):" skills/*/SKILL.md

# Validate metadata JSON
python3 -m json.tool manus-skills.json >/dev/null
```

## Coding Style & Naming Conventions
- Every `SKILL.md` starts with YAML frontmatter.
- Required fields: `name`, `description`.
- Keep names lowercase kebab-case and aligned with folder names.
- Keep instructions direct, task-oriented, and example-driven.

## Testing Guidelines
- Run frontmatter checks for every changed skill.
- Validate `manus-skills.json` after regeneration.
- Test each edited skill manually in Manus tooling.

## Commit & Pull Request Guidelines
Use Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`).
- Keep one logical change per commit.
- PRs should include changed skills and validation commands.

## Security & Configuration Tips
- Do not commit API keys or local credentials.
- Keep generated temp artifacts out of version control.

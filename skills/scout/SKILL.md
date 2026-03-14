---
name: scout
description: "Quick project reconnaissance and codebase analysis. Use when: first encountering a new codebase, onboarding to a project, generating a project overview, checking project health, identifying tech stack, or understanding architecture before making changes."
---

# Scout

Rapidly analyze a codebase and produce a structured overview covering tech stack, architecture, file statistics, health indicators, and entry points. Designed for the first thing you do when encountering a new project.

## Quick Start

```bash
bash /home/ubuntu/skills/scout/scripts/scout.sh /path/to/project
```

The script auto-detects the project type and produces a report covering languages, frameworks, infrastructure, file counts, line counts, directory structure, entry points, and health indicators.

## What Scout Detects

### Languages
Python, TypeScript, JavaScript, Rust, Go, C#, Java, Ruby, Swift — detected by file extension presence.

### Frameworks
Detected from `package.json`, `requirements.txt`, and `pyproject.toml`:

| Category | Frameworks Detected |
|----------|-------------------|
| Frontend | React, Next.js, Vue, Svelte, Tailwind |
| Backend | Express, Fastify, Django, Flask, FastAPI |
| Build | Vite, Webpack, TypeScript |
| ORM | Prisma, Drizzle |
| ML/AI | PyTorch, TensorFlow, Pandas |

### Infrastructure
Docker, GitHub Actions, GitLab CI, Vercel, Netlify, Terraform — detected from config files.

### Health Indicators

| Indicator | Good | Warning | Missing |
|-----------|------|---------|---------|
| README | 20+ lines | Under 20 lines | No file |
| LICENSE | Present | — | No file |
| Tests | Test files found | — | No test files |
| CI/CD | Workflow configured | — | No CI config |
| .gitignore | Present | — | No file |
| .env files | None in repo | Found in repo | — |
| Git activity | Recent commits | — | Not a git repo |

## Workflow

### 1. Run Scout
Execute the script against the project directory. It completes in seconds.

### 2. Read the Report
The report is printed to stdout in a structured format with labeled sections: LANGUAGES, FRAMEWORKS, INFRA, FILE_TYPES, LINE_COUNTS, ENTRY_POINTS, STRUCTURE, HEALTH.

### 3. Dive Deeper
Based on the scout report, decide what to investigate further. Common next steps:

| Scout Finding | Next Action |
|--------------|-------------|
| No tests | Set up test framework |
| Missing README | Use the `docs` skill to generate one |
| .env files in repo | Add to .gitignore, rotate secrets |
| No CI/CD | Set up GitHub Actions |
| Large file count | Run `quality-audit` for deeper analysis |
| Unfamiliar framework | Research with `swarm` skill |

## Use with Other Skills

Scout is designed as the entry point that feeds into other skills:

**Scout → Docs:** Scout identifies the tech stack and structure, then the `docs` skill generates appropriate documentation.

**Scout → Quality Audit:** Scout provides the overview, then `quality-audit` runs deep analysis tools on the specific areas that need attention.

**Scout → Swarm:** If scout reveals unfamiliar technologies, use `swarm` to research them in parallel.

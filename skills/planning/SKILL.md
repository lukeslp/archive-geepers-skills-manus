---
name: planning
description: >
  Project planning, building, scouting, quality auditing, testing, and validation.
  Includes task prioritization (geepers-planner), implementation execution
  (geepers-builder), project reconnaissance (scout), code quality auditing with
  real tools (quality-audit), test strategy (geepers-testing), and project
  validation (geepers-validate). Use when planning work, building from plans,
  auditing code quality, or validating project health.
---

# Planning

Plan, build, scout, audit, test, and validate projects. This skill covers the full lifecycle from reconnaissance through implementation to quality assurance.

## Quick Start

### Scout a project
```bash
bash scripts/scout.sh /path/to/project
```

### Run a quality audit
```bash
bash scripts/audit.sh /path/to/project
bash scripts/audit.sh /path/to/project --domain security
bash scripts/audit.sh /path/to/project --domain deps
```

Reports are saved to `<project>/.audit-reports/` as JSON.

## Planner: Task Prioritization

The planner transforms scattered plans, TODOs, and suggestions into prioritized, sequenced work queues.

### Plan Sources (Priority Order)

1. **Explicit plans**: PROJECT_PLAN.md, IMPLEMENTATION_PLAN.md, ROADMAP.md
2. **Task lists**: TODO.md, SUGGESTIONS.md, BACKLOG.md
3. **Embedded tasks**: `grep -rn "TODO:\|FIXME:\|HACK:\|XXX:" --include="*.{js,ts,py,md}"`
4. **Previous outputs**: Recommendation files, CRITIC.md, *-report.md

### Prioritization Algorithm

```
Impact Score (1-5): 5=critical bug, 4=important feature, 3=nice-to-have, 2=code quality, 1=cosmetic
Effort Score (1-5): 5=multiple days, 4=full day, 3=half day, 2=1-2 hours, 1=<1 hour
Risk Score  (1-5): 5=high regression, 4=moderate, 3=some, 2=low, 1=minimal

Priority = (Impact x 2) - Effort - (Risk x 0.5)
Quick Win  = Impact >= 3 AND Effort <= 2
```

### Estimation Heuristics

| Task Type | Typical Effort |
|-----------|----------------|
| Add environment variable | 1 |
| Fix typo/copy | 1 |
| Add simple validation | 1-2 |
| New utility function | 2 |
| New component | 2-3 |
| New API endpoint | 3 |
| Database migration | 3-4 |
| New feature (full) | 4-5 |
| Major refactor | 5 |

### Task Queue Output Format

Generate a queue file with sections: Ready to Build (priority order), Blocked Tasks, Deferred (low priority), and Statistics. Each task includes source reference, impact/effort/priority scores, description, affected files, and dependencies.

## Builder: Implementation Execution

The builder takes prioritized work items and implements them efficiently.

### Build Protocol

**Pre-Implementation**: Read task spec fully, identify affected files, understand existing patterns, check for related tests, plan changes.

**Implementation**: Make smallest working change, follow existing code style, add/update tests if pattern exists, keep commits atomic, document non-obvious logic.

**Post-Implementation**: Run existing tests, verify no regressions, self-review changes, prepare commit message, update task status.

### Commit Message Format
```
{type}: {brief description}

{Optional detailed explanation}

Implements: {task reference}
```

Types: feat, fix, refactor, style, docs, test, chore.

### Task Status

A task is **COMPLETE** when all specified functionality works, no regressions, tests pass, and code follows conventions. A task is **BLOCKED** when missing a dependency, spec is unclear, or architecture decision is needed. A task is **DEFERRED** when scope is larger than estimated or prerequisite work was found.

## Scout: Project Reconnaissance

Rapidly analyze a codebase and produce a structured overview.

### What Scout Detects

| Category | Details |
|----------|---------|
| Languages | Python, TypeScript, JavaScript, Rust, Go, C#, Java, Ruby, Swift |
| Frameworks | React, Next.js, Vue, Svelte, Tailwind, Express, Django, Flask, FastAPI |
| Infrastructure | Docker, GitHub Actions, GitLab CI, Vercel, Terraform |

### Health Indicators

| Indicator | Good | Warning | Missing |
|-----------|------|---------|---------|
| README | 20+ lines | Under 20 lines | No file |
| LICENSE | Present | — | No file |
| Tests | Test files found | — | No test files |
| CI/CD | Workflow configured | — | No CI config |
| .gitignore | Present | — | No file |
| .env files | None in repo | Found in repo | — |

### Scout Workflow
1. Run scout script against project directory (completes in seconds)
2. Read the structured report (LANGUAGES, FRAMEWORKS, INFRA, FILE_TYPES, etc.)
3. Decide next steps based on findings

| Scout Finding | Next Action |
|--------------|-------------|
| No tests | Set up test framework |
| Missing README | Use content skill to generate one |
| .env files in repo | Add to .gitignore, rotate secrets |
| No CI/CD | Set up GitHub Actions |
| Large file count | Run quality-audit for deeper analysis |

## Quality Audit: Real Analysis Tools

Run actual quality analysis tools (not just guidelines) against a codebase.

### Audit Domains

| Domain | What It Checks | Tools Used |
|--------|---------------|------------|
| deps | Vulnerable/outdated dependencies | npm audit, pip-audit |
| security | Exposed secrets, dangerous patterns | bandit, grep patterns |
| perf | Bundle size, large files, heavy deps | du, find, bundle analysis |
| a11y | Alt text, lang attrs, viewport, headings | HTML pattern scanning |

### Project Type Detection

| File Found | Detected Type | Tools Available |
|------------|--------------|-----------------|
| package.json | Node.js | npm audit, eslint, tsc |
| requirements.txt / pyproject.toml | Python | pip-audit, bandit, ruff, mypy |
| Cargo.toml | Rust | cargo audit, clippy |
| go.mod | Go | govulncheck |

### Triage Findings

| Priority | Category | Action |
|----------|----------|--------|
| Critical | Exposed secrets, known CVEs | Fix immediately |
| High | Security vulnerabilities, XSS risks | Fix before deploy |
| Medium | Outdated dependencies, missing a11y | Fix in next sprint |
| Low | Code style, minor warnings | Fix opportunistically |

For deeper analysis beyond the basic audit script, see `references/tools.md`.

## Quality Orchestration

Coordinate multiple audit agents for comprehensive quality assessment across accessibility, performance, API design, and dependencies.

### Scoring System

| Component | Weight | Score Range |
|-----------|--------|-------------|
| Accessibility | 25% | 0-100 |
| Performance | 25% | 0-100 |
| API Design | 25% | 0-100 |
| Dependencies | 25% | 0-100 |

Ratings: 90-100 Excellent, 75-89 Good, 60-74 Fair, Below 60 Needs Attention.

### Audit Modes
- **Full Audit**: All four domains in parallel
- **Frontend Focus**: Accessibility + client-side performance
- **Backend Focus**: API design + server-side performance + security
- **Security Focus**: Vulnerability scan + API security patterns

## Testing: Strategy and Coverage

Design test suites, write effective tests, and analyze coverage.

### Test Frameworks

| Ecosystem | Framework | Command |
|-----------|-----------|---------|
| Python | pytest | `pytest tests/ -v --cov=app --cov-report=html` |
| JS/TS | Vitest/Jest | `vitest run --coverage` |

### Test Categories

| Type | Purpose | Speed |
|------|---------|-------|
| Unit | Single function | Fast (ms) |
| Integration | Multiple components | Medium (s) |
| E2E | Full user flows | Slow (min) |

### Test Quality Principles (FIRST)
1. **Fast** — Quick execution
2. **Isolated** — No dependencies between tests
3. **Repeatable** — Same result every time
4. **Self-validating** — Clear pass/fail
5. **AAA Pattern** — Arrange, Act, Assert

## Validation: Project Health Checks

Comprehensive validation of configurations, paths, permissions, integrations, and overall project health. Use before deployments, after significant changes, or for periodic health checks.

### Validation Domains
1. **Configuration**: Service manager syntax, environment files, JSON/YAML configs
2. **Paths**: Script paths, working directories, log directories, static assets
3. **Permissions**: File permissions, directory write access
4. **Integrations**: API endpoints, database connections, external services
5. **Security**: Exposed secrets, file permissions, .gitignore coverage

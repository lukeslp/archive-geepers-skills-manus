---
name: quality-audit
description: "Code quality auditing skill that runs real analysis tools in the sandbox. Use when: auditing a codebase for security vulnerabilities, checking dependency health, scanning for accessibility issues, measuring performance, running linters, or generating a comprehensive quality report for a project."
---

# Quality Audit

Run real quality analysis tools against a codebase and produce practical reports. Unlike guideline-only approaches, this skill installs and executes actual tools (npm audit, bandit, eslint, ruff, etc.) in the Manus sandbox and reports real findings.

## Quick Start

### Full audit (all domains)
```bash
bash /home/ubuntu/skills/quality-audit/scripts/audit.sh /path/to/project
```

### Single domain
```bash
bash /home/ubuntu/skills/quality-audit/scripts/audit.sh /path/to/project --domain security
bash /home/ubuntu/skills/quality-audit/scripts/audit.sh /path/to/project --domain deps
bash /home/ubuntu/skills/quality-audit/scripts/audit.sh /path/to/project --domain perf
bash /home/ubuntu/skills/quality-audit/scripts/audit.sh /path/to/project --domain a11y
```

Reports are saved to `<project>/.audit-reports/` as JSON files for programmatic use.

## Audit Domains

| Domain | What It Checks | Tools Used |
|--------|---------------|------------|
| deps | Vulnerable dependencies, outdated packages | npm audit, pip-audit |
| security | Exposed secrets, dangerous patterns, code vulnerabilities | bandit, grep patterns, .gitignore checks |
| perf | Bundle size, large files, heavy dependencies | du, find, bundle analysis |
| a11y | Alt text, lang attributes, viewport, heading hierarchy | HTML pattern scanning |

## Workflow

### 1. Detect Project Type

The audit script auto-detects the project type from manifest files:

| File Found | Detected Type | Tools Available |
|------------|--------------|-----------------|
| package.json | Node.js | npm audit, eslint, tsc |
| requirements.txt / pyproject.toml | Python | pip-audit, bandit, ruff, mypy |
| Cargo.toml | Rust | cargo audit, clippy |
| go.mod | Go | govulncheck |

### 2. Run Audit

The script installs missing tools automatically (using `sudo pip3 install` or `npx`), runs each tool, and saves structured output to `.audit-reports/`.

### 3. Interpret Results

After running the audit script, read the JSON reports for detailed findings. The console output provides a summary with color-coded PASS/WARN/FAIL indicators.

### 4. Prioritize Fixes

Triage findings by severity:

| Priority | Category | Action |
|----------|----------|--------|
| Critical | Exposed secrets, known CVEs | Fix immediately |
| High | Security vulnerabilities, XSS risks | Fix before deploy |
| Medium | Outdated dependencies, missing a11y | Fix in next sprint |
| Low | Code style, minor warnings | Fix opportunistically |

## Advanced Tools

For deeper analysis beyond the basic audit script, see `references/tools.md` for tool-specific commands covering linting, type checking, test coverage, bundle analysis, license compliance, and more.

## Parallel Audits

For large projects or monorepos, combine with the `swarm` skill to audit multiple packages in parallel. Each subtask can run the audit script on a different package and return structured results for comparison.

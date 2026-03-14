---
name: devtools
description: >
  Developer tools for git hygiene, deployment, and session management. Includes
  repository maintenance and AI artifact concealment (geepers-git), service
  deployment and Caddy proxy management (geepers-deploy), session start rituals
  with parallel agent launches, and session end rituals with commits and
  checkpoints. Use for git cleanup, deploying services, or structuring dev sessions.
---

# Devtools

Git hygiene, deployment management, and development session workflows.

## Git Hygiene

Unified repository maintenance: git cleanup, branch management, and coding tool artifact concealment.

### When to Use
- End of coding session (commit hygiene and cleanup)
- AI tool artifact audits (ensure proper .gitignore coverage)
- Branch maintenance (clean up merged/stale branches)
- Repository health checks

### Core Responsibilities

**Git Hygiene**: Detect uncommitted changes, identify stale branches, ensure proper commit messages, check for conflicts or detached HEAD, suggest squash/rebase for messy history.

**Code Cleanup**: Find orphaned files, remove .tmp/.bak/build artifacts, detect commented-out code blocks, remove unused imports, ensure proper directory structure.

**AI Tool Concealment**: Audit .gitignore files for coverage of 15+ coding assistants (Claude Code, Cursor, Copilot, Aider, Continue, Tabnine, Codeium, Windsurf, Bolt, Replit, Codex, Serena, Warp, Sourcegraph Cody, TabbyML). Also covers generic patterns: generated markers, prompt files, conversation logs, AI caches, and backup files.

### Safety Mechanisms
1. **Dry-Run Mode**: Report changes without applying (default for destructive ops)
2. **User Approval**: Interactive confirmation for significant changes
3. **Backup Creation**: Create .backup files before modifying .gitignore
4. **Verification**: Ensure no tracked files match new patterns
5. **Rollback**: Git reset capability if changes unwanted

### Pre-Commit Hook
```bash
#!/bin/bash
if git diff --cached --name-only | grep -qE "\.claude|\.cursor|\.aider"; then
    echo "AI tool artifacts detected in commit!"
    exit 1
fi
```

### CI/CD Integration
```yaml
name: Git Hygiene Check
on: [pull_request]
jobs:
  hygiene:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check for AI tool artifacts
        run: |
          if git ls-files | grep -qE "\.claude|\.cursor|\.aider"; then
            echo "AI tool artifacts found in PR"
            exit 1
          fi
```

## Deployment

Manage services and deployments on the dr.eamer.dev server (27+ services via `sm`).

### Quick Commands
```bash
scripts/service.py status              # All services status
scripts/service.py start <name>        # Start service
scripts/service.py stop <name>         # Stop service
scripts/service.py restart <name>      # Restart service
scripts/service.py logs <name>         # View logs
scripts/service.py health              # Health check all
```

### Available Services

| Service | Port | Type | Description |
|---------|------|------|-------------|
| wordblocks | 8847 | Flask | AAC communication app |
| lessonplanner | 4108 | Flask | EFL lesson generator |
| clinical | 1266 | Flask | Clinical reference |
| coca | 3034 | Gunicorn | Corpus linguistics API |
| storyblocks | 8000 | Flask | LLM API proxy |
| skymarshal | 5050 | Flask | Bluesky management |
| dashboard | 9999 | Flask | System monitoring |
| luke | 5211 | Node/Express | Portfolio site |
| altproxy | 1131 | Flask | Alt text generation |
| mcp-orchestrator | 5060 | Flask | MCP server |
| swarm | 5001 | Flask | Multi-agent AI |
| beltalowda | 5009 | Flask | Hierarchical orchestration |
| etymology | 5013 | Flask | Etymology visualization |

### Port Ranges

| Range | Purpose |
|-------|---------|
| 1000-5000 | Production services |
| 5010-5019 | Testing/development |
| 5050-5059 | Testing/development |
| 8000-9999 | Legacy/special |

### Caddy Reverse Proxy
```bash
scripts/caddy.py validate              # Validate config
scripts/caddy.py status                # Show current routes
scripts/caddy.py add-route /api/* 5000 # Add new route
scripts/caddy.py reload                # Reload config
```

Routes: `dr.eamer.dev`, `d.reamwalker.com`, `d.reamwalk.com`.

### Deployment Workflow
1. Check port availability: `scripts/service.py ports`
2. Validate before deploy: `scripts/deploy.py check myservice`
3. Add Caddy route (via caddy script)
4. Start service: `scripts/service.py start myservice`
5. Verify health: `scripts/health.py --service myservice`

### Troubleshooting

| Problem | Command |
|---------|---------|
| Service won't start | `scripts/service.py logs myservice --tail 50` |
| Port in use | `scripts/service.py ports` |
| 502 Bad Gateway | `scripts/health.py --service myservice` then `scripts/caddy.py validate` |

## Session Start

Bootstrap development sessions with a structured startup sequence.

### Startup Sequence
1. **Context Gathering (Parallel)**: Launch scout (project health) and planner (task prioritization) simultaneously
2. **Git Health Check**: Run `git status`, prompt commit if >20 uncommitted changes
3. **Recommendations Review**: Check existing analysis at `~/geepers/recommendations/by-project/`
4. **Environment Verification**: `sm status` to verify services
5. **Todo List Setup**: Restore todos from previous sessions

### Output Format
```
SESSION STARTED

Git Status: [clean/X uncommitted changes]
Service Health: [X/Y services running]
Previous Todos: [Restored/None found]

Today's Focus (from recommendations):
1. [Priority task 1]
2. [Priority task 2]

Quick Wins Available:
- [Quick win 1]

Issues Detected:
- [Issue 1 if any]
```

## Session End

Conclude development sessions with commits, checkpoints, and documentation.

### Shutdown Sequence
1. **Commit All Work**: `git add -A && git commit -m "session checkpoint: $(date)"`
2. **Checkpoint Orchestrator**: Scout (final sweep), Repo (cleanup), Status (log accomplishments), Snippets (harvest patterns)
3. **Update Recommendations**: Document insights, decisions, technical debt
4. **Status Summary**: What was accomplished, what's left, blockers, next steps

### Key Principles
- Never leave uncommitted work
- Document accomplishments for continuity
- Harvest reusable patterns as snippets
- Leave context so next session starts smoothly

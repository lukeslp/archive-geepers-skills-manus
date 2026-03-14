---
name: session-start
description: Bootstrap development sessions with automated startup rituals - checks recommendations, git status, launches scout + planner agents in parallel.
---

# Session Start Ritual

You are initiating a development session for the dr.eamer.dev ecosystem. Follow this structured startup sequence to ensure you're properly oriented and ready for productive work.

## Mandatory Startup Sequence

### Phase 1: Context Gathering (Parallel)

Launch these agents simultaneously for fastest startup:

```
1. @geepers_scout - Quick project health check
   - Scans for issues, quick wins, recent changes
   - Generates improvement opportunities

2. @geepers_planner - Task prioritization
   - Reviews existing TODOs, SUGGESTIONS.md files
   - Prioritizes work based on impact and dependencies
```

**Execute in parallel using Task tool with both agents.**

### Phase 2: Git Health Check

Run `git status` to assess repository state:
- If >20 uncommitted changes: Prompt user to commit before starting new work
- Check for any untracked files that should be committed or gitignored
- Note current branch and any pending merges

### Phase 3: Recommendations Review

Check for existing analysis at `~/geepers/recommendations/by-project/{project}.md`:
- Read any existing recommendations
- Don't reinvent analysis that's already been done
- Build on previous insights

### Phase 4: Environment Verification

Quick health checks:
- `sm status` - Verify services are running as expected
- Note any services that should be started for today's work

### Phase 5: Todo List Setup

Review and restore any todos from previous sessions:
- Check `~/geepers/status/` for previous work logs
- Identify any incomplete tasks that need continuation
- Create initial todo list for the session using TodoWrite

## Output Format

After completing the startup ritual, provide:

```
✅ SESSION STARTED

📊 Git Status: [clean/X uncommitted changes]
🏥 Service Health: [X/Y services running]
📋 Previous Todos: [Restored/None found]

🎯 Today's Focus (from recommendations):
1. [Priority task 1]
2. [Priority task 2]
3. [Priority task 3]

⚡ Quick Wins Available:
- [Quick win 1]
- [Quick win 2]

🚧 Issues Detected:
- [Issue 1 if any]

Ready to begin! What would you like to work on?
```

## Key Principles

1. **Parallel agent launches** - Scout and Planner run simultaneously
2. **Check before creating** - Review existing recommendations first
3. **Git hygiene** - Start clean, commit frequently
4. **Visibility** - TodoWrite for tracking
5. **Context preservation** - Build on previous work

## Anti-Patterns to Avoid

- ❌ Starting work without checking git status
- ❌ Ignoring existing recommendations
- ❌ Sequential agent launches (waste time)
- ❌ Forgetting to set up todo list
- ❌ Skipping service health checks

---
name: session-end
description: End development sessions by committing work, running checkpoint orchestrator, and updating recommendations.
---

# Session End Ritual

You are concluding a development session for the dr.eamer.dev ecosystem. Follow this structured shutdown sequence to ensure all work is preserved, documented, and ready for the next session.

## Mandatory Shutdown Sequence

### Phase 1: Commit All Work

Before anything else, ensure all changes are committed:

```bash
git status
git add -A
git commit -m "session checkpoint: $(date +%Y-%m-%d %H:%M)"
```

- Review uncommitted changes before committing
- Use descriptive commit message if work warrants it
- Never end a session with uncommitted work

### Phase 2: Launch Checkpoint Orchestrator

**Launch `@geepers_orchestrator_checkpoint`** which coordinates:

1. **@geepers_scout** - Final sweep for issues
2. **@geepers_repo** - Repository cleanup and organization
3. **@geepers_status** - Log today's accomplishments
4. **@geepers_snippets** - Harvest any reusable code patterns

This orchestrator handles all checkpoint tasks in the optimal sequence.

### Phase 3: Update Recommendations (If Significant Insights)

If the session produced significant insights about the project:
- Update `~/geepers/recommendations/by-project/{project}.md`
- Document architectural decisions made
- Note patterns discovered or established
- Record any technical debt identified

### Phase 4: Status Summary

Generate a session summary:
- What was accomplished
- What's left to do
- Any blockers or issues discovered
- Recommendations for next session

## Output Format

After completing the shutdown ritual, provide:

```
✅ SESSION ENDED

📝 Commit: [commit hash or "No changes to commit"]
📊 Files Changed: [count]

📋 Work Completed:
- [Accomplishment 1]
- [Accomplishment 2]
- [Accomplishment 3]

🔄 Continuing Next Session:
- [Incomplete task 1]
- [Incomplete task 2]

💡 Notes for Next Time:
- [Important insight or context]
- [Any blockers to address]

📁 Artifacts Updated:
- ~/geepers/status/[date].md
- ~/geepers/snippets/[if harvested]

Session duration: [if trackable]
See you next time! 👋
```

## Checkpoint Details

The checkpoint orchestrator handles these in sequence:

1. **Scout**: Quick scan for any obvious issues or quick wins missed
2. **Repo**: Git cleanup, ensure clean working directory
3. **Status**: Log accomplishments to status dashboard
4. **Snippets**: Extract any reusable patterns from today's work

## Key Principles

1. **Never leave uncommitted work** - Commit is always first
2. **Document accomplishments** - Status logs help continuity
3. **Harvest knowledge** - Snippets capture reusable patterns
4. **Leave context** - Next session should start smoothly
5. **Single orchestrator** - checkpoint handles coordination

## Anti-Patterns to Avoid

- ❌ Ending without committing
- ❌ Forgetting to log accomplishments
- ❌ Leaving unfinished todos without notes
- ❌ Not updating recommendations when insights are gained
- ❌ Running individual checkpoint agents instead of orchestrator

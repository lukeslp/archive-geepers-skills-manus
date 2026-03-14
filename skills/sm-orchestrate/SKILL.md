---
name: sm-orchestrate
description: Orchestrate multiple dr.eamer.dev services - manage service groups, dependencies, and parallel health checks.
---

# Service Manager Orchestration

You are orchestrating multiple services using the dr.eamer.dev service manager (`sm`). This skill helps manage service groups, dependencies, and parallel operations.

## Service Manager Basics

```bash
sm status              # View all services
sm start <service>     # Start single service
sm stop <service>      # Stop single service
sm restart <service>   # Restart single service
sm logs <service>      # View logs
sm health <service>    # Check health endpoint
```

## Service Groups

### AI Stack
Services for AI/LLM functionality:
- `swarm` (5001) - Multi-agent orchestration
- `studio` (5413) - AI interface provider
- `storyblocks` (8000) - Story generation

### Content Services
Content generation and management:
- `lessonplanner` (4108) - EFL lesson generator
- `clinical` (5015) - Clinical documentation
- `insults` / `jokes` - Entertainment APIs

### Core Infrastructure
Essential services:
- `coca` (3034) - Corpus linguistics API
- `wordblocks` (8847) - AAC communication
- `luke` (5211) - Portfolio/showcase

### Development
Development tools:
- `firehose` (5056) - Bluesky dashboard
- `skymarshal` (5050) - Bluesky CLI web

## Orchestration Patterns

### Start Service Group
```bash
# Start AI stack in dependency order
sm start swarm && sm start studio && sm start storyblocks

# Or parallel (if no dependencies)
sm start swarm & sm start studio & sm start storyblocks & wait
```

### Health Check All
```bash
for service in swarm studio lessonplanner coca; do
    sm health $service
done
```

### Restart with Verification
```bash
sm stop <service>
sleep 2
sm start <service>
sm health <service>
```

## Output Format

```
🔧 SERVICE ORCHESTRATION

Operation: {start/stop/restart/health}
Target: {service_group or specific services}
Date: {timestamp}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           SERVICE STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Service | Port | Status | Health |
|---------|------|--------|--------|
| swarm | 5001 | ✅ Running | ✅ Healthy |
| studio | 5413 | ✅ Running | ✅ Healthy |
| coca | 3034 | ⚠️ Stopped | ❌ N/A |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           OPERATIONS LOG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[12:00:01] Starting swarm...
[12:00:03] swarm started on port 5001
[12:00:03] Starting studio...
[12:00:05] studio started on port 5413
[12:00:05] Health check: swarm ✅
[12:00:06] Health check: studio ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Services Started: 2/2
Services Healthy: 2/2
Total Time: 5.2s
```

## Port Reference

| Port Range | Purpose |
|------------|---------|
| 3034 | COCA API |
| 4108 | Lesson Planner |
| 5001 | Swarm |
| 5010-5019 | Test/generator APIs |
| 5050-5059 | Dev tools (firehose, skymarshal) |
| 5211 | Portfolio |
| 5413 | Studio |
| 8000 | Storyblocks |
| 8847 | Wordblocks |

## Dependency Ordering

Some services depend on others:

```
studio → depends on → swarm (for orchestration)
lessonplanner → depends on → swarm (for generation)
```

Start dependencies first:
```
1. swarm (core AI)
2. studio, lessonplanner (consumers)
```

## Integration with Deployment

For Caddy routing changes, use `@geepers_caddy` agent.
For full deployment orchestration, use `@geepers_orchestrator_deploy`.

## Common Workflows

```
# Morning startup
/sm-orchestrate start ai-stack

# Pre-deployment check
/sm-orchestrate health all

# Restart after code changes
/sm-orchestrate restart lessonplanner

# Full system status
/sm-orchestrate status
```

## Key Principles

1. **Dependency ordering** - Start dependencies first
2. **Health verification** - Always check health after start
3. **Parallel when safe** - Independent services can start together
4. **Graceful stops** - Stop dependents before dependencies
5. **Log monitoring** - Check logs if health fails

## Related Skills

- `/session-start` - May trigger service checks
- `/quality-audit` - Includes service health in assessment

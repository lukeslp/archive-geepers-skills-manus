---
name: orchestration
description: >
  Multi-agent orchestration, team coordination, and service management. Includes
  the master conductor for routing to specialist agents, Dream Cascade
  (hierarchical 3-tier synthesis), Dream Swarm (parallel multi-domain search),
  executive/product/engineering/finance orchestrators, and service manager
  orchestration. Use when coordinating multiple agents, running multi-agent
  research workflows, managing service groups, or routing complex tasks.
---

# Orchestration

Coordinate multi-agent workflows, route tasks to specialists, and manage service orchestration.

## Team Conductor

The master orchestrator that analyzes situations, determines which agents are needed, and dispatches them in the optimal sequence.

### Decision Matrix

| Request Pattern | Route To |
|----------------|----------|
| Session start | Scout + recommendations review |
| Session end / checkpoint | Checkpoint orchestrator |
| Deployment / infrastructure | Deploy orchestrator |
| Code review / quality audit | Quality orchestrator |
| Full-stack feature | Fullstack orchestrator |
| Data gathering / research | Research orchestrator |
| Build from plans / backlog | Hive orchestrator |
| Frontend / UI work | Frontend orchestrator |
| Flask web app | Web orchestrator |
| Python project | Python orchestrator |
| Game development | Games orchestrator |
| Linguistics / NLP | Corpus orchestrator |
| Quick health check | Canary agent |
| Deep cleanup | Janitor agent |
| UX / architecture critique | Critic agent |
| Full system check | System diagnostics |

### Available Orchestrators

| Orchestrator | Scope |
|-------------|-------|
| Checkpoint | Scout, repo, status, snippets, janitor |
| Deploy | Validator, caddy, services, canary, security |
| Quality | A11y, perf, API, deps, critic, testing, security |
| Fullstack | API, DB, services, Express + design, a11y, React |
| Frontend | CSS, TypeScript, motion, webperf + React, design, a11y |
| Hive | Planner, builder, quickwin, integrator, refactor |
| Research | Fetcher, searcher, data, links, diag, citations |
| Games | Gamedev, game, React, Godot |
| Corpus | Corpus, corpus UX, DB |
| Web | Flask, React, design, a11y, critic |
| Python | Flask, pycli, API, deps |

### Workflow Requirements
1. Create a plan for multi-step tasks
2. Read before editing files
3. Commit before major changes
4. Check existing state before acting
5. Review existing recommendations first
6. Get user sign-off before modifying 3+ files
7. Batch independent operations in parallel
8. Verify after changes (tests, services, configs)

## Dream Cascade: Hierarchical Synthesis

Three-tier hierarchical research workflow via the dr.eamer.dev API.

### Architecture
```
Tier 1: Belters (Workers) — 1-30+ parallel agents with unique specializations
    ↓
Tier 2: Drummers (Synthesizers) — Aggregate every 5 Belter responses
    ↓
Tier 3: Camina (Executive) — Final strategic report
```

### API Endpoint
```bash
POST https://api.dr.eamer.dev/v1/orchestrate/cascade
{
  "task": "Analyze the current state of quantum computing hardware",
  "num_agents": 8,
  "provider": "anthropic"
}
```

### CLI Usage
```bash
python3 scripts/orchestrator.py "What is the future of AGIs?"
python3 scripts/orchestrator.py "Analyze semiconductor supply chain" \
  --belters 15 --drummers 3 --caminas 1 --pdf
```

### MCP Tool: `dream_orchestrate_research`
Parameters: `task` (required), `num_agents` (default 5), `enable_drummer` (default true), `enable_camina` (default false), `provider_name` (default "anthropic").

### When to Use
- Complex research requiring multiple perspectives
- Cross-domain synthesis that would take multiple sequential queries
- Long-horizon analysis where parallelism saves time

### When NOT to Use
- Simple single-source queries (use data fetching instead)
- Need fine-grained control over individual agents
- Latency-critical scenarios (orchestration takes 10-60 seconds)

## Dream Swarm: Parallel Multi-Domain Search

Launch parallel search workflows across 17 data sources simultaneously.

### Architecture
```
Search Query → Fan out to domain agents (parallel) → Aggregator (dedupe + synthesize)
```

### API Endpoint
```bash
POST https://api.dr.eamer.dev/v1/orchestrate/swarm
{
  "query": "What are the most effective treatments for Type 2 diabetes?",
  "sources": ["pubmed", "semantic_scholar", "wikipedia"],
  "num_agents": 5
}
```

### CLI Usage
```bash
scripts/swarm-search.py "LLM safety research" --domains arxiv github news
scripts/swarm-search.py "climate change" --agents 10 --parallel 5
scripts/swarm-search.py "quantum computing" --all-domains
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| --domains | arxiv,news | Comma-separated domain list |
| --agents | 5 | Parallel agents (1-20) |
| --parallel | 3 | Max concurrent searches (1-10) |
| --provider | xai | LLM provider for synthesis |
| --max-results | 10 | Results per domain |
| --stream | false | Enable SSE streaming |
| --output | stdout | Output format (stdout, json, markdown) |

### Swarm vs Cascade

| Aspect | Dream Swarm | Dream Cascade |
|--------|-------------|---------------|
| Speed | Faster (parallel) | Slower (hierarchical) |
| Depth | Broad coverage | Deep analysis |
| Use case | Data gathering | Research synthesis |
| Agent count | Many simple agents | Fewer complex agents |
| Cost | Lower | Higher |

## Executive Orchestration

High-level strategic planning and cross-team coordination.

### Executive (CEO)
Decomposes high-level goals into team directives. Coordinates handoffs between Product, Finance, Engineering.

**Workflows**:
- Venture creation: Product research → Finance monetization → Engineering MVP
- Organizational audit: Code review → UX/features review → Stability verification

### Product (Head of Product)
Market research, PRDs, roadmaps, and feature specs.
- New product discovery: deep research → synthesize findings → propose strategy
- Implementation planning: define requirements → user stories → handoff to engineering

### Engineering (VP of Engineering)
System architecture, full-stack implementation, refactoring.
- Build feature: architect → implement backend → implement frontend → verify
- Architecture review: analyze dependencies → propose improvements → document

### Finance (CFO/CMO)
Monetization strategies, financial modeling, marketing plans.
- Monetization review: analyze models → estimate pricing → propose revenue strategy
- Marketing plan: identify channels → create messaging → define timeline

## Service Manager Orchestration

Manage service groups, dependencies, and parallel health checks on the dr.eamer.dev server.

### Quick Commands
```bash
sm status              # View all services
sm start <service>     # Start single service
sm stop <service>      # Stop single service
sm restart <service>   # Restart service
sm logs <service>      # View logs
sm health <service>    # Check health endpoint
```

### Service Groups

| Group | Services | Ports |
|-------|----------|-------|
| AI Stack | swarm, studio, storyblocks | 5001, 5413, 8000 |
| Content | lessonplanner, clinical | 4108, 5015 |
| Core | coca, wordblocks, luke | 3034, 8847, 5211 |
| Dev Tools | firehose, skymarshal | 5056, 5050 |

### Dependency Ordering
```
studio → depends on → swarm (for orchestration)
lessonplanner → depends on → swarm (for generation)
```
Start dependencies first, stop dependents before dependencies.

### Orchestration Patterns
```bash
# Start group in dependency order
sm start swarm && sm start studio && sm start storyblocks

# Parallel start (independent services)
sm start swarm & sm start studio & sm start storyblocks & wait

# Health check all
for service in swarm studio lessonplanner coca; do sm health $service; done

# Restart with verification
sm stop <service> && sleep 2 && sm start <service> && sm health <service>
```

## Authentication

All API endpoints require authentication:
```bash
export GEEPERS_API_KEY=your_api_key_here   # DREAMER_API_KEY also accepted
```

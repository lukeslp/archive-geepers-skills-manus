# geepers-skills (Manus)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Platform: Manus](https://img.shields.io/badge/platform-Manus-teal.svg)
![Skills: 35](https://img.shields.io/badge/skills-35-brightgreen.svg)

35 skills for planning, building, shipping, and researching — packaged for the Manus runtime.

Part of the [geepers](https://github.com/lukeslp/geepers) ecosystem — [PyPI](https://pypi.org/project/geepers-llm/) · [MCP servers](https://github.com/lukeslp/geepers-kernel) · [Claude Code](https://github.com/lukeslp/geepers-skills) · [Codex CLI](https://github.com/lukeslp/geepers-gpt) · [Gemini](https://github.com/lukeslp/geepers-gemini) · [ClawHub](https://github.com/lukeslp/geepers-api-skills) · [beltalowda](https://github.com/lukeslp/beltalowda)

## Install

Import individual skills via Manus Settings > Skills > Import from GitHub, or copy the `skills/` directory to your Manus skill path.

## What's Included

**Orchestration**
- `geepers-team` — routes any request to the right specialist
- `geepers-executive`, `geepers-engineering`, `geepers-finance` — domain-specific orchestration
- `geepers-dream-swarm`, `geepers-swarm`, `geepers-mcp` — parallel multi-agent workflows
- `geepers-orchestrate` — multi-agent Dream Cascade and Dream Swarm orchestration
- `sm-orchestrate` — service manager orchestration for dr.eamer.dev

**Planning & Building**
- `geepers-planner` — breaks down tasks and sequences work
- `geepers-builder` — executes implementation plans
- `geepers-scout` / `scout` — fast project reconnaissance and quick wins
- `geepers-quality` / `quality-audit` — parallel a11y, perf, security, and dep checks
- `geepers-testing` — test strategy and implementation
- `geepers-validate` — comprehensive project validation

**Dev Tools**
- `geepers-git` — repo cleanup and artifact hygiene
- `geepers-deploy` — deploy and manage services on dr.eamer.dev
- `session-start` — bootstrap development sessions with startup rituals
- `session-end` — end sessions with commits and checkpoints

**Research & Data**
- `geepers-fetch` / `data-fetch` — pulls from 17+ structured APIs (Census, arXiv, GitHub, NASA, etc.)
- `geepers-data` — aggregated data API access
- `geepers-corpus` — COCA corpus linguistics
- `geepers-etymology` — historical linguistics and etymology
- `geepers-llm` — unified access across multiple model providers
- `swarm` — parallel research at scale using Manus map tool

**Visualization & Content**
- `geepers-datavis` / `datavis` — D3.js and Chart.js visualization workflows
- `data-artist` — beautiful visualizations with mathematical elegance
- `docs` — documentation generation and technical writing
- `humanize` — remove AI writing indicators from prose
- `ux-journey` — comprehensive UX analysis

**Product**
- `geepers-product` — PRD generation and product planning

## Ecosystem

- **Python**: [`geepers-llm`](https://pypi.org/project/geepers-llm/) · [`geepers-kernel`](https://pypi.org/project/geepers-kernel/)
- **MCP servers**: [`geepers-unified` · `geepers-providers` · `geepers-data` · `geepers-websearch`](https://github.com/lukeslp/geepers-kernel)
- **Orchestration**: [beltalowda](https://github.com/lukeslp/beltalowda) · [multi-agent-orchestration](https://github.com/lukeslp/multi-agent-orchestration)
- **Claude Code**: [geepers-skills](https://github.com/lukeslp/geepers-skills)
- **Codex CLI**: [geepers-gpt](https://github.com/lukeslp/geepers-gpt)
- **Gemini**: [geepers-gemini](https://github.com/lukeslp/geepers-gemini)
- **ClawHub**: [geepers-api-skills](https://github.com/lukeslp/geepers-api-skills)

## Author

**Luke Steuber**
- [lukesteuber.com](https://lukesteuber.com)
- [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com) on Bluesky

## License

MIT

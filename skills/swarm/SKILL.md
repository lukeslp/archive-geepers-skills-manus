---
name: swarm
description: "Parallel research and data gathering at scale using Manus's map tool. Use when: researching complex topics from multiple angles, gathering information across many entities in parallel, conducting competitive analysis, collecting data from multiple sources simultaneously, or any task that benefits from throwing many parallel workers at a problem."
---

# Swarm

Launch massively parallel research and data-gathering operations using Manus's `map` tool, which can spawn up to 2,000 independent subtasks simultaneously. Each subtask runs in its own sandbox with full internet access, search capabilities, and browser automation.

## When to Use Swarm

Use this skill whenever a task can be decomposed into independent, similarly-structured subtasks. The key question is: "Can I describe what I need as the same operation applied to N different inputs?"

**Strong fits:** Research N companies, gather data on N topics, analyze N URLs, compare N products, collect information about N people, audit N repositories.

**Poor fits:** Sequential tasks where step 2 depends on step 1's output, tasks requiring shared state between workers, single deep-dive research on one topic.

## Architecture

Swarm operates in three phases:

1. **Decompose** — Break the research question into independent facets, angles, or entities. Each becomes one subtask input.
2. **Dispatch** — Use the `map` tool to launch all subtasks in parallel. Each subtask gets a prompt template and one input from the list.
3. **Synthesize** — Aggregate the returned structured data into a unified report, resolving conflicts and identifying cross-cutting themes.

## Decomposition Strategies

### By Entity
Research the same question across many subjects.

**Example:** "Research the AI strategy of each Fortune 10 company"
- Inputs: `["Apple", "Microsoft", "Amazon", "Alphabet", "Meta", "Berkshire Hathaway", "UnitedHealth", "JPMorgan", "Johnson & Johnson", "Visa"]`
- Prompt: `"Research {{input}}'s AI strategy, investments, and recent announcements. Find their key AI products, R&D spending, and strategic partnerships."`

### By Facet
Research one topic from many different angles.

**Example:** "Comprehensive research on WebAssembly"
- Inputs: `["WebAssembly performance benchmarks vs JavaScript", "WebAssembly adoption in production systems 2024-2025", "WebAssembly security model and sandboxing", "WebAssembly outside the browser WASI serverless edge", "WebAssembly language support Rust Go Python compilation", "WebAssembly component model and interface types"]`
- Prompt: `"Research the following aspect of WebAssembly: {{input}}. Find recent developments, key players, benchmarks, and expert opinions. Cite sources."`

### By Source Type
Gather information from different source categories.

**Example:** "Research quantum computing readiness"
- Inputs: `["academic papers on quantum computing breakthroughs 2024-2025", "industry reports on quantum computing market size and forecasts", "government policy and funding for quantum computing programs", "startup landscape in quantum computing and recent funding rounds", "open source quantum computing frameworks and developer adoption"]`
- Prompt: `"Search for and summarize: {{input}}. Provide key findings, notable sources, and quantitative data where available."`

### By URL
Process a known list of URLs or resources.

**Example:** "Analyze competitor landing pages"
- Inputs: list of URLs
- Prompt: `"Visit {{input}} and analyze: value proposition, pricing model, target audience, key features, design quality, and calls to action."`

## Output Schema Design

Every swarm needs a consistent output schema so results can be aggregated. Design fields that capture the essential information each subtask should return.

**Good schema design principles:**
- Include a `summary` field (string) for the main finding
- Include a `confidence` field (string: "high", "medium", "low") so the synthesizer can weight results
- Include a `sources` field (string) for citation URLs
- Use `number` type for quantitative data that will be compared across results
- Use `file` type if subtasks produce documents or images that need to be collected

**Example schema for company research:**
```json
[
  {"name": "company", "type": "string", "title": "Company", "description": "Company name", "format": "Exact company name, e.g. 'Apple Inc.'"},
  {"name": "ai_strategy", "type": "string", "title": "AI Strategy", "description": "Summary of AI strategy and key initiatives", "format": "2-3 paragraph summary"},
  {"name": "ai_products", "type": "string", "title": "AI Products", "description": "Key AI products and services", "format": "Comma-separated list"},
  {"name": "rd_investment", "type": "string", "title": "R&D Investment", "description": "AI-related R&D spending or investment figures", "format": "Dollar amount with year, e.g. '$10B in 2024'"},
  {"name": "confidence", "type": "string", "title": "Confidence", "description": "Confidence in findings", "format": "high, medium, or low"},
  {"name": "sources", "type": "string", "title": "Sources", "description": "Source URLs", "format": "Newline-separated URLs"}
]
```

## Synthesis

After the map tool returns results, synthesize them into a coherent deliverable:

1. **Triage by confidence.** Weight high-confidence results more heavily. Flag low-confidence results for the user.
2. **Find cross-cutting themes.** What patterns appear across multiple subtask results? These are the most valuable insights.
3. **Resolve conflicts.** When subtasks return contradictory information, note the disagreement and cite both sources.
4. **Structure the output.** Organize by theme rather than by subtask input. The user wants insights, not a list of raw results.
5. **Cite sources.** Every factual claim in the synthesis should trace back to a source URL from the subtask results.

## Scaling Guidelines

| Subtask Count | Use Case | Notes |
|---------------|----------|-------|
| 5-10 | Focused comparison | Quick competitive analysis, small entity list |
| 10-50 | Broad research | Industry survey, multi-facet deep dive |
| 50-200 | Large-scale data gathering | Full market scan, extensive entity research |
| 200-2000 | Exhaustive collection | Scraping many pages, processing large datasets |

Start with fewer subtasks and scale up. Each subtask has its own sandbox and internet access, so there is real cost to over-decomposing. A good rule: if two subtasks would search for nearly identical information, merge them into one.

## Common Patterns

### Deep Research (Cascade Pattern)
For topics requiring depth, run two rounds: a broad first pass, then a targeted second pass based on findings.

**Round 1:** 5-8 subtasks covering major facets of the topic.
**Synthesis:** Identify gaps, surprises, and areas needing deeper investigation.
**Round 2:** 3-5 subtasks targeting the specific gaps identified in round 1.
**Final synthesis:** Merge both rounds into a comprehensive report.

### Competitive Intelligence
Research N competitors with identical prompts, then build a comparison matrix.

### Data Collection
Gather structured data from N sources, validate consistency, and merge into a single dataset.

### Multi-Source Verification
Research the same claim from N independent sources to assess reliability.

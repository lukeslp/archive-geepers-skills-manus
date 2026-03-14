---
name: research
description: >
  Data fetching, parallel research, and API access across 17+ sources. Includes
  universal data fetching (arXiv, Census, NASA, GitHub, PubMed, Wikipedia, news,
  finance, weather, and more), COCA corpus linguistics, word etymology and
  diachronic linguistics, multi-provider LLM access, and parallel swarm research
  using Manus map tool. Use for gathering data from authoritative sources,
  linguistic research, or large-scale parallel information gathering.
---

# Research

Fetch structured data from 17+ authoritative APIs, run parallel research at scale, and access specialized linguistic and LLM endpoints.

## Data Fetching (17 Sources)

Access structured data through the dr.eamer.dev API or directly via the DataFetchingFactory library.

### Authentication
```bash
export GEEPERS_API_KEY=your_api_key_here   # DREAMER_API_KEY also accepted
```

### Available Sources

| Source | ID | Best For |
|--------|-----|----------|
| arXiv | arxiv | Research papers, preprints |
| Semantic Scholar | semantic_scholar | Academic citations, papers |
| PubMed | pubmed | Medical/biomedical research |
| Census Bureau | census | US demographics, economic data |
| FEC | fec | Campaign finance |
| Judiciary | judiciary | Court records, cases |
| Wikipedia | wikipedia | General knowledge |
| News APIs | news | Current events (80+ outlets) |
| Archive.org | archive | Historical web content |
| GitHub | github | Repositories, code |
| YouTube | youtube | Video content, transcripts |
| NASA | nasa | Space, astronomy data |
| Wolfram Alpha | wolfram | Computational answers |
| Finance | finance | Stock prices, market data |
| Weather | weather | Weather forecasts |
| OpenLibrary | openlibrary | Books, authors |
| MyAnimeList | mal | Anime/manga data |

### API Endpoints
```bash
# List available sources
GET https://api.dr.eamer.dev/v1/data

# Search across sources
POST https://api.dr.eamer.dev/v1/data/search
{ "source": "arxiv", "query": "machine learning interpretability", "limit": 10 }
```

### MCP Server Tools
The data fetch MCP server exposes these tools:
- `dream_of_arxiv` — Search arXiv papers (query, max_results, category)
- `dream_of_census_acs` — US Census ACS data (year, variables, state, geography)
- `dream_of_weather` — Current weather (location)
- `dream_of_news` — News articles (query, category)
- `dream_of_github_repos` — GitHub repos (query, sort)

### Python Library Usage
```python
from data_fetching import DataFetchingFactory
factory = DataFetchingFactory()

# Single source
client = factory.create_client('arxiv')
results = await client.search("quantum computing", max_results=10)

# Multi-source parallel
import asyncio
sources = ['arxiv', 'wikipedia', 'news']
tasks = [factory.create_client(s).search(query) for s in sources]
results = await asyncio.gather(*tasks)
```

### Source Selection Guide

| Query Type | Recommended Sources |
|------------|---------------------|
| Academic research | arxiv, semantic_scholar, pubmed |
| Current events | news, wikipedia |
| Technical/code | github |
| Demographics | census |
| Historical | archive, wikipedia |
| Scientific facts | nasa, wolfram |
| Books/literature | openlibrary |

### CLI Scripts
```bash
scripts/fetch.py arxiv "quantum computing" --limit 10
scripts/fetch-arxiv.py "transformer architectures" --category cs.AI
```

## COCA Corpus Linguistics

Query the Corpus of Contemporary American English (1+ billion words from spoken, fiction, magazine, newspaper, and academic sources).

### Endpoints
```bash
# Concordance (keyword-in-context)
GET https://api.dr.eamer.dev/v1/corpus/search?word=serendipity&limit=20

# Collocations (statistically co-occurring words)
GET https://api.dr.eamer.dev/v1/corpus/collocations?word=run&pos=verb&limit=20

# Frequency (per million words, with genre filter)
GET https://api.dr.eamer.dev/v1/corpus/frequency?word=algorithm&genre=academic
```

Genres: `spoken`, `fiction`, `magazine`, `newspaper`, `academic`.

### When to Use
- Checking how formal or common a word is in real American English
- Finding natural collocations for writing assistance
- Linguistic research on word usage patterns
- Historical frequency trends across decades

## Etymology and Historical Linguistics

Word origins, sound changes, and language family exploration.

### Endpoints
```bash
# Word etymology (origin, root words, first known use)
GET https://api.dr.eamer.dev/v1/etymology/word?word=serendipity

# Full etymology chain with language family context
GET https://api.dr.eamer.dev/v1/etymology/explore?word=knight&lang=en

# Sound change rules between proto-languages and descendants
GET https://api.dr.eamer.dev/v1/etymology/sound-changes?from=proto-indo-european&to=english
```

### When to Use
- Researching word origins and historical meaning shifts
- Understanding cognates across related languages
- Exploring pronunciation changes over centuries
- Writing that benefits from etymological depth

## Multi-Provider LLM Access

Access 12 LLM providers through a single unified API.

### Endpoints
```bash
# Chat completion
POST https://api.dr.eamer.dev/v1/llm/chat
{ "model": "claude-sonnet-4-5-20250929", "messages": [...], "provider": "anthropic" }

# List models
GET https://api.dr.eamer.dev/v1/llm/models

# Vision (image analysis)
POST https://api.dr.eamer.dev/v1/llm/vision
{ "model": "...", "image_url": "...", "prompt": "Describe this image" }

# Image generation
POST https://api.dr.eamer.dev/v1/llm/image
{ "prompt": "A sunset over the ocean", "provider": "openai" }

# Text-to-speech
POST https://api.dr.eamer.dev/v1/llm/tts
{ "text": "Hello world", "voice": "alloy" }
```

Providers: `anthropic`, `openai`, `xai`, `mistral`, `cohere`, `gemini`, `perplexity`, `groq`, `huggingface`, `ollama`.

## Parallel Swarm Research (Manus Map Tool)

Launch massively parallel research using Manus's `map` tool (up to 2,000 independent subtasks, each with its own sandbox and internet access).

### When to Use Swarm
Use whenever a task can be decomposed into independent, similarly-structured subtasks. The key question: "Can I describe what I need as the same operation applied to N different inputs?"

**Strong fits**: Research N companies, gather data on N topics, analyze N URLs, compare N products, audit N repositories.

**Poor fits**: Sequential tasks where step 2 depends on step 1, tasks requiring shared state, single deep-dive on one topic.

### Decomposition Strategies

**By Entity**: Research the same question across many subjects.
- Inputs: list of company/person/product names
- Prompt: "Research {{input}}'s [specific aspect]. Find [specific data points]."

**By Facet**: Research one topic from many angles.
- Inputs: list of angles/aspects to investigate
- Prompt: "Research the following aspect of [topic]: {{input}}. Find recent developments and cite sources."

**By Source Type**: Gather from different source categories.
- Inputs: list of source-specific search queries
- Prompt: "Search for and summarize: {{input}}. Provide key findings and quantitative data."

**By URL**: Process a known list of URLs.
- Inputs: list of URLs
- Prompt: "Visit {{input}} and analyze: [specific criteria]."

### Output Schema Design
- Include `summary` (string) for main finding
- Include `confidence` (string: high/medium/low) for weighting
- Include `sources` (string) for citation URLs
- Use `number` type for quantitative comparisons
- Use `file` type if subtasks produce documents

### Synthesis Process
1. Triage by confidence (weight high-confidence results more)
2. Find cross-cutting themes across subtask results
3. Resolve conflicts (note disagreements, cite both sources)
4. Structure output by theme, not by subtask input
5. Cite sources for every factual claim

### Scaling Guidelines

| Subtask Count | Use Case |
|---------------|----------|
| 5-10 | Focused comparison, small entity list |
| 10-50 | Broad research, industry survey |
| 50-200 | Large-scale data gathering, market scan |
| 200-2000 | Exhaustive collection, processing large datasets |

### Deep Research (Cascade Pattern)
For topics requiring depth, run two rounds:
1. **Round 1**: 5-8 subtasks covering major facets
2. **Synthesis**: Identify gaps and areas needing deeper investigation
3. **Round 2**: 3-5 subtasks targeting specific gaps
4. **Final synthesis**: Merge both rounds into comprehensive report

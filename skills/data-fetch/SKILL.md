---
name: data-fetch
description: Fetch and aggregate data from 17 external APIs including Census, arXiv, NASA, Wikipedia, PubMed, and GitHub.
---

# Data Fetch

You are fetching and aggregating data from multiple external sources using the shared library's DataFetchingFactory. This skill provides access to 17 structured API clients.

## Available Data Sources

| Source | Client | Best For |
|--------|--------|----------|
| **Academic** | | |
| arXiv | `arxiv` | Research papers, preprints |
| Semantic Scholar | `semantic_scholar` | Academic citations, papers |
| PubMed | `pubmed` | Medical/biomedical research |
| **Government** | | |
| Census Bureau | `census` | Demographics, economic data |
| FEC | `fec` | Campaign finance |
| Judiciary | `judiciary` | Court records, cases |
| **Web/News** | | |
| Wikipedia | `wikipedia` | General knowledge |
| News APIs | `news` | Current events |
| Archive.org | `archive` | Historical web content |
| **Tech** | | |
| GitHub | `github` | Repositories, code |
| YouTube | `youtube` | Video content, transcripts |
| **Scientific** | | |
| NASA | `nasa` | Space, astronomy data |
| Wolfram Alpha | `wolfram` | Computational answers |
| **Other** | | |
| Finance | `finance` | Stock data, markets |
| Weather | `weather` | Weather forecasts |
| OpenLibrary | `openlibrary` | Books, authors |
| MyAnimeList | `myanimelist` | Anime/manga data |

## Execution Strategy

### Single Source Query
```python
from data_fetching import DataFetchingFactory
factory = DataFetchingFactory()
client = factory.create_client('arxiv')
results = await client.search("quantum computing", max_results=10)
```

### Multi-Source Aggregation (PARALLEL)
```python
import asyncio
sources = ['arxiv', 'wikipedia', 'news']
tasks = [factory.create_client(s).search(query) for s in sources]
results = await asyncio.gather(*tasks)
```

## Source Selection Guide

| Query Type | Recommended Sources |
|------------|---------------------|
| Academic research | arxiv, semantic_scholar, pubmed |
| Current events | news, wikipedia |
| Technical/code | github, stackoverflow |
| Demographics | census |
| Historical | archive, wikipedia |
| Scientific facts | nasa, wolfram |
| Books/literature | openlibrary |

## Output Format

```
📊 DATA FETCH RESULTS

Query: {query}
Sources: {sources_used}
Date: {timestamp}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          SOURCE: {source_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Results: {count}

1. {title}
   - {metadata}
   - URL: {url}

2. {title}
   ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           AGGREGATED INSIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cross-Source Themes:
1. {theme} - Found in: {sources}
2. {theme} - Found in: {sources}

Conflicts/Discrepancies:
- {source1} says X, {source2} says Y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              CITATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] {citation}
[2] {citation}
```

## Integration with Orchestrators

For complex research, combine with orchestration:

```
/data-fetch → provides raw data
    ↓
DreamCascade → synthesizes findings
    ↓
/data-artist → visualizes results
```

## Key Principles

1. **Parallel fetching** - Query multiple sources simultaneously
2. **Source attribution** - Always cite data origins
3. **Deduplication** - Merge overlapping results
4. **Rate limiting** - Respect API limits per client
5. **Caching** - Use MCP cache for repeated queries

## Common Workflows

```
# Census demographics
/data-fetch census "housing prices by county"

# Academic research
/data-fetch arxiv,pubmed "CRISPR gene editing"

# Tech exploration
/data-fetch github "machine learning frameworks" --stars >1000

# Current events
/data-fetch news,wikipedia "climate summit 2026"
```

## Related Skills

- `/data-artist` - Visualize fetched data beautifully
- `/quality-audit` - Verify data quality and validate findings

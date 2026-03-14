---
name: docs
description: "Documentation generation and technical writing skill. Use when: creating README files, writing API documentation, generating code documentation (Python docstrings, JSDoc), building user guides, producing architecture overviews, or improving existing documentation quality."
---

# Documentation Generator

Generate clear, task-oriented documentation for projects, APIs, and code. Covers READMEs, API references, inline docs, architecture overviews, and user guides.

## Principles

Write for the reader's skill level. Focus on what users want to accomplish, not what the code does internally. Show examples before explaining theory. Keep documentation scannable with headers, tables, and code blocks. Stale docs are worse than no docs — scope documentation to what will be maintained.

## Workflow

Determine the documentation type needed, then follow the appropriate section below:

**Creating new documentation?** Start with the matching template and adapt to the project.
**Improving existing docs?** Audit against the quality checklist at the bottom, then fix gaps.

## README.md

A README is the front door. Structure it for someone who has never seen the project:

```markdown
# Project Name

One sentence: what it does and who it's for.

## Quick Start

\`\`\`bash
npm install project-name
npx project-name init
\`\`\`

## Features

| Feature | Description |
|---------|-------------|
| Auth | JWT-based authentication with refresh tokens |
| API | REST endpoints with OpenAPI spec |

## Configuration

| Variable | Purpose | Default |
|----------|---------|---------|
| `PORT` | Server port | `3000` |
| `DB_URL` | Database connection string | Required |

## Usage

[Most common use case with working code example]

## API Reference

Brief overview here, link to detailed docs if they exist.

## Contributing

[How to set up dev environment, run tests, submit PRs]

## License

MIT
```

Adapt sections to the project. A CLI tool needs a "Commands" section. A library needs "Installation" and "API" sections. A web app needs "Deployment" instructions.

## API Documentation

Document every endpoint with parameters, response shape, and error codes:

```markdown
## `GET /api/users/:id`

Retrieve a user by ID.

**Parameters:**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| `id` | path | string | yes | User UUID |
| `fields` | query | string | no | Comma-separated field list |

**Response `200`:**
\`\`\`json
{
  "id": "abc-123",
  "name": "Jane Doe",
  "email": "jane@example.com"
}
\`\`\`

**Errors:**

| Status | Code | Description |
|--------|------|-------------|
| 404 | `USER_NOT_FOUND` | No user with this ID |
| 401 | `UNAUTHORIZED` | Missing or invalid token |
```

For OpenAPI/Swagger specs, generate from code annotations when possible rather than maintaining a separate spec file.

## Code Documentation

### Python (docstrings)

Use Google-style docstrings. Document parameters, return values, exceptions, and include a usage example for non-obvious functions:

```python
def fetch_records(query: str, limit: int = 100) -> list[Record]:
    """Fetch records matching a search query.

    Args:
        query: Search string, supports wildcards with *.
        limit: Maximum records to return. Capped at 1000.

    Returns:
        List of matching Record objects, sorted by relevance.

    Raises:
        ConnectionError: When the database is unreachable.
        ValueError: When query is empty or limit < 1.

    Example:
        >>> records = fetch_records("user:jane*", limit=10)
        >>> len(records)
        3
    """
```

### TypeScript / JavaScript (JSDoc)

```typescript
/**
 * Fetch records matching a search query.
 *
 * @param query - Search string, supports wildcards with `*`
 * @param options - Optional configuration
 * @param options.limit - Max records to return (default: 100, max: 1000)
 * @returns Matching records sorted by relevance
 * @throws {ConnectionError} When the database is unreachable
 *
 * @example
 * const records = await fetchRecords("user:jane*", { limit: 10 });
 */
```

## Architecture Overview

For complex projects, create an architecture document that answers: what are the major components, how do they communicate, and where does data flow?

```markdown
# Architecture

## System Overview

[One paragraph describing the system's purpose and boundaries]

## Components

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| API Gateway | Request routing, auth | Express + JWT |
| Worker | Background jobs | Bull + Redis |
| Database | Persistent storage | PostgreSQL |

## Data Flow

1. Client sends request to API Gateway
2. Gateway validates JWT, routes to handler
3. Handler queries Database or enqueues Worker job
4. Response returns to client (sync) or via webhook (async)

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| PostgreSQL over MongoDB | Relational data with complex joins |
| Bull over SQS | Self-hosted, no AWS dependency |
```

## Output Formats

Manus can produce documentation in multiple formats. Choose based on the audience:

| Format | Best For | How |
|--------|----------|-----|
| Markdown | GitHub repos, developer docs | Write `.md` files directly |
| HTML | Hosted documentation sites | Build with web dev tools |
| PDF | Formal deliverables, reports | Use `manus-md-to-pdf` utility |

## Quality Checklist

Before delivering documentation, verify:

- Every code example runs without modification
- All links resolve to valid targets
- Configuration variables list actual defaults, not placeholders
- The reader can go from zero to working in under 5 minutes with Quick Start
- Technical terms are defined on first use
- No stale references to removed features or old APIs
- Tables are used for structured comparisons, not buried in prose

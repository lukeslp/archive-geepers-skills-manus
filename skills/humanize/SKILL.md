---
name: humanize
description: "Remove AI writing indicators from documentation and prose. Use when: cleaning up AI-generated text before publishing, making documentation sound more human, removing em-dashes, corporate jargon, passive voice, hedge phrases, or converting 'we' to 'I' for solo developer contexts."
---

# Humanize

Detect and remove AI writing indicators from documentation and prose. Transforms AI-generated text into natural, human-sounding writing while preserving technical accuracy.

## Quick Start

### Scan a file for AI indicators
```bash
python3 /home/ubuntu/skills/humanize/scripts/detect.py README.md
```

### Auto-fix high-confidence issues
```bash
python3 /home/ubuntu/skills/humanize/scripts/detect.py README.md --fix
```

### Scan an entire docs directory
```bash
python3 /home/ubuntu/skills/humanize/scripts/detect.py docs/ --recursive
```

### Get JSON report for programmatic use
```bash
python3 /home/ubuntu/skills/humanize/scripts/detect.py README.md --json
```

## Detection Patterns

The detector identifies 15 categories of AI writing indicators, each with a confidence score that determines whether to auto-fix, suggest, or flag for review.

| Pattern | Confidence | Action | Example |
|---------|-----------|--------|---------|
| AI attribution | 1.00 | Auto-fix | "Claude generated this" → remove |
| Em-dashes | 0.95 | Auto-fix | "critical—and important—feature" → commas |
| Redundancy | 0.95 | Auto-fix | "advance planning" → "planning" |
| Corporate jargon | 0.90 | Auto-fix | "leverage" → "use" |
| Buzzword clusters | 0.90 | Auto-fix | 3+ buzzwords in one sentence |
| Stiff construction | 0.90 | Auto-fix | "It is important to note that" → remove |
| We→I conversion | 0.90 | Suggest | "We implemented" → "I implemented" |
| Passive voice | 0.85 | Suggest | "is processed by" → active voice |
| Formal metadata | 0.85 | Suggest | "This document provides" → remove |
| Hedge phrases | 0.80 | Suggest | "might potentially" → be direct |
| Acronym expansion | 0.80 | Suggest | "JWT" → "JSON Web Tokens (JWT)" |
| Transition phrases | 0.75 | Suggest | "Furthermore," → remove or simplify |
| Excessive dates | 0.75 | Flag | Timestamps in narrative prose |
| Over-structuring | 0.70 | Flag | Numbered lists for 2-3 items |

**Confidence thresholds:** >= 0.90 auto-fix, 0.70-0.89 suggest with preview, < 0.70 flag for human review.

## Workflow

### Phase 1: Scan

Run the detector on target files. It skips code blocks, frontmatter, headings, and table rows automatically. The output groups findings by category and shows before/after previews.

### Phase 2: Fix

**Auto-fix** applies to high-confidence patterns where the replacement is unambiguous. The script preserves leading whitespace and line structure. Use `--output` to write to a new file instead of overwriting.

**Manual review** is needed for suggestions and flags. For each suggestion, the report shows the line number, matched pattern, and proposed fix. Apply judgment — not every passive voice sentence needs rewriting, and some "we" usage is intentional.

### Phase 3: Verify

After fixing, re-run the detector to confirm the count dropped. Read the output to make sure meaning was preserved. Technical specifications, API schemas, and code examples should never be modified.

## Jargon Replacement Dictionary

When manually humanizing text beyond what the script catches, use these replacements:

| AI Buzzword | Plain Alternative |
|-------------|-------------------|
| leverage | use |
| utilize | use |
| robust | reliable, strong |
| seamless | smooth |
| ecosystem | system, tools |
| paradigm | approach |
| synergy | cooperation |
| innovative | new |
| cutting-edge | modern |
| empower | enable, help |
| holistic | complete |
| optimize | improve |
| scalable | flexible, can grow |
| streamline | simplify |
| facilitate | help |
| delve | explore |
| actionable | practical |
| impactful | effective |

## Rules

1. **Never change meaning.** Preserve intent, facts, and technical accuracy.
2. **Never modify code blocks.** Code examples, configs, and commands are untouched.
3. **Never remove real attribution.** Only remove AI attribution ("Claude", "the assistant").
4. **Always preview changes.** Show before/after diffs for transparency.
5. **Always back up first.** Copy originals before bulk operations.
6. **Context matters for we→I.** Keep "we" in team docs, user instructions ("we recommend"), and inclusive language. Convert only in solo developer contexts.

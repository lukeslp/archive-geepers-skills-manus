---
name: datavis
description: "Data visualization skill for creating interactive, accessible, and mathematically sound visualizations. Use when: building D3.js or Chart.js visualizations, designing color palettes, choosing scales and encodings, analyzing data distributions, creating data pipelines, crafting narrative-driven data stories, or generating charts with plotly/matplotlib/seaborn."
---

# Data Visualization

Create interactive, accessible, and mathematically sound data visualizations. Supports D3.js (web), Chart.js, plotly, matplotlib, and seaborn.

## Philosophy

Every visualization should reveal truth through data, evoke wonder through design, respect the viewer through accessibility, and honor complexity through elegant simplification.

## Quick Start

### Scaffold a D3.js Project
```bash
python3 /home/ubuntu/skills/datavis/scripts/d3-scaffold.py my-viz --type force-network --single-file
```
Templates: `force-network`, `timeline`, `choropleth`, `bar-race`, `treemap`, `sankey`, `radial-tree`, `bubble-chart`. See `references/gallery.md` for data formats.

### Analyze a Dataset's Distribution
```bash
python3 /home/ubuntu/skills/datavis/scripts/analyze-distribution.py data.csv --column population
```
Outputs statistics, recommended D3 scale, and ready-to-use code.

### Generate a Color Palette
```bash
python3 /home/ubuntu/skills/datavis/scripts/color-palette.py --type sequential --hue blue --steps 7
```
Types: `sequential`, `diverging`, `categorical`, `colorblind-safe`.

## Scale Selection

| Scale | Use When | Example |
|-------|----------|---------|
| Linear | Evenly distributed data | Temperature, scores |
| Log | Multiple orders of magnitude | Population (100 to 1B) |
| Sqrt | Encoding area (circles, bubbles) | Bubble chart radius |
| Symlog | Data crossing zero with wide range | Profit/loss |
| Time | Temporal axis | Date series |

Area scales with the square of radius. Always use `d3.scaleSqrt()` for bubble/circle size encoding to maintain perceptual accuracy.

## Color Design

**Palette types and when to use them:**

| Type | Purpose | Max Items |
|------|---------|-----------|
| Categorical | Distinct groups, nominal data | 8 |
| Sequential | Ordered magnitude, single variable | 9 |
| Diverging | Two extremes around a midpoint | 11 |

**Colorblind-safe default palette (8 colors):**
```javascript
const palette = ['#332288','#117733','#44AA99','#88CCEE','#DDCC77','#CC6677','#AA4499','#882255'];
```

Always use redundant encoding. Never rely on color alone; pair with shape, pattern, or label.

## D3.js Patterns

**Responsive SVG:**
```javascript
const svg = d3.select('#chart').append('svg')
  .attr('viewBox', `0 0 ${width} ${height}`)
  .attr('preserveAspectRatio', 'xMidYMid meet');
```

**Force simulation:**
```javascript
const sim = d3.forceSimulation(nodes)
  .force('charge', d3.forceManyBody().strength(-300))
  .force('link', d3.forceLink(links).id(d => d.id))
  .force('center', d3.forceCenter(width/2, height/2))
  .force('collision', d3.forceCollide().radius(d => d.r + 2));
```

**Touch-friendly targets** (minimum 44x44px):
```javascript
node.append('circle').attr('class','hit-area')
  .attr('r', Math.max(actualRadius, 22)).attr('fill','transparent');
```

## Python Visualization (plotly, matplotlib, seaborn)

These libraries are pre-installed in the sandbox. Use them for quick static or interactive charts:

```python
import plotly.express as px
fig = px.scatter(df, x="gdp", y="life_exp", size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=60)
fig.write_html("scatter.html")
```

For static images when web output is not needed:
```python
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df, x="category", y="value", ax=ax)
plt.savefig("chart.png", dpi=150, bbox_inches="tight")
```

## Narrative Structure

Build visualizations in three acts:

1. **Invitation** — What draws the viewer in? A striking number, a question, a visual hook.
2. **Discovery** — What patterns emerge through interaction? Tooltips, filters, zoom.
3. **Reflection** — What should the viewer understand or feel? Summary, call to action.

Use progressive disclosure: Overview first, then exploration, then detail-on-demand.

## Data Pipeline

When building from raw data, follow this sequence:

1. **Fetch** — Collect from APIs or files, cache raw responses.
2. **Clean** — Handle missing values, normalize formats, deduplicate.
3. **Validate** — Run `analyze-distribution.py`, check for outliers, verify ranges.
4. **Transform** — Apply scales, aggregations, joins.
5. **Export** — Output as JSON for D3 or DataFrame for plotly/matplotlib.

Document every dataset: source URL, access date, license, field descriptions, known limitations.

## Quality Checklist

Before delivering any visualization, verify:

- Scale choice is justified for the data distribution
- Color palette is colorblind-safe (test with simulator)
- Touch targets are at least 44x44px
- Viewer has a clear entry point (title, subtitle, annotation)
- All data sources are documented
- Visualization is responsive on mobile
- Hover/click interactivity is present
- Error states are handled (missing data, failed loads)

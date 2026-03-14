---
name: visualization
description: >
  Data visualization, color design, UX analysis, and narrative-driven data
  storytelling. Includes D3.js scaffolding, Chart.js, plotly, matplotlib, seaborn,
  color palette generation, distribution analysis, perceptual encoding, force
  networks, timelines, choropleths, and comprehensive UX journey analysis. Use
  when building visualizations, designing color palettes, analyzing data
  distributions, or evaluating user experience.
---

# Visualization

Create beautiful, mathematically elegant, accessible data visualizations and conduct comprehensive UX analysis.

## Quick Start

### Scaffold a D3.js project
```bash
python3 scripts/d3-scaffold.py my-viz --type force-network --single-file
```
Templates: `force-network`, `timeline`, `choropleth`, `bar-race`, `treemap`, `sankey`, `radial-tree`, `bubble-chart`. See `references/gallery.md` for data formats.

### Analyze a dataset's distribution
```bash
python3 scripts/analyze-distribution.py data.csv --column population
```
Outputs statistics, recommended D3 scale, and ready-to-use code.

### Generate a color palette
```bash
python3 scripts/color-palette.py --type sequential --hue blue --steps 7
```
Types: `sequential`, `diverging`, `categorical`, `colorblind-safe`.

### Generate a visualization from data
```bash
python3 scripts/viz-generator.py data.json --template sankey
python3 scripts/viz-generator.py data.csv --template bar-race
```

## Philosophy: "Data is Beautiful"

Every visualization should reveal truth through data, evoke wonder through design, respect the viewer through accessibility, and honor complexity through elegant simplification.

### What Makes Data Beautiful
- **Clarity** — The data speaks without distortion
- **Proportion** — Visual weight matches data importance
- **Rhythm** — Patterns emerge naturally from the encoding
- **Surprise** — Reveals insights not obvious in raw numbers
- **Humanity** — Connects data to human experience

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

### Palette Types

| Type | Purpose | Max Items |
|------|---------|-----------|
| Categorical | Distinct groups, nominal data | 8 |
| Sequential | Ordered magnitude, single variable | 9 |
| Diverging | Two extremes around a midpoint | 11 |

### Colorblind-Safe Default Palette (8 colors)
```javascript
const palette = ['#332288','#117733','#44AA99','#88CCEE','#DDCC77','#CC6677','#AA4499','#882255'];
```

### Signature Palettes
```css
/* Elegant Sequential */
--seq: #F7FBFF → #DEEBF7 → #9ECAE1 → #4292C6 → #084594

/* Thoughtful Diverging */
--div: #B2182B (negative) → #F7F7F7 (neutral) → #2166AC (positive)

/* Accessible Categorical */
--cat: #1B9E77, #D95F02, #7570B3, #E7298A, #66A61E
```

Always use redundant encoding. Never rely on color alone; pair with shape, pattern, or label.

## Visual Encoding Hierarchy

| Encoding | Accuracy | Best For |
|----------|----------|----------|
| Position | Most accurate | Comparison, trends |
| Length/height | Good | Bar charts, rankings |
| Angle/slope | Moderate | Rates of change |
| Area | Requires sqrt scaling | Proportional symbols |
| Color intensity | Least precise | Heatmaps, density |

## D3.js Patterns

### Responsive SVG
```javascript
const svg = d3.select('#chart').append('svg')
  .attr('viewBox', `0 0 ${width} ${height}`)
  .attr('preserveAspectRatio', 'xMidYMid meet');
```

### Force Simulation
```javascript
const sim = d3.forceSimulation(nodes)
  .force('charge', d3.forceManyBody().strength(-300))
  .force('link', d3.forceLink(links).id(d => d.id))
  .force('center', d3.forceCenter(width/2, height/2))
  .force('collision', d3.forceCollide().radius(d => d.r + 2));
```

### Touch-Friendly Targets (44x44px minimum)
```javascript
node.append('circle').attr('class','hit-area')
  .attr('r', Math.max(actualRadius, 22)).attr('fill','transparent');
```

## Python Visualization

Pre-installed in the sandbox: plotly, matplotlib, seaborn.

```python
# Interactive (plotly)
import plotly.express as px
fig = px.scatter(df, x="gdp", y="life_exp", size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=60)
fig.write_html("scatter.html")

# Static (matplotlib + seaborn)
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

Progressive disclosure: Overview first, then exploration, then detail-on-demand.

### Metaphor Selection
- Timelines: rivers, journeys
- Networks: galaxies, ecosystems
- Proportions: physical objects, scale comparisons
- Change: growth, transformation

## Visualization Types

| Type | Best For | Avoid When |
|------|----------|------------|
| Bar Chart | Comparing categories | Too many categories (>12) |
| Line Chart | Trends over time | Discrete, unordered data |
| Scatter Plot | Relationships | Overplotting (use density) |
| Pie Chart | Part-of-whole (few) | >5 segments |
| Treemap | Hierarchical proportions | Deep hierarchies |
| Force Network | Relationships | >100 nodes without clustering |
| Choropleth | Geographic patterns | Unequal area regions |
| Timeline | Temporal events | Too many overlapping events |
| Sankey | Flow between categories | Too many nodes |

## Anti-Patterns
- 3D effects that distort perception
- Truncated axes that exaggerate differences
- Rainbow color scales (not perceptually uniform)
- Dual Y-axes (confusing comparisons)
- Pie charts for comparison across groups
- Chartjunk (unnecessary decoration)

## Data Pipeline

1. **Fetch** — Collect from APIs or files, cache raw responses
2. **Clean** — Handle missing values, normalize formats, deduplicate
3. **Validate** — Run `analyze-distribution.py`, check for outliers
4. **Transform** — Apply scales, aggregations, joins
5. **Export** — JSON for D3, DataFrame for plotly/matplotlib

Document every dataset: source URL, access date, license, field descriptions, limitations.

## UX Journey Analysis

Comprehensive user experience evaluation combining design, accessibility, and engagement.

### Design System Review
- Grid systems and mathematical precision
- Typography hierarchy (size, weight, color)
- Whitespace and rhythm
- Color application (purposeful, not decorative)
- Consistency across components
- Natural eye flow and clear importance hierarchy

### Accessibility Review (WCAG 2.1 AA)
- Keyboard navigation
- Screen reader support
- Touch targets (44x44px minimum)
- Color independence
- Motion sensitivity (prefers-reduced-motion)
- Cognitive accessibility

### Engagement Analysis
- Core loop: fundamental interaction pattern, progression, satisfaction
- Feedback systems: immediate, satisfying, multi-modal
- Reward structures: frequency, variety, intrinsic/extrinsic balance

### User Flow Analysis
- Navigation clarity
- Form interactions
- Error handling and recovery
- Loading states and feedback
- Mobile considerations

## Quality Checklist

- Scale choice justified for data distribution
- Color palette is colorblind-safe (test with simulator)
- Touch targets at least 44x44px
- Clear entry point for viewer
- Sources documented
- Responsive on mobile
- Hover/click interactivity present
- Error states handled

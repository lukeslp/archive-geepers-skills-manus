---
name: data-artist
description: Create beautiful data visualizations with mathematical elegance, color theory, and narrative design - the "Data is Beautiful" aesthetic.
---

# Data Artist

You are creating a work of data art. This skill brings together mathematical elegance, emotional resonance, narrative design, and technical excellence to transform raw data into something beautiful that tells a story and moves the viewer.

## The "Data is Beautiful" Philosophy

### Core Principles

1. **Life is Beautiful** - Data visualization should reveal the wonder in information
2. **Mathematical Elegance** - Perceptually accurate encodings, thoughtful scales
3. **Emotional Resonance** - Create moments of awe, reflection, insight
4. **Swiss Minimalism** - Clean geometry, purposeful color, no chartjunk
5. **Narrative Journey** - Guide the viewer through a story

### What Makes Data Beautiful

- **Clarity** - The data speaks clearly without distortion
- **Proportion** - Visual weight matches data importance
- **Rhythm** - Patterns emerge naturally from the encoding
- **Surprise** - Reveals insights not obvious in raw numbers
- **Humanity** - Connects data to human experience

## Visualization Domains

### 1. Mathematical Foundations (@geepers_datavis_math)

**Scale Selection:**
- Linear for comparison
- Log for orders of magnitude
- Sqrt for area perception
- Time scales for temporal data

**Visual Encoding:**
- Position (most accurate)
- Length/height (good)
- Angle/slope (moderate)
- Area (requires sqrt scaling)
- Color intensity (least precise)

**Perceptual Accuracy:**
- Ensure encodings don't mislead
- Account for human perception biases
- Use perceptually uniform color scales

### 2. Color Design (@geepers_datavis_color)

**Palette Types:**
- Sequential: Low → High (single hue)
- Diverging: Negative ↔ Neutral ↔ Positive
- Categorical: Distinct groups (max 7-9)

**Color Principles:**
- Perceptual uniformity (Lab/HCL color space)
- Colorblind accessibility (avoid red-green only)
- Emotional resonance (warm/cool, muted/vibrant)
- Cultural considerations

**Signature Palettes:**
```css
/* Elegant Sequential */
--seq-1: #F7FBFF;
--seq-2: #DEEBF7;
--seq-3: #9ECAE1;
--seq-4: #4292C6;
--seq-5: #084594;

/* Thoughtful Diverging */
--div-neg: #B2182B;
--div-neutral: #F7F7F7;
--div-pos: #2166AC;

/* Accessible Categorical */
--cat-1: #1B9E77;
--cat-2: #D95F02;
--cat-3: #7570B3;
--cat-4: #E7298A;
--cat-5: #66A61E;
```

### 3. Narrative Design (@geepers_datavis_story)

**Story Arc:**
1. **Hook** - What draws the viewer in?
2. **Context** - Why does this matter?
3. **Journey** - Guide through the data
4. **Insight** - The "aha" moment
5. **Reflection** - What does it mean?

**Emotional Calibration:**
- What emotion should viewers feel?
- How do we honor the subject matter?
- Where are moments of wonder/pause/reflection?

**Metaphor Selection:**
- Timelines → Rivers, journeys
- Networks → Galaxies, ecosystems
- Proportions → Physical objects, scale comparisons
- Change → Growth, transformation

### 4. Technical Implementation (@geepers_datavis_viz)

**Tools:**
- D3.js for custom visualizations
- Chart.js for standard charts
- SVG for crisp, scalable graphics
- Canvas for high-performance rendering

**Interaction Patterns:**
- Hover for details
- Click for drill-down
- Drag for exploration
- Scroll for revelation

**Responsive Design:**
- Mobile-first
- Touch-friendly interactions
- Graceful degradation

### 5. Data Integrity (@geepers_datavis_data)

**Source Verification:**
- Cite authoritative sources
- Document methodology
- Note limitations/caveats

**Data Pipeline:**
- Clean, validated data
- Reproducible transformations
- Cached appropriately

## Execution Strategy

**For a new visualization, launch in PARALLEL:**

```
1. @geepers_datavis_story - Define narrative arc and emotional journey
2. @geepers_datavis_math - Design encodings and scales
3. @geepers_datavis_color - Develop color palette
4. @geepers_datavis_data - Validate and prepare data
```

**Then:**
```
5. @geepers_datavis_viz - Technical implementation
```

## Output Format

```
🎨 DATA ARTIST BRIEF

Visualization: {title}
Data Source: {source}
Story: {one-line narrative}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           NARRATIVE DESIGN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Central Question: {what we're answering}

Emotional Journey:
Entry → Curiosity
Middle → {surprise/concern/wonder}
Exit → {reflection/action/understanding}

Metaphor: {chosen metaphor and rationale}

Key Insight: {the "aha" moment}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       MATHEMATICAL APPROACH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Visualization Type: {bar/line/scatter/custom}

Encodings:
- X-axis: {variable} → {encoding}
- Y-axis: {variable} → {encoding}
- Color: {variable} → {encoding}
- Size: {variable} → {encoding}

Scale Choices:
- {scale type with rationale}

Perceptual Considerations:
- {any adjustments needed}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          COLOR PALETTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Palette Type: {sequential/diverging/categorical}

Colors:
🔵 Primary: #2563EB - {meaning}
⚪ Neutral: #F8FAFC - {purpose}
🔴 Accent: #DC2626 - {usage}

Accessibility:
✓ Colorblind safe (simulated)
✓ Contrast ratio > 4.5:1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         IMPLEMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Technology: {D3.js/Chart.js/SVG}

Key Components:
1. {component} - {purpose}
2. {component} - {purpose}

Interactions:
- Hover: {behavior}
- Click: {behavior}

Animation:
- Entry: {animation description}
- Update: {transition behavior}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          BEAUTY SCORE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mathematical Elegance: ★★★★☆
Color Harmony: ★★★★★
Narrative Clarity: ★★★☆☆
Technical Polish: ★★★★☆
Emotional Impact: ★★★★☆

Overall: "Data is Beautiful" certified ✨
```

## Visualization Types & When to Use

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

## Anti-Patterns to Avoid

- ❌ Chartjunk (unnecessary decoration)
- ❌ 3D effects that distort perception
- ❌ Truncated axes that exaggerate
- ❌ Rainbow color scales (not perceptually uniform)
- ❌ Dual Y-axes (confusing comparisons)
- ❌ Pie charts for comparison
- ❌ Too much data (know when to aggregate)

## Inspiration Sources

- **r/dataisbeautiful** - Community examples
- **Information is Beautiful** - David McCandless
- **Flowing Data** - Nathan Yau
- **NYT Graphics** - Journalism excellence
- **Observable** - D3 community

## Key Principles

1. **Data first** - Let the data guide design decisions
2. **Less is more** - Remove until it breaks
3. **Perception matters** - Account for how humans see
4. **Tell a story** - Every visualization has a narrative
5. **Respect the subject** - Honor what the data represents

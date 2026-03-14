# Visualization Gallery

Templates available via `d3-scaffold.py` and their expected data formats.

## 1. Force-Directed Network
**Template:** `force-network`
**Best for:** Relationship mapping, social networks, dependency graphs.
```json
{
  "nodes": [{"id": "A", "group": 1}],
  "links": [{"source": "A", "target": "B", "value": 1}]
}
```

## 2. Timeline
**Template:** `timeline`
**Best for:** Historical events, project milestones, chronological data.
```json
[{"date": "2024-01-15", "title": "Event", "description": "Details"}]
```

## 3. Choropleth Map
**Template:** `choropleth`
**Best for:** Geographic data, state/country comparisons.
```json
[["06", 85], ["48", 72]]
```
Values are `[FIPS_code, value]` pairs for US states.

## 4. Bar Race
**Template:** `bar-race`
**Best for:** Animated rankings over time, competitive comparisons.
```json
[{"name": "Item", "values": [{"date": "2020", "value": 100}]}]
```

## 5. Treemap
**Template:** `treemap`
**Best for:** Hierarchical part-to-whole relationships, budget breakdowns.
```json
{"name": "Root", "children": [{"name": "A", "value": 100}]}
```

## 6. Sankey Diagram
**Template:** `sankey`
**Best for:** Flow and transfer visualization, energy/budget flows.
```json
{
  "nodes": [{"name": "Source"}, {"name": "Target"}],
  "links": [{"source": 0, "target": 1, "value": 10}]
}
```

## 7. Radial Tree
**Template:** `radial-tree`
**Best for:** Deep hierarchies (3+ levels), taxonomies, org charts.
```json
{"name": "Root", "children": [{"name": "Branch", "children": [{"name": "Leaf", "value": 100}]}]}
```

## 8. Bubble Chart
**Template:** `bubble-chart`
**Best for:** 3-variable comparison (x, y, size), cluster analysis.
```json
[{"label": "Group", "data": [{"x": 10, "y": 20, "r": 5}]}]
```

---
name: excalidraw-diagrams
description: "Create Excalidraw diagrams via MCP - architecture, flowcharts, concept maps saved to Obsidian"
metadata:
  openclaw:
    emoji: "📐"
    requires:
      config: []
---

# Excalidraw Diagrams via MCP

Create hand-drawn style diagrams programmatically.

## Diagram Types

| Type | Use Case |
|------|----------|
| Architecture | System components and connections |
| Flowcharts | Process steps and decisions |
| Concept Maps | Ideas and relationships |
| Sequence | API flows, interactions |
| Entity Relations | Database schemas |

## Style Preferences

- Clean and readable
- Consistent color scheme
- Clear labels on everything
- Under 15 elements per diagram
- Hand-drawn aesthetic

## Usage

```
Create an architecture diagram of:
- Web server
- API gateway
- Database
- Cache layer
- Background workers
```

## Output

Saved to: `/Diagrams/[descriptive-name].excalidraw`

Opens directly in Obsidian with Excalidraw plugin.

## MCP Tool

```json
{
  "tool": "excalidraw",
  "action": "create",
  "elements": [
    { "type": "rectangle", "text": "Server", "x": 0, "y": 0 },
    { "type": "arrow", "from": "Server", "to": "Database" }
  ]
}
```

## Example: System Architecture

```
┌─────────────┐     ┌─────────────┐
│   Client    │────▶│  API GW     │
└─────────────┘     └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Backend    │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
  ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
  │  Database   │   │   Cache     │   │  Workers    │
  └─────────────┘   └─────────────┘   └─────────────┘
```

## Obsidian Integration

Requires Excalidraw plugin in Obsidian:
1. Settings → Community plugins → Excalidraw
2. Install and enable
3. .excalidraw files open automatically

## Color Scheme

| Element Type | Color |
|--------------|-------|
| Services | Blue #4F46E5 |
| Databases | Green #059669 |
| External | Orange #EA580C |
| Users | Purple #7C3AED |
| Arrows | Gray #6B7280 |

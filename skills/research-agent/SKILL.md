---
name: research-agent
description: "Deep research with parallel sub-agents scanning Twitter, Reddit, HN, YouTube, and blogs for comprehensive topic analysis"
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      config: []
---

# Research Agent with Parallel Sub-Agents

Launch simultaneous research across multiple platforms for deep topic analysis.

## Platforms to Scan

1. **Twitter/X** - Tweets, threads, discussions (last 2 weeks)
2. **Reddit** - Relevant subreddits, posts, comments
3. **Hacker News** - Stories and comment threads
4. **YouTube** - Recent videos, angles, view counts, comments
5. **Web/Blogs** - Articles, documentation, blog posts

## Sub-Agent Output Format

Each sub-agent produces:
- Key findings and insights
- Notable opinions (positive and negative)
- Links to sources
- Patterns or trends
- Gaps - things nobody is discussing

## Final Synthesis

After all sub-agents report, create:

```markdown
# Research: [TOPIC] - YYYY-MM-DD

## Executive Summary
[Current state of topic in 2-3 sentences]

## Key Themes and Patterns
- Theme 1: [Description]
- Theme 2: [Description]

## Common Pain Points
- Pain point 1
- Pain point 2

## What's Working Well
- [Positive aspects]

## What's Missing
- [Gaps in coverage]

## Opportunities
- [Angles nobody has covered]

## Sources by Platform

### Twitter/X
- [Link] - [Brief description]

### Reddit
- [Link] - [Brief description]

### Hacker News
- [Link] - [Brief description]

### YouTube
- [Link] - [Brief description]

### Web/Blogs
- [Link] - [Brief description]
```

## Output Path

Save to: `/Research/YYYY-MM-DD-[topic-slug].md`

## Usage

```
Research [TOPIC] using parallel agents
```

The agent will:
1. Spawn 5 parallel sub-agents
2. Each covers one platform
3. Wait for all results
4. Synthesize into single document
5. Save to Obsidian vault

## Example Topics

- "Solana memecoin trends 2024"
- "AI coding assistants comparison"
- "Indie hacker marketing strategies"

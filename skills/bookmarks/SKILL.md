---
name: bookmarks
description: "Discord-based bookmark system replacing Raindrop - auto-summarize, tag, and save to Obsidian"
metadata:
  openclaw:
    emoji: "🔖"
    requires:
      config: []
---

# Discord Bookmarks (Raindrop Replacement)

Drop a link, get a summary, save to Obsidian.

## How It Works

1. Drop a URL in #inbox channel
2. Agent fetches and reads content
3. Generates 2-3 sentence summary
4. Auto-tags based on content
5. Saves to Obsidian vault

## Auto-Tags

| Tag | Triggers |
|-----|----------|
| #ai | AI, ML, LLM, GPT, neural |
| #dev-tools | tools, libraries, frameworks, SDK |
| #business | startup, funding, revenue, SaaS |
| #design | UI, UX, design, figma |
| #productivity | workflow, automation, efficiency |
| #crypto | crypto, blockchain, solana, defi |
| #solana | solana, SPL, pump.fun |

## Output Format

### Discord Response
```
🔖 [Title]

Summary: [2-3 sentences]

Tags: #ai #dev-tools

✅ Saved to Bookmarks
```

### Obsidian File
Path: `/Bookmarks/YYYY-MM-DD-[title-slug].md`

```markdown
---
url: https://example.com/article
tags: [ai, dev-tools, productivity]
date: 2024-02-21
summary: Brief summary of the content.
---

# [Article Title]

## Key Takeaway
[Main point of the article]

## Notes
[Any additional notes if provided]
```

## Query Bookmarks

Ask: "What did I save about [topic]?"

Agent searches bookmarks and summarizes relevant saves.

## Connecting Dots

When a new link relates to previous saves:
```
🔗 This connects to that article about [X] you saved last week.
[Link to previous bookmark]
```

## Keep It Short

In #inbox channel:
- Summary, tags, saved confirmation
- That's it - no walls of text

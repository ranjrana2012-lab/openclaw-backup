---
name: morning-briefing
description: "Daily morning Twitter/X briefing with AI-curated top tweets, Obsidian summaries, and video idea tracking"
metadata:
  openclaw:
    emoji: "🌅"
    requires:
      config: []
---

# Morning Twitter Briefing

Daily automated briefing that scans Twitter/X timeline and produces structured summaries.

## What It Does

1. Scans last ~100 tweets from followed accounts
2. Picks top 10 most relevant based on interests
3. Writes summary to Obsidian vault
4. Appends video ideas to backlog
5. Sends Discord summary

## Interests to Filter For

- AI / Machine Learning
- Developer tools
- Indie hacking
- Content creation
- Tech business
- Crypto / Solana (Ranj's interests)

## Output Format

### Obsidian Daily Briefing
Path: `/Daily/YYYY-MM-DD-briefing.md`

```markdown
# Morning Briefing - YYYY-MM-DD

## Top Stories
- [Story 1 with link]
- [Story 2 with link]

## Interesting Threads
- [Thread summary with link]

## Video Ideas
- [Idea 1 - from @username]
- [Idea 2 - from @username]

## Quick Hits
- [Brief item 1]
- [Brief item 2]
```

### Video Ideas Backlog
Path: `/Projects/video-ideas.md`

Append format:
```markdown
- [ ] YYYY-MM-DD: [Video idea] (source: @username)
```

## Discord Summary

Keep to 2-minute read. Key highlights + action items only.

## Cron Schedule

```bash
# Add to crontab: 7:00 AM daily
0 7 * * * openclaw cron run morning-briefing
```

## Setup Required

- Twitter/X API access (or nitter scraping)
- Obsidian vault path configured
- Discord #briefing channel

---
name: youtube-stats
description: "YouTube channel analytics with natural language queries - retention, engagement, growth trends, and topic analysis"
metadata:
  openclaw:
    emoji: "📊"
    requires:
      config: []
---

# YouTube Stats and Analytics

Natural language queries for YouTube channel performance.

## Capabilities

### Questions You Can Ask

- "How did my last 5 videos compare on retention?"
- "Which topics get the most engagement?"
- "Compare my OpenClaw videos to my Claude Code videos"
- "What's my subscriber growth trend this month?"
- "Which video had the best click-through rate?"
- "What's my average view duration?"

### What You Get

- Raw numbers AND interpretation
- What the data means
- What you should do about it
- Proactive pattern spotting

## API Setup

### YouTube Data API
```bash
# OAuth credentials needed
YOUTUBE_CLIENT_ID=xxx
YOUTUBE_CLIENT_SECRET=xxx
YOUTUBE_REFRESH_TOKEN=xxx
```

### YouTube Analytics API
- Channel ID
- OAuth tokens for analytics access

## Sample Queries

### Retention Analysis
```
Fetch retention curves for last 5 videos.
Compare average percentage viewed.
Identify where viewers drop off.
```

### Topic Performance
```
Group videos by topic tag.
Show views, CTR, retention by topic.
Highlight best/worst performers.
```

### Growth Trends
```
30/60/90 day subscriber change.
View count trends over time.
Identify growth accelerators.
```

## Proactive Insights

Agent should mention patterns without being asked:
- "By the way, your Tuesday uploads consistently outperform Monday uploads"
- "Your thumbnail style change in March improved CTR by 15%"
- "Videos under 12 minutes have 20% better retention"

## Response Format

```
📈 [Query Result]

[Data visualization or numbers]

💡 What this means:
[Interpretation]

🎯 Recommendation:
[Action to take]
```

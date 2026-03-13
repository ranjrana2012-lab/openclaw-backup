---
name: discord-architecture
description: "Discord server optimization for OpenClaw workflows - channel setup, model routing, context isolation"
metadata:
  openclaw:
    emoji: "🎮"
    requires:
      config: []
---

# Discord Channel Architecture

Optimized Discord server setup for OpenClaw workflows.

## Channel Structure

| Channel | Purpose | Model |
|---------|---------|-------|
| #general | Daily tasks, quick questions | GLM-4.7-Flash (balanced) |
| #youtube-stats | YouTube analytics queries | GLM-4.7-Flash (fast, data) |
| #video-research | Content research, deep context | GLM-5 (deep thinking) |
| #inbox | Bookmark processing | GLM-4.7-Flash (fast) |
| #monitoring | Server health, alerts, cron reports | GLM-4.7-Flash (fast) |
| #briefing | Morning briefings, daily summaries | GLM-4.7 (balanced) |

## Model Routing Configuration

```json5
{
  bindings: [
    {
      agentId: "main",
      match: { channel: "discord", guildId: "YOUR_GUILD_ID", channelId: "VIDEO_RESEARCH_ID" },
      model: "zai/glm-5"
    },
    {
      agentId: "main", 
      match: { channel: "discord", guildId: "YOUR_GUILD_ID" },
      model: "zai/glm-4.7-flash"
    }
  ]
}
```

## Context Isolation

Each channel has isolated context:
- Conversations in #youtube-stats don't bleed into #video-research
- #video-research builds context over weeks
- #general stays fresh for daily tasks

## Permissions

| Channel | Read | Write | Special |
|---------|------|-------|---------|
| #general | All | All | - |
| #youtube-stats | All | All | - |
| #video-research | All | All | - |
| #inbox | All | All | - |
| #monitoring | All | Bot only | Admin can post |
| #briefing | All | Bot only | Cron posts here |

## Setup Commands

```bash
# Create channels
# (Do this in Discord UI or via bot API)

# Configure model routing in openclaw.json
# See model routing config above

# Restart gateway to apply
openclaw gateway restart
```

## Bot Permissions Required

- View Channels
- Send Messages
- Read Message History
- Add Reactions
- Create Threads
- Pin Messages

## Invite Link (Admin)

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot
```

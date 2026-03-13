---
name: voice-transcription
description: "Automatic voice message transcription using Whisper - works in WhatsApp, Telegram, Discord"
metadata:
  openclaw:
    emoji: "🎤"
    requires:
      config: []
---

# Voice Note Transcription

Automatic transcription of voice messages using Whisper.

## How It Works

1. Voice message received in any channel
2. Audio extracted and sent to Whisper
3. Text transcription generated
4. Agent responds to the transcribed content

## Supported Platforms

- WhatsApp
- Telegram
- Discord

## Use Cases

- Quick thoughts while driving
- Shopping lists while walking
- Meeting notes on the go
- Hands-free commands

## Setup

Enable during onboarding or install the Whisper skill:

```bash
openclaw skills install whisper-transcription
```

## No Prompt Needed

This is automatic - just send a voice message and the agent handles the rest.

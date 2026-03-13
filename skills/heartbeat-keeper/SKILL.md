---
name: heartbeat-keeper
description: "Keep gateway and API connections alive with periodic pings"
metadata:
  {
    "openclaw": {
      "emoji": "💓",
      "category": "monitoring",
      "type": "python-skill"
    }
  }
---

# Heartbeat Keeper

**Category:** Monitoring
**Location:** `/workspace/skills/monitoring/heartbeat-keeper/`

## Overview

Keep OpenClaw gateway and z.ai API connections alive with periodic health checks.

## Usage

```bash
skill-run monitoring heartbeat-keeper <action>
```

## Actions

- `check` - Check both gateway and API health
- `gateway` - Ping gateway only
- `api` - Ping API only

## Examples

```bash
# Check both gateway and API
skill-run monitoring heartbeat-keeper check

# Check gateway only
skill-run monitoring heartbeat-keeper gateway

# Check API only
skill-run monitoring heartbeat-keeper api
```

## Implementation

- **Source:** `/workspace/skills/monitoring/heartbeat-keeper/src/main.py`
- **Runtime:** Python 3

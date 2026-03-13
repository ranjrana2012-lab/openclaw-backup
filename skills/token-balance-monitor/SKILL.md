---
name: token-balance-monitor
description: "Check z.ai GLM 4.7 token balance and usage statistics"
metadata:
  {
    "openclaw": {
      "emoji": "💰",
      "category": "monitoring",
      "type": "python-skill"
    }
  }
---

# Token Balance Monitor

**Category:** Monitoring
**Location:** `/workspace/skills/monitoring/token-balance-monitor/`

## Overview

Check current z.ai GLM 4.7 token balance and usage statistics.

## Usage

```bash
skill-run monitoring token-balance-monitor check
```

## Examples

```bash
# Check token balance
skill-run monitoring token-balance-monitor check
```

## Implementation

- **Source:** `/workspace/skills/monitoring/token-balance-monitor/src/main.py`
- **Runtime:** Python 3

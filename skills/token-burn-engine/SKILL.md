---
name: token-burn-engine
description: "Burn tokens by executing strategic API calls"
metadata:
  {
    "openclaw": {
      "emoji": "🔥",
      "category": "monitoring",
      "type": "python-skill"
    }
  }
---

# Token Burn Engine

**Category:** Monitoring
**Location:** `/workspace/skills/monitoring/token-burn-engine/`

## Overview

Burn tokens by making strategic API calls to z.ai GLM 4.7.

## Usage

```bash
skill-run monitoring token-burn-engine burn [--amount=N]
```

## Examples

```bash
# Burn 1 prompt (default)
skill-run monitoring token-burn-engine burn

# Burn 10 prompts
skill-run monitoring token-burn-engine burn amount=10

# Burn 100 prompts
skill-run monitoring token-burn-engine burn amount=100
```

## Implementation

- **Source:** `/workspace/skills/monitoring/token-burn-engine/src/main.py`
- **Runtime:** Python 3

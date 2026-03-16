---
name: token-burn-optimizer
description: "Optimize z.ai GLM 4.7 token usage with automated burning and monitoring"
metadata:
  {
    "openclaw": {
      "emoji": "🔥",
      "category": "monitoring",
      "type": "python-skill"
    }
  }
---

# Token Burn Optimizer

**Category:** Monitoring
**Location:** `/workspace/skills/monitoring/token-burn-optimizer/`

## Overview

Automated token monitoring and burn optimization for z.ai GLM 4.7 API usage. Maintains 90% token burn rate with 2,400 prompts per 5-hour cycle until March 2027.

## Usage

Run this skill via the OpenClaw Lab skill runner:

```bash
skill-run monitoring token-burn-optimizer <action> [options]
```

## Available Actions

- `start` - Start the token burn optimizer daemon
- `stop` - Stop the optimizer daemon
- `status` - Get current optimizer status and metrics
- `balance` - Check current z.ai token balance
- `burn` - Manually trigger token burn
- `logs` - View recent activity logs
- `config` - View or update configuration

## Examples

```bash
# Start the optimizer
skill-run monitoring token-burn-optimizer start

# Check current status
skill-run monitoring token-burn-optimizer status

# View token balance
skill-run monitoring token-burn-optimizer balance

# Manual burn with custom amount
skill-run monitoring token-burn-optimizer burn amount=100

# View recent logs
skill-run monitoring token-burn-optimizer logs lines=50

# Update configuration
skill-run monitoring token-burn-optimizer config target_burn_rate=0.95
```

## Configuration

Configuration is stored in `config.json` within the skill directory.

Default settings:
- Target burn rate: 90%
- Prompts per cycle: 2,400
- Cycle duration: 5 hours
- Heartbeat interval: 60 seconds
- End date: March 2027

## Implementation

- **Source:** `/workspace/skills/monitoring/token-burn-optimizer/src/main.py`
- **Runtime:** Python 3 with OpenClaw Lab runtime templates
- **Dependencies:** aiohttp, asyncio, OpenClaw SkillBase

## Dashboard

Real-time metrics available in OpenClaw Web UI at http://[PRIVATE_HOST]/

Metrics include:
- Current token balance
- Burn progress percentage
- Prompts this cycle
- Time remaining until next cycle
- Health status

## Notes

This is an OpenClaw Lab Python skill. It runs in the container's Python environment with access to Docker, GPU, and system resources.

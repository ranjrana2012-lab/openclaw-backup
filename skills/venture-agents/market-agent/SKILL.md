---
name: market-agent
description: Daily market scouting, competitor analysis, and idea generation for the venture studio
version: 1.0.0
author: venture-studio
created: 2026-02-22
---

## Purpose

Scouts markets daily for new business opportunities, tracks competitor movements, and generates/evaluates ideas for the venture studio pipeline.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| focus_area | string | no | Specific market to scout (e.g., "UK professional services") |
| competitor_list | array | no | Specific competitors to track |
| idea_count | integer | no | Number of ideas to generate (default: 5) |

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| ideas | array | New business ideas with scores |
| competitor_updates | array | Notable competitor changes |
| market_signals | array | Market trends and opportunities |

---

## Permissions Required

| Permission | Scope | Justification |
|------------|-------|---------------|
| browser | restricted | Scout competitor websites, LinkedIn |
| web_search | full | Research market trends |
| files | /Venture/venture/ | Write to market_backlog.md |

---

## Allowed Directories

- `/home/ranj/.openclaw/workspace/Venture/venture/`
- `/home/ranj/.openclaw/workspace/Venture/venture/businesses/`

---

## Gating Requirements

| Requirement | Type | Notes |
|-------------|------|-------|
| Z_AI_API_KEY | env_var | For AI-powered analysis |
| Human approval | approval | Only for adding ideas to active validation |

---

## Rate Limits

| Limit | Value |
|-------|-------|
| Web searches per run | 20 |
| Browser pages per run | 10 |

---

## Cost Caps

| Cap | Value | Action if exceeded |
|-----|-------|-------------------|
| Daily | £1 | Stop and alert |
| Monthly | £20 | Stop and alert |

---

## Daily Tasks

### Morning Scout (09:00 UK)

1. **Competitor Check**
   - Review top 5 competitors per active business
   - Log pricing changes, feature updates
   - Alert on significant moves

2. **Market Signals**
   - Search for "[industry] pain points 2026"
   - Check Reddit, LinkedIn, Twitter for complaints
   - Identify emerging trends

3. **Idea Generation**
   - Generate 5 new ideas based on signals
   - Score using standard rubric
   - Add top ideas to market_backlog.md

---

## Scoring Rubric

| Criterion | Weight | Max Score |
|-----------|--------|-----------|
| Speed to revenue | 25% | 25 |
| Technical simplicity | 20% | 20 |
| Market size | 20% | 20 |
| DGX advantage | 15% | 15 |
| Competition gap | 10% | 10 |
| Founder fit | 10% | 10 |
| **Total** | 100% | **100** |

---

## Audit Logging

Logged to `/Venture/venture/logs/market-agent.log`:

| Event | Fields Logged |
|-------|---------------|
| Scout run | timestamp, ideas_generated, sources_checked |
| Competitor update | timestamp, competitor, change_type, details |
| Idea added | timestamp, idea_name, score, evidence_tags |

---

## Safety Checklist

- [x] Input validation implemented
- [x] Path sanitisation for file operations
- [x] Whitelisted domains for network calls
- [x] Secrets masked in logs
- [x] Rate limiting respected
- [x] Try/catch with safe fallbacks

---

## Review Sign-offs

| Reviewer | Date | Status |
|----------|------|--------|
| SecurityAgent | 2026-02-22 | Pending |
| ComplianceAgent | 2026-02-22 | Pending |
| Human | 2026-02-22 | Pending |

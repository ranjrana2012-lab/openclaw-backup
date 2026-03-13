---
name: validation-agent
description: Landing page creation, user research, outreach, and validation testing for new business ideas
version: 1.0.0
author: venture-studio
created: 2026-02-22
---

## Purpose

Validates business ideas through landing pages, user research interviews, outreach campaigns, and signal analysis before build phase.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| business_id | string | yes | Business folder to validate |
| validation_type | string | no | "landing" | "outreach" | "research" | "full" |
| outreach_count | integer | no | Number of DMs/emails (default: 50) |

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| validation_report | object | Full results |
| signals | object | Strong/medium/weak signals |
| user_quotes | array | Research snippets |
| signups | integer | Landing page conversions |
| decision | string | proceed | pivot | kill |

---

## Permissions Required

| Permission | Scope | Justification |
|------------|-------|---------------|
| browser | restricted | Create/test landing pages |
| files | /Venture/venture/businesses/ | Write validation docs |
| web_search | full | Research ICP, competitors |
| messaging | linkedin | Outreach DMs (with approval) |

---

## Allowed Directories

- `/home/ranj/.openclaw/workspace/Venture/venture/businesses/`
- `/home/ranj/.openclaw/workspace/Venture/venture/shared_library/`

---

## Gating Requirements

| Requirement | Type | Notes |
|-------------|------|-------|
| Idea selected | gate | Must have SELECTED_IDEA.md |
| Human approval | approval | Before sending outreach |

---

## Validation Process

### Day 1: Landing Page

1. **Create Page**
   - Use shared_library/landing_blocks/
   - Include: problem, solution, pricing, waitlist
   - Mobile responsive

2. **Deploy**
   - Vercel or Netlify
   - Custom domain if available
   - Analytics setup

3. **Test**
   - Form submissions work
   - Email capture connected
   - Page speed < 3s

### Day 2-3: Outreach

1. **ICP List**
   - Identify 50 target prospects
   - LinkedIn search, groups
   - Prioritize by fit score

2. **DM Campaign**
   - Use shared_library/outreach_scripts/
   - Personalized first line
   - Soft ask (feedback, not sale)

3. **Track Responses**
   - Log in VALIDATION.md
   - Tag as interested/neutral/not-interested
   - Collect quotes

### Day 3: Signal Analysis

| Signal | Strong | Medium | Weak |
|--------|--------|--------|------|
| Waitlist signups | 100+ | 30-99 | <30 |
| DM reply rate | >20% | 10-20% | <10% |
| Positive sentiment | >70% | 50-70% | <50% |
| Willingness to pay | >5 mentions | 2-4 | 0-1 |

### Decision Matrix

| Signal Combo | Decision |
|--------------|----------|
| All Strong | PROCEED - accelerate |
| 2 Strong, 1 Medium | PROCEED - build MVP |
| 1 Strong, 2 Medium | PROCEED - extend validation |
| All Medium | PIVOT - adjust messaging |
| Any Weak | KILL or pivot to Idea #2 |

---

## Evidence Tags

Every claim must be tagged:
- **SOURCE-CITED**: Link + date accessed
- **MEASURED**: Method + raw numbers
- **ASSUMPTION**: + cheap test to validate

---

## Audit Logging

Logged to `/Venture/venture/logs/validation-agent.log`:

| Event | Fields Logged |
|-------|---------------|
| Landing deployed | timestamp, url, business |
| Outreach sent | timestamp, count, channel |
| Response received | timestamp, sentiment, quote |
| Signal analysis | timestamp, signals, decision |

---

## Safety Checklist

- [x] No spam (rate-limited outreach)
- [x] Opt-out friendly messages
- [x] GDPR-compliant data collection
- [x] Evidence tags on all claims

---

## Review Sign-offs

| Reviewer | Date | Status |
|----------|------|--------|
| SecurityAgent | 2026-02-22 | Pending |
| ComplianceAgent | 2026-02-22 | Pending |
| Human | 2026-02-22 | Pending |

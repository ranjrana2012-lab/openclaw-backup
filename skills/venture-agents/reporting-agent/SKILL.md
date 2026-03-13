---
name: reporting-agent
description: Generates daily scores, updates leaderboard, produces weekly reports, and maintains portfolio dashboard
version: 1.0.0
author: venture-studio
created: 2026-02-22
---

## Purpose

Calculates daily business scores, maintains the agent leaderboard, generates weekly reports, and keeps the portfolio dashboard up to date.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| report_type | string | no | "daily" | "weekly" | "monthly" (default: daily) |
| business_id | string | no | Specific business (default: all) |
| date_range | object | no | Start/end dates for report |

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| scores | array | Calculated scores per business |
| leaderboard | array | Updated rankings |
| report | object | Generated report content |
| dashboard_updates | object | Changes to dashboard.md |

---

## Permissions Required

| Permission | Scope | Justification |
|------------|-------|---------------|
| files | /Venture/venture/ | Read/write reports, leaderboard |
| network | stripe_api | Read revenue data |
| network | paypal_api | Read transaction data |

---

## Allowed Directories

- `/home/ranj/.openclaw/workspace/Venture/venture/`
- `/home/ranj/.openclaw/workspace/Venture/venture/leaderboard/`
- `/home/ranj/.openclaw/workspace/Venture/venture/businesses/`
- `/home/ranj/.openclaw/workspace/Venture/venture/finance/`

---

## Daily Scoring (20:00 UK)

### Score Calculation

```
Base Score = Revenue - Refunds - Payment Fees - Tool Costs - Infrastructure

Modifiers:
+10% if Retention Rate > 50%
+5% if Repeat Purchase Rate > 30%
+5% if Avg Support Time < 5 minutes
-20% if Dispute Rate > 5%

Final Score = Base Score × (1 + Total Modifiers)
```

### Revenue Sources

| Source | Tracking |
|--------|----------|
| Stripe payments | Dashboard → Payments |
| PayPal payments | Activity → All transactions |
| Invoice payments | Manual entry |

### Cost Deductions

| Item | Daily Approx |
|------|--------------|
| Stripe fees | 1.4% + 20p (UK) |
| PayPal fees | 2.9% + 30p |
| VPS | £0.50-1.67/day |
| APIs | Variable |

---

## Weekly Report (Sunday 18:00 UK)

### Report Structure

1. **Executive Summary**
   - Portfolio MRR
   - Week-over-week growth
   - Top performer / biggest concern

2. **Per-Business Breakdown**
   - Revenue, costs, net
   - KPIs vs targets
   - Issues and resolutions

3. **Pipeline Status**
   - Ideas in validation
   - Build progress
   - Launch schedule

4. **Leaderboard Update**
   - Agent rankings
   - Notable achievements

5. **Risk Assessment**
   - Kill switch status
   - Targets at risk

---

## Leaderboard Maintenance

### Directory Structure

```
/leaderboard/
├── daily/           # Daily score files
│   └── 2026-02-22.md
├── weekly/          # Weekly summaries
│   └── 2026-W08.md
├── champions/       # Hall of fame
└── audits/          # Anti-gaming audits
```

### Agent Rankings

| Rank | Agent | Criteria |
|------|-------|----------|
| 1 | Top performer | Highest combined business scores |
| 2 | Runner-up | Second highest |
| ... | ... | ... |

---

## Dashboard Updates

Keeps `/dashboard.md` current with:
- Portfolio MRR
- Run-rate progress
- Live businesses table
- Pipeline status
- Top risks

---

## Audit Logging

Logged to `/Venture/venture/logs/reporting-agent.log`:

| Event | Fields Logged |
|-------|---------------|
| Score calculated | timestamp, business, base, modifiers, final |
| Report generated | timestamp, type, businesses_included |
| Dashboard updated | timestamp, sections_changed |

---

## Safety Checklist

- [x] No secrets in reports
- [x] Conservative estimates for missing data
- [x] Evidence tags for all claims
- [x] Anti-gaming checks applied

---

## Review Sign-offs

| Reviewer | Date | Status |
|----------|------|--------|
| SecurityAgent | 2026-02-22 | Pending |
| ComplianceAgent | 2026-02-22 | Pending |
| Human | 2026-02-22 | Pending |

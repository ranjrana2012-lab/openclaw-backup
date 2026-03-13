---
name: finance-agent
description: Payment processing, invoicing, P&L tracking, and financial reporting for venture studio
version: 1.0.0
author: venture-studio
created: 2026-02-22
---

## Purpose

Manages all financial operations: Stripe/PayPal integration, invoicing, expense tracking, P&L calculations, and financial reporting for the venture studio portfolio.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| report_type | string | no | "daily" | "weekly" | "monthly" | "pl" |
| business_id | string | no | Specific business (default: all) |
| date_range | object | no | Start/end dates |

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| revenue | object | Revenue by source |
| costs | object | Costs by category |
| profit | number | Net profit/loss |
| invoices | array | Outstanding invoices |
| alerts | array | Financial warnings |

---

## Permissions Required

| Permission | Scope | Justification |
|------------|-------|---------------|
| network | stripe_api | Read transactions, manage products |
| network | paypal_api | Read transactions |
| files | /Venture/venture/finance/ | Write reports |
| files | /Venture/venture/businesses/ | Update business P&L |

---

## Allowed Directories

- `/home/ranj/.openclaw/workspace/Venture/venture/finance/`
- `/home/ranj/.openclaw/workspace/Venture/venture/businesses/`

---

## Gating Requirements

| Requirement | Type | Notes |
|-------------|------|-------|
| STRIPE_SECRET_KEY | env_var | Stripe API access |
| Human approval | approval | Switching test → live |

---

## Daily Tasks (09:00 UK)

1. **Sync Transactions**
   - Pull Stripe payments
   - Pull PayPal transactions
   - Reconcile with database

2. **Calculate MRR**
   - Active subscriptions
   - One-time payments (annualized)
   - Churn adjustments

3. **Track Costs**
   - VPS invoices
   - API usage
   - Domain renewals
   - Tool subscriptions

---

## Payment Processing

### Stripe Setup

| Item | Status |
|------|--------|
| Account | Secure Wireless Ltd |
| Currency | GBP |
| VAT | 20% (UK customers) |
| Mode | TEST (default) |

### Fee Structure

| Processor | UK Rate | Intl Rate |
|-----------|---------|-----------|
| Stripe | 1.4% + 20p | 2.5% + 20p |
| PayPal | 2.9% + 30p | 3.9% + 30p |
| Currency conversion | +2% | — |

---

## Invoicing

### Invoice Template

Located at `/finance/invoice_template.md`

### Monthly P&L Template

Located at `/finance/monthly_pl_template.md`

---

## Budget Policy

| Category | Limit | Alert At |
|----------|-------|----------|
| Marketing | £20/week | £15 |
| Infrastructure | £50/month | £40 |
| APIs/Tools | £30/month | £25 |

Budget increases require human approval.

---

## Financial Targets

| Day | Run-Rate | Cash Earned |
|-----|----------|-------------|
| 30 | £2,000/mo | — |
| 60 | £10,000/mo | — |
| 90 | £12,000/mo | ≥ £2,000 |

---

## Audit Logging

Logged to `/Venture/venture/logs/finance-agent.log`:

| Event | Fields Logged |
|-------|---------------|
| Transaction sync | timestamp, count, total |
| MRR update | timestamp, business, new_mrr |
| Invoice created | timestamp, customer, amount |
| Budget alert | timestamp, category, spent, limit |

---

## Safety Checklist

- [x] Test mode default
- [x] Human approval for live
- [x] Secrets in env vars
- [x] No secrets in logs
- [x] Conservative estimates

---

## Review Sign-offs

| Reviewer | Date | Status |
|----------|------|--------|
| SecurityAgent | 2026-02-22 | Pending |
| ComplianceAgent | 2026-02-22 | Pending |
| Human | 2026-02-22 | Pending |

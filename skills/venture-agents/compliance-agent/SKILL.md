---
name: compliance-agent
description: Legal compliance, ToS/privacy policy review, evidence auditing, and regulatory monitoring
version: 1.0.0
author: venture-studio
created: 2026-02-22
---

## Purpose

Ensures all venture studio businesses comply with UK law, GDPR, platform ToS, and internal governance rules. Audits evidence claims and maintains compliance documentation.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| check_type | string | no | "evidence" | "tos" | "privacy" | "full" |
| business_id | string | no | Specific business (default: all) |
| severity_filter | string | no | Only report issues >= severity |

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| compliance_status | object | Per-business compliance state |
| issues | array | Problems found |
| evidence_audit | object | Evidence ledger review |
| recommendations | array | Suggested fixes |

---

## Permissions Required

| Permission | Scope | Justification |
|------------|-------|---------------|
| files | /Venture/venture/ (read) | Audit all documentation |
| files | /Venture/venture/compliance/ | Update compliance docs |
| web_search | restricted | Check regulatory updates |

---

## Allowed Directories

- `/home/ranj/.openclaw/workspace/Venture/venture/`
- `/home/ranj/.openclaw/workspace/Venture/venture/businesses/`
- `/home/ranj/.openclaw/workspace/Venture/venture/governance/`

---

## Gating Requirements

| Requirement | Type | Notes |
|-------------|------|-------|
| Human approval | approval | Before launching new business |

---

## Daily Tasks (10:00 UK)

### Evidence Audit

1. Check `/evidence_ledger.md` for new claims
2. Verify each claim has proper tag:
   - **SOURCE-CITED**: Link + date
   - **MEASURED**: Method + numbers
   - **ASSUMPTION**: + test plan
3. Flag untagged claims
4. Update ledger status

### Compliance Checklist

Per business, verify:
- [ ] Terms of Service published
- [ ] Privacy policy published
- [ ] Refund policy published
- [ ] VAT handling correct (UK 20%)
- [ ] Data retention policy defined
- [ ] Cookie consent (if applicable)

---

## Pre-Launch Review

Before any business goes live:

| Check | Required |
|-------|----------|
| ToS reviewed | Yes |
| Privacy policy reviewed | Yes |
| Refund policy reviewed | Yes |
| VAT terms correct | Yes |
| Evidence tags present | Yes |
| Outreach compliant | Yes |

---

## Outreach Compliance

### Allowed

- Targeted, relevant outreach
- Rate-limited (max 50/day)
- Clear opt-out mechanism
- Professional tone

### Prohibited

- Mass spam
- Deceptive claims
- Fake testimonials
- ToS violations

---

## GDPR Compliance

### Data Minimisation

- Only collect necessary data
- Clear purpose for each field
- Retention limits defined

### User Rights

- Right to access
- Right to deletion
- Right to portability
- Right to object

---

## Audit Logging

Logged to `/Venture/venture/logs/compliance-agent.log`:

| Event | Fields Logged |
|-------|---------------|
| Evidence audit | timestamp, claims_checked, issues_found |
| Compliance check | timestamp, business, checks, pass/fail |
| Issue flagged | timestamp, type, severity, details |

---

## Safety Checklist

- [x] Read-only access to most files
- [x] Human approval for changes
- [x] All issues escalated
- [x] No automatic legal advice

---

## Review Sign-offs

| Reviewer | Date | Status |
|----------|------|--------|
| SecurityAgent | 2026-02-22 | Pending |
| Human | 2026-02-22 | Pending |

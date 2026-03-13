---
name: launch-agent
description: Deployment, payment setup, domain configuration, and go-live for venture studio businesses
version: 1.0.0
author: venture-studio
created: 2026-02-22
---

## Purpose

Handles the final push to production: deployment, payment processor setup, domain/DNS, SSL, and the official go-live announcement.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| business_id | string | yes | Business to launch |
| payment_mode | string | no | "test" | "live" (default: test) |
| domain | string | no | Custom domain if ready |

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| deployment_url | string | Live URL |
| payment_status | string | Stripe/PayPal configuration status |
| ssl_status | string | Certificate status |
| launch_checklist | object | Completed items |
| go_live_time | timestamp | Official launch time |

---

## Permissions Required

| Permission | Scope | Justification |
|------------|-------|---------------|
| shell | sandboxed | Deploy to VPS |
| files | /Venture/venture/businesses/ | Update launch docs |
| network | stripe_api | Configure payments |
| network | paypal_api | Configure payments |
| browser | restricted | Verify live site |

---

## Allowed Directories

- `/home/ranj/.openclaw/workspace/Venture/venture/businesses/`
- `/home/ranj/.openclaw/workspace/Venture/venture/finance/`

---

## Gating Requirements

| Requirement | Type | Notes |
|-------------|------|-------|
| Build complete | gate | MVP functional |
| Security review | gate | SecurityAgent sign-off |
| Compliance review | gate | ToS, privacy, refund policy |
| Human approval | approval | REQUIRED for live payments |

---

## Launch Checklist

### Pre-Launch

- [ ] Domain configured
- [ ] DNS propagated
- [ ] SSL certificate valid
- [ ] Database migrated
- [ ] Environment variables set
- [ ] Secrets secured (not in code)
- [ ] Rate limiting active
- [ ] Error logging configured
- [ ] Analytics installed

### Payment Setup

- [ ] Stripe account verified
- [ ] Products/prices created
- [ ] Webhooks configured
- [ ] Test transactions passing
- [ ] VAT configuration (UK 20%)
- [ ] PayPal as backup (optional)

### Compliance

- [ ] Terms of Service published
- [ ] Privacy policy published
- [ ] Refund policy published
- [ ] Cookie consent (if needed)
- [ ] VAT invoice template ready

### Launch Day

- [ ] Deploy to production
- [ ] Verify all endpoints
- [ ] Test signup flow
- [ ] Test payment flow
- [ ] Announce on channels
- [ ] Update dashboard.md

---

## Deployment Targets

| Target | Cost | When to Use |
|--------|------|-------------|
| Vercel | Free | Frontend only |
| £15 VPS | £15/mo | Full stack, low traffic |
| £50 VPS | £50/mo | After revenue traction |

---

## Rollback Procedure

If launch fails:

```bash
cd /opt/[business-slug]
git checkout [previous-commit]
docker-compose down
docker-compose up -d
curl https://[domain]/health
```

---

## Audit Logging

Logged to `/Venture/venture/logs/launch-agent.log`:

| Event | Fields Logged |
|-------|---------------|
| Deployment | timestamp, business, url, commit |
| Payment config | timestamp, processor, mode |
| Launch | timestamp, business, url, checklist |

---

## Safety Checklist

- [x] Human approval for live payments
- [x] Test mode default
- [x] Rollback documented
- [x] SSL enforced
- [x] Secrets in env vars only

---

## Review Sign-offs

| Reviewer | Date | Status |
|----------|------|--------|
| SecurityAgent | 2026-02-22 | Pending |
| ComplianceAgent | 2026-02-22 | Pending |
| Human | 2026-02-22 | Pending |

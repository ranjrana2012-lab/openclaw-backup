---
name: security-agent
description: Security audits, secret scanning, permission reviews, and incident response for venture studio
version: 1.0.0
author: venture-studio
created: 2026-02-22
---

## Purpose

Protects the venture studio from security threats through regular audits, secret scanning, permission reviews, and incident response coordination.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| scan_type | string | no | "secrets" | "permissions" | "dependencies" | "full" |
| target_path | string | no | Specific directory to scan |
| severity_filter | string | no | Only report issues >= severity |

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| scan_results | object | Findings by category |
| secrets_found | array | Exposed secrets (masked) |
| permission_issues | array | Overly permissive access |
| vulnerabilities | array | Dependency vulnerabilities |
| recommendations | array | Remediation steps |

---

## Permissions Required

| Permission | Scope | Justification |
|------------|-------|---------------|
| files | /Venture/venture/ (scan) | Scan for secrets |
| shell | sandboxed | Run security tools |
| network | scan_only | Port scanning, SSL checks |

---

## Allowed Directories

- `/home/ranj/.openclaw/workspace/Venture/`
- `/home/ranj/.openclaw/workspace/Projects/`
- `/home/ranj/.openclaw/credentials/`

---

## Gating Requirements

| Requirement | Type | Notes |
|-------------|------|-------|
| Human approval | approval | Before fixing critical issues |

---

## Daily Scans (03:00 UK)

### Secret Scan

Scan all code for:
- API keys (regex patterns)
- Passwords in code
- Private keys
- Database credentials
- OAuth tokens

**Action on found:** Mask in logs, alert human immediately

### Permission Audit

Check:
- File permissions (700 for sensitive)
- Directory permissions
- Agent permission matrix compliance
- API key scopes

### Dependency Check

- npm audit
- pip audit
- Container image scans (Trivy)

---

## Weekly Review (Sunday)

### Full Security Audit

1. Review all agent permissions
2. Check API key rotation schedule
3. Audit database access logs
4. Review SSL certificate expiry
5. Check firewall rules
6. Verify backup integrity

---

## Incident Response

### Severity Levels

| Level | Definition | Response |
|-------|------------|----------|
| CRITICAL | Active breach, data exposure | Immediate human alert |
| HIGH | Vulnerability exploitable | Fix within 24h |
| MEDIUM | Security weakness | Fix within 1 week |
| LOW | Best practice violation | Fix within 1 month |

### Response Steps

1. **Detect** - Automated scan or report
2. **Assess** - Determine severity
3. **Contain** - Isolate if needed
4. **Alert** - Notify human (P1/P2)
5. **Remediate** - Apply fix
6. **Document** - Update incident log
7. **Post-mortem** - For P1/P2

---

## Secret Management

| Secret Type | Storage | Access |
|-------------|---------|--------|
| API keys | Environment variables | Root only |
| Database creds | Env vars | BuildAgent only |
| Stripe keys | Env vars | FinanceAgent only |
| User data | Encrypted at rest | OperationsAgent (read) |

**Never:**
- Log secrets
- Commit secrets to git
- Display secrets in UI
- Share secrets between agents

---

## Permission Matrix

| Agent | Browser | Shell | Files | Network | Payments |
|-------|---------|-------|-------|---------|----------|
| MarketAgent | Restricted | No | Write backlog | Whitelist | No |
| ValidationAgent | Restricted | No | Write validation | Whitelist | No |
| BuildAgent | No | Sandboxed | Full | Restricted | No |
| LaunchAgent | Restricted | No | Assets only | Whitelist | No |
| OperationsAgent | Limited | No | Read logs | No | No |
| ComplianceAgent | Read-only | No | Read-only | No | No |
| FinanceAgent | No | No | Finance dir | Stripe/PayPal | Test mode |
| SecurityAgent | Sandboxed | Sandboxed | Scan only | Scan only | No |
| ReportingAgent | No | No | Reports only | No | No |

---

## Audit Logging

Logged to `/Venture/venture/logs/security-agent.log`:

| Event | Fields Logged |
|-------|---------------|
| Scan complete | timestamp, type, findings, severity |
| Secret found | timestamp, type, location (masked) |
| Incident | timestamp, severity, details, resolution |
| Permission change | timestamp, agent, change, approver |

---

## Safety Checklist

- [x] Secrets always masked in logs
- [x] Sandboxed execution
- [x] Human approval for critical fixes
- [x] No destructive actions without approval
- [x] Incident log maintained

---

## Review Sign-offs

| Reviewer | Date | Status |
|----------|------|--------|
| Human | 2026-02-22 | Pending |

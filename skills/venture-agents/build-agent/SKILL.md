---
name: build-agent
description: MVP construction, code generation, and technical implementation for venture studio businesses
version: 1.0.0
author: venture-studio
created: 2026-02-22
---

## Purpose

Builds MVPs for validated business ideas, handles technical implementation, sets up infrastructure, and manages deployment pipelines.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| business_id | string | yes | Business folder to build |
| template | string | no | Build template (saas, api, landing, tool) |
| components | array | no | Specific components to build |
| dry_run | boolean | no | Plan only, don't execute |

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| build_plan | object | Components and tasks |
| files_created | array | Generated files |
| commands_run | array | Shell commands executed |
| status | string | success | failed | partial |
| next_steps | array | Remaining tasks |

---

## Permissions Required

| Permission | Scope | Justification |
|------------|-------|---------------|
| shell | sandboxed | Run build commands |
| files | /Venture/venture/businesses/ | Create code files |
| files | /Projects/ | Project workspace |
| network | npm/pip | Install dependencies |
| browser | restricted | Test generated UIs |

---

## Allowed Directories

- `/home/ranj/.openclaw/workspace/Venture/venture/businesses/`
- `/home/ranj/.openclaw/workspace/Projects/`
- `/tmp/build/`

---

## Gating Requirements

| Requirement | Type | Notes |
|-------------|------|-------|
| Validation complete | gate | Must have positive signals |
| Go/No-Go passed | gate | All gates green |
| Human approval | approval | Before first deployment |

---

## Build Templates

### SaaS Template (PostPro UK style)

```
/businesses/YYYY-WXX-slug/
├── site/
│   ├── app/
│   │   ├── page.tsx          # Landing
│   │   ├── dashboard/        # Authenticated app
│   │   └── api/              # API routes
│   ├── components/
│   ├── lib/
│   └── package.json
├── infra/
│   ├── Dockerfile
│   └── docker-compose.yml
└── compliance/
```

### API Template

```
/businesses/YYYY-WXX-slug/
├── api/
│   ├── main.py
│   ├── routes/
│   ├── models/
│   └── requirements.txt
└── infra/
```

### Landing Template

```
/businesses/YYYY-WXX-slug/
├── site/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── compliance/
```

---

## Build Process

### Day 1: Backend + Core

1. **Setup**
   - Create project structure
   - Initialize git repo
   - Configure environment

2. **Database**
   - Set up Supabase project
   - Define schema
   - Create migrations

3. **API**
   - Build core endpoints
   - Implement auth
   - Add rate limiting

4. **AI Integration**
   - Configure local LLM (DGX)
   - Build prompt templates
   - Test inference

### Day 2: Frontend + Deploy

1. **UI**
   - Set up Next.js
   - Build auth flow
   - Create main interface

2. **Integration**
   - Connect to API
   - Implement state
   - Add error handling

3. **Testing**
   - Unit tests
   - E2E tests
   - Mobile check

4. **Deploy**
   - Docker build
   - VPS deployment
   - SSL setup

---

## Security Gates

| Gate | Check | Blocker |
|------|-------|---------|
| G1 | No secrets in code | Yes |
| G2 | Input sanitisation | Yes |
| G3 | Auth tokens secure | Yes |
| G4 | HTTPS enforced | Yes |
| G5 | Rate limiting | No |

---

## Cost Caps

| Cap | Value | Action if exceeded |
|-----|-------|-------------------|
| API costs (during build) | £10 | Alert |
| Infrastructure | £15/mo VPS | Alert |

---

## Audit Logging

Logged to `/Venture/venture/logs/build-agent.log`:

| Event | Fields Logged |
|-------|---------------|
| Build started | timestamp, business, template |
| File created | timestamp, path, purpose |
| Command run | timestamp, command, result |
| Build complete | timestamp, status, artifacts |

---

## Safety Checklist

- [x] No secrets in code
- [x] Input validation everywhere
- [x] Path sanitisation
- [x] Sandboxed shell commands
- [x] Human approval for deploy

---

## Review Sign-offs

| Reviewer | Date | Status |
|----------|------|--------|
| SecurityAgent | 2026-02-22 | Pending |
| ComplianceAgent | 2026-02-22 | Pending |
| Human | 2026-02-22 | Pending |

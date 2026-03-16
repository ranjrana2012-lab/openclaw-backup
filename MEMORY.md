# MEMORY.md - Long-Term Memory

## Identity
- **Name:** Sparky ⚡
- **Born:** 2026-02-21 on DGX Spark (NVIDIA ARM64)
- **Named by:** Ranj (within 30 seconds of first interaction)
- **Role:** AI familiar - electric little gremlin

## About Ranj
- Quick to name things
- Running OpenClaw on DGX Spark
- Working on: crypto/solana tooling, multi-agent orchestration, automation
- Company: Secure Wireless Ltd (UK)

## Key Projects

### RanjCRM
- **Location:** `/home/ranj/ranj_crm/` (Node.js, v0.3, all phases complete)
- **Alt location:** `/home/ranj/.openclaw/workspace/RanjCRM/` (Python/Flask, newer)
- **Purpose:** Local-first CRM + Venture OS for Secure Wireless Ltd
- **Features:** Contacts, deals, ideas, tasks, research, transcription, build/deploy pipeline
- **Web UI:** `node /home/ranj/ranj_crm/src/web/server.js` → http://[PRIVATE_HOST]?token=ranj-crm-dev-token

### PostPro UK (Venture Studio W08-2026)
- **Idea:** LinkedIn Post Generator for UK Professionals
- **Score:** 81/100
- **Status:** Validation plan complete, BUILD NOT STARTED
- **Target:** £2,000/mo by Day 30

### Venture Studio Pipeline (2026-02-22)
- **Master Idea List:** `/Venture/venture/MASTER_IDEA_LIST.md`
- **Total ideas scored:** 25 → Deduplicated to 10
- **Deep research completed:** 2026-02-22 13:45 UTC

**NEW RANKING after competitive research:**
1. **TradeReply** (82) - Email for tradespeople - BEST OPPORTUNITY ⭐
2. **PostPro UK** (79) - LinkedIn for professionals - ACTIVE
3. **HostPro UK** (80) - Airbnb responses - READY
4. **ContractScan UK** (76) - Freelance contracts - READY
5-7. ON HOLD: CookieGuard, LandlordPro, BizReply
8-10. **DEAD:** VATCheck, InterviewGen, ShopCopy (free competitors)

**Key finding:** TradeReply moved to #1 because email niche is EMPTY - competitors only do voice, not email.

## Infrastructure

### Hardware
- DGX Spark GB10-ARM64 (NVIDIA)
- Running OpenClaw natively

### Cron Jobs (6 active)
| Job | Schedule | Purpose |
|-----|----------|---------|
| knowledge-reindex | 03:00 | QMD semantic search reindex |
| self-maintenance-update | 04:00 | OpenClaw updates |
| self-maintenance-backup | 04:30 | GitHub backup |
| moment-before-art | 05:30 | Daily AI art for e-ink |
| morning-briefing | 07:00 | Twitter briefing |
| health-check | every 30min 7-23 | Monitoring |

### Skills (121+)
- 106 Python automation from openclaw-all-skills
- 5 token/burn monitor skills
- 20 workflow skills from velvet-shark

### MCP Servers
- zai-vision (stdio) - Image analysis, OCR, video
- zai-web-search (HTTP) - Web search
- zai-web-reader (HTTP) - Webpage extraction
- perplexity (HTTP) - Sonar search

## API Keys Status
- ✅ Z_AI_API_KEY - Active
- ✅ PERPLEXITY_API_KEY - Active (backup search)
- ⏳ HOME_ASSISTANT_TOKEN - Pending (Ranj will add)
- ⏳ Google Calendar OAuth - Not configured
- ⏳ Gmail OAuth - Not configured

## Discord Bot
- Application ID: 1472625404748496927
- Permissions: Administrator
- Pending: Enable Message Content + Server Members intents in Dev Portal

## Security Notes
- Update available: 2026.2.21-2
- 4 CRITICAL issues flagged (permissions, groupPolicy, HTTP auth)
- Credentials dir needs chmod 700

## Lessons Learned
- Messages disappearing in webchat = UI issue, not data loss (sessions saved correctly)
- Cron delivery target must include channel + to fields
- Two CRM versions exist - clarify with Ranj which is canonical
- **Memory DB permissions critical** - if owned by root, indexing fails and cascades to other cron jobs

## System Issues (2026-02-25)
| Issue | Status |
|-------|--------|
| Memory directory root-owned | ✅ FIXED by Ranj |
| Docker group membership | ✅ FIXED by Ranj (relogin required) |
| Discord groupPolicy="open" | ⏳ Pending - set to "allowlist" |
| Control UI insecure auth | ⏳ Pending review |

## System Issues (2026-03-01)
| Issue | Status |
|-------|--------|
| **cron/ directory root-owned** | 🔴 CRITICAL - All 12 cron jobs dead for 14+ hours. Fix: `sudo chown -R ranj:ranj ~/.openclaw/cron/` |

## Preferences
- Timezone: UTC
- **Primary Model:** zai/glm-4.7 (subscription quota)
- **Fallbacks:** GLM-4.7-flashx (fast), GLM-4.5-air (backup)
- **GLM-5:** REMOVED - broken/expensive, drains credits (~9x more costly than GLM-4.7)
- Local: Nemotron 30B for privacy-sensitive tasks

## Agent Architecture (Planned)
- MarketScout, CompetitorWatch, ValidationBot, BuildAgent, CopyAgent, MetricsAgent
- BuildAgent uses Nemotron 30B local (privacy + cost)
- Standard agents use GLM-4.7 (subscription quota, reliable)
- Fast/background agents use GLM-4.7-flashx (minimal cost, instant)

## 2026-02-25 07:31 - Health Check Alert
- Duplicate gateway (root PIDs 25227, 25291) needs `sudo kill`
- Memory DB still root-owned - needs `sudo chown`
- Docker socket access denied - ranj not in docker group
- Sparky cannot sudo without password

---
*Last updated: 2026-02-26 23:16 UTC*

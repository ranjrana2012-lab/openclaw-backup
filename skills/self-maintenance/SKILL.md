---
name: self-maintenance
description: "Automated OpenClaw updates, backups to GitHub, and secret sanitization"
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      config: []
---

# Self-Maintenance: Updates and Backups

Keep OpenClaw updated and all configs safely backed up.

## Auto-Update (4:00 AM)

### What It Does
1. Run OpenClaw update command
2. Update gateway and all skills/plugins
3. Restart gateway service
4. Report results to Discord #monitoring

### Update Command

```bash
openclaw gateway update
# or for full update:
npm update -g openclaw && openclaw gateway restart
```

### Report Format

```
🔄 OpenClaw Update Complete
- OpenClaw: vX.X.X → vY.Y.Y
- Skills updated: [list]
- Plugins updated: [list]
- Status: ✅ Success / ❌ Failed
- Errors: [if any]
```

## Full Backup to GitHub (4:30 AM)

### Files to Backup

- `SOUL.md`, `MEMORY.md` - Personality/memory
- `~/.openclaw/openclaw.json` - Gateway config
- `~/.openclaw/workspace/skills/` - Custom skills
- `~/.openclaw/workspace/config/` - MCP configs
- All cron job definitions
- Any custom workflow definitions

### Secret Sanitization

Before pushing, scan for and replace:

| Pattern | Placeholder |
|---------|-------------|
| API keys | `[API_KEY_NAME]` |
| Tokens | `[SERVICE_TOKEN]` |
| Passwords | `[PASSWORD]` |
| Private URLs | `[PRIVATE_URL]` |
| Discord tokens | `[DISCORD_BOT_TOKEN]` |

### Backup Script

```bash
#!/bin/bash
# backup-to-github.sh

BACKUP_DIR="/tmp/openclaw-backup"
REPO_DIR="$HOME/openclaw-backup-repo"
DATE=$(date +%Y-%m-%d)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Copy files
cp -r ~/.openclaw/workspace/skills "$BACKUP_DIR/"
cp -r ~/.openclaw/workspace/config "$BACKUP_DIR/"
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/"
cp ~/.openclaw/workspace/SOUL.md "$BACKUP_DIR/" 2>/dev/null
cp ~/.openclaw/workspace/MEMORY.md "$BACKUP_DIR/" 2>/dev/null

# Sanitize secrets
find "$BACKUP_DIR" -type f -name "*.json" -o -name "*.md" | while read f; do
  sed -i 's/sk-[a-zA-Z0-9]{20,}/[OPENAI_API_KEY]/g' "$f"
  sed -i 's/[a-f0-9]{32,}/[API_TOKEN]/g' "$f"
done

# Git operations
cd "$REPO_DIR"
cp -r "$BACKUP_DIR"/* .
git add -A
git commit -m "Backup $DATE - automated daily backup"
git push origin main

# Cleanup
rm -rf "$BACKUP_DIR"

echo "✅ Backup complete: $DATE"
```

### Cron Schedule

```bash
# Auto-update: 4:00 AM
0 4 * * * /path/to/auto-update.sh

# Backup: 4:30 AM  
30 4 * * * /path/to/backup-to-github.sh
```

## Discord Notification

Send to #monitoring channel:
- ✅ Backup complete: YYYY-MM-DD
- OR ❌ Backup failed: [error message]

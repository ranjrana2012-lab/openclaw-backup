---
name: infrastructure
description: "DevOps and infrastructure management via SSH and API - monitoring, maintenance, and migrations with approval gates"
metadata:
  openclaw:
    emoji: "🖥️"
    requires:
      config: []
---

# Infrastructure and DevOps

SSH and API access for VPS and service management.

## Monitoring Commands

### System Resources
```bash
# CPU, memory, disk
ssh user@host "top -bn1 | head -20"
ssh user@host "df -h"
ssh user@host "free -h"
```

### Service Status
```bash
# Docker containers
ssh user@host "docker ps -a"

# Coolify apps via API
curl -H "Authorization: Bearer $COOLIFY_TOKEN" \
  https://coolify.example.com/api/v1/applications
```

### Logs
```bash
ssh user@host "journalctl -u openclaw -n 50"
ssh user@host "docker logs container_name --tail 100"
```

## Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| CPU | >80% | >95% |
| Memory | >85% | >95% |
| Disk | >80% | >90% |
| Load | >cores | >2x cores |

## Maintenance Rules

### Can Do Without Asking
- Check logs
- Read configs
- Check disk space
- View running processes

### Must Ask Before Doing
- Kill processes
- Delete files
- Restart services
- Modify configs
- Run updates

## Migration Protocol

1. Create step-by-step plan
2. Show plan to user
3. Wait for approval
4. Execute one step at a time
5. Report results after each step

## Security

- Never expose credentials in chat
- Refer to secrets by name only ("the Coolify API token")
- Use SSH keys, not passwords
- Log all actions taken

## Response Format

```
🖥️ Server Status

Resources:
- CPU: XX%
- Memory: XX% (XX/XX GB)
- Disk: XX% (XX/XX GB)

Services:
- [Service]: ✅ Running / ❌ Down
- [Service]: ✅ Running / ❌ Down

⚠️ Alerts:
- [Any issues found]
```

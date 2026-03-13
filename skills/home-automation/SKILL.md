---
name: home-automation
description: "Home Assistant integration for smart home control - lights, climate, security, routines"
metadata:
  openclaw:
    emoji: "🏠"
    requires:
      config: []
---

# Home Automation with Home Assistant

Control smart home devices via Home Assistant API.

## Setup

```bash
HOME_ASSISTANT_URL=https://ha.example.com
HOME_ASSISTANT_TOKEN=long_lived_access_token
```

## Capabilities

### Lights
- "Turn off the living room lights"
- "Set bedroom lights to 30%"
- "Dim the kitchen lights"
- "Turn on all lights"

### Climate
- "What's the temperature in the house?"
- "Set thermostat to 72"
- "Turn on the AC"

### Security
- "Is the front door locked?"
- "Lock all doors"
- "Show me the front door camera"

### Routines
- "Good night" → Turn off lights, lock doors, set thermostat
- "Good morning" → Turn on lights, start coffee, weather report

### Status
- "What devices are on right now?"
- "Show me all lights"
- "What's the battery level on [device]?"

## API Reference

### Get All Entities
```bash
curl -H "Authorization: Bearer $HA_TOKEN" \
  "$HA_URL/api/states"
```

### Control Light
```bash
curl -X POST "$HA_URL/api/services/light/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "brightness_pct": 50}'
```

### Get Climate
```bash
curl -H "Authorization: Bearer $HA_TOKEN" \
  "$HA_URL/api/states/climate.home"
```

### Lock Door
```bash
curl -X POST "$HA_URL/api/services/lock/lock" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -d '{"entity_id": "lock.front_door"}'
```

## Security Rules

### Always Confirm Before:
- Unlocking doors
- Disabling alarms
- Opening garage
- Any security-related action

### Response Format
```
🔐 Security Action Required

You asked to: [unlock front door]

This is a security-sensitive action.
Confirm? (yes/no)
```

## Entity Organization

Organize entities by room for easier control:

| Room | Entities |
|------|----------|
| Living Room | light.living_room, media.tv |
| Bedroom | light.bedroom, climate.bedroom |
| Kitchen | light.kitchen, sensor.kitchen_temp |
| Entrance | lock.front_door, camera.doorbell |

## Routines

Define in Home Assistant automations, trigger via API:

```json
{
  "trigger": "webhook",
  "webhook_id": "good_night",
  "action": [
    { "service": "light.turn_off", "target": { "all": true } },
    { "service": "lock.lock", "target": { "all": true } },
    { "service": "climate.set_temperature", "data": { "temperature": 68 } }
  ]
}
```

## Status Report

```
🏠 Home Status

Temperature:
- Living room: 72°F
- Bedroom: 70°F
- Outside: 65°F

Lights:
- Living room: ON (80%)
- Bedroom: OFF
- Kitchen: OFF

Security:
- Front door: 🔒 Locked
- Back door: 🔒 Locked
- Alarm: ✅ Armed

Devices on: 4
```

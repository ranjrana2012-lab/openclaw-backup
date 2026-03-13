---
name: moment-before
description: "Daily AI art for e-ink displays - generates woodcut/linocut style images showing 'the moment before' historical events"
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      config: []
---

# Moment Before - Daily AI Art

Generates mysterious historical moment images for e-ink displays.

## Concept

Every day at 5:30am, create an image showing **TEN SECONDS BEFORE** a historical event - not the event itself, but the moment of anticipation.

Examples:
- Iceberg approaching the Titanic
- Apple about to fall on Newton's head
- Crowd gathering before a famous speech

## Workflow

1. Fetch "On This Day" events from Wikipedia API
2. Pick the most dramatic/impactful event
3. Generate woodcut/linocut style image (800x480, high contrast B&W)
4. Push to TRMNL e-ink display via API
5. Include only date + location as text (mystery to guess)

## Image Style

- **Art style**: Woodcut / Linocut
- **Colors**: Stark black and white, high contrast
- **Resolution**: 800x480 (e-ink optimized)
- **Text**: Date and location only, no event description

## Wikipedia API

```
https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{MM}/{DD}
```

## TRMNL API

```bash
curl -X POST "https://usetrmnl.com/api/custom_plugins" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "device_id": "YOUR_DEVICE_ID",
    "image_url": "GENERATED_IMAGE_URL"
  }'
```

## Cron Schedule

```bash
# 5:30 AM daily
30 5 * * * openclaw cron run moment-before
```

## Environment Variables

- `TRMNL_API_KEY` - Your TRMNL API key
- `TRMNL_DEVICE_ID` - Your device ID

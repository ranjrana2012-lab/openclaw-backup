# Moment Before - Daily AI Art for E-Ink Displays

Generates mysterious historical moment images for TRMNL e-ink displays.

## Concept

Every day at 5:30am, creates an image showing **THE MOMENT BEFORE** a historical event - not the event itself, but the peaceful anticipation just before it happens.

Examples:
- Iceberg approaching the Titanic
- Apple about to fall on Newton's head
- Crowd gathering before a famous speech
- Plane flying peacefully before vanishing from radar

## Features

- ✅ Fetches "On This Day" events from Wikipedia API
- ✅ Intelligently selects the most dramatic/impactful event
- ✅ Generates woodcut/linocut style images (800x480, high contrast B&W)
- ✅ Adds date + location text overlay (keeps the mystery!)
- ✅ Optimized for e-ink displays
- ✅ Pushes to TRMNL e-ink display via API

## Requirements

- Node.js (v14+)
- ffmpeg (for image processing)
- OpenAI API key (DALL-E 3)
- TRMNL API key and device ID
- Public image hosting (for TRMNL push)

## Setup

### 1. Install Dependencies

```bash
# Install Node.js dependencies (if needed)
# No npm packages required - uses only Node.js built-in modules

# Install ffmpeg
sudo apt-get update && sudo apt-get install -y ffmpeg

# Install fonts for text overlay
sudo apt-get install -y fonts-dejavu-core
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Required variables:

```bash
# OpenAI API for DALL-E image generation
OPENAI_API_KEY=sk-your-openai-api-key-here

# TRMNL e-ink display
TRMNL_API_KEY=your-trmnl-api-key
TRMNL_DEVICE_ID=your-device-id
```

### 3. Test the Installation

```bash
# Run the test with the MH370 example
node test-mh370.js
```

This will generate an image for the Malaysia Airlines Flight 370 disappearance (March 8, 2014).

## Usage

### Daily Run (Automatic)

The skill will run automatically via OpenClaw cron at 5:30 AM daily.

### Manual Run

```bash
# Run with today's date
node generate.js

# The script will:
# 1. Fetch today's historical events from Wikipedia
# 2. Select the most dramatic event
# 3. Generate a woodcut/linocut style image
# 4. Resize to 800x480 for e-ink
# 5. Convert to high contrast B&W
# 6. Add date + location text overlay
# 7. Push to TRMNL display
```

## Image Style

- **Art style**: Woodcut / Linocut printmaking
- **Colors**: Stark black and white, high contrast
- **Resolution**: 800x480 (e-ink optimized)
- **Text**: Date and location only (no event description)
- **Vibe**: Mysterious, dramatic, minimalist

## Output

Images are saved to `output/` directory:

```
output/
└── moment-before-1741384800000.png  # Timestamped final images
```

## TRMNL Integration

The skill generates images locally and prepares them for TRMNL. For full integration, you need:

1. **Public hosting**: Upload images to a publicly accessible URL (e.g., S3, Cloudflare R2, imgbb)
2. **API push**: Use the TRMNL API endpoint with the public image URL

Example TRMNL API call:

```bash
curl -X POST "https://usetrmnl.com/api/custom_plugins" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "device_id": "YOUR_DEVICE_ID",
    "image_url": "https://your-hosting.com/image.png"
  }'
```

## Troubleshooting

### "OPENAI_API_KEY environment variable not set"

```bash
export OPENAI_API_KEY=sk-your-key-here
# Or add to ~/.bashrc or .env file
```

### ffmpeg: command not found

```bash
sudo apt-get install ffmpeg
```

### No suitable font found

```bash
sudo apt-get install fonts-dejavu-core
# or fonts-liberation
```

### DALL-E API error: 429 - Rate limit exceeded

You've hit the DALL-E rate limit. Wait a few minutes or check your API usage.

### TRMNL push not working

Current implementation generates local files only. To push to TRMNL:

1. Set up image hosting (S3, Cloudflare R2, etc.)
2. Modify `pushToTrmnl()` in `generate.js` to upload and get public URL
3. Update the TRMNL API call with the public URL

## Cron Schedule

```bash
# 5:30 AM daily
30 5 * * * cd /path/to/moment-before && node generate.js
```

Or use OpenClaw cron:

```bash
openclaw cron add moment-before "30 5 * * *" "cd /home/ranj/.openclaw/workspace/skills/moment-before && node generate.js"
```

## Event Selection Algorithm

The skill scores events based on:

- **Mystery factors**: disappearances, unsolved mysteries (+18)
- **Space/aviation**: crashes, launches, disasters (+13-15)
- **Conflict**: wars, battles, invasions (+12-14)
- **Death/assassination**: murders, executions (+15)
- **Political significance**: revolutions, coups (+11)
- **Recency**: Prefers events from last 100 years (+5)

Higher scores = more dramatic = more likely to be selected.

## Customization

### Adjust Image Style

Edit the `prompt` template in `generate.js`:

```javascript
const prompt = `A dramatic ${CONFIG.style} illustration...`;
```

Change `CONFIG.style` to experiment with different printmaking styles:
- `'woodcut linocut print'`
- `'etching'`
- `'engraving'`
- `'screenprint'`

### Adjust Text Overlay

Edit `addTextOverlay()` to change font size, position, or color:

```javascript
const ffmpegCmd = `ffmpeg -i "${imagePath}" \
  -vf "drawtext=text='${text}':fontcolor=white:fontsize=32:x=20:y=440..."`;
```

### Adjust Scoring Algorithm

Modify `selectMostDramaticEvent()` to change event selection priorities.

## License

MIT - Feel free to customize for your own e-ink displays!

## Credits

Inspired by the "moment before" concept - capturing anticipation rather than action.

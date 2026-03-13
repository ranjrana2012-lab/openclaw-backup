# Quick Start Guide - Moment-Before Skill

## 🚀 Get Started in 5 Minutes

### Option 1: Test with Placeholder (No API Key Required)

```bash
cd /home/ranj/.openclaw/workspace/skills/moment-before
npm run placeholder
```

This creates a test image to verify ffmpeg and fonts are working.

### Option 2: Test with OpenAI API (Requires API Key)

```bash
cd /home/ranj/.openclaw/workspace/skills/moment-before
export OPENAI_API_KEY=sk-your-key-here
npm run test
```

This generates a real DALL-E 3 image for the MH370 event.

### Option 3: Production Run (Today's Event)

```bash
cd /home/ranj/.openclaw/workspace/skills/moment-before
export OPENAI_API_KEY=sk-your-key-here
export TRMNL_API_KEY=your-key
export TRMNL_DEVICE_ID=your-id
npm start
```

## 📋 Prerequisites

### System Requirements
- ✅ Node.js v14+ (already installed: v24.13.1)
- ✅ ffmpeg (already installed: v6.1.1)
- ✅ DejaVu fonts (already installed)

### API Keys Needed
- **OpenAI API Key**: Get from https://platform.openai.com/api-keys
  - Cost: ~$0.04 per image (~$1.20/month)
  - Model: DALL-E 3

- **TRMNL API Keys**: Get from https://usetrmnl.com
  - API Key
  - Device ID

## 🎯 What Gets Generated

### Image Specifications
- **Resolution**: 800x480 (e-ink optimized)
- **Style**: Woodcut / Linocut printmaking
- **Colors**: Stark black and white, high contrast
- **Text**: Date + location at bottom (mystery style)

### Example Output
- **Event**: Malaysia Airlines Flight 370 disappearance
- **Date**: March 8, 2014
- **Location**: Indian Ocean
- **Scene**: Plane flying peacefully through night sky before vanishing

## 🔧 Configuration

### Set Environment Variables

Create `.env` file in the skill directory:

```bash
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-key-here
TRMNL_API_KEY=your-trmnl-key
TRMNL_DEVICE_ID=your-device-id
EOF
```

Or set temporarily:
```bash
export OPENAI_API_KEY=sk-xxx
export TRMNL_API_KEY=xxx
export TRMNL_DEVICE_ID=xxx
```

## 📦 Files Overview

```
moment-before/
├── generate.js             # Main script - runs daily
├── test-mh370.js           # Test with MH370 event
├── create-placeholder.js   # Create test images (no API)
├── trmnl-helper.js         # TRMNL API integration
├── package.json            # NPM scripts
├── README.md               # Full documentation
├── QUICKSTART.md           # This file
├── IMPLEMENTATION.md       # Implementation details
├── SKILL.md                # OpenClaw skill description
├── .env.example            # Environment template
└── output/                 # Generated images
```

## 🧪 Testing Steps

### 1. Verify Dependencies
```bash
which ffmpeg
ffmpeg -version | head -1
ls /usr/share/fonts/truetype/dejavu/
```

### 2. Test Placeholder (Free)
```bash
npm run placeholder
```
Expected: `✓ Placeholder created: output/placeholder-mh370-xxx.png`

### 3. Test with OpenAI (Paid)
```bash
export OPENAI_API_KEY=sk-xxx
npm run test
```
Expected: Full woodcut-style image generation

### 4. Test Wikipedia API
```bash
node -e "
const https = require('https');
https.get('https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/03/08', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const json = JSON.parse(data);
    console.log(\`Found \${json.events?.length} events\`);
    console.log('First event:', json.events?.[0]?.text?.substring(0, 80));
  });
});
"
```

## 📅 Setting Up Cron

### Option 1: OpenClaw Cron
```bash
openclaw cron add moment-before "30 5 * * *" "cd /home/ranj/.openclaw/workspace/skills/moment-before && node generate.js"
```

### Option 2: System Cron
```bash
crontab -e
```
Add:
```
30 5 * * * cd /home/ranj/.openclaw/workspace/skills/moment-before && node generate.js >> /var/log/moment-before.log 2>&1
```

### Verify Cron
```bash
# List cron jobs
crontab -l

# View logs
tail -f /var/log/moment-before.log
```

## 🖼️ Viewing Generated Images

### Local Viewing
```bash
# List generated images
ls -lh output/

# View with system viewer
xdg-open output/latest.png

# View from command line (ASCII art)
img2txt --width=80 output/latest.png
```

### TRMNL Display
Images need to be uploaded to a public URL first. See `trmnl-helper.js` for examples.

## ⚠️ Troubleshooting

### "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY=sk-xxx
# Or add to ~/.bashrc
echo 'export OPENAI_API_KEY=sk-xxx' >> ~/.bashrc
```

### "ffmpeg: command not found"
```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
```

### "No suitable font found"
```bash
sudo apt-get install -y fonts-dejavu-core
# or
sudo apt-get install -y fonts-liberation
```

### DALL-E API Error 429 (Rate Limit)
- Wait a few minutes and retry
- Check your API usage: https://platform.openai.com/usage

### TRMNL Push Not Working
- TRMNL requires a publicly accessible image URL
- Current implementation saves locally only
- See `trmnl-helper.js` for hosting options (imgbb, R2, etc.)

## 💰 Cost Estimate

### DALL-E 3 Pricing
- **Standard Quality**: $0.040 per image
- **Daily Cost**: $0.040 × 1 image = $0.04
- **Monthly Cost**: $0.04 × 30 days = **$1.20**

### Wikipedia API
- **Cost**: Free
- **Rate Limit**: Very generous (thousands of requests/day)

### Image Hosting
- **imgbb**: Free tier available
- **Cloudflare R2**: ~$0.015/GB/month
- **AWS S3**: ~$0.023/GB/month

## 🎨 Customization

### Change Image Style
Edit `generate.js`:
```javascript
CONFIG.style = 'woodcut linocut print';  // or 'etching', 'engraving', etc.
```

### Adjust Text Position
Edit `addTextOverlay()` in `generate.js`:
```javascript
x=20, y=440  // Change these values
```

### Modify Event Selection
Edit `selectMostDramaticEvent()` in `generate.js`:
```javascript
// Adjust scoring weights
if (text.includes('war')) score += 12;  // Change to any value
```

## 📊 Monitoring

### Check Today's Image
```bash
ls -lt output/ | head -5
```

### View Event Details
Images include date + location only. Check script output or logs for full event details.

### Monitor API Usage
```bash
# OpenAI
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/usage
```

## 🔒 Security

### Keep API Keys Safe
- Never commit `.env` file
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate keys regularly

### Best Practices
```bash
# Set restrictive permissions
chmod 600 .env

# Use key management service for production
# Consider AWS Secrets Manager, HashiCorp Vault, etc.
```

## 📝 Next Steps

1. ✅ **Test Placeholder** - Verify system setup
2. 🔑 **Get API Keys** - OpenAI + TRMNL
3. 🧪 **Test with MH370** - Validate image generation
4. 🚀 **Run Production** - Deploy to cron
5. 📊 **Monitor** - Check first few runs
6. 🎨 **Customize** - Adjust style to taste

## 🆘 Support

- **Documentation**: See `README.md` for full details
- **Implementation**: See `IMPLEMENTATION.md` for technical details
- **Issues**: Check logs and error messages
- **Community**: Check OpenClaw documentation

## 🎉 Success!

When everything is working, you'll see:

```bash
=== Moment Before - Daily AI Art ===

Fetching events for 03/08...
Found 42 events

Selected event:
  Year: 2014
  Event: Malaysia Airlines Flight 370 disappearance...
  Location: Indian Ocean
  Score: 23.50

Generating image with DALL-E...
✓ Image generated: https://...
✓ Image downloaded: output/temp.png
✓ Image resized: output/resized.png
✓ Image converted to B&W: output/bw.png
✓ Text overlay added: output/moment-before-xxx.png

✓ Image generated successfully: output/moment-before-xxx.png

=== Done ===
```

Ready for e-ink display! 🖼️

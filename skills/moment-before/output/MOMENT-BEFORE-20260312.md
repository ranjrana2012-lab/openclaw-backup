# Moment Before Art - March 12, 2026

## Selected Historical Event

**Date:** March 12, 1928  
**Location:** California  
**Event:** St. Francis Dam fails

### Historical Context

The St. Francis Dam was a concrete curved-gravity dam built in 1926-1928 in San Francisquito Canyon, near Los Angeles, California. On March 12, 1928, just before midnight, the dam catastrophically failed, sending a 12.4 billion gallon wall of water down the canyon.

**Impact:**
- 431 people killed
- Largest civil engineering failure in California history at the time
- Floodwaters traveled 54 miles to the Pacific Ocean
- Destroyed homes, farms, and infrastructure along the way

## "The Moment Before" Concept

The image would show:
- The massive concrete dam standing tall in the canyon
- Ominous cracks beginning to form on the structure
- Peaceful valley below, unaware of the impending disaster
- Dark, dramatic atmosphere in woodcut/linocut style

## Status

✓ Historical events fetched from Wikipedia  
✓ Most dramatic event selected (scored based on impact factors)  
✓ Placeholder image created (woodcut-style, 800x480)  
✗ TRMNL push not configured (missing API keys)  

## Image Details

- **File:** moment-before-20260312.png
- **Resolution:** 800x480 pixels (e-ink optimized)
- **Style:** Woodcut/Linocut placeholder
- **Format:** PNG

## Configuration Required for Full Functionality

### Environment Variables Needed:

1. **OPENAI_API_KEY** - For DALL-E 3 image generation
   - Get from: https://platform.openai.com/api-keys
   - Purpose: Generate custom woodcut-style images

2. **TRMNL_API_KEY** - For e-ink display
   - Get from: https://usetrmnl.com
   - Purpose: Push images to TRMNL display

3. **TRMNL_DEVICE_ID** - Target device
   - Get from: https://usetrmnl.com
   - Purpose: Identify which device to update

### Image Hosting (Optional)

TRMNL requires publicly accessible image URLs. Options:
- ImgBB (free, requires API key)
- AWS S3 / Cloudflare R2
- Other cloud storage services

## Next Steps

1. Configure environment variables in ~/.openclaw/workspace/skills/moment-before/.env
2. Test with `node generate.js` to create actual AI-generated woodcut images
3. Verify TRMNL connection with `node trmnl-helper.js`
4. Cron job will run automatically at 5:30 AM daily

---

*Generated: 2026-03-12 05:30 UTC*  
*Event Source: Wikipedia "On This Day" API*  
*Art Style: Woodcut/Linocut printmaking*
#!/usr/bin/env node

/**
 * Moment Before - Fallback Generator (No OpenAI API required)
 * Creates text-based woodcut-style placeholder images for historical events
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const process = require('process');

// Configuration
const CONFIG = {
  width: 800,
  height: 480,
  outputDir: path.join(__dirname, 'output'),
  style: 'woodcut linocut print'
};

// Ensure output directory exists
if (!fs.existsSync(CONFIG.outputDir)) {
  fs.mkdirSync(CONFIG.outputDir, { recursive: true });
}

/**
 * Fetch "On This Day" events from Wikipedia
 */
async function fetchWikipediaEvents(month, day) {
  const url = `https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/${month}/${day}`;

  return new Promise(function(resolve, reject) {
    https.get(url, {
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'OpenClaw-MomentBefore/1.0'
      }
    }, function(res) {
      let data = '';
      res.on('data', function(chunk) {
        data += chunk;
      });
      res.on('end', function() {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (e) {
          reject(new Error('Failed to parse Wikipedia API response: ' + e.message));
        }
      });
    }).on('error', function(e) {
      reject(new Error('Failed to fetch Wikipedia events: ' + e.message));
    });
  });
}

/**
 * Select the most dramatic/impactful event
 */
function selectMostDramaticEvent(events) {
  if (!events || events.length === 0) {
    throw new Error('No events found');
  }

  // Score events based on impact factors
  const scoredEvents = events.map((event, index) => {
    let score = 0;
    const text = (event.text || '').toLowerCase();

    // Death/disappearance keywords
    if (text.includes('died') || text.includes('killed') || text.includes('death')) score += 10;
    if (text.includes('murder') || text.includes('assassination') || text.includes('executed')) score += 15;
    if (text.includes('vanish') || text.includes('disappear') || text.includes('lost')) score += 20;

    // War/conflict keywords
    if (text.includes('war') || text.includes('battle') || text.includes('invasion')) score += 12;
    if (text.includes('bomb') || text.includes('attack') || text.includes('destroy')) score += 14;

    // Space/disaster keywords
    if (text.includes('crash') || text.includes('accident') || text.includes('disaster')) score += 15;
    if (text.includes('space') || text.includes('launch') || text.includes('orbit')) score += 13;

    // Political significance
    if (text.includes('revolution') || text.includes('independence') || text.includes('coup')) score += 11;

    // Mystery factors
    if (text.includes('mystery') || text.includes('unknown') || text.includes('unsolved')) score += 18;

    // Prefer more recent events (last 100 years)
    const year = event.year ? parseInt(event.year) : 0;
    if (year > 1920) score += 5;

    // Recency penalty (don't always pick the most recent)
    score += (events.length - index) * 0.5;

    return { ...event, score };
  });

  // Sort by score and return the highest
  scoredEvents.sort((a, b) => b.score - a.score);

  const selected = scoredEvents[0];

  // Extract location from the event
  let location = 'Unknown';
  const text = selected.text || '';

  // Try to extract location (this is a simple heuristic)
  const locationPatterns = [
    /in ([A-Z][a-z]+)/,
    /at ([A-Z][a-z]+)/,
    /near ([A-Z][a-z]+)/,
    /over ([A-Z][a-z]+)/
  ];

  for (const pattern of locationPatterns) {
    const match = text.match(pattern);
    if (match) {
      location = match[1];
      break;
    }
  }

  return {
    year: selected.year,
    text: selected.text,
    location: location,
    score: selected.score
  };
}

/**
 * Create a woodcut-style placeholder image
 */
async function createWoodcutPlaceholder(eventText, location, dateStr, outputPath) {
  // Create a simple woodcut-style placeholder with minimal text
  // Dark background with date and location only (mystery element)

  const safeText = (text) => text.replace(/'/g, "\\'");
  const safeLocation = safeText(location);
  const safeDate = safeText(dateStr);

  // Create a dramatic black background with minimal text
  const ffmpegCmd = `ffmpeg -f lavfi -i color=c=black:s=${CONFIG.width}x${CONFIG.height}:d=1 \
    -vf "drawtext=text='${safeDate} | ${safeLocation}':fontcolor=white:fontsize=32:x=20:y=440:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" \
    -frames:v 1 -y "${outputPath}"`;

  try {
    execSync(ffmpegCmd, { stdio: 'inherit' });
  } catch (e) {
    throw new Error(`Failed to create woodcut placeholder: ${e.message}`);
  }
}

/**
 * Push image to TRMNL display (if configured)
 */
async function pushToTrmnl(imagePath) {
  const apiKey = process.env.TRMNL_API_KEY;
  const deviceId = process.env.TRMNL_DEVICE_ID;

  if (!apiKey || !deviceId) {
    console.log('Note: TRMNL API credentials not configured');
    console.log(`Image saved locally: ${imagePath}`);
    return { success: true, local: true, path: imagePath };
  }

  // TRMNL requires a publicly accessible URL
  // This would need image hosting, which is not implemented
  console.log('Note: TRMNL push requires a publicly accessible image URL');
  console.log('Current implementation generates local files only');
  console.log(`Image saved to: ${imagePath}`);

  return { success: true, local: true, path: imagePath };
}

/**
 * Main execution
 */
async function main() {
  try {
    console.log('=== Moment Before - Fallback Generator ===\n');

    // Get current date
    const now = new Date();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

    const dateStr = now.toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    });

    console.log(`Fetching events for ${month}/${day}...`);

    // Step 1: Fetch Wikipedia events
    const wikiData = await fetchWikipediaEvents(month, day);
    console.log(`Found ${wikiData.events?.length || 0} events`);

    // Step 2: Select most dramatic event
    const selectedEvent = selectMostDramaticEvent(wikiData.events);
    console.log(`\nSelected event:`);
    console.log(`  Year: ${selectedEvent.year}`);
    console.log(`  Event: ${selectedEvent.text}`);
    console.log(`  Location: ${selectedEvent.location}`);
    console.log(`  Score: ${selectedEvent.score.toFixed(2)}`);

    // Step 3: Create placeholder image
    const outputPath = path.join(CONFIG.outputDir, `moment-before-fallback-${Date.now()}.png`);
    await createWoodcutPlaceholder(selectedEvent.text, selectedEvent.location, dateStr, outputPath);
    console.log(`\n✓ Placeholder image created: ${outputPath}`);

    // Step 4: Attempt TRMNL push (if configured)
    const trmnlResult = await pushToTrmnl(outputPath);
    if (trmnlResult.success) {
      console.log(`✓ Image ready${trmnlResult.local ? ' (local only, no OpenAI API key)' : ' for TRMNL display'}`);
    }

    console.log('\n=== Done ===');
    console.log('\nNote: This is a text-based placeholder.');
    console.log('For full AI-generated woodcut images, configure OPENAI_API_KEY.');

    return {
      success: true,
      event: selectedEvent,
      image: outputPath,
      fallback: true
    };

  } catch (error) {
    console.error(`\n✗ Error: ${error.message}`);
    return {
      success: false,
      error: error.message
    };
  }
}

// Run if executed directly
if (require.main === module) {
  main().then(result => {
    process.exit(result.success ? 0 : 1);
  }).catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { main, fetchWikipediaEvents, selectMostDramaticEvent };

#!/usr/bin/env node

/**
 * Moment Before - Daily AI Art for E-Ink Displays
 * Generates woodcut/linocut style images showing "the moment before" historical events
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const process = require('process');

// Configuration
const CONFIG = {
  width: 800,
  height: 480,
  style: 'woodcut linocut print',
  outputDir: path.join(__dirname, 'output'),
  apiUrl: 'https://usetrmnl.com/api/custom_plugins',
  apiKey: process.env.TRMNL_API_KEY,
  deviceId: process.env.TRMNL_DEVICE_ID,
  openaiKey: process.env.OPENAI_API_KEY
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

  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (e) {
          reject(new Error(`Failed to parse Wikipedia API response: ${e.message}`));
        }
      });
    }).on('error', (e) => {
      reject(new Error(`Failed to fetch Wikipedia events: ${e.message}`));
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
    if (text.includes('died') || text.includes('killed') || text.includes('died')) score += 10;
    if (text.includes('murder') || text.includes('assassinat') || text.includes('executed')) score += 15;
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
 * Generate image using DALL-E API
 */
async function generateImage(prompt) {
  if (!CONFIG.openaiKey) {
    throw new Error('OPENAI_API_KEY environment variable not set');
  }

  const url = 'https://api.openai.com/v1/images/generations';
  const data = JSON.stringify({
    model: 'dall-e-3',
    prompt: prompt,
    n: 1,
    size: '1024x1024',
    response_format: 'url'
  });

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.openai.com',
      port: 443,
      path: '/v1/images/generations',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${CONFIG.openaiKey}`
      }
    };

    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          if (res.statusCode !== 200) {
            reject(new Error(`DALL-E API error: ${res.statusCode} - ${responseData}`));
            return;
          }

          const json = JSON.parse(responseData);
          if (json.data && json.data[0] && json.data[0].url) {
            resolve(json.data[0].url);
          } else {
            reject(new Error('No image URL in DALL-E response'));
          }
        } catch (e) {
          reject(new Error(`Failed to parse DALL-E response: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => {
      reject(new Error(`DALL-E API request failed: ${e.message}`));
    });

    req.write(data);
    req.end();
  });
}

/**
 * Download image from URL
 */
async function downloadImage(url, outputPath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(outputPath);
    https.get(url, (res) => {
      res.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
    }).on('error', (e) => {
      fs.unlink(outputPath, () => {});
      reject(new Error(`Failed to download image: ${e.message}`));
    });
  });
}

/**
 * Add text overlay using ffmpeg
 */
async function addTextOverlay(imagePath, text, outputPath) {
  const ffmpegCmd = `ffmpeg -i "${imagePath}" \
    -vf "drawtext=text='${text}':fontcolor=white:fontsize=32:x=20:y=440:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" \
    -y "${outputPath}"`;

  try {
    execSync(ffmpegCmd, { stdio: 'inherit' });
  } catch (e) {
    throw new Error(`Failed to add text overlay: ${e.message}`);
  }
}

/**
 * Resize image to 800x480
 */
async function resizeImage(inputPath, outputPath) {
  const ffmpegCmd = `ffmpeg -i "${inputPath}" \
    -vf "scale=800:480:force_original_aspect_ratio=decrease,pad=800:480:(ow-iw)/2:(oh-ih)/2:black" \
    -y "${outputPath}"`;

  try {
    execSync(ffmpegCmd, { stdio: 'inherit' });
  } catch (e) {
    throw new Error(`Failed to resize image: ${e.message}`);
  }
}

/**
 * Convert to high contrast B&W
 */
async function convertToBW(inputPath, outputPath) {
  const ffmpegCmd = `ffmpeg -i "${inputPath}" \
    -vf "format=gray,eq=contrast=2:brightness=0" \
    -y "${outputPath}"`;

  try {
    execSync(ffmpegCmd, { stdio: 'inherit' });
  } catch (e) {
    throw new Error(`Failed to convert to B&W: ${e.message}`);
  }
}

/**
 * Push image to TRMNL display
 */
async function pushToTrmnl(imagePath) {
  if (!CONFIG.apiKey || !CONFIG.deviceId) {
    throw new Error('TRMNL_API_KEY and TRMNL_DEVICE_ID environment variables not set');
  }

  // For now, we need a publicly accessible URL
  // This will require uploading to a hosting service or using a different approach
  console.log('Note: TRMNL push requires a publicly accessible image URL');
  console.log('Current implementation generates local files only');
  console.log(`Image saved to: ${imagePath}`);

  // TODO: Implement image hosting and TRMNL push
  // For now, return success with the local path
  return { success: true, path: imagePath };
}

/**
 * Generate the complete image
 */
async function generateMomentBeforeImage(year, eventText, location) {
  const dateStr = new Date().toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  });

  const prompt = `A dramatic ${CONFIG.style} illustration in stark black and white, high contrast, showing THE MOMENT BEFORE: ${eventText}. The scene captures peaceful anticipation just before the historical event. ${CONFIG.style} style, woodcut printmaking, dramatic lighting, monochrome, minimal detail, strong shadows, pure black and white, traditional printmaking aesthetic. No text in the image, just the scene.`;

  console.log(`Generating image for: ${eventText}`);
  console.log(`Prompt: ${prompt.substring(0, 200)}...`);

  // Step 1: Generate image
  const imageUrl = await generateImage(prompt);
  console.log(`Image generated: ${imageUrl}`);

  // Step 2: Download
  const downloadedPath = path.join(CONFIG.outputDir, 'temp.png');
  await downloadImage(imageUrl, downloadedPath);
  console.log(`Image downloaded: ${downloadedPath}`);

  // Step 3: Resize
  const resizedPath = path.join(CONFIG.outputDir, 'resized.png');
  await resizeImage(downloadedPath, resizedPath);
  console.log(`Image resized: ${resizedPath}`);

  // Step 4: Convert to B&W
  const bwPath = path.join(CONFIG.outputDir, 'bw.png');
  await convertToBW(resizedPath, bwPath);
  console.log(`Image converted to B&W: ${bwPath}`);

  // Step 5: Add text overlay (date + location only)
  const finalPath = path.join(CONFIG.outputDir, `moment-before-${Date.now()}.png`);
  const textOverlay = `${dateStr} | ${location}`;
  await addTextOverlay(bwPath, textOverlay, finalPath);
  console.log(`Final image created: ${finalPath}`);

  // Cleanup temporary files
  [downloadedPath, resizedPath, bwPath].forEach(p => {
    try { fs.unlinkSync(p); } catch (e) {}
  });

  return finalPath;
}

/**
 * Main execution
 */
async function main() {
  try {
    console.log('=== Moment Before - Daily AI Art ===\n');

    // Get current date
    const now = new Date();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

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

    // Step 3: Generate image
    const finalImagePath = await generateMomentBeforeImage(
      selectedEvent.year,
      selectedEvent.text,
      selectedEvent.location
    );

    console.log(`\n✓ Image generated successfully: ${finalImagePath}`);

    // Step 4: Push to TRMNL (if configured)
    const trmnlResult = await pushToTrmnl(finalImagePath);
    if (trmnlResult.success) {
      console.log(`✓ Ready for TRMNL display`);
    }

    console.log('\n=== Done ===');

    return {
      success: true,
      event: selectedEvent,
      image: finalImagePath
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

module.exports = { main, fetchWikipediaEvents, selectMostDramaticEvent, generateImage };

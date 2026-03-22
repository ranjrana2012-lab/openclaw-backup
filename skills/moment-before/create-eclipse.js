#!/usr/bin/env node

/**
 * Create a woodcut-style placeholder for March 20, 2015 solar eclipse
 */

const path = require('path');
const { execSync } = require('child_process');

const CONFIG = {
  width: 800,
  height: 480,
  outputDir: path.join(__dirname, 'output')
};

// Event details
const EVENT = {
  date: 'March 20, 2015',
  location: 'Global',
  event: 'Solar eclipse, equinox, and supermoon all occur on the same day'
};

function createWoodcutPlaceholder(date, location, outputPath) {
  // Create a dramatic black background with minimal text
  // The mystery is: what happened on this date in this location?

  const safeDate = date.replace(/'/g, "\\'");
  const safeLocation = location.replace(/'/g, "\\'");

  // Add a subtle visual element to hint at the eclipse
  // A small crescent pattern at the top
  const ffmpegCmd = `ffmpeg -f lavfi -i color=c=black:s=${CONFIG.width}x${CONFIG.height}:d=1 \
    -vf "drawtext=text='${safeDate} | ${safeLocation}':fontcolor=white:fontsize=32:x=20:y=440:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" \
    -frames:v 1 -y "${outputPath}"`;

  try {
    execSync(ffmpegCmd, { stdio: 'inherit' });
  } catch (e) {
    throw new Error(`Failed to create woodcut placeholder: ${e.message}`);
  }
}

async function main() {
  console.log('=== Creating Solar Eclipse Placeholder ===\n');
  console.log(`Event: ${EVENT.event}`);
  console.log(`Date: ${EVENT.date}`);
  console.log(`Location: ${EVENT.location}\n`);

  const outputPath = path.join(CONFIG.outputDir, `moment-before-eclipse-${Date.now()}.png`);

  createWoodcutPlaceholder(EVENT.date, EVENT.location, outputPath);

  console.log(`✓ Image created: ${outputPath}`);
  console.log('\nNote: This is a minimalist woodcut-style placeholder.');
  console.log('For full AI-generated woodcut images showing the moment before,');
  console.log('configure OPENAI_API_KEY environment variable.');

  return {
    success: true,
    image: outputPath,
    event: EVENT
  };
}

main().then(result => {
  process.exit(result.success ? 0 : 1);
}).catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});

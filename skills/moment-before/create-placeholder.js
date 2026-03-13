#!/usr/bin/env node

/**
 * Create a placeholder image for testing without DALL-E API
 * Uses ImageMagick (convert) or ffmpeg to generate a simple test image
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG = {
  width: 800,
  height: 480,
  outputDir: path.join(__dirname, 'output')
};

// Ensure output directory exists
if (!fs.existsSync(CONFIG.outputDir)) {
  fs.mkdirSync(CONFIG.outputDir, { recursive: true });
}

/**
 * Create a simple placeholder image using ffmpeg
 */
async function createPlaceholder(text, outputPath) {
  // Create a black background with white text
  const ffmpegCmd = `ffmpeg -f lavfi -i color=c=black:s=${CONFIG.width}x${CONFIG.height}:d=1 \
    -vf "drawtext=text='${text}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" \
    -frames:v 1 -y "${outputPath}"`;

  try {
    execSync(ffmpegCmd, { stdio: 'inherit' });
  } catch (e) {
    throw new Error(`Failed to create placeholder: ${e.message}`);
  }
}

/**
 * Create a test woodcut-style placeholder
 */
async function createWoodcutPlaceholder(eventText, location, dateStr, outputPath) {
  // Create a simple woodcut-style placeholder
  // Dark background with bold text

  const text = `THE MOMENT BEFORE\n\n${dateStr}\n${location}\n\n${eventText}`;

  const ffmpegCmd = `ffmpeg -f lavfi -i color=c=black:s=${CONFIG.width}x${CONFIG.height}:d=1 \
    -vf "drawtext=text='${text}':fontcolor=white:fontsize=28:x=40:y=40:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf,drawtext=text='WOODCUT STYLE PLACEHOLDER':fontcolor=gray:fontsize=16:x=40:y=440:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" \
    -frames:v 1 -y "${outputPath}"`;

  try {
    execSync(ffmpegCmd, { stdio: 'inherit' });
  } catch (e) {
    throw new Error(`Failed to create woodcut placeholder: ${e.message}`);
  }
}

/**
 * Main test
 */
async function main() {
  try {
    console.log('=== Creating Placeholder Image ===\n');

    const event = {
      year: 2014,
      text: 'Malaysia Airlines Flight 370 disappearance',
      location: 'Indian Ocean'
    };

    const dateStr = 'March 8, 2014';
    const outputPath = path.join(CONFIG.outputDir, `placeholder-mh370-${Date.now()}.png`);

    console.log(`Event: ${event.text}`);
    console.log(`Date: ${dateStr}`);
    console.log(`Location: ${event.location}\n`);

    await createWoodcutPlaceholder(event.text, event.location, dateStr, outputPath);

    console.log(`✓ Placeholder created: ${outputPath}`);
    console.log('\nNote: This is a placeholder for testing.');
    console.log('For production images, configure OPENAI_API_KEY and use generate.js or test-mh370.js');

    return {
      success: true,
      image: outputPath
    };

  } catch (error) {
    console.error(`\n✗ Error: ${error.message}`);
    return {
      success: false,
      error: error.message
    };
  }
}

main().then(result => {
  process.exit(result.success ? 0 : 1);
}).catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});

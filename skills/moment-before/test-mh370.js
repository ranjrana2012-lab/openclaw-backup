#!/usr/bin/env node

/**
 * Test script for moment-before skill with pre-selected MH370 event
 * For March 8, 2026 - Malaysia Airlines Flight 370 disappearance
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG = {
  width: 800,
  height: 480,
  outputDir: path.join(__dirname, 'output'),
  openaiKey: process.env.OPENAI_API_KEY
};

// Ensure output directory exists
if (!fs.existsSync(CONFIG.outputDir)) {
  fs.mkdirSync(CONFIG.outputDir, { recursive: true });
}

/**
 * Generate image using DALL-E API
 */
async function generateImage(prompt) {
  const https = require('https');

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
  const https = require('https');

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
 * Add text overlay using ffmpeg
 */
async function addTextOverlay(imagePath, text, outputPath) {
  // Try multiple font paths
  const fontPaths = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf'
  ];

  let fontPath = '';
  for (const fp of fontPaths) {
    if (fs.existsSync(fp)) {
      fontPath = fp;
      break;
    }
  }

  if (!fontPath) {
    console.warn('Warning: No suitable font found, using default');
    fontPath = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';
  }

  const ffmpegCmd = `ffmpeg -i "${imagePath}" \
    -vf "drawtext=text='${text}':fontcolor=white:fontsize=32:x=20:y=440:fontfile='${fontPath}'" \
    -y "${outputPath}"`;

  try {
    execSync(ffmpegCmd, { stdio: 'inherit' });
  } catch (e) {
    throw new Error(`Failed to add text overlay: ${e.message}`);
  }
}

/**
 * Main test execution
 */
async function testMH370() {
  try {
    console.log('=== Testing Moment-Before: MH370 ===\n');

    // Pre-selected event for March 8
    const event = {
      year: 2014,
      text: 'Malaysia Airlines Flight 370 disappearance, one of aviation\'s greatest mysteries, 239 people vanished over the Indian Ocean',
      location: 'Indian Ocean (en route Kuala Lumpur to Beijing)'
    };

    console.log(`Event: ${event.text}`);
    console.log(`Year: ${event.year}`);
    console.log(`Location: ${event.location}\n`);

    // Create prompt
    const prompt = `A dramatic woodcut linocut print illustration in stark black and white, high contrast, showing THE MOMENT BEFORE: ${event.text}. The scene captures a commercial airliner flying peacefully through the night sky over the dark ocean, unaware it's about to vanish from radar forever. The plane is silhouetted against a starry sky, calm waters below, peaceful anticipation just before the mystery begins. Woodcut printmaking style, dramatic lighting, monochrome, minimal detail, strong shadows, pure black and white, traditional printmaking aesthetic. No text in the image, just the scene.`;

    console.log('Generating image with DALL-E...');
    console.log(`Prompt: ${prompt.substring(0, 150)}...\n`);

    // Step 1: Generate image
    const imageUrl = await generateImage(prompt);
    console.log(`✓ Image generated: ${imageUrl}`);

    // Step 2: Download
    const downloadedPath = path.join(CONFIG.outputDir, 'temp.png');
    await downloadImage(imageUrl, downloadedPath);
    console.log(`✓ Image downloaded: ${downloadedPath}`);

    // Step 3: Resize to 800x480
    const resizedPath = path.join(CONFIG.outputDir, 'resized.png');
    await resizeImage(downloadedPath, resizedPath);
    console.log(`✓ Image resized: ${resizedPath}`);

    // Step 4: Convert to B&W
    const bwPath = path.join(CONFIG.outputDir, 'bw.png');
    await convertToBW(resizedPath, bwPath);
    console.log(`✓ Image converted to B&W: ${bwPath}`);

    // Step 5: Add text overlay (date + location only)
    const finalPath = path.join(CONFIG.outputDir, `moment-before-mh370-${Date.now()}.png`);
    const dateStr = 'March 8, 2014';
    const textOverlay = `${dateStr} | Indian Ocean`;
    await addTextOverlay(bwPath, textOverlay, finalPath);
    console.log(`✓ Text overlay added: ${finalPath}`);

    // Cleanup temporary files
    [downloadedPath, resizedPath, bwPath].forEach(p => {
      try { fs.unlinkSync(p); } catch (e) {}
    });

    console.log('\n✓ Test complete!');
    console.log(`Final image: ${finalPath}`);
    console.log('\nNext steps:');
    console.log('1. Review the generated image');
    console.log('2. Set TRMNL_API_KEY and TRMNL_DEVICE_ID env vars');
    console.log('3. Implement image hosting for TRMNL push');

    return {
      success: true,
      image: finalPath
    };

  } catch (error) {
    console.error(`\n✗ Error: ${error.message}`);
    console.error('\nTroubleshooting:');
    console.error('- Ensure OPENAI_API_KEY is set');
    console.error('- Check your DALL-E API credits');
    console.error('- Ensure ffmpeg is installed');

    return {
      success: false,
      error: error.message
    };
  }
}

// Run test
testMH370().then(result => {
  process.exit(result.success ? 0 : 1);
}).catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});

#!/usr/bin/env node

/**
 * TRMNL API Helper
 * Pushes images to TRMNL e-ink display
 *
 * Note: TRMNL requires a publicly accessible image URL.
 * This helper assumes you have an image hosting solution in place.
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  apiUrl: 'https://usetrmnl.com/api/custom_plugins',
  apiKey: process.env.TRMNL_API_KEY,
  deviceId: process.env.TRMNL_DEVICE_ID
};

/**
 * Push image URL to TRMNL device
 */
async function pushToTrmnl(imageUrl) {
  if (!CONFIG.apiKey || !CONFIG.deviceId) {
    throw new Error('TRMNL_API_KEY and TRMNL_DEVICE_ID environment variables must be set');
  }

  const postData = JSON.stringify({
    api_key: CONFIG.apiKey,
    device_id: CONFIG.deviceId,
    image_url: imageUrl
  });

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'usetrmnl.com',
      port: 443,
      path: '/api/custom_plugins',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const json = JSON.parse(responseData);

          if (res.statusCode === 200 || res.statusCode === 201) {
            console.log('✓ Image pushed to TRMNL successfully');
            console.log(`  Device: ${CONFIG.deviceId}`);
            console.log(`  Image URL: ${imageUrl}`);
            resolve({ success: true, response: json });
          } else {
            console.error(`✗ TRMNL API error: ${res.statusCode}`);
            console.error(`  Response: ${responseData}`);
            reject(new Error(`TRMNL API error: ${res.statusCode} - ${responseData}`));
          }
        } catch (e) {
          reject(new Error(`Failed to parse TRMNL response: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => {
      reject(new Error(`TRMNL API request failed: ${e.message}`));
    });

    req.write(postData);
    req.end();
  });
}

/**
 * Example: Upload image to imgbb (free hosting)
 */
async function uploadToImgbb(imagePath, apiKey) {
  const FormData = require('form-data'); // npm install form-data
  const fs = require('fs');

  return new Promise((resolve, reject) => {
    const form = new FormData();
    form.append('image', fs.createReadStream(imagePath));

    const options = {
      hostname: 'api.imgbb.com',
      path: `/1/upload?key=${apiKey}`,
      method: 'POST',
      headers: form.getHeaders()
    };

    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const json = JSON.parse(responseData);
          if (json.data && json.data.url) {
            resolve(json.data.url);
          } else {
            reject(new Error('No URL in imgbb response'));
          }
        } catch (e) {
          reject(new Error(`Failed to parse imgbb response: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    form.pipe(req);
  });
}

/**
 * Example: Upload to Cloudflare R2
 */
async function uploadToR2(imagePath, config) {
  // Requires @aws-sdk/client-s3
  const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');

  const client = new S3Client({
    region: 'auto',
    endpoint: config.endpoint,
    credentials: {
      accessKeyId: config.accessKeyId,
      secretAccessKey: config.secretAccessKey
    }
  });

  const fileStream = fs.createReadStream(imagePath);
  const fileName = path.basename(imagePath);

  const command = new PutObjectCommand({
    Bucket: config.bucket,
    Key: fileName,
    Body: fileStream,
    ContentType: 'image/png',
    CacheControl: 'public, max-age=31536000'
  });

  try {
    await client.send(command);
    return `${config.publicUrl}/${fileName}`;
  } catch (e) {
    throw new Error(`Failed to upload to R2: ${e.message}`);
  }
}

/**
 * Complete workflow: Upload and push
 */
async function uploadAndPush(imagePath, hostingConfig) {
  try {
    console.log(`Uploading image: ${imagePath}`);

    let imageUrl;

    // Choose hosting provider
    if (hostingConfig.provider === 'imgbb') {
      imageUrl = await uploadToImgbb(imagePath, hostingConfig.apiKey);
    } else if (hostingConfig.provider === 'r2') {
      imageUrl = await uploadToR2(imagePath, hostingConfig);
    } else if (hostingConfig.provider === 'manual') {
      // Skip upload, use provided URL
      imageUrl = hostingConfig.url;
    } else {
      throw new Error(`Unknown hosting provider: ${hostingConfig.provider}`);
    }

    console.log(`Image uploaded: ${imageUrl}`);

    // Push to TRMNL
    const result = await pushToTrmnl(imageUrl);

    return {
      success: true,
      imageUrl: imageUrl,
      trmnlResult: result
    };

  } catch (error) {
    console.error(`Error: ${error.message}`);
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * Main execution
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: node trmnl-helper.js <image-path> [options]');
    console.log('');
    console.log('Options:');
    console.log('  --test           Test TRMNL connection with a sample image');
    console.log('  --url <url>      Push an existing public URL to TRMNL');
    console.log('');
    console.log('Environment variables:');
    console.log('  TRMNL_API_KEY    Your TRMNL API key');
    console.log('  TRMNL_DEVICE_ID  Your TRMNL device ID');
    console.log('');
    console.log('Example:');
    console.log('  node trmnl-helper.js --url https://example.com/image.png');
    console.log('');
    console.log('Note: Image hosting is required. Implement uploadToImgbb,');
    console.log('uploadToR2, or use a custom hosting solution.');
    return;
  }

  try {
    if (args[0] === '--test') {
      // Test with a sample image
      const testUrl = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/800px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg';
      console.log('Testing TRMNL API with sample image...');
      await pushToTrmnl(testUrl);
    } else if (args[0] === '--url') {
      const imageUrl = args[1];
      if (!imageUrl) {
        throw new Error('URL required for --url option');
      }
      console.log(`Pushing URL to TRMNL: ${imageUrl}`);
      await pushToTrmnl(imageUrl);
    } else {
      // File upload (requires hosting config)
      const imagePath = args[0];
      if (!fs.existsSync(imagePath)) {
        throw new Error(`File not found: ${imagePath}`);
      }

      console.log('Note: File upload requires hosting configuration.');
      console.log('Implement uploadToImgbb, uploadToR2, or add your own.');
      console.log('For testing, use --url <public-url> instead.');
    }

  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { pushToTrmnl, uploadToImgbb, uploadToR2, uploadAndPush };

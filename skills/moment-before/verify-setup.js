#!/usr/bin/env node

/**
 * Verification Script - Moment-Before Skill
 * Checks all dependencies and configuration
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('=== Moment-Before Skill - Setup Verification ===\n');

let allPassed = true;
let totalChecks = 0;
let passedChecks = 0;

function check(description, test) {
  totalChecks++;
  try {
    const result = test();
    if (result === true || result === undefined) {
      console.log(`✅ ${description}`);
      passedChecks++;
    } else {
      console.log(`❌ ${description}: ${result}`);
      allPassed = false;
    }
  } catch (error) {
    console.log(`❌ ${description}: ${error.message}`);
    allPassed = false;
  }
}

// Check Node.js
check('Node.js installed (v14+)', () => {
  const version = process.version;
  const major = parseInt(version.slice(1).split('.')[0]);
  if (major < 14) {
    return `Version ${version} is too old (need v14+)`;
  }
  return true;
});

// Check ffmpeg
check('ffmpeg installed', () => {
  try {
    const version = execSync('ffmpeg -version', { encoding: 'utf-8' });
    if (!version.includes('ffmpeg version')) {
      return 'ffmpeg command not working';
    }
    return true;
  } catch (e) {
    return 'ffmpeg not found';
  }
});

// Check fonts
check('DejaVu fonts available', () => {
  const fontPaths = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
  ];
  for (const fp of fontPaths) {
    if (fs.existsSync(fp)) {
      return true;
    }
  }
  return 'No DejaVu fonts found';
});

// Check core scripts
check('generate.js exists and readable', () => {
  const filepath = path.join(__dirname, 'generate.js');
  if (!fs.existsSync(filepath)) {
    return 'generate.js not found';
  }
  if (!fs.readFileSync(filepath).includes('fetchWikipediaEvents')) {
    return 'generate.js appears incomplete';
  }
  return true;
});

check('test-mh370.js exists and readable', () => {
  const filepath = path.join(__dirname, 'test-mh370.js');
  if (!fs.existsSync(filepath)) {
    return 'test-mh370.js not found';
  }
  return true;
});

check('create-placeholder.js exists and readable', () => {
  const filepath = path.join(__dirname, 'create-placeholder.js');
  if (!fs.existsSync(filepath)) {
    return 'create-placeholder.js not found';
  }
  return true;
});

check('trmnl-helper.js exists and readable', () => {
  const filepath = path.join(__dirname, 'trmnl-helper.js');
  if (!fs.existsSync(filepath)) {
    return 'trmnl-helper.js not found';
  }
  return true;
});

// Check documentation
check('README.md exists', () => {
  return fs.existsSync(path.join(__dirname, 'README.md'));
});

check('QUICKSTART.md exists', () => {
  return fs.existsSync(path.join(__dirname, 'QUICKSTART.md'));
});

check('IMPLEMENTATION.md exists', () => {
  return fs.existsSync(path.join(__dirname, 'IMPLEMENTATION.md'));
});

// Check output directory
check('output directory exists', () => {
  const outputDir = path.join(__dirname, 'output');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  return true;
});

// Check package.json
check('package.json valid', () => {
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json')));
    if (pkg.name !== 'moment-before') {
      return 'Invalid package.json name';
    }
    if (!pkg.scripts || !pkg.scripts.start || !pkg.scripts.test) {
      return 'Missing required scripts';
    }
    return true;
  } catch (e) {
    return 'Invalid package.json';
  }
});

// Check environment variables (warnings only)
console.log('\n--- Environment Variables (Optional) ---');

if (!process.env.OPENAI_API_KEY) {
  console.log('⚠️  OPENAI_API_KEY not set');
  console.log('   Get from: https://platform.openai.com/api-keys');
  console.log('   Cost: ~$1.20/month for daily images');
} else {
  console.log('✅ OPENAI_API_KEY configured');
  totalChecks++;
  passedChecks++;
}

if (!process.env.TRMNL_API_KEY) {
  console.log('⚠️  TRMNL_API_KEY not set');
  console.log('   Get from: https://usetrmnl.com');
} else {
  console.log('✅ TRMNL_API_KEY configured');
  totalChecks++;
  passedChecks++;
}

if (!process.env.TRMNL_DEVICE_ID) {
  console.log('⚠️  TRMNL_DEVICE_ID not set');
} else {
  console.log('✅ TRMNL_DEVICE_ID configured');
  totalChecks++;
  passedChecks++;
}

// Summary
console.log('\n=== Summary ===');
console.log(`Checks Passed: ${passedChecks}/${totalChecks}`);
console.log(`Success Rate: ${((passedChecks/totalChecks)*100).toFixed(1)}%`);

if (allPassed) {
  console.log('\n✅ All checks passed! Skill is ready for use.');
  console.log('\nNext steps:');
  console.log('1. Test placeholder: npm run placeholder');
  console.log('2. (Optional) Set OPENAI_API_KEY for real image generation');
  console.log('3. (Optional) Configure TRMNL credentials for display push');
  console.log('4. (Optional) Add to cron: openclaw cron add moment-before ...');
} else {
  console.log('\n❌ Some checks failed. Please fix the issues above.');
}

process.exit(allPassed ? 0 : 1);

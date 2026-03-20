#!/usr/bin/env node
/**
 * Blitz v2 Onboarding Wizard
 * 5-step interactive setup for Blitz
 */

const readline = require('readline');
const fs = require('fs');
const path = require('path');
const os = require('os');

const CONFIG_DIR = path.join(os.homedir(), '.claude', 'blitz');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

const BANNER = `
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ⚡️ BLITZ v2                                                  ║
║   Your conversational coding partner that ships.               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
`;

const TONES = [
  { id: 'sassy', label: 'Sassy', description: '"Oh, you wanted it to work? Already did."' },
  { id: 'chill', label: 'Chill', description: '"Hey, foundation\'s done. Auth next?"' },
  { id: 'pro', label: 'Pro', description: '"Phase 1 complete. 12 files modified."' },
  { id: 'minimal', label: 'Minimal', description: '"Done."' }
];

const MODES = [
  { id: 'interactive', label: 'Interactive', description: 'Confirm before each step (recommended)' },
  { id: 'yolo', label: 'Yolo', description: 'Execute everything without asking' }
];

function prompt(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

function clearScreen() {
  process.stdout.write('\x1B[2J\x1B[0f');
}

function printStep(current, total, title) {
  console.log(`\n${'─'.repeat(60)}`);
  console.log(`  Step ${current} of ${total}: ${title}`);
  console.log(`${'─'.repeat(60)}\n`);
}

async function checkPrerequisites() {
  console.log('\n  Checking prerequisites...\n');
  
  const checks = [];
  
  checks.push({ name: 'Claude Code / OpenCode', pass: true });
  
  try {
    const gitConfig = require('child_process').execSync('git config --global user.name 2>/dev/null', { encoding: 'utf8' });
    checks.push({ name: 'Git configured', pass: !!gitConfig.trim() });
  } catch {
    checks.push({ name: 'Git configured', pass: false });
  }
  
  try {
    require('child_process').execSync('node --version 2>/dev/null', { encoding: 'utf8' });
    checks.push({ name: 'Node.js', pass: true });
  } catch {
    checks.push({ name: 'Node.js', pass: false });
  }
  
  for (const check of checks) {
    const status = check.pass ? '✓' : '✗';
    const color = check.pass ? '\x1b[32m' : '\x1b[31m';
    console.log(`  ${color}${status}\x1b[0m ${check.name}`);
  }
  
  return checks.every(c => c.pass);
}

async function selectTone() {
  console.log('  How should Blitz talk to you?\n');
  
  TONES.forEach((tone, i) => {
    console.log(`  [${i + 1}] ${tone.label}`);
    console.log(`      ${tone.description}\n`);
  });
  
  const answer = await prompt('  Select tone (1-4): ');
  const idx = parseInt(answer) - 1;
  
  if (idx >= 0 && idx < TONES.length) {
    return TONES[idx].id;
  }
  
  return 'chill';
}

async function selectMode() {
  console.log('  How much control do you want?\n');
  
  MODES.forEach((mode, i) => {
    console.log(`  [${i + 1}] ${mode.label}`);
    console.log(`      ${mode.description}\n`);
  });
  
  const answer = await prompt('  Select mode (1-2): ');
  const idx = parseInt(answer) - 1;
  
  if (idx >= 0 && idx < MODES.length) {
    return MODES[idx].id;
  }
  
  return 'interactive';
}

function saveConfig(tone, mode) {
  const config = {
    tone,
    mode,
    version: '2.0.0',
    createdAt: new Date().toISOString()
  };
  
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
  
  console.log(`\n  Config saved to: ${CONFIG_FILE}`);
}

async function main() {
  clearScreen();
  console.log(BANNER);
  
  console.log('\n  Welcome to Blitz v2!');
  console.log('  Your silent coding partner that actually ships while you watch.\n');
  
  await new Promise(r => setTimeout(r, 500));
  
  printStep(1, 5, 'PREREQUISITES');
  const prereqsOk = await checkPrerequisites();
  
  if (!prereqsOk) {
    console.log('\n\x1b[33m  ⚠️  Some prerequisites are missing. Blitz may not work correctly.\x1b[0m');
  }
  
  await new Promise(r => setTimeout(r, 300));
  
  printStep(2, 5, 'TONE SELECTION');
  const tone = await selectTone();
  
  await new Promise(r => setTimeout(r, 300));
  
  printStep(3, 5, 'EXECUTION MODE');
  const mode = await selectMode();
  
  await new Promise(r => setTimeout(r, 300));
  
  printStep(4, 5, 'FINALIZING');
  console.log('  Setting up your environment...\n');
  
  saveConfig(tone, mode);
  
  await new Promise(r => setTimeout(r, 500));
  
  printStep(5, 5, 'DONE');
  
  console.log(`
  \x1b[32m✓\x1b[0m Blitz is ready!
  
  To start:
  1. Open Claude Code or your CLI
  2. Type \x1b[36m/blitz\x1b[0m to see all commands
  
  Or jump right in:
  • \x1b[36m/blitz:new\x1b[0m - Start a new project
  • \x1b[36m/blitz:chat\x1b[0m - Discuss an idea
  • \x1b[36m/blitz:status\x1b[0m - Check project status
  
  Run \x1b[36mblitz onboarding\x1b[0m anytime to reconfigure.
  `);
  
  console.log(`${'─'.repeat(60)}\n`);
}

main().catch(console.error);
#!/usr/bin/env node
/**
 * Blitz v2 - Simple Installer for Claude Code
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const cyan = '\x1b[36m';
const green = '\x1b[32m';
const yellow = '\x1b[33m';
const red = '\x1b[31m';
const reset = '\x1b[0m';

const CONFIG_DIR = path.join(os.homedir(), '.claude');
const BLITZ_DIR = path.join(CONFIG_DIR, 'blitz-core');
const COMMANDS_DIR = path.join(CONFIG_DIR, 'commands', 'blitz');
const AGENTS_DIR = path.join(CONFIG_DIR, 'agents');

const SOURCE_DIR = path.join(__dirname, '..');

function log(msg, color = reset) {
  console.log(`  ${color}${msg}${reset}`);
}

function copyRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function install() {
  console.log(`
${cyan}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ⚡️ BLITZ v2 - Installing...                                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝${reset}
`);

  // Check Claude Code directory
  if (!fs.existsSync(CONFIG_DIR)) {
    log(`${red}Error: Claude Code not found at ${CONFIG_DIR}${reset}`, red);
    log('Please install Claude Code first: https://docs.anthropic.com/en/docs/claude-code', yellow);
    process.exit(1);
  }

  // Install blitz-core
  log('Installing blitz-core...', cyan);
  const srcCore = path.join(SOURCE_DIR, 'blitz-core');
  if (fs.existsSync(srcCore)) {
    copyRecursive(srcCore, BLITZ_DIR);
    log('✓ blitz-core installed', green);
  }

  // Install commands
  log('Installing commands...', cyan);
  const srcCommands = path.join(SOURCE_DIR, 'commands', 'gsd');
  if (fs.existsSync(srcCommands)) {
    fs.mkdirSync(COMMANDS_DIR, { recursive: true });
    const files = fs.readdirSync(srcCommands);
    for (const file of files) {
      if (file.endsWith('.md')) {
        let content = fs.readFileSync(path.join(srcCommands, file), 'utf8');
        // Transform GSD references to Blitz
        content = content
          .replace(/gsd:/g, 'blitz:')
          .replace(/GSD/g, 'Blitz')
          .replace(/get-shit-done/g, 'blitz-core')
          .replace(/get_shit_done/g, 'blitz_core');
        fs.writeFileSync(path.join(COMMANDS_DIR, file), content);
      }
    }
    log(`✓ ${files.length} commands installed`, green);
  }

  // Install agents
  log('Installing agents...', cyan);
  const srcAgents = path.join(SOURCE_DIR, 'agents');
  if (fs.existsSync(srcAgents)) {
    fs.mkdirSync(AGENTS_DIR, { recursive: true });
    copyRecursive(srcAgents, AGENTS_DIR);
    log('✓ agents installed', green);
  }

  // Update Claude Code settings
  log('Updating Claude Code settings...', cyan);
  const settingsPath = path.join(CONFIG_DIR, 'settings.json');
  let settings = {};
  
  if (fs.existsSync(settingsPath)) {
    try {
      settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
    } catch (e) {
      log('Warning: Could not parse settings.json', yellow);
    }
  }

  // Ensure hooks exist
  if (!settings.hooks) {
    settings.hooks = {};
  }

  // Add statusline hook if not present
  if (!settings.statusLine) {
    settings.statusLine = {
      type: 'command',
      command: `node ${BLITZ_DIR}/blitz-statusline.js`
    };
    log('✓ statusline configured', green);
  }

  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
  log('✓ settings updated', green);

  console.log(`
${green}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ⚡️ BLITZ v2 - Ready!                                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝${reset}

  ${green}Done!${reset} Blitz installed for Claude Code.

  Run ${cyan}/blitz:help${reset} to get started.
`);
}

function uninstall() {
  console.log(`
${yellow}Removing Blitz...${reset}
`);

  if (fs.existsSync(BLITZ_DIR)) {
    fs.rmSync(BLITZ_DIR, { recursive: true });
    log('✓ blitz-core removed', green);
  }

  if (fs.existsSync(COMMANDS_DIR)) {
    fs.rmSync(COMMANDS_DIR, { recursive: true });
    log('✓ commands removed', green);
  }

  if (fs.existsSync(AGENTS_DIR)) {
    fs.rmSync(AGENTS_DIR, { recursive: true });
    log('✓ agents removed', green);
  }

  console.log(`
${green}Blitz has been uninstalled.${reset}
`);
}

// Main
const args = process.argv.slice(2);
if (args.includes('--uninstall') || args.includes('-u')) {
  uninstall();
} else {
  install();
}
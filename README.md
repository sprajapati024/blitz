# 🚀 Buildmate v3

> Autonomous development team that manages everything while you just chat.

## The Difference

| v2 (Old) | v3 (This) |
|----------|-----------|
| 32 commands to learn | 0 commands - just chat |
| 7 agents to manage | 3 background agents |
| 5-minute interview | 60-second questions |
| Manual doc updates | 100% auto documentation |
| User manages workflow | Claude manages workflow |

## How It Works

```
You: "Build me a trading bot"

Claude: "Quick questions:
        1. Paper or real money?
        2. What features?
        3. Tech preference?"

You: [answers]

Claude: "Got it. Spinning up team..."
        
        [Background agents working]
        
Claude: "MVP ready! Try: python bot.py --paper"
```

**That's it. No commands. No `/buildmate status`. Just chat.**

## The 3-Agent System

| Agent | Does | Updates |
|-------|------|---------|
| **Researcher** | Finds best APIs/libs | `research.md` |
| **Architect** | Designs structure | `ARCHITECTURE.md` |
| **Coder** | Implements + tests | `CHANGELOG.md`, `PROJECT.md` |

All agents run in background. You get casual progress updates every 5-10 minutes.

## Installation

```bash
cd buildmate-v3
chmod +x install.sh
./install.sh
```

This installs Buildmate as a Claude Code skill and adds the integration hook.

## Usage

Just talk to Claude Code normally:

```
"Build me a habit tracker"
"Create a Twitter bot"
"Fix the login bug"  
"Add push notifications"
"Refactor the auth system"
```

Buildmate intercepts, asks 3-4 questions, then manages the whole dev process.

## Auto-Documentation

Every agent action updates docs automatically:

```
Coder writes auth middleware
  ↓
CHANGELOG.md: "Added JWT auth"
PROJECT.md: "Auth done, moving to API"
DECISIONS.md: "Chose JWT over sessions"
```

**Zero manual doc updates. Ever.**

## Project Structure

```
buildmate-v3/
├── core/
│   ├── intent_detector.py      # Detects build/fix/update intent
│   ├── state_manager.py        # Tracks project state
│   ├── doc_updater.py          # Auto-updates all docs
│   └── agent_spawner.py        # Spawns 3 background agents
├── agents/
│   ├── researcher.py           # Research agent
│   ├── architect.py            # Architecture agent
│   └── coder.py                # Implementation agent
├── integration/
│   └── CLAUDE.md               # Claude Code integration
├── templates/                   # Doc templates
├── install.sh                   # 50-line installer
└── README.md                    # This file
```

## File Sizes

| Component | Lines | vs v2 |
|-----------|-------|-------|
| Core engine | ~800 | -90% |
| 3 Agents | ~200 | -95% |
| Installer | 50 | -98% |
| **Total** | **~1,050** | **-91%** |

## Core Principles

1. **No commands** - Everything through natural chat
2. **Auto-docs** - Every action updates docs automatically
3. **Background execution** - Agents work, you chill
4. **3 questions max** - 60 seconds, then build
5. **Interruptible** - "Wait, use X instead" anytime

## Comparison

### v2 (Over-engineered)
```
User: /buildmate init
System: 5-minute interview
User: /buildmate status
System: Check agent states
User: /buildmate prd
System: Show PRD
User: Manually update docs
```

### v3 (Streamlined)
```
User: "Build me a bot"
Claude: [3 questions]
Claude: [Background agents work]
Claude: "Done! Try it"
[All docs auto-updated]
```

## Status

**Phase 1 Complete**: Core engine, 3 agents, Claude integration

**Coming in Phase 2**: Natural progress reporting, error recovery

**Coming in Phase 3**: Trust modes (notify → auto → ghost)

## Why This Approach

v2 had 12,000 lines describing how AI *should* work. v3 has 1,000 lines that *actually* work.

The insight: **Claude Code is already the orchestrator.** Buildmate shouldn't replace it - it should enhance it with background agents and auto-documentation.

---

**Built for vibe coding without chaos.** 🔥

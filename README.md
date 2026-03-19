# ⚡️ Blitz

> Autonomous development team that manages everything while you just chat.

## The Problem

You want to **vibe code** - describe what you need in plain English and have it just work. But:
- ❌ No structure to how projects start
- ❌ No guardrails on what gets built
- ❌ No memory between sessions
- ❌ Scope creep into infinity

## The Fix

**Blitz is an invisible control layer for Claude Code.**

Instead of talking directly to Claude, Blitz manages a team of 3 background agents that:
- Research the best options
- Design the architecture  
- Implement the code

**While you just chat normally.**

## How It Works

```
You: "Build me a trading bot"

Claude: "Quick questions:
        1. Paper or real money?
        2. What features?
        3. Tech preference?"

[60 seconds later]

Claude: "Got it. Spinning up team..."

[Background agents working]
        
Claude: "MVP ready! Try: python bot.py --paper"
```

**No commands. No `/blitz status`. Just chat.**

## The 3-Agent System

| Agent | Does | Auto-Updates |
|-------|------|--------------|
| **Researcher** 🔬 | Finds best APIs/libs | `research.md` |
| **Architect** 📐 | Designs structure | `ARCHITECTURE.md` |
| **Coder** 💻 | Implements + tests | `CHANGELOG.md`, `PROJECT.md` |

All agents run in background. You get casual progress updates every 5-10 minutes.

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

## Installation

```bash
git clone https://github.com/sprajapati024/blitz.git
cd blitz
chmod +x install.sh
./install.sh
```

This installs Blitz as a Claude Code skill and adds the integration hook.

## Usage

Just talk to Claude Code normally:

```
"Build me a habit tracker"
"Create a Twitter bot"
"Fix the login bug"  
"Add push notifications"
"Refactor the auth system"
```

Blitz intercepts, asks 3-4 questions, then manages the whole dev process.

## What Makes It Different

| Others | Blitz |
|--------|-------|
| 30+ slash commands | **0 commands** - just chat |
| 7 agents to manage | **3 background agents** |
| Long interviews | **60-second questions** |
| Manual doc updates | **100% auto docs** |
| You manage workflow | **Claude manages it** |

## Project Structure

```
blitz/
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
├── install.sh                   # Simple installer
└── README.md                    # This file
```

## Size

| Component | Lines | 
|-----------|-------|
| Core engine | ~800 |
| 3 Agents | ~200 |
| Installer | 81 |
| **Total** | **~1,100** |

Minimal, focused, actually works.

## Core Principles

1. **No commands** - Everything through natural chat
2. **Auto-docs** - Every action updates docs automatically
3. **Background execution** - Agents work, you chill
4. **3 questions max** - 60 seconds, then build
5. **Interruptible** - "Wait, use X instead" anytime

## Status

**v3.0 - Phase 1 Complete**: Core engine, 3 agents, Claude integration

**Coming:**
- Natural progress reporting every 5-10 min
- Trust modes (notify → auto → ghost)
- Error recovery

## The Story

Built after months of chaotic Claude Code sessions. Tried complex orchestration (v2) - 12,000 lines that didn't work. Stripped to essentials (v3) - 1,100 lines that actually ship.

**The insight:** Claude Code is already the orchestrator. Blitz just adds background agents and auto-documentation.

---

**Built for vibe coding without chaos.** ⚡️

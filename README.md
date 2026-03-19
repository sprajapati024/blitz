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

Instead of talking directly to Claude, Blitz manages a team of background agents that:
- Design the architecture (with inline research)
- Implement the code
- Handle interruptions gracefully

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

[5 min] "Research done - going with AlphaVantage. Cheaper, reliable."
[15 min] "Architecture set - 3-layer design. Building now..."
[25 min] "Data layer done. Working on trading logic..."
        
Claude: "MVP ready! Try: python bot.py --paper"
```

**No commands. No `/blitz status`. Just chat.**

## The 2-Agent System

| Agent | Does | Auto-Updates |
|-------|------|--------------|
| **Architect** 📐 | Researches + designs structure | `ARCHITECTURE.md`, `.blitz/decisions.md` |
| **Coder** 💻 | Implements + tests + progress updates | `CHANGELOG.md`, `PROJECT.md` |

All agents run in background. You get casual progress updates every 5-10 minutes.

## Smart Interruptions

Change your mind mid-build? No problem.

```
You: "Wait, use PostgreSQL instead of SQLite"

Claude: "Got it. Pausing coder agent...

         Current state:
         - Data layer: 80% done (SQLite)
         - API layer: Not started

         Options:
         1. Finish current task, then switch (no loss)
         2. Pause now, resume with change (lose 5-10 min)
         3. Rewind to checkpoint (clean slate)
         4. Start fresh with reference (keep old code)

         What works?"
```

**Checkpoints save full file snapshots.** Rewind anytime.

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

## Error Recovery

When things go wrong, Blitz handles it gracefully:

```
Claude: "Hit a snag - Yahoo Finance API is down (503).

         Options:
         1. Switch to AlphaVantage (recommended)
         2. Use mock data for now
         3. Add retry logic with backoff

         What do you want to do?"
```

No crashes. No stack traces. Just options.

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
| 7 agents to manage | **2 background agents** |
| Long interviews | **60-second questions** |
| Manual doc updates | **100% auto docs** |
| Crash on errors | **Graceful recovery** |
| Lose work on interruption | **Smart checkpoints** |

## Project Structure

```
blitz/
├── core/
│   ├── intent_detector.py      # Detects build/fix/update intent
│   ├── state_manager.py        # Tracks project state
│   ├── checkpoint_manager.py   # Smart interruptions & rewind
│   ├── progress_streamer.py    # Natural progress updates
│   ├── doc_updater.py          # Auto-updates all docs
│   └── agent_spawner.py        # Spawns background agents
├── agents/
│   ├── architect.py            # Architecture + research agent
│   └── coder.py                # Implementation agent
├── integration/
│   └── CLAUDE.md               # Claude Code integration
├── templates/                   # Doc templates
├── tests/                       # Integration tests
├── install.sh                   # Simple installer
└── README.md                    # This file
```

## Size

| Component | Lines | 
|-----------|-------|
| Core engine | ~1,600 |
| 2 Agents | ~180 |
| Tests | ~400 |
| Installer | 81 |
| **Total** | **~2,300** |

Minimal, focused, actually works.

## Core Principles

1. **No commands** - Everything through natural chat
2. **Auto-docs** - Every action updates docs automatically
3. **Background execution** - Agents work, you chill
4. **3 questions max** - 60 seconds, then build
5. **Interruptible** - "Wait, use X instead" anytime
6. **Graceful errors** - Options, not crashes
7. **Real checkpoints** - Full file snapshots, actually restore

## Status

**v3.1 - Phase 2 Complete**

✅ **Phase 1**: Core engine, 2 agents, Claude integration  
✅ **Phase 2**: Progress reporting, error recovery, smart interruptions  
🔄 **Phase 3**: Trust modes (notify → auto → ghost) - *Next*

## The Story

Built after months of chaotic Claude Code sessions. Tried complex orchestration (v2) - 12,000 lines that didn't work. Stripped to essentials (v3) - 1,100 lines that actually ship.

**The insight:** Claude Code is already the orchestrator. Blitz just adds background agents and auto-documentation.

---

**Built for vibe coding without chaos.** ⚡️

# Blitz

> **The development autopilot. You describe what you want. Blitz handles research, architecture, and building — all in the background.**

```
You: "Build me a trading bot"
Blitz: "Ooh, we're building things now? Love it. Quick vibe check..."
You: "Paper, alerts + stop-losses, you choose"
[25 minutes later]
Blitz: "🎉 Your MVP is ALIVE! Try: cd trading-bot && python bot.py --paper"
```

**No commands. No workflow management. No decision fatigue.** Just building.

---

## The Problem

> *"I just wanted to build a trading bot. Three hours later I was still debating folder structure."*

You have an idea. You want to build it. But instead of coding, you get stuck in the meta-work:
- Researching which database to use
- Deciding folder structure  
- Documenting why you chose X over Y
- Managing the project's chaos

**The work before the work kills momentum.**

---

## The Solution

**Blitz streamlines development by handling everything in the background.**

You describe what you want → Blitz asks 3 questions → Background agents research, design, and build → You get progress updates → MVP delivered.

**While you focus on the project itself, Blitz handles:**

| Background Task | How Blitz Handles It |
|-----------------|----------------------|
| Research | Architect agent compares options, picks best |
| Architecture | Auto-generates `ARCHITECTURE.md` with rationale |
| Building | Coder agent implements with progress streaming |
| Documentation | Every action updates `CHANGELOG.md`, `PROJECT.md` |
| Errors | Graceful recovery with 2-3 options, never crashes |
| Changes of mind | Real checkpoints — rewind anytime |

---

## Before & After

### Without Blitz ❌

```
my-project/
├── main.py          # Started here, abandoned
├── main_v2.py       # Refactored, also abandoned  
├── test.py          # Not sure what this tests
├── utils.py         # 600 lines of random helpers
├── old/
│   ├── backup_main.py
│   └── backup_utils.py
├── ideas.md         # Notes from 3 sessions ago
└── README.md        # Empty

Result: 6 hours, nothing deployable, forgot why you started
```

### With Blitz ✅

```
trading-bot/
├── src/
│   ├── main.py          # Clean entry point
│   ├── data.py          # Price fetching
│   └── trading.py       # Paper trading logic
├── tests/
│   └── test_trading.py
├── .blitz/
│   ├── state.json       # Project status
│   ├── decisions.md     # Why we chose X
│   └── checkpoints/     # Rewind to any point
├── ARCHITECTURE.md      # Full design
├── CHANGELOG.md         # What got built
└── PROJECT.md           # Scope & progress

Result: 30 minutes, MVP running, full context preserved
```

---

## The Timeline

| Time | What You See | What's Happening |
|------|--------------|------------------|
| **0:00** | *"Spinning up team..."* | Architect researching APIs |
| **0:08** | *"Research done — going with AlphaVantage"* | Designing 3-layer structure |
| **0:15** | *"Architecture set. Building data layer..."* | Coder implementing |
| **0:25** | *"Data layer done. Trading logic next..."* | Stop-loss engine |
| **0:30** | *"MVP ready! Try: python bot.py --paper"* | Tests passing, docs updated |

**You didn't type a command. You didn't manage agents. You just described what you wanted.**

---

## Why I Built This

> *"I was spending more time managing the development process than actually developing. Every session started with 30 minutes of yak shaving — folder structure, tech choices, documentation. I tried complex orchestration (12,000 lines that broke constantly). Stripped it down to what actually works: a system that handles the background work so I can focus on building."*

**— After my 50th abandoned side project**

---

## Key Features

### Smart Interruptions
Change your mind mid-build? No problem.

```
You: "Wait, use PostgreSQL instead of SQLite"

Blitz: "Got it. Current state: data layer 80% done.
        
        Options:
        1. Finish task, then migrate (no loss)
        2. Pause now, switch (lose 5 min)  
        3. Rewind to checkpoint (clean slate)
        
        What works?"
```

**Real checkpoints.** Full file snapshots. Rewind anytime.

### Graceful Errors
When things go wrong, you get options — not crashes.

```
Blitz: "Hit a snag — Yahoo Finance API down (503).

        Options:
        1. Switch to AlphaVantage (recommended)
        2. Use mock data for now
        3. Add retry logic

        What do you want to do?"
```

### Auto-Documentation
Documentation happens automatically. Every action updates the right file.

```
Coder writes auth middleware
  ↓
CHANGELOG.md: "Added JWT auth"
PROJECT.md:   "✓ Auth complete"
DECISIONS.md: "Chose JWT over sessions"
```

**Zero manual doc updates.**

### Choose Your Personality
Blitz adapts to how you like to work. Pick your vibe during setup:

| Tone | Style | Example |
|------|-------|---------|
| **Sassy & Fun** | Professional with personality | "Your MVP is ALIVE! 🚀" |
| **Chill & Casual** | Like a smart friend | "Cool, structure's locked in." |
| **Professional** | Straight to business | "Project structure complete." |
| **Minimal** | Just the facts | Updates only when you ask |

### Trust Modes
How hands-on do you want to be? Blitz grows with you:

| Mode | Behavior | Unlocks After |
|------|----------|---------------|
| **Notify** *(default)* | "About to do X — sound good?" | Start |
| **Auto** | Does it, then tells you | 3 successful projects |
| **Ghost** | Silent execution, daily summary | 10 successful projects |

---

## Quick Start

### Install

```bash
git clone https://github.com/sprajapati024/blitz.git
cd blitz
chmod +x install.sh
./install.sh
```

### The Onboarding Vibe

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ⚡️ Welcome to the Other Side, Builder                       ║
║                                                              ║
║  You found Blitz — where ideas actually become real.         ║
║  No more abandoned projects. No more decision fatigue.       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

◆ Step 1: Pick Your Vibe

  1. ● Sassy & Fun
     "Your MVP is ALIVE! 🚀"

  2. ○ Chill & Casual  
     "Cool, structure's locked in."

  3. ○ Professional
     "Project structure complete."

  4. ○ Minimal
     Updates only when you ask

◆ Step 2: Choose Your Trust Mode

  1. ● Notify Mode
     Best for: Getting to know Blitz

  2. ○ Auto Mode (unlock after 3 projects)
     Best for: Regular users

  3. ○ Ghost Mode (unlock after 10 projects)  
     Best for: Full trust

✓ Preferences saved!

Welcome to the other side. Let's build something awesome.
```

**Interactive onboarding will guide you through:**
- ✅ Tone selection (Sassy, Chill, Professional, Minimal)
- ✅ Trust mode setup (Notify → Auto → Ghost)
- ✅ Claude Code integration

No Docker. No dependencies. One command.

### Use

Just describe what you want:

```
"Build me a habit tracker"
"Create a Twitter bot"
"Fix the login bug"
"Add notifications"
"Refactor to OAuth"
```

**That's it.** Blitz handles everything in the background.

---

## Project Structure

```
blitz/
├── core/
│   ├── checkpoint_manager.py   # Pause, resume, rewind
│   ├── progress_streamer.py    # Natural updates
│   ├── agent_spawner.py        # Spawns agents
│   ├── state_manager.py        # Tracks everything
│   └── doc_updater.py          # Auto-docs
├── agents/
│   ├── architect.py            # Research + design
│   └── coder.py                # Build + test
└── tests/                      # 7 integration tests
```

**~2,500 lines.** No bloat. Just what works.

---

## Status

**v3.1 — Interactive Onboarding Live** 🎉

✅ **Phase 1:** Core engine, 2 agents, Claude integration  
✅ **Phase 2:** Progress reporting, error recovery, smart interruptions  
✅ **Phase 3:** Trust modes (notify → auto → ghost)  
✅ **New:** Interactive setup with personality selection

---

## The Philosophy

> *"I don't want to manage agents. I don't want to write prompts. I don't want to update documentation. I just want to focus on building things and have them work."*

**Principles:**
1. **No commands** — Natural chat only
2. **60 seconds max** — Questions, not interviews  
3. **Background execution** — You build, Blitz handles the rest
4. **Interruptible** — Change direction anytime
5. **Auto-docs** — Context preserved automatically
6. **Graceful errors** — Options, not crashes

---

## One More Thing

> *"I built this because I was tired of starting projects and abandoning them. Now I finish them. Not because I'm more disciplined — because the friction is gone. Everything that used to slow me down is handled in the background."*

**Ready to just... build?**

```bash
git clone https://github.com/sprajapati024/blitz.git
```

---

*Streamlined development. Everything handled in the background.* ⚡️

# Blitz

> **"I just wanted to build a trading bot. Three hours later I was still debating folder structure."**

Sound familiar?

## The Problem

You have an idea. You want to build it. But instead of coding, you get stuck in:
- Deciding folder structure
- Researching which database to use
- Documenting why you chose X over Y
- Managing the project's chaos

**The work before the work.** It kills momentum.

## The Solution

**Blitz streamlines development by handling everything in the background.**

You describe what you want. Blitz asks 3 quick questions. Then it manages a team of agents that research, design, and build while you focus on the project itself.

**No commands. No setup. No decision fatigue.** Just building.

```
You: "Build me a habit tracker"

Blitz: "Quick questions: 1) Who's using it? 2) Key features? 3) Tech preference?"

You: "Just me, daily check-ins and streaks, you choose"

Blitz: "Got it. Spinning up team..."

[20 minutes later]

Blitz: "Done. Try it: cd habit-tracker && python main.py"
```

**You didn't manage a workflow. You didn't update documentation. You didn't coordinate agents.** You just described what you wanted, and it got built.

---

## Why I Built This

> *"I was spending more time managing the development process than actually developing. 'What's the best folder structure?' 'Should I use SQLite or Postgres?' 'Wait, did we document why we chose FastAPI?' Every session started with 30 minutes of meta-work."*
> 
> **— After my 50th abandoned side project**

I tried complex orchestration. 12,000 lines that broke constantly. Stripped it down to what actually works: **a system that handles the background work so you can focus on building.**

---

## The Chaos vs. The Calm

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
├── todo.txt         # Outdated
└── README.md        # Empty

Result: 6 hours in, nothing deployable, forgot why you started
```

### With Blitz ✅

```
habit-tracker/
├── src/
│   ├── __init__.py
│   ├── main.py          # Clean entry point
│   ├── cli.py           # Typer commands
│   ├── models.py        # SQLAlchemy models
│   └── tracker.py       # Core logic
├── tests/
│   ├── test_tracker.py
│   └── test_cli.py
├── docs/
│   └── ARCHITECTURE.md  # Why we chose SQLite + Typer
├── .blitz/
│   ├── state.json       # Project status
│   ├── decisions.md     # "Chose SQLite over Postgres (MVP)"
│   └── checkpoints/     # Rewind to any point
├── CHANGELOG.md         # What got built when
├── PROJECT.md           # Scope & progress
└── README.md            # Actually useful

Result: 30 minutes in, MVP running, full context preserved
```

**Same effort. Completely different outcome.**

---

## How It Actually Works

### The 60-Second Setup

```
You: "Build me a trading bot"

Blitz: "Quick questions:
        1. Paper or real money?
        2. What features? (pick 2-3)
        3. Any tech preference or I choose?"

You: "Paper, price alerts + stop-losses, you choose"

Blitz: "Got it. Spinning up team..."
```

### What Happens Next

| Time | What You See | What's Happening |
|------|--------------|------------------|
| **0:00** | *"Spinning up team..."* | Architect agent starts researching APIs |
| **0:08** | *"Research done - going with AlphaVantage. Free tier, reliable."* | Architect designs 3-layer structure |
| **0:15** | *"Architecture set. Coder building data layer..."* | Coder implements price fetching |
| **0:25** | *"Data layer done. Working on trading logic..."* | Stop-loss engine coming together |
| **0:30** | *"MVP ready! Try: `python bot.py --paper --ticker AAPL`"* | Tests passing, docs updated |

**You didn't type a single command.** You focused on what you were building while Blitz handled everything in the background.

---

## The Streamlined Experience

### 1. Change Your Mind Mid-Build

```
You: "Wait, use PostgreSQL instead of SQLite"

Blitz: "Got it. Pausing coder...

        Current state:
        - Data layer: 80% done (SQLite)
        
        Options:
        1. Finish task, then migrate (no loss)
        2. Pause now, switch (lose 5 min)
        3. Rewind to checkpoint (clean slate)
        
        What works?"
```

**Checkpoints are real.** Full file snapshots. Rewind anytime. Blitz handles the complexity.

### 2. When Things Go Wrong

```
Blitz: "Hit a snag - Yahoo Finance API is down (503).

        Options:
        1. Switch to AlphaVantage (recommended)
        2. Use mock data for now  
        3. Add retry logic

        What do you want to do?"
```

**No crashes.** No stack traces in your chat. Just options. Blitz manages the recovery.

### 3. Documentation Just... Happens

```
Coder writes auth middleware
  ↓
CHANGELOG.md: "Added JWT auth with refresh tokens"
PROJECT.md:   "✓ Auth complete → starting API layer"
DECISIONS.md: "Chose JWT over sessions (stateless, simpler)"
```

**Zero manual doc updates.** Context is preserved automatically in the background.

---

## Real Talk: What This Actually Solves

| Without Blitz | With Blitz |
|---------------|------------|
| 30 min debating folder structure | 60 seconds of questions, then building |
| "Wait, why did we choose X?" | Decisions auto-logged, context always available |
| Lost work when changing approach | Rewind to any checkpoint, change direction freely |
| Documentation? Maybe later. | Every action updates docs automatically |
| Crashes kill the momentum | Graceful recovery with clear options |
| Managing the process | Just focusing on the project |
| 6 hours, nothing deployable | 30 minutes, MVP running |

---

## Installation

```bash
git clone https://github.com/sprajapati024/blitz.git
cd blitz
chmod +x install.sh
./install.sh
```

That's it. No Docker. No Python env setup. No config files.

---

## Usage

Literally just describe what you want:

```
"Build me a habit tracker"
"Create a Twitter bot that posts daily"
"Fix the login bug in my Flask app"
"Add email notifications to the trading bot"
"Refactor the auth system to use OAuth"
```

**Zero commands.** Zero context switching. Zero workflow management. Just describe what you want and Blitz handles everything in the background.

---

## The Philosophy

> *"I don't want to manage agents. I don't want to write prompts. I don't want to update documentation. I just want to focus on building things and have them work."*

Blitz is **invisible infrastructure.** It handles the coordination, the documentation, the state management — all in the background — so you can stay focused on the actual project.

**Principles:**
1. **No commands** — Everything through natural chat
2. **60 seconds max** — Questions, not interviews  
3. **Background execution** — You focus on building, Blitz handles the rest
4. **Interruptible** — Change direction anytime
5. **Auto-docs** — Context preserved automatically
6. **Graceless errors** — Options, not crashes

---

## Project Structure

```
blitz/
├── core/
│   ├── intent_detector.py      # "Is this a build request?"
│   ├── checkpoint_manager.py   # Pause, resume, rewind
│   ├── progress_streamer.py    # Natural language updates
│   ├── agent_spawner.py        # Spawns architect + coder
│   ├── state_manager.py        # Tracks everything
│   └── doc_updater.py          # Auto-updates docs
├── agents/
│   ├── architect.py            # Research + design (8-12 min)
│   └── coder.py                # Build + test (20-30 min)
├── integration/
│   └── CLAUDE.md               # Claude Code integration guide
└── tests/                      # Integration tests (7/7 passing)
```

**~2,500 lines.** No bloat. No enterprise patterns. Just what works.

---

## Current Status

**v3.1 — Phase 2 Complete**

✅ **Phase 1:** Core engine, 2 agents, Claude integration  
✅ **Phase 2:** Progress reporting, error recovery, smart interruptions  
🔄 **Phase 3:** Trust modes (notify → auto → ghost)

**Stable.** **Tested.** **Actually used.**

---

## The Story

Built after months of chaotic development sessions. v1 was duct tape. v2 was 12,000 lines of over-engineering that broke constantly. v3 is what survived — the essential 10% that delivers 90% of the value.

**The insight:** Claude Code is already powerful. Blitz just adds:
- Background agents that research/design/build
- Smart interruptions with real checkpoints  
- Auto-documentation so context never dies
- Graceful errors that don't kill momentum

All running in the background while you focus on the project.

---

## One More Thing

> *"I built this because I was tired of starting projects and abandoning them. Now I finish them. Not because I'm more disciplined — because the friction is gone. Everything that used to slow me down is handled in the background."*

**Ready to just... build?**

```bash
git clone https://github.com/sprajapati024/blitz.git
```

---

*Streamlined development. Everything handled in the background.* ⚡️

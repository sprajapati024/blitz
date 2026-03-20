<div align="center">

# ⚡️ BLITZ

**English**

**You talk. Blitz builds.** — Conversational development powered by GSD's infrastructure.

**Sassy, chill, or professional** — Blitz adapts to your vibe while shipping real code.

[**English**](README.md)

[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)

<br>

```bash
# Clone from GitHub
git clone https://github.com/sprajapati024/blitz.git
cd blitz

# Run the simple installer (Claude Code only)
node bin/install-simple.js

# Or run onboarding to configure
node bin/onboarding.js
```

**Works on Mac, Windows, and Linux.**

<br>

*"Describe what you want. Watch it get built. Move on with your life."*

*"Finally, a dev partner that doesn't need constant hand-holding."*

*"GSD's power, Blitz's personality. Shipped more in a week than I did in a month."*

<br>

[Why I Built This](#why-i-built-this) · [How It Works](#how-it-works) · [Commands](#commands) · [Tones](#tones) · [Configuration](#configuration)

</div>

---

## Why I Built This

Look, I was tired of the meta-work killing the actual work.

You want to build something cool. Instead, you're stuck debating folder structure, researching which database "feels right," and writing documentation that explains why you chose option A over option B.

The work before the work is killing your momentum.

So I forked GSD (Get Shit Done) — because when it comes to context engineering and spec-driven development, GSD *just works* — and gave it some personality.

Blitz is GSD's infrastructure with Blitz's soul. The same wave execution, agent orchestration, and state management. But now you can tell it to "build me a trading bot" and it actually does it while keeping the conversation flowing.

No discrete commands interrupting your train of thought. No "please confirm step 47 of 52." Just you and Blitz, vibing until the code is done.

**TL;DR:** GSD builds things reliably. Blitz builds things reliably *and* doesn't bore you while doing it.

— **Blitz**

---

## Who This Is For

Developers who want to describe what they want and have it built — without pretending they're running a standup meeting with themselves.

---

## Getting Started

```bash
git clone https://github.com/sprajapati024/blitz.git
cd blitz
node bin/install.js
```

The installer walks you through:
1. **Tone** — How should Blitz talk to you? (Sassy, Chill, Pro, Minimal)
2. **Mode** — Interactive (confirm each step) or Yolo (just execute)

Verify with:
- Claude Code: `/blitz:help`
- OpenCode: `/blitz-help`

### Staying Updated

Blitz evolves. Pull and reinstall:

```bash
cd blitz
git pull origin macbook
node bin/install.js
```

---

## How It Works

### 1. You Describe What You Want

```
/blitz:new
```

Tell Blitz what you're building. It asks a few questions, sets up the project structure, and creates:
- `PROJECT.md` — Your vision
- `ROADMAP.md` — The phases
- `REQUIREMENTS.md` — What's in scope
- `STATE.md` — Project memory

If it's a frontend project, Blitz creates a design system (`DESIGN.md`) first. Because looking good matters.

---

### 2. Discuss the Phase

```
/blitz:discuss 1
```

**This is where you shape the implementation.**

Your roadmap has a sentence or two per phase. That's not enough context to build what *you* imagine. This step captures your preferences before planning starts.

Blitz identifies gray areas based on what you're building:
- **UI features** → Layout, interactions, states
- **APIs** → Response format, error handling
- **Content** → Structure, flow, tone

For each area, you make the call. Blitz documents it. Planner respects it.

---

### 3. Plan the Phase

```
/blitz:plan 1
```

Blitz:
1. **Researches** — Investigates how to implement, guided by your decisions
2. **Plans** — Creates atomic task plans with dependency analysis
3. **Verifies** — Checks plans against requirements

Each plan is small enough to execute in a fresh context. No degradation. No "I'll be more concise."

---

### 4. Execute

```
/blitz:execute 1
```

Blitz:
1. **Runs plans in waves** — Parallel where possible, sequential when dependent
2. **Fresh context per plan** — 200k tokens purely for implementation
3. **Commits per task** — Every task gets its own atomic commit
4. **Verifies against goals** — Confirms the phase delivered what it promised

Walk away. Come back to completed work with clean git history.

**How Wave Execution Works:**

```
┌────────────────────────────────────────────────────────────────────┐
│  PHASE EXECUTION                                                   │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  WAVE 1 (parallel)          WAVE 2 (parallel)          WAVE 3    │
│  ┌─────────┐ ┌─────────┐    ┌─────────┐ ┌─────────┐    ┌─────────┐ │
│  │ Task 01 │ │ Task 02 │ →  │ Task 03 │ │ Task 04 │ →  │ Task 05 │ │
│  │         │ │         │    │         │ │         │    │         │ │
│  │ Auth    │ │ Config  │    │ API     │ │ UI      │    │ Tests   │ │
│  └─────────┘ └─────────┘    └─────────┘ └─────────┘    └─────────┘ │
│       │           │              ↑           ↑              ↑      │
│       └───────────┴──────────────┴───────────┘              │      │
│              Dependencies: Task 03 needs Task 01            │      │
│                          Task 04 needs Task 02              │      │
│                          Task 05 needs Tasks 03 + 04        │      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

**Why waves matter:**
- Independent tasks → Same wave → Run in parallel
- Dependent tasks → Later wave → Wait for dependencies
- Blitz figures it out so you don't have to

---

### 5. Verify

```
/blitz:verify 1
```

**Did it actually work?**

Automated checks confirm code exists and tests pass. But does it work the way you expected? This is your chance to use it.

Blitz walks you through one at a time. Can you log in? Yes/no. Can you post? Yes/no. Something broken? Blitz spawns debug agents to find root causes and creates fix plans.

---

### 6. Ship or Continue

```
/blitz:ship 1
```

Creates a PR from verified phase work.

Or just keep going:

```
/blitz:continue
```

The conversation picks up where it left off.

---

### Quick Mode

```
/blitz:quick Add dark mode toggle
```

**For ad-hoc tasks that don't need full planning.**

Same quality guarantees (atomic commits, state tracking) with a faster path. No research, no verification unless you ask.

---

## Tones

Blitz has personality. GSD doesn't. That's the point.

### How Tone Affects Output

| Context | Sassy | Chill | Pro | Minimal |
|---------|-------|-------|-----|---------|
| Phase start | "Alright, let's build this thing" | "Starting Phase 1..." | "Executing phase 1" | "Phase 1" |
| Task complete | "Nailed it" | "Cool, auth's working" | "Auth endpoint complete" | "Done" |
| Error | "Plot twist - something broke" | "Hey, hit a snag" | "Error in auth module" | "Error" |
| All done | "You're welcome" | "Ship it!" | "Milestone complete" | "Done" |

### Sassy Mode

```
"Ugh, you wanted it to work? Already did."

"Finally. That took forever."
```

### Chill Mode

```
"Hey, foundation's done. Auth next?"

"No worries, I got this."
```

### Pro Mode

```
"Phase 1 complete. 12 files modified, 3 tests added."

"Resolving conflict in auth/model.ts"
```

### Minimal Mode

```
"Done."

"Error."

"Phase 1."
```

---

## Commands

### Core Workflow

| Command | What it does |
|---------|--------------|
| `/blitz:new` | Start fresh — questions, setup, ready to build |
| `/blitz:continue` | Resume where we left off |
| `/blitz:chat` | Discuss ideas, make decisions, Blitz documents |
| `/blitz:status` | Where are we? Phase progress, blockers |
| `/blitz:discuss [phase]` | Capture implementation decisions |
| `/blitz:plan [phase]` | Create execution plans for a phase |
| `/blitz:execute [phase]` | Execute all plans in parallel waves |
| `/blitz:verify [phase]` | Confirm phase goals achieved |
| `/blitz:ship [phase]` | Create PR from verified work |
| `/blitz:auto` | Execute all phases — just watch |

### Navigation

| Command | What it does |
|---------|--------------|
| `/blitz:next` | Auto-detect state, run next step |
| `/blitz:progress` | Where am I? What's next? |
| `/blitz:help` | Show all commands |
| `/blitz:health` | Validate `.planning/` integrity |

### Phase Management

| Command | What it does |
|---------|--------------|
| `/blitz:add-phase` | Append phase to roadmap |
| `/blitz:insert-phase [n]` | Insert urgent work between phases |
| `/blitz:checkpoint` | Create manual checkpoint |
| `/blitz:checkpoint list` | List all checkpoints |
| `/blitz:checkpoint rewind [n]` | Rewind to checkpoint n |

### Configuration

| Command | What it does |
|---------|--------------|
| `/blitz:mode [mode]` | Switch execution mode (interactive/yolo) |
| `/blitz:tone [tone]` | Change how Blitz talks (sassy/chill/pro/minimal) |
| `/blitz:config` | Re-run onboarding |

### Quick Mode

| Command | What it does |
|---------|--------------|
| `/blitz:quick [task]` | Execute task without full planning |

---

## Configuration

Blitz stores project settings in `.planning/config.json`. Configure during `/blitz:new` or update later.

### Core Settings

| Setting | Options | Default | What it controls |
|---------|---------|---------|------------------|
| `tone` | `sassy`, `chill`, `pro`, `minimal` | `chill` | How Blitz talks to you |
| `mode` | `yolo`, `interactive` | `interactive` | Auto-approve vs confirm at each step |

---

## Agents

Blitz has 6 specialized agents:

| Agent | Purpose |
|-------|---------|
| **blitz-researcher** | Stack analysis, codebase mapping, pattern recognition |
| **blitz-designer** | Design systems for frontend projects |
| **blitz-architect** | System design, data modeling, API design |
| **blitz-planner** | Task decomposition, dependency analysis, wave planning |
| **blitz-executor** | Executes plans, writes code, runs tests, manages git |
| **blitz-verifier** | Goal verification, quality assessment |

---

## Project Structure

```
.planning/
├── PROJECT.md           # Project vision
├── ROADMAP.md          # Phase structure
├── REQUIREMENTS.md     # Scoped requirements
├── STATE.md            # Project memory
├── DESIGN.md           # Design system (frontend only)
├── research/           # Initial research
│   ├── STACK.md
│   ├── FEATURES.md
│   └── SUMMARY.md
└── phases/
    ├── 01-foundation/
    │   ├── 01-01-PLAN.md
    │   └── 01-SUMMARY.md
    └── ...
```

---

## Troubleshooting

**Commands not found after install?**
- Restart your runtime to reload commands
- Verify files exist in `~/.claude/commands/blitz/`
- Re-run `npx blitz-cc@latest`

**Want to change tone or mode?**
```bash
/blitz:tone sassy
/blitz:mode yolo
```

**Updating to latest?**
```bash
npx blitz-cc@latest
```

---

## Credits

Blitz is a fork of [GSD (Get Shit Done)](https://github.com/gsd-build/get-shit-done) by [TÂCHES](https://github.com/glittercowboy).

GSD's architecture is battle-tested:
- Wave-based parallel execution
- Agent orchestration
- State management
- Planning system

Blitz adds:
- Personality and tone system
- Design system phase
- 6 focused agents with embedded skills
- Conversational UX

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

**You talk. Blitz builds.**

</div>
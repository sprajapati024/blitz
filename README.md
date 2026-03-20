# ⚡️ Blitz v2

**Blitz** is GSD's infrastructure with Blitz's soul. Same proven agent orchestration, wave execution, and state management - wrapped in Blitz's personality and conversational UX.

> Forked from [GSD (Get Shit Done)](https://github.com/gsd-build/get-shit-done) by [TÂCHES](https://github.com/glittercowboy/blitz-core)  
> License: MIT

---

## Philosophy

**GSD**: "Get Shit Done" - aggressive, functional, no-nonsense  
**Blitz**: Sassy, chill, competent - like a senior dev who ships while you watch

```
Blitz = You drive, Blitz executes
Blitz = You talk, Blitz builds

The conversation never stops.
You discuss, Blitz builds, you discuss more, Blitz builds more.
No discrete commands - continuous flow.
```

---

## Installation

```bash
npm install -g blitz-cc
```

Or run directly:

```bash
npx blitz-cc@latest
```

---

## Quick Start

```bash
# Run onboarding (first time only)
blitz onboarding

# Start a new project
/blitz:new

# Resume last project
/blitz:continue

# Chat about an idea
/blitz:chat

# Check status
/blitz:status
```

---

## Commands

### Primary Commands

| Command | Purpose |
|---------|---------|
| `/blitz:new` | Start a new project - brief chat, Blitz sets up + starts building |
| `/blitz:continue` | Resume last project from where we left off |
| `/blitz:chat` | Plan mode - discuss ideas, make decisions, Blitz documents |
| `/blitz:status` | Where are we? Shows project state, phase progress, blockers |
| `/blitz:auto` | Auto mode - Blitz executes all phases, you just watch |
| `/blitz:execute [phase]` | Execute a specific phase (default: current) |
| `/blitz:verify [phase]` | Verify phase goals achieved |
| `/blitz:ship [phase]` | Create PR from phase work |

### Supporting Commands

| Command | Purpose |
|---------|---------|
| `/blitz:discuss [phase]` | Capture implementation decisions before planning |
| `/blitz:plan [phase]` | Create execution plans for a phase |
| `/blitz:add-phase` | Append new phase to roadmap |
| `/blitz:insert-phase [n]` | Insert urgent work between phases |
| `/blitz:checkpoint` | Create manual checkpoint before risky move |
| `/blitz:checkpoint list` | List all checkpoints |
| `/blitz:checkpoint rewind [n]` | Rewind to checkpoint n |
| `/blitz:mode [mode]` | Switch execution mode (interactive/yolo) |
| `/blitz:quick [task]` | Quick task - skip planning, execute immediately |
| `/blitz:health` | Validate .planning/ directory integrity |
| `/blitz:config` | Re-run onboarding / change settings |
| `/blitz:help` | Show all commands |

---

## Tones

Unlike GSD's purely functional output, Blitz has personality:

```
/blitz:tone sassy     # "Oh, you wanted it to work? Already did."
/blitz:tone chill     # "Hey, foundation's done. Auth next?"
/blitz:tone pro       # "Phase 1 complete. 12 files modified."
/blitz:tone minimal   # "Done."
```

---

## Execution Modes

| Mode | Behavior |
|------|----------|
| `interactive` | Confirm before each plan execution (default) |
| `yolo` | Execute without confirmation |

---

## Project Structure

```
.planning/
├── PROJECT.md           # Project vision and context
├── config.json          # Workflow preferences
├── STATE.md            # Project memory across sessions
├── ROADMAP.md          # Phase structure
├── REQUIREMENTS.md     # Scoped requirements
├── DESIGN.md           # Design system (frontend projects only)
├── research/           # Initial research (if enabled)
│   ├── STACK.md
│   ├── FEATURES.md
│   ├── ARCHITECTURE.md
│   ├── PITFALLS.md
│   └── SUMMARY.md
└── phases/
    ├── 01-foundation/
    │   ├── 01-01-PLAN.md
    │   └── ...
    └── ...
```

---

## Agents

Blitz has 6 specialized agents, each with defined skills:

| Agent | Purpose | Skills |
|-------|---------|--------|
| **blitz-researcher** | Initial project research | Codebase mapping, Stack analysis, Pattern recognition, Synthesis |
| **blitz-designer** | Design system creation (frontend only) | Visual design, Component systems, Color theory, User patterns |
| **blitz-architect** | System design and architecture | System design, Data modeling, API design |
| **blitz-planner** | Creates execution plans | Task decomposition, Dependency analysis, Wave planning |
| **blitz-executor** | Executes plans, writes code | Coding, Testing, Git operations, Debugging, File organization |
| **blitz-verifier** | Goal verification | Verification patterns, Quality assessment, UAT facilitation |

---

## How It Works

### Full Project Flow

```
/blitz:new
    │
    ├─► Requirements Phase
    │
    ├─► Design Phase (if frontend project detected)
    │       └─► Creates DESIGN.md
    │
    ├─► Research Phase
    │       └─► blitz-researcher (4 parallel tasks)
    │
    ├─► Architect Phase
    │       └─► blitz-architect (synthesizes → ARCHITECTURE.md)
    │
    ├─► Planner Phase
    │       └─► blitz-planner (creates plans with waves)
    │
    └─► STATE.md, ROADMAP.md, REQUIREMENTS.md created
```

### Phase Execution Flow

```
/blitz:execute [phase]
    │
    ├─► Wave 1 (parallel): blitz-executor × n
    │
    ├─► Wave 2 (parallel): blitz-executor × n (after Wave 1)
    │
    └─► blitz-verifier (confirms goals)
```

---

## Credits

Blitz v2 is a fork of [GSD (Get Shit Done)](https://github.com/gsd-build/get-shit-done) by TÂCHES.

GSD's architecture provides:
- Wave-based parallel execution
- Agent orchestration
- State management
- Planning system

Blitz adds:
- Personality and tone system
- Design system phase for frontend projects
- 6 focused agents with embedded skills
- Conversational UX (continuous chat, not discrete commands)

---

## License

MIT

---

## Links

- [Blitz Repository](https://github.com/glittercowboy/blitz-core)
- [GSD Repository](https://github.com/gsd-build/get-shit-done)
- [Documentation](./docs/BLITZ-v2-SPEC.md)
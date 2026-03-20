# BLITZ v2 - Specification

**Forked from GSD (Get Shit Done) by TÂCHES**  
**License: MIT**

---

## Overview

Blitz v2 is GSD's infrastructure with Blitz's soul. Same proven agent orchestration, wave execution, and state management - wrapped in Blitz's personality and conversational UX.

**GSD**: "Get Shit Done" - aggressive, functional, no-nonsense  
**Blitz**: Sassy, chill, competent - like a senior dev who ships while you watch

---

## Core Philosophy

```
GSD = You drive, GSD executes
Blitz = You talk, Blitz builds

The conversation never stops.
You discuss, Blitz builds, you discuss more, Blitz builds more.
No discrete commands - continuous flow.
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

## Execution Modes

| Mode | Behavior |
|------|----------|
| `interactive` | Confirm before each plan execution (default) |
| `yolo` | Execute without confirmation |

```
/blitz:mode yolo    # Run everything without asking
/blitz:mode interactive  # Confirm each step
```

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
├── phases/
│   ├── 01-foundation/
│   │   ├── 01-01-PLAN.md
│   │   ├── 01-01-SUMMARY.md
│   │   ├── 01-02-PLAN.md
│   │   ├── 01-02-SUMMARY.md
│   │   ├── 01-CONTEXT.md
│   │   ├── 01-RESEARCH.md
│   │   ├── 01-VERIFICATION.md
│   │   └── 01-UAT.md
│   └── 02-authentication/
│       └── ...
└── todos/
```

---

## Agent Team

Blitz has 6 specialized agents, each with defined skills:

### Agent Overview

| Agent | Purpose | Skills |
|-------|---------|--------|
| **blitz-researcher** | Initial project research | Codebase mapping, Stack analysis, Pattern recognition, Synthesis |
| **blitz-designer** | Design system creation (frontend only) | Visual design, Component systems, Color theory, User patterns |
| **blitz-architect** | System design and architecture | System design, Data modeling, API design |
| **blitz-planner** | Creates execution plans | Task decomposition, Dependency analysis, Wave planning |
| **blitz-executor** | Executes plans, writes code | Coding, Testing, Git operations, Debugging, File organization |
| **blitz-verifier** | Goal verification | Verification patterns, Quality assessment, UAT facilitation |

### Skills System

Each agent has skills embedded in their definition. Skills power the agent's capabilities:

#### blitz-executor Skills

```markdown
<skill:coding>
- Write working code, not pseudocode
- Follow existing patterns in codebase
- Include error handling
- MVP quality, ship it
</skill>

<skill:testing>
- Unit tests for core logic
- Integration tests for APIs
- Put tests in tests/ directory
- Run tests before marking done
</skill>

<skill:git>
- Commit after each task: atomic, meaningful message
- Format: type(scope): description
- Examples: feat(auth): add login endpoint
</skill>

<skill:file-organization>
- Code goes in src/
- Tests in tests/
- Docs in docs/
- Config at root
- Keep root clean
</skill>
```

#### blitz-designer Skills (Frontend Projects Only)

```markdown
<skill:visual-design>
- Create consistent visual language
- Use color theory principles
- Ensure accessibility (contrast, sizing)
</skill>

<skill:component-systems>
- Design reusable components
- Document states (default, hover, disabled, error)
- Define props and APIs for each component
</skill>

<skill:color-theory>
- Create harmonious palettes
- Define semantic colors (success, warning, error)
- Support dark/light themes if needed
</skill>

<skill:user-patterns>
- Follow platform conventions (web, mobile)
- Design for common flows (forms, lists, navigation)
- Consider responsive design
</skill>
```

---

## Planning Flow (from GSD)

### Full Project Flow

```
/blitz:new
    │
    ├─► Requirements Phase
    │       └─► "What are we building?"
    │
    ├─► Design Phase (if frontend project detected)
    │       ├─► "Show me designs you like"
    │       ├─► "Colors? Dark/Light? Vibes?"
    │       ├─► "Components needed?"
    │       └─► Creates DESIGN.md
    │
    ├─► Research Phase
    │       └─► blitz-researcher (4 parallel tasks)
    │               ├─► Stack research
    │               ├─► Features research
    │               ├─► Architecture research
    │               └─► Pitfalls research
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
    │       └─► Each executor reads DESIGN.md first (if frontend)
    │
    ├─► Wave 2 (parallel): blitz-executor × n (after Wave 1)
    │
    ├─► Wave 3 (if needed)
    │
    └─► blitz-verifier (confirms goals)
```

### Design System Detection

Blitz automatically detects if a project needs design:

1. User describes project in `/blitz:new`
2. If keywords: "web", "app", "frontend", "UI", "dashboard", "landing page"
3. Blitz asks: "Is this a frontend project? Should I create a design system?"
4. If yes → runs design phase before research

---

## Personality System

### Tone Options

Unlike GSD's purely functional output, Blitz has personality:

```
/blitz:tone sassy     # "Oh, you wanted it to work? Already did."
/blitz:tone chill     # "Hey, foundation's done. Auth next?"
/blitz:tone pro       # "Phase 1 complete. 12 files modified."
/blitz:tone minimal   # "Done."
```

### How Tone Affects Output

| Context | Sassy | Chill | Pro | Minimal |
|---------|-------|-------|-----|---------|
| Phase start | "Alright, let's build this thing" | "Starting Phase 1..." | "Executing phase 1" | "Phase 1" |
| Task complete | "Nailed it" | "Cool, auth's working" | "Auth endpoint complete" | "Done" |
| Error | "Plot twist - something broke" | "Hey, hit a snag" | "Error in auth module" | "Error" |
| All done | "You're welcome" | "Ship it!" | "Milestone complete" | "Done" |

---

## Onboarding

### Installation

```bash
npx blitz-cc@latest
```

### Onboarding Flow

```
blitz onboarding
        │
        ▼
┌─────────────────────────────────────────────┐
│  1. WELCOME                                  │
│                                               │
│  ⚡️ Welcome to Blitz                          │
│                                               │
│  "Your silent coding partner that actually    │
│   ships while you watch."                     │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│  2. PREREQUISITES CHECK                      │
│                                               │
│  ✓ Claude Code / OpenCode detected           │
│  ✓ Git configured                            │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│  3. TONE SELECTION                           │
│                                               │
│  How should Blitz talk to you?               │
│                                               │
│  ○ Sassy      "Oh, you wanted it to work?"   │
│  ● Chill      "Hey, auth's done. Nice."      │
│  ○ Pro        "Phase 1 complete. 12 files." │
│  ○ Minimal    "Done."                         │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│  4. EXECUTION MODE                           │
│                                               │
│  How much control do you want?               │
│                                               │
│  ● Interactive  (confirm before each step)   │
│  ○ Yolo         (execute everything)         │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│  5. DONE                                     │
│                                               │
│  ⚡️ Blitz is ready!                          │
│                                               │
│  To start:                                    │
│  1. Open Claude Code                          │
│  2. Type /blitz to see all commands          │
│                                               │
│  Or jump right in:                           │
│  • /blitz:new - Start a new project          │
│  • /blitz:chat - Discuss an idea             │
└─────────────────────────────────────────────┘
```

### Reconfiguration

```bash
blitz config     # Re-run onboarding / change settings
```

---

## Branding

### Visual Identity

- **Colors**: Electric blue (#00D4FF) + Purple (#8B5CF6) accent
- **Vibe**: Terminal-native, dark theme, premium feel
- **Logo**: ⚡️ Blitz

### README Opening

> Blitz is a conversational development system for Claude Code and OpenCode.
>
> Unlike other tools that make you drive the process, Blitz is your silent coding partner.
> Tell it what you want, go get coffee, come back to shipped code.
>
> Built on GSD's proven architecture.

---

## Technical Implementation

### Directory Structure (Post-Fork)

```
blitz-cc/
├── bin/
│   ├── install.js          # Installer
│   └── blitz-tools.cjs     # CLI tools
├── commands/blitz/         # /blitz:* commands
├── blitz-core/
│   ├── agents/             # Agent definitions (blitz-*.md)
│   ├── workflows/          # Execution workflows
│   ├── templates/          # Document templates
│   └── references/         # Reference docs
├── hooks/dist/             # Claude Code hooks
└── docs/                   # Documentation
```

### Key Replacements from GSD

| GSD | Blitz |
|-----|-------|
| `commands/gsd/` | `commands/blitz/` |
| `get-shit-done/` | `blitz-core/` |
| `gsd-planner` | `blitz-planner` |
| `gsd-executor` | `blitz-executor` |
| `gsd-verifier` | `blitz-verifier` |
| `gsd-tools.cjs` | `blitz-tools.cjs` |
| `~/.claude/get-shit-done/` | `~/.claude/blitz/` |
| `/gsd:` | `/blitz:` |

### What to Keep from GSD (Proven)

- Wave-based parallel execution
- Agent orchestration pattern (orchestrator → specialized agents)
- Fresh 200k context per executor
- Goal-backward verification
- STATE.md / ROADMAP.md / PLAN.md structure
- Atomic commits per task
- Dependency analysis for wave assignment

---

## DESIGN.md Template

For frontend projects, DESIGN.md is created by blitz-designer:

```markdown
# Design System - [PROJECT_NAME]

## Colors

### Primary Palette
- Primary: #3B82F6 (blue-500)
- Primary Hover: #2563EB (blue-600)
- Secondary: #8B5CF6 (purple-500)

### Semantic Colors
- Success: #10B981 (green-500)
- Warning: #F59E0B (amber-500)
- Error: #EF4444 (red-500)
- Info: #3B82F6 (blue-500)

### Neutral Colors
- Background: #0F172A (slate-900)
- Surface: #1E293B (slate-800)
- Border: #334155 (slate-700)
- Text Primary: #F8FAFC (slate-50)
- Text Secondary: #94A3B8 (slate-400)

## Typography

- Font Family: Inter, system-ui, sans-serif
- Headings:
  - H1: 32px/40px bold
  - H2: 24px/32px bold
  - H3: 20px/28px semibold
- Body: 14px/20px regular
- Small: 12px/16px regular

## Spacing

Base unit: 4px

- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px

## Border Radius

- sm: 4px
- md: 6px
- lg: 8px
- xl: 12px
- full: 9999px

## Shadows

- sm: 0 1px 2px rgba(0, 0, 0, 0.3)
- md: 0 4px 6px rgba(0, 0, 0, 0.3)
- lg: 0 10px 15px rgba(0, 0, 0, 0.3)

## Components

### Button

**Variants:**
- Primary: bg-primary, text-white, hover:bg-primary-hover
- Secondary: bg-transparent, border-primary, text-primary
- Ghost: bg-transparent, text-primary, hover:bg-slate-800

**Sizes:**
- sm: px-3 py-1.5 text-sm
- md: px-4 py-2 text-base
- lg: px-6 py-3 text-lg

**States:**
- Default, Hover (darken 10%), Active (darken 15%), Disabled (opacity 50%)

### Card

- Background: surface color
- Border: 1px slate-700
- Radius: lg (8px)
- Padding: md (16px)
- Shadow: md

### Modal

- Overlay: black 50% opacity
- Centered, max-width based on size prop
- Background: surface color
- Border radius: xl (12px)
- Close button: top-right corner

### Form Elements

**Input:**
- Height: 40px
- Padding: 0 12px
- Border: 1px slate-700
- Focus: ring-2 ring-primary
- Error: border-red-500, ring-red-500

**Select:**
- Same as input
- Chevron icon on right

### Navigation

- Height: 64px
- Background: background color
- Border bottom: 1px slate-700
- Items: horizontal layout, centered

### Table

- Header: bg-slate-800, font-semibold
- Rows: alternating bg-slate-900 / bg-slate-800/50
- Hover: bg-slate-700
- Border: 1px slate-700

---

## GSD Credit

> Blitz is a fork of [GSD (Get Shit Done)](https://github.com/gsd-build/get-shit-done) by [TÂCHES](https://github.com/glittercowboy).
> We keeping GSD's proven architecture and adding Blitz's personality and UX.

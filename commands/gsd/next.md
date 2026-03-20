---
name: blitz:next
description: Automatically advance to the next logical step in the Blitz workflow
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - SlashCommand
---
<objective>
Detect the current project state and automatically invoke the next logical Blitz workflow step.
No arguments needed — reads STATE.md, ROADMAP.md, and phase directories to determine what comes next.

Designed for rapid multi-project workflows where remembering which phase/step you're on is overhead.
</objective>

<execution_context>
@~/.claude/blitz-core/workflows/next.md
</execution_context>

<process>
Execute the next workflow from @~/.claude/blitz-core/workflows/next.md end-to-end.
</process>

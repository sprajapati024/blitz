---
name: blitz:do
description: Route freeform text to the right Blitz command automatically
argument-hint: "<description of what you want to do>"
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
---
<objective>
Analyze freeform natural language input and dispatch to the most appropriate Blitz command.

Acts as a smart dispatcher — never does the work itself. Matches intent to the best Blitz command using routing rules, confirms the match, then hands off.

Use when you know what you want but don't know which `/blitz:*` command to run.
</objective>

<execution_context>
@~/.claude/blitz-core/workflows/do.md
@~/.claude/blitz-core/references/ui-brand.md
</execution_context>

<context>
$ARGUMENTS
</context>

<process>
Execute the do workflow from @~/.claude/blitz-core/workflows/do.md end-to-end.
Route user intent to the best Blitz command and invoke it.
</process>

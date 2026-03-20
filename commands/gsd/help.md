---
name: blitz:help
description: Show available Blitz commands and usage guide
---
<objective>
Display the complete Blitz command reference.

Output ONLY the reference content below. Do NOT add:
- Project-specific analysis
- Git status or file context
- Next-step suggestions
- Any commentary beyond the reference
</objective>

<execution_context>
@~/.claude/blitz-core/workflows/help.md
</execution_context>

<process>
Output the complete Blitz command reference from @~/.claude/blitz-core/workflows/help.md.
Display the reference content directly — no additions or modifications.
</process>

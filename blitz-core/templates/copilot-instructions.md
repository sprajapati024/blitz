# Instructions for GSD

- Use the blitz-core skill when the user asks for Blitz or uses a `blitz-*` command.
- Treat `/blitz-...` or `blitz-...` as command invocations and load the matching file from `.github/skills/blitz-*`.
- When a command says to spawn a subagent, prefer a matching custom agent from `.github/agents`.
- Do not apply Blitz workflows unless the user explicitly asks for them.
- After completing any `blitz-*` command (or any deliverable it triggers: feature, bug fix, tests, docs, etc.), ALWAYS: (1) offer the user the next step by prompting via `ask_user`; repeat this feedback loop until the user explicitly indicates they are done.

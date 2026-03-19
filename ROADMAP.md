# ⚡️ Blitz Enhancement Roadmap

## Current State (v3.0)
✅ Core engine (intent, state, docs, spawner)
✅ 3 agents (researcher, architect, coder)
✅ Auto-documentation
✅ Natural chat interface
✅ ~1,100 lines

---

## Phase 2: Polishing (Next)

### 2.1 Natural Progress Reporting
**Problem:** User doesn't know what's happening during the 20-30 min build

**Solution:** Casual updates every 5-10 minutes

```
[5 min] "Research done - going with AlphaVantage API. 
         Cheaper than Bloomberg, reliable."

[10 min] "Architecture set - 3-layer design. 
          Moving to implementation."

[20 min] "Data layer done. Working on trading logic now."

[30 min] "MVP ready! Paper trading works. Want to see it?"
```

**Implementation:**
- Coder agent streams progress to state.json
- Claude checks state every 5 min
- Natural language summary, not raw logs

**Effort:** 2-3 days
**Value:** High - user feels connected to process

---

### 2.2 Error Recovery
**Problem:** When agents fail, everything stops

**Solution:** Graceful degradation

```
Claude: "Hit a snag - the Yahoo Finance API isn't responding.
         
         Options:
         1. Try AlphaVantage instead (slower but reliable)
         2. Skip live data, use mock data for now
         3. Pause and investigate
         
         What do you want to do?"
```

**Implementation:**
- Try/catch around agent execution
- Log errors to blockers in state.json
- Present 2-3 recovery options
- Auto-retry with exponential backoff for transient errors

**Effort:** 3-4 days
**Value:** High - makes it robust

---

### 2.3 Smart Interruptions ✅ COMPLETE
**Problem:** User wants to change direction mid-build

**Solution:** Pause/resume gracefully

```
User: "Wait, use PostgreSQL instead of SQLite"

Claude: "Got it. Pausing coder agent...
         
         Current state:
         - Data layer: 80% done (SQLite)
         - API layer: Not started
         
         Options:
         1. Finish current task, then switch
         2. Pause now, resume with change
         3. Rewind to checkpoint (lose current progress)
         4. Start fresh with reference
         
         What works?"
```

**Implementation:**
- ✅ Checkpoints before each major task (auto + manual)
- ✅ Full file snapshots saved to `.blitz/checkpoints/`
- ✅ Can rewind to any checkpoint
- ✅ Dry-run compare shows what would be lost
- ✅ Pause/resume agent state
- ✅ Thread-safe concurrent operations
- ✅ Registry persists across restarts

**Files:**
- `core/checkpoint_manager.py` - 900 lines, full implementation
- `core/agent_spawner.py` - Integrated checkpoint methods
- `tests/test_checkpoint_integration.py` - 7 passing tests

**Effort:** 4-5 days ✅ Done in 1 session
**Value:** Medium-High - flexibility without chaos

---

## Phase 3: Trust Modes ✅ COMPLETE

### 3.1 Notify Mode (Default) ✅
Current behavior - tells user what it's about to do, waits for "ok"

### 3.2 Auto Mode ✅
**For:** After you've worked with Blitz on 3+ projects

```
Claude: "Building habit tracker now. I'll update you in 20 min."

[20 min later]

Claude: "Done! Features: daily check-in, streaks, reminders.
         
         ARCHITECTURE.md has the design.
         
         cd habit-tracker && npm start to try it."
```

**Implementation:**
- ✅ Setting in `~/.blitz/preferences.json`
- ✅ Require 3 successful projects before enabling
- ✅ Can switch back to notify anytime
- ✅ Suppresses "starting" messages
- ✅ Only major milestone updates

### 3.3 Ghost Mode ✅
**For:** After 10+ successful projects, maximum trust

- ✅ Agents work silently
- ✅ Daily summary only
- ✅ Interrupt anytime with "wait..."

```
[Next day]

Claude: "Yesterday's progress:
         ✅ Trading bot: Paper trading complete
         ✅ Added stop-losses
         ⏳ Live broker integration: In progress
         
         Type 'status' anytime for details."
```

**Implementation:**
- ✅ Require 10 successful projects
- ✅ Logs to daily summaries
- ✅ Critical actions still ask permission

**Files:**
- `core/trust_manager.py` - 600 lines, full implementation
- `core/agent_spawner.py` - Integrated trust mode methods
- `tests/test_trust_manager.py` - 12 passing tests

**Effort:** 2 days ✅ Done in 1 session
**Value:** Medium - saves time for power users

---

## Phase 4: Intelligence

### 4.1 Pattern Learning
**Problem:** Starting from scratch every project

**Solution:** Remember what worked

```
Blitz: "I see you've built 3 Python CLI tools.
        
        I'll default to:
        - Typer (you used it 100% of the time)
        - pytest + coverage (you added it manually 2/3 times)
        - Skip Docker (you removed it from 2 projects)
        
        Sound good or want to adjust?"
```

**Implementation:**
- Read `~/.blitz/history.json`
- Track: tech choices, patterns, what was removed
- Suggest defaults based on frequency

**Effort:** 3-4 days
**Value:** High - personalized experience

---

### 4.2 Smart Templates
**Problem:** Starting from blank slate

**Solution:** Project templates based on type

```
User: "Build me a trading bot"

Blitz: "I have a 'trading bot' template from your previous project.
        
        Includes:
        - Data fetching layer
        - Paper trading engine
        - Alert system
        
        Use it as starting point? [Y/n]"
```

**Templates:**
- Web app (React + FastAPI)
- CLI tool (Typer/Click)
- Trading bot
- API service
- Automation script

**Implementation:**
- `templates/projects/[type]/`
- Clone and customize
- Learn from user's past projects

**Effort:** 5-7 days
**Value:** High - massive time saver

---

### 4.3 Cross-Project Memory
**Problem:** Rebuilding auth for every project

**Solution:** Reuse components

```
Claude: "I see you built JWT auth in 2 previous projects.
         
         Want me to:
         1. Copy that pattern (customized for this stack)
         2. Build fresh (might be different)
         3. Show you both, you decide"
```

**Implementation:**
- Index reusable components from PROJECT.md
- Match by tech stack
- Show diff of how it would fit new project

**Effort:** 5-7 days
**Value:** Medium - good for common patterns

---

## Phase 5: Git Integration

### 5.1 Smart Commits
**Problem:** Commit messages are garbage

**Solution:** Auto-generate from CHANGELOG

```
git log:
- "feat: Add paper trading engine"
- "feat: Implement stop-loss logic"  
- "fix: Handle API rate limiting"
- "docs: Update ARCHITECTURE with data flow"
```

**Implementation:**
- Parse CHANGELOG.md entries
- Format as conventional commits
- Auto-commit every 10-15 min during coding

**Effort:** 2 days
**Value:** Medium - nice to have

---

### 5.2 Branch Management
**Problem:** Working on multiple features

**Solution:** Auto-branch per feature

```
User: "Add user profiles"

Claude: "Creating branch feature/user-profiles...
        
        Will merge when done.
        Main branch stays stable."
```

**Implementation:**
- `git checkout -b feature/[name]`
- Work on branch
- Merge when complete
- Keep main deployable

**Effort:** 3 days
**Value:** Medium - good practice

---

## Phase 6: Advanced Agents (Careful!)

### 6.1 Testing Agent
**Risk:** Adds complexity, might not be needed

**Alternative:** Coder writes tests (already does)

**Verdict:** Skip - keep it simple

---

### 6.2 Review Agent
**Risk:** LLM reviewing LLM code = echo chamber

**Alternative:** Claude reviews in conversation

**Verdict:** Skip - use human review

---

### 6.3 Security Agent
**Risk:** False sense of security

**Alternative:** Coder includes security considerations

**Verdict:** Skip - document security reqs in PROJECT.md

---

## What NOT to Add

| Feature | Why Skip |
|---------|----------|
| Dashboard/Web UI | Against philosophy (invisible) |
| More than 3 agents | Complexity, coordination overhead |
| Real-time collaboration | Scope creep |
| CI/CD integration | Use existing tools |
| Database for state | File-based is feature, not bug |
| Plugin system | Complexity, maintenance |

---

## Priority Ranking

### Must Have (Do First)
1. ✅ Natural progress reporting
2. ✅ Error recovery
3. ✅ Smart interruptions

### Should Have (Do Next)
4. Pattern learning
5. Smart templates
6. Trust modes

### Could Have (Later)
7. Git integration (commits, branches)
8. Cross-project memory

### Won't Have (Keep It Simple)
9. More agents
10. Web UI
11. Plugin system

---

## Success Metrics

After Phase 2:
- [ ] User never wonders "what's happening?"
- [ ] Agent failures are recovered gracefully
- [ ] User can interrupt without losing work

After Phase 3:
- [ ] Power users enable auto mode
- [ ] 90% of projects use learned defaults
- [ ] Templates save 50% setup time

After Phase 4:
- [ ] Blitz knows user's preferences
- [ ] Reusable components suggested automatically
- [ ] Commits are meaningful

---

## The Goal

> **Every enhancement should make Blitz more invisible, not more visible.**

If a feature requires:
- Learning new commands → Skip it
- More UI/UX → Skip it  
- More agents → Skip it
- More configuration → Skip it

If a feature:
- Removes decisions → Keep it
- Happens automatically → Keep it
- Learns from user → Keep it
- Saves time without effort → Keep it

**Blitz should feel like magic, not software.** ⚡️

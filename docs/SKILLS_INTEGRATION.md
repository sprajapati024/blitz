# Skills Integration for Blitz

## The Problem Skills Solve

**Current Blitz (without skills):**
```
User: "Build me a trading bot"

Architect agent: "Hmm, let me research trading bot patterns... 
                  [5 minutes of LLM reasoning]
                  Okay, here's a structure..."
                  
Result: 12 minutes, $0.40 in tokens, generic architecture
```

**Blitz with Skills:**
```
User: "Build me a trading bot"

Blitz: Detects "trading-bot" intent → Loads trading-bot skill
       
Architect agent: "[Loaded trading-bot skill with proven patterns]
                  Using AlphaVantage for data, paper trading engine,
                  SQLite for MVP. Here's the architecture..."
                  
Result: 3 minutes, $0.08 in tokens, battle-tested patterns
```

**10x faster. 5x cheaper. Better results.**

---

## How Skills Work in Blitz

### 1. Project Type Skills (Auto-Loaded)

When user says "Build me...", Blitz detects project type and loads the skill:

```python
# intent_detector.py
PROJECT_TYPE_SKILLS = {
    "trading-bot":     "projects/trading-bot",
    "web-app":         "projects/web-app",
    "cli-tool":        "projects/cli-tool",
    "api-service":     "projects/api-service",
    "automation":      "projects/automation",
    "discord-bot":     "projects/discord-bot",
    "mobile-app":      "projects/mobile-app",
}

# When intent detected:
skill_name = detect_project_type(user_input)  # "trading-bot"
loaded_skill = skill_manager.load_skill(f"blitz/{skill_name}")

# Architect agent now has access to:
# - Recommended tech stack
# - Folder structure template
# - Common patterns
# - Pitfalls to avoid
```

**Skill contents:**
```
skills/blitz/projects/trading-bot/
├── SKILL.md              # When to use, patterns, decisions
├── templates/
│   ├── structure.yaml    # Folder structure
│   ├── stack.yaml        # Tech stack with rationale
│   └── patterns/
│       ├── data-fetching.md
│       ├── paper-trading.md
│       └── alerting.md
└── examples/
    └── mvp/              # Minimal working example
```

### 2. Architecture Pattern Skills (On-Demand)

During build, agents can load specific pattern skills:

```python
# Architect agent reasoning:
"User wants auth. I'll load the jwt-auth skill."

skill = load_skill("blitz/patterns/jwt-auth")
# Now has:
# - JWT implementation pattern
# - Refresh token strategy
# - Security best practices
# - Common mistakes to avoid
```

**Available pattern skills:**
- `jwt-auth` - Authentication with JWT
- `oauth` - OAuth 2.0 integration
- `database-layer` - Repository pattern, migrations
- `api-design` - REST vs GraphQL decisions
- `testing-strategy` - Unit vs integration tests
- `deployment` - Docker, VPS, serverless
- `background-jobs` - Celery, cron, queues

### 3. Tech Stack Skills (Reference)

Coder agent loads these when implementing:

```python
# Coder agent: "Need to implement FastAPI with PostgreSQL"

skill = load_skill("blitz/stacks/fastapi-postgres")
# Has:
# - SQLAlchemy setup
# - Pydantic models pattern
# - Dependency injection examples
# - Testing patterns
# - Migration commands
```

**Stack skills:**
- `fastapi-postgres`
- `fastapi-sqlite`
- `flask-sqlalchemy`
- `react-vite`
- `nextjs-prisma`
- `typer-cli`
- `discord-py`

---

## Skill Contents

### SKILL.md Format

```yaml
---
name: trading-bot
description: |
  Use for: Trading bots, stock/crypto automation, paper trading systems
  Triggers: User mentions "trading bot", "stock bot", "paper trading", "algorithmic trading"
  Stack: Python, AlphaVantage/yfinance, SQLite/PostgreSQL
---

# Trading Bot Project Skill

## When to Use
- Paper trading systems
- Price alert automation
- Portfolio tracking
- NOT for: Live trading with real money (requires compliance)

## Recommended Stack
- **Language**: Python (ecosystem, libraries)
- **Data**: AlphaVantage (free tier, reliable) or yfinance
- **Database**: SQLite (MVP) → PostgreSQL (scale)
- **Scheduling**: APScheduler or cron
- **Notifications**: Email (SMTP) or Discord webhook

## Architecture Pattern
```
bot/
├── data/
│   ├── fetcher.py       # API wrappers
│   └── cache.py         # Reduce API calls
├── trading/
│   ├── engine.py        # Paper trading logic
│   ├── positions.py     # Position tracking
│   └── rules.py         # Entry/exit rules
├── alerts/
│   └── notifier.py      # Email/Discord
└── config.py            # API keys, settings
```

## Common Patterns

### Data Fetching
- Always cache results (rate limits)
- Retry with exponential backoff
- Mock data for testing

### Paper Trading
- Track cash balance separately
- Simulate slippage (0.1-0.5%)
- Log every trade with timestamp

### Stop Losses
- Use trailing stops for winners
- Hard stops for losers (-5%)
- Test with historical data first

## Pitfalls to Avoid
1. **Over-trading** - More trades ≠ more profit
2. **Curve fitting** - Strategy works on backtest, fails live
3. **API limits** - Yahoo Finance blocks frequent requests
4. **No logging** - Can't debug without trade history

## MVP Checklist
- [ ] Fetch real-time prices
- [ ] Paper trading engine
- [ ] Basic buy/sell logic
- [ ] Position tracking
- [ ] Trade logging
- [ ] Price alerts
- [ ] CLI interface

## Examples
See `examples/mvp/` for minimal working trading bot.
```

---

## Implementation Plan

### Phase 1: Project Type Skills

1. **Create skill structure**
   ```
   skills/blitz/projects/
   ├── trading-bot/
   ├── web-app/
   ├── cli-tool/
   └── api-service/
   ```

2. **Integrate with intent_detector**
   ```python
   # Detect project type → Load skill → Pass to architect
   ```

3. **Architect uses skill context**
   - Instead of researching from scratch, references skill
   - Faster, more consistent results
   - Learns from previous projects

### Phase 2: Pattern Skills

1. **Create pattern library**
   - Common architectural patterns
   - Security patterns
   - Testing patterns

2. **Agent loads on demand**
   - "Need auth → load jwt-auth skill"
   - "Need database → load repository-pattern skill"

### Phase 3: Learning from Usage

1. **Track what works**
   - Which skills lead to successful projects?
   - Which patterns get used most?

2. **Auto-improve skills**
   - Add new patterns from successful projects
   - Update recommendations based on usage

---

## Benefits

| Without Skills | With Skills |
|----------------|-------------|
| Generic architecture every time | Battle-tested patterns |
| 10-15 min research per project | 1-2 min skill load |
| Inconsistent quality | Consistent, proven approaches |
| Re-learns patterns each time | Builds institutional knowledge |
| $0.30-0.50 per architecture | $0.05-0.10 per architecture |

---

## Example: Trading Bot with Skills

### User Request
```
"Build me a trading bot for Canadian stocks"
```

### Without Skills (Current)
```
Architect: [Thinks for 5 minutes]
"Okay, for trading bots I should research... 
 [Searches APIs]
 [Compares databases]
 [Designs structure from scratch]
 
Result: Generic, takes 12 minutes"
```

### With Skills
```
Blitz: Detect "trading-bot" → Load skill

Architect: "[Loaded trading-bot skill]
          Canadian stocks → TSX data needed
          Skill recommends: Yahoo Finance (free, has TSX)
          Pattern: 3-layer with paper trading
          Pitfall: API limits → add caching
          
Result: Specific, takes 3 minutes, proven patterns"
```

---

## Next Steps

1. **Extract patterns from your projects**
   - What structures do you use repeatedly?
   - What decisions do you make every time?
   - What mistakes do you see?

2. **Create first 3 skills**
   - trading-bot (you're building one)
   - web-app (common request)
   - cli-tool (you use Typer often)

3. **Integrate with Blitz**
   - Skill loading in intent_detector
   - Skill context passed to agents
   - Skill usage tracking

4. **Iterate**
   - Add more project types
   - Add pattern skills
   - Learn from usage

---

*Skills make Blitz 10x faster and 5x cheaper while delivering better results.*

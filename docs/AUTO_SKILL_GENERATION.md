# Auto-Generated Skills for Blitz

## The Vision

**Blitz doesn't start with skills. It creates them as it builds.**

```
Project 1: "Build trading bot"
  ↓
Architect: Researches APIs, picks AlphaVantage
Coder: Implements paper trading logic
  ↓
Blitz: "I see patterns here..."
  ↓
Auto-creates: blitz/skill/trading-bot-patterns
  ↓
Project 2: "Build crypto trading bot"  
  ↓
Blitz: Detects similarity → Loads trading-bot-patterns skill
  ↓
Faster build, proven patterns, no re-research
```

**Skills emerge from builds, not defined upfront.**

---

## How It Works

### 1. Pattern Recognition During Build

**Architect Phase:**
```python
# As architect makes decisions, Blitz captures:

decisions = [
    {"what": "AlphaVantage for data", "why": "Free tier, reliable", "context": "trading"},
    {"what": "SQLite for MVP", "why": "Zero config, migrate later", "context": "database"},
    {"what": "3-layer architecture", "why": "Separation of concerns", "context": "structure"}
]

# Pattern detector analyzes:
- Tech choices with context
- Architecture decisions  
- Trade-offs considered

# If patterns look reusable → Flag for skill extraction
```

**Coder Phase:**
```python
# As coder implements:

solutions = [
    {"problem": "API rate limiting", "solution": "Caching with 5-min TTL", "context": "data-fetching"},
    {"problem": "Position tracking", "solution": "Dictionary with timestamp history", "context": "state-management"},
    {"problem": "Stop-loss logic", "solution": "Trailing stop with 5% threshold", "context": "trading-logic"}
]

# If solution is elegant and reusable → Flag for skill extraction
```

### 2. Skill Extraction Triggers

**Auto-extract skill when:**

```python
def should_extract_skill(project_data) -> bool:
    """Determine if this project should generate a skill"""
    
    # Threshold: Project completed successfully
    if not project_data['completed']:
        return False
    
    # Threshold: Has reusable patterns
    if len(project_data['unique_patterns']) < 3:
        return False
    
    # Threshold: Similar projects don't exist
    similar_skills = find_similar_skills(project_data['tech_stack'])
    if similar_skills and similarity > 0.8:
        # Enhance existing skill instead
        return False
    
    # Threshold: Novel enough to be worth it
    if project_data['novelty_score'] < 0.6:
        return False
    
    return True
```

### 3. Auto-Create Skill Content

**From Project 1 (Trading Bot), Blitz extracts:**

```yaml
# .blitz/skills/extracted/trading-bot-patterns/SKILL.md
---
name: trading-bot-patterns
source_project: trading-bot-aapl
created_at: 2026-03-19
confidence: 0.85
project_count: 1
---

# Auto-Extracted Trading Bot Patterns

## Detected From
- Project: trading-bot-aapl
- Tech Stack: Python, AlphaVantage, SQLite, Typer
- Duration: 45 minutes
- Status: ✅ Completed successfully

## Patterns Discovered

### Data Fetching Pattern
**Context:** API rate limits, need caching
**Solution:** 
```python
class CachedPriceFetcher:
    TTL = 300  # 5 minutes
    
    def get_price(self, symbol):
        if cache.is_fresh(symbol, self.TTL):
            return cache.get(symbol)
        price = self.api.fetch(symbol)
        cache.set(symbol, price)
        return price
```
**Why it works:** Reduces API calls by ~80%, handles failures gracefully

### Paper Trading Engine Pattern
**Context:** Simulate trades without real money
**Solution:** Track cash + positions separately, validate before trade
```python
class PaperTrader:
    def buy(self, symbol, shares, price):
        cost = shares * price
        if cost > self.cash:
            raise InsufficientFunds()
        self.cash -= cost
        self.positions[symbol] = Position(...)
```
**Why it works:** Simple, testable, matches real broker API

### Architecture Pattern
**Structure:** 3-layer (data → trading → CLI)
**Rationale:** Each layer testable independently, can swap CLI for API later

## Tech Stack Decisions (Auto-Logged)

| Component | Chosen | Alternatives | Reason |
|-----------|--------|--------------|---------|
| Data API | AlphaVantage | Yahoo Finance, Bloomberg | Free tier, reliable |
| Database | SQLite | PostgreSQL | Zero config for MVP |
| CLI Framework | Typer | Click, Argparse | Type hints, modern |
| Scheduler | APScheduler | Cron, Celery | In-process, simple |

## Pitfalls Discovered

1. **Yahoo Finance blocks** - Use AlphaVantage or add delays
2. **SQLite concurrency** - Fine for single-user, use WAL mode
3. **Float precision** - Use Decimal for money calculations

## Confidence Score: 85%

This skill was extracted from 1 successful project. 
Confidence increases as more projects use these patterns.

## Usage

When Blitz detects "trading bot" or "stock automation":
- Load this skill
- Suggest AlphaVantage + SQLite + 3-layer structure
- Warn about Yahoo Finance blocking
- Include caching pattern in data layer
```

### 4. Skill Registry & Evolution

```python
# skills_registry.json
{
  "skills": [
    {
      "id": "trading-bot-patterns",
      "name": "Trading Bot Patterns",
      "source_projects": ["trading-bot-aapl"],
      "confidence": 0.85,
      "usage_count": 0,
      "created_at": "2026-03-19",
      "last_updated": "2026-03-19",
      "tags": ["trading", "finance", "automation"],
      "tech_stack": ["python", "sqlite", "typer"],
      "status": "experimental"  # → "proven" after 3 uses
    }
  ]
}
```

**Skill evolves over time:**
```python
# Project 3 also builds trading bot
# Blitz loads skill, uses patterns
# After successful completion:

skill['confidence'] += 0.05  # 0.85 → 0.90
skill['usage_count'] += 1     # 0 → 1
skill['source_projects'].append('trading-bot-tsx')
skill['status'] = 'proven' if skill['usage_count'] >= 3 else 'experimental'

# If Project 3 found better pattern:
# Add alternative to skill, mark as "variant"
```

---

## Skill Detection & Matching

### When to Load a Skill

```python
def detect_skill_match(user_request: str, project_context: dict) -> Optional[Skill]:
    """Find relevant skill for this project"""
    
    # Method 1: Keyword matching
    keywords = extract_keywords(user_request)
    # "trading bot" → ["trading", "bot", "stocks"]
    
    matching_skills = []
    for skill in all_skills:
        overlap = set(keywords) & set(skill['tags'])
        if overlap:
            matching_skills.append((skill, len(overlap)))
    
    # Method 2: Tech stack similarity
    if project_context.get('tech_preference'):
        for skill in all_skills:
            if skill['tech_stack'] == project_context['tech_preference']:
                matching_skills.append((skill, 0.5))  # Lower weight
    
    # Method 3: Intent similarity (embeddings)
    request_embedding = embed(user_request)
    for skill in all_skills:
        similarity = cosine_similarity(request_embedding, skill['embedding'])
        if similarity > 0.8:
            matching_skills.append((skill, similarity))
    
    # Return best match above threshold
    if matching_skills:
        best = max(matching_skills, key=lambda x: x[1])
        if best[1] > 0.7:  # Confidence threshold
            return best[0]
    
    return None
```

### Skill Loading in Workflow

```python
# Modified Blitz workflow

def start_project(user_request):
    # 1. Detect intent
    intent = detect_intent(user_request)
    
    # 2. Try to load relevant skill
    skill = detect_skill_match(user_request, context)
    
    if skill:
        # 2a. Skill exists → Use it
        architect_prompt = f"""
        User wants: {user_request}
        
        RELEVANT SKILL DETECTED: {skill['name']}
        Confidence: {skill['confidence']}
        
        Use patterns from skill:
        {skill['patterns']}
        
        Consider tech stack:
        {skill['tech_stack']}
        
        Avoid pitfalls:
        {skill['pitfalls']}
        """
    else:
        # 2b. No skill → Build from scratch, will extract after
        architect_prompt = standard_prompt(user_request)
    
    # 3. Run architect with (or without) skill context
    architecture = run_architect(architect_prompt)
    
    # 4. After project completes, maybe extract skill
    if should_extract_skill(project_data):
        new_skill = extract_skill(project_data)
        save_skill(new_skill)
```

---

## Example: Full Lifecycle

### Project 1: "Build trading bot" (No skill exists)

```
User: "Build me a trading bot"
Blitz: "No relevant skills found. Building from scratch..."

[Architect researches for 12 minutes]
[Coder implements for 30 minutes]
[Project completes successfully]

Blitz: "Patterns detected! Extracting skill..."
→ Created: trading-bot-patterns (confidence: 0.85)

Result: 42 minutes, $0.50, no skill reuse yet
```

### Project 2: "Build crypto trading bot" (Skill exists)

```
User: "Build me a crypto trading bot"
Blitz: "Skill match: trading-bot-patterns (confidence: 0.85)"
       "Adapting patterns for crypto..."

[Architect uses skill patterns, adapts for crypto]
[Coder implements with skill patterns]
[Project completes successfully]

Blitz: "Skill performed well! Updating..."
→ Updated: trading-bot-patterns (confidence: 0.90, uses: 1)
→ Added variant: "Works for crypto too"

Result: 25 minutes, $0.25, 40% faster with skill
```

### Project 3: "Build stock screener" (Partial match)

```
User: "Build me a stock screener"
Blitz: "Partial skill match: trading-bot-patterns (0.65 confidence)"
       "Some patterns relevant (data fetching), adapting..."

[Uses: CachedPriceFetcher pattern from skill]
[Ignores: PaperTrading pattern (not relevant)]
[Adds: Screening logic (new pattern)]

Blitz: "New patterns detected! Creating screener skill..."
→ Created: stock-screener-patterns (confidence: 0.80)
→ Linked to: trading-bot-patterns (similar domain)

Result: 20 minutes, $0.20, used partial skill
```

---

## Implementation in Blitz

### New Components

```python
# core/skill_extractor.py
class SkillExtractor:
    """Extracts skills from completed projects"""
    
    def extract_from_project(self, project_dir: Path) -> Optional[Skill]:
        # Analyze decisions.md
        # Analyze architecture.md
        # Identify reusable patterns
        # Generate skill content
        pass

# core/skill_registry.py  
class SkillRegistry:
    """Manages auto-generated skills"""
    
    def find_match(self, user_request: str) -> Optional[Skill]:
        # Keyword matching
        # Embedding similarity
        # Tech stack matching
        pass
    
    def update_skill(self, skill_id: str, project_data: dict):
        # Increase confidence
        # Add variants
        # Update patterns
        pass

# core/skill_loader.py
class SkillLoader:
    """Loads skills into agent context"""
    
    def load_for_architect(self, skill: Skill) -> str:
        # Format skill as architect prompt context
        pass
```

### Modified Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ User: "Build trading bot"                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Blitz: detect_skill_match()                                 │
│ Result: No skill found                                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Standard build process                                      │
│ Architect + Coder work from scratch                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Project completes successfully                              │
│ Blitz: should_extract_skill()? → YES                        │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Extract patterns → Create skill                             │
│ "trading-bot-patterns" created (confidence: 0.85)           │
└─────────────────────────────────────────────────────────────┘

Next time: "Build crypto bot"
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Blitz: detect_skill_match()                                 │
│ Result: trading-bot-patterns (0.85 confidence)              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Load skill context into architect prompt                    │
│ Faster build, proven patterns                               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Project completes                                           │
│ Update skill: confidence 0.85 → 0.90, usage_count 1         │
└─────────────────────────────────────────────────────────────┘
```

---

## Benefits

| Without Auto-Skills | With Auto-Skills |
|---------------------|------------------|
| Every project starts from scratch | Projects leverage previous learnings |
| 12-15 min research each time | 2-3 min skill loading |
| Generic, inconsistent patterns | Proven, battle-tested patterns |
| Knowledge lost between sessions | Institutional memory builds over time |
| $0.40-0.50 per architecture | $0.08-0.12 with skill reuse |
| Manual skill curation | Fully automatic extraction |

---

## Key Insights

**1. Skills emerge, not defined**
- No upfront work
- Natural selection: useful patterns survive

**2. Confidence scores matter**
- Experimental (1 project)
- Proven (3+ projects)
- Established (10+ projects)

**3. Partial matching**
- Skills don't have to be perfect matches
- Use relevant patterns, ignore irrelevant ones

**4. Continuous evolution**
- Skills get better with each use
- New variants added automatically
- Outdated patterns deprecated

---

*Blitz starts dumb. Every project makes it smarter.*

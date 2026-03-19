#!/bin/bash
# Blitz v3 Installer
# Simple 50-line installer

set -e

echo "🚀 Installing Blitz v3..."

# Find project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLITZ_DIR="$SCRIPT_DIR"

# Find Claude Code skills directory
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"

if [ ! -d "$CLAUDE_DIR" ]; then
    echo "❌ Claude Code not found at ~/.claude"
    echo "   Install Claude Code first: https://claude.ai/code"
    exit 1
fi

# Create skills directory if needed
mkdir -p "$SKILLS_DIR"

# Copy Blitz to Claude skills
BLITZ_SKILL_DIR="${SKILLS_DIR}/blitz-v3"
echo "📦 Installing to: $BLITZ_SKILL_DIR"

# Remove old version if exists
rm -rf "$BLITZ_SKILL_DIR"

# Copy files
cp -r "$BLITZ_DIR" "$BLITZ_SKILL_DIR"

# Create symlink for easy access
ln -sf "$BLITZ_SKILL_DIR" "${SKILLS_DIR}/blitz" 2>/dev/null || true

# Install CLAUDE.md hook
echo "🔗 Installing CLAUDE.md hook..."

# Check if user has existing CLAUDE.md
USER_CLAUDE_MD="${CLAUDE_DIR}/CLAUDE.md"
if [ -f "$USER_CLAUDE_MD" ]; then
    echo "⚠️  Existing CLAUDE.md found"
    echo "   Backup saved to: ${USER_CLAUDE_MD}.backup"
    cp "$USER_CLAUDE_MD" "${USER_CLAUDE_MD}.backup"
fi

# Append Blitz instructions to CLAUDE.md
cat >> "$USER_CLAUDE_MD" << 'EOF'

# Blitz v3 Integration

When user wants to build/create/fix something:

1. Ask 3-4 quick clarification questions (60 seconds)
2. Initialize project with blitz_v3.core
3. Spawn background agents (researcher, architect, coder)
4. Execute agents and give natural progress updates every 5-10 min
5. Deliver working code with auto-updated docs

Key rules:
- No commands - user just chats
- Auto-update all docs (never ask user)
- Background execution - casual updates only
- Interruptible anytime

Import from: ${SKILLS_DIR}/blitz-v3/core
EOF

echo ""
echo "✅ Blitz v3 installed!"
echo ""

# Run interactive setup
python3 "${BLITZ_SKILL_DIR}/setup.py"

echo ""
echo "Documentation: ${BLITZ_SKILL_DIR}/README.md"

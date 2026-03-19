#!/bin/bash
# Buildmate v3 Installer
# Simple 50-line installer

set -e

echo "🚀 Installing Buildmate v3..."

# Find project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILDMATE_DIR="$SCRIPT_DIR"

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

# Copy Buildmate to Claude skills
BUILDMATE_SKILL_DIR="${SKILLS_DIR}/buildmate-v3"
echo "📦 Installing to: $BUILDMATE_SKILL_DIR"

# Remove old version if exists
rm -rf "$BUILDMATE_SKILL_DIR"

# Copy files
cp -r "$BUILDMATE_DIR" "$BUILDMATE_SKILL_DIR"

# Create symlink for easy access
ln -sf "$BUILDMATE_SKILL_DIR" "${SKILLS_DIR}/buildmate" 2>/dev/null || true

# Install CLAUDE.md hook
echo "🔗 Installing CLAUDE.md hook..."

# Check if user has existing CLAUDE.md
USER_CLAUDE_MD="${CLAUDE_DIR}/CLAUDE.md"
if [ -f "$USER_CLAUDE_MD" ]; then
    echo "⚠️  Existing CLAUDE.md found"
    echo "   Backup saved to: ${USER_CLAUDE_MD}.backup"
    cp "$USER_CLAUDE_MD" "${USER_CLAUDE_MD}.backup"
fi

# Append Buildmate instructions to CLAUDE.md
cat >> "$USER_CLAUDE_MD" << 'EOF'

# Buildmate v3 Integration

When user wants to build/create/fix something:

1. Ask 3-4 quick clarification questions (60 seconds)
2. Initialize project with buildmate_v3.core
3. Spawn background agents (researcher, architect, coder)
4. Execute agents and give natural progress updates every 5-10 min
5. Deliver working code with auto-updated docs

Key rules:
- No commands - user just chats
- Auto-update all docs (never ask user)
- Background execution - casual updates only
- Interruptible anytime

Import from: ${SKILLS_DIR}/buildmate-v3/core
EOF

echo ""
echo "✅ Buildmate v3 installed!"
echo ""
echo "Next steps:"
echo "1. Start a new Claude Code session"
echo "2. Say: 'Build me a [project]'"
echo "3. Answer 3-4 quick questions"
echo "4. Let Buildmate work"
echo ""
echo "Documentation: ${BUILDMATE_SKILL_DIR}/README.md"

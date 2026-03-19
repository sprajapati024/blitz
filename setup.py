#!/usr/bin/env python3
"""
Blitz v3 Setup Wizard
Interactive onboarding when installing Blitz
"""

import os
import sys
import json
from pathlib import Path
from enum import Enum
from datetime import datetime, timezone

# Colors for terminal output
class Colors:
    GOLD = "\033[1;33m"
    CYAN = "\033[1;36m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[1;31m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

def print_header(text: str):
    """Print a styled header"""
    print(f"\n{Colors.CYAN}◆ {text}{Colors.RESET}")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text: str):
    """Print info text"""
    print(f"{Colors.DIM}  {text}{Colors.RESET}")

def prompt(question: str, default: str = None) -> str:
    """Prompt for input"""
    if default:
        display = f"{Colors.YELLOW}{question} [{default}]: {Colors.RESET}"
    else:
        display = f"{Colors.YELLOW}{question}: {Colors.RESET}"
    try:
        value = input(display).strip()
        return value or default or ""
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(1)

def prompt_choice(question: str, choices: list, default: int = 0) -> int:
    """Prompt for a choice from a list"""
    print(f"\n{Colors.CYAN}{question}{Colors.RESET}")
    for i, choice in enumerate(choices):
        marker = "●" if i == default else "○"
        if i == default:
            print(f"  {Colors.GREEN}{marker} {choice}{Colors.RESET}")
        else:
            print(f"  {marker} {choice}")
    print(f"{Colors.DIM}  Enter 1-{len(choices)} (default: {default + 1}){Colors.RESET}")

    while True:
        try:
            value = input(f"{Colors.YELLOW}  Select: {Colors.RESET}").strip()
            if not value:
                return default
            idx = int(value) - 1
            if 0 <= idx < len(choices):
                return idx
            print_error(f"Please enter a number between 1 and {len(choices)}")
        except ValueError:
            print_error("Please enter a number")
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(1)

def check_claude_code() -> bool:
    """Check if Claude Code is installed"""
    claude_dir = Path.home() / ".claude"
    return claude_dir.exists()

def print_welcome_banner():
    """Print the welcome banner"""
    banner = f"""
{Colors.GOLD}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ⚡️ {Colors.BOLD}Welcome to the Other Side, Builder{Colors.RESET}{Colors.GOLD}                    ║
║                                                              ║
║  {Colors.DIM}You found Blitz — where ideas actually become real.{Colors.RESET}{Colors.GOLD}        ║
║  {Colors.DIM}No more abandoned projects. No more decision fatigue.{Colors.RESET}{Colors.GOLD}       ║
║  {Colors.DIM}Just describe what you want, and watch it happen.{Colors.RESET}{Colors.GOLD}          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def select_tone() -> str:
    """Let user select their preferred tone"""
    print_header("Step 1: Pick Your Vibe")
    print_info("This changes how Blitz talks to you during builds")
    print()

    tones = [
        ("Sassy & Fun", "Professional but with personality. 'Your MVP is ALIVE! 🚀'"),
        ("Chill & Casual", "Like a smart friend. 'Cool, structure's locked in.'"),
        ("Professional", "Straight to business. 'Project structure complete.'"),
        ("Minimal", "Just the facts. Updates only when you ask."),
    ]

    for i, (name, desc) in enumerate(tones):
        print(f"  {i+1}. {Colors.BOLD}{name}{Colors.RESET}")
        print(f"     {Colors.DIM}{desc}{Colors.RESET}")
        print()

    choice = prompt_choice("How should Blitz talk to you?", [t[0] for t in tones], 0)
    selected = tones[choice][0].lower().split()[0]  # 'sassy', 'chill', 'professional', 'minimal'

    print_success(f"Tone set: {tones[choice][0]}")
    return selected

def select_trust_mode() -> str:
    """Let user select their trust mode"""
    print_header("Step 2: Choose Your Trust Mode")
    print_info("How much should Blitz work independently?")
    print()

    modes = [
        ("Notify Mode", "Blitz tells you what it's about to do, waits for OK", "Best for: Getting to know Blitz", 0),
        ("Auto Mode", "Blitz executes directly, tells you after it's done", "Best for: Regular users", 3),
        ("Ghost Mode", "Blitz works silently, daily summary only", "Best for: Full trust / power users", 10),
    ]

    for i, (name, desc, best_for, _) in enumerate(modes):
        print(f"  {i+1}. {Colors.BOLD}{name}{Colors.RESET}")
        print(f"     {desc}")
        print(f"     {Colors.DIM}{best_for}{Colors.RESET}")
        print()

    choice = prompt_choice("How hands-on do you want to be?", [m[0] for m in modes], 0)
    selected = modes[choice][0].lower().split()[0]  # 'notify', 'auto', 'ghost'

    print_success(f"Trust mode: {modes[choice][0]}")
    return selected

def save_preferences(tone: str, trust_mode: str):
    """Save user preferences to ~/.blitz/ where trust_manager expects them"""
    blitz_home = Path.home() / ".blitz"
    prefs_file = blitz_home / "preferences.json"

    prefs = {
        "trust_mode": trust_mode,
        "tone": tone,
        "onboarded": True,
        "version": "3.1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "settings": {
            "auto_switch_threshold": True,
            "ghost_summary_time": "09:00",
            "progress_update_interval": 300
        }
    }

    blitz_home.mkdir(parents=True, exist_ok=True)
    prefs_file.write_text(json.dumps(prefs, indent=2))
    print_info(f"Preferences saved to: {prefs_file}")

def print_next_steps():
    """Print what to do next"""
    print_header("You're In! 🎉")
    print()
    print(f"{Colors.BOLD}Next steps:{Colors.RESET}")
    print("  1. Start a new Claude Code session")
    print("  2. Say: 'Build me a trading bot' or whatever you want")
    print("  3. Answer 3-4 quick questions")
    print("  4. Watch your team work ⚡️")
    print()
    print(f"{Colors.DIM}Change settings anytime: blitz config{Colors.RESET}")
    print()

def run_setup():
    """Main setup flow"""
    print_welcome_banner()

    # Check Claude Code
    print_header("Checking Prerequisites")
    if check_claude_code():
        print_success("Claude Code detected ✓")
    else:
        print_error("Claude Code not found")
        print_info("Install Claude Code first: https://claude.ai/code")
        print()
        response = prompt("Continue anyway? (y/n)", "n").lower()
        if response not in ('y', 'yes'):
            print_info("Setup cancelled. Install Claude Code and try again.")
            return

    # Select preferences
    tone = select_tone()
    trust_mode = select_trust_mode()

    # Save preferences
    print_header("Saving Your Preferences")
    save_preferences(tone, trust_mode)
    print_success("All set!")

    # Next steps
    print_next_steps()

    print(f"{Colors.GOLD}{Colors.BOLD}Welcome to the other side. Let's build something awesome.{Colors.RESET}")
    print()

if __name__ == "__main__":
    try:
        run_setup()
    except KeyboardInterrupt:
        print()
        print_info("Setup cancelled. Run again anytime with: python setup.py")
        sys.exit(0)

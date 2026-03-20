#!/usr/bin/env python3
"""
Blitz v3 Setup Wizard
Interactive onboarding with curses arrow key navigation
"""

import os
import sys
import json
import subprocess
import curses
from pathlib import Path
from datetime import datetime, timezone


# ============================================================================
# Colors for non-curses fallback
# ============================================================================
class Colors:
    GOLD = "\033[38;5;220m"
    CYAN = "\033[38;5;51m"
    GREEN = "\033[38;5;82m"
    YELLOW = "\033[38;5;227m"
    RED = "\033[38;5;196m"
    MAGENTA = "\033[38;5;201m"
    ORANGE = "\033[38;5;208m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


# ============================================================================
# Curses-based Interactive Menu
# ============================================================================


def curses_menu(
    stdscr,
    title: str,
    options: list,
    descriptions: list = None,
    current_idx: int = 0,
    show_current: str = None,
) -> int:
    """
    Display an interactive menu with arrow key navigation

    Args:
        stdscr: curses window
        title: Menu title
        options: List of option strings
        descriptions: Optional list of descriptions for each option
        current_idx: Default selected index
        show_current: Text to show as [current] next to current selection

    Returns:
        Selected index
    """
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    # Enable colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)  # Title
    curses.init_pair(2, curses.COLOR_GREEN, -1)  # Selected
    curses.init_pair(3, curses.COLOR_WHITE, -1)  # Normal
    curses.init_pair(4, curses.COLOR_YELLOW, -1)  # Highlight
    curses.init_pair(5, 245, -1)  # Dim
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)  # Accent

    selected = current_idx

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Draw banner top
        banner_text = "⚡️ BLITZ SETUP"
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1, (width - len(banner_text)) // 2, banner_text)
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # Draw separator line
        stdscr.attron(curses.color_pair(5))
        stdscr.addstr(2, 2, "─" * (width - 4))
        stdscr.attroff(curses.color_pair(5))

        # Draw title
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(4, 4, f"◆ {title}")
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # Draw options
        start_y = 6
        for i, option in enumerate(options):
            y = start_y + i * 2

            if i == selected:
                # Selected item
                arrow = "▶"
                stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                stdscr.addstr(y, 4, f"{arrow} {option}")
                if show_current and i == current_idx:
                    stdscr.addstr(y, 4 + len(arrow) + len(option) + 2, "[current]")
                stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

                # Description
                if descriptions and i < len(descriptions):
                    stdscr.attron(curses.color_pair(5))
                    stdscr.addstr(y + 1, 8, descriptions[i])
                    stdscr.attroff(curses.color_pair(5))
            else:
                # Unselected item
                arrow = "○"
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(y, 4, f"{arrow} {option}")
                if show_current and i == current_idx:
                    stdscr.attron(curses.color_pair(6))
                    stdscr.addstr(y, 4 + len(arrow) + len(option) + 2, "[current]")
                    stdscr.attroff(curses.color_pair(6))
                stdscr.attroff(curses.color_pair(3))

                # Description
                if descriptions and i < len(descriptions):
                    stdscr.attron(curses.color_pair(5))
                    stdscr.addstr(y + 1, 8, descriptions[i])
                    stdscr.attroff(curses.color_pair(5))

        # Draw footer
        footer_y = height - 2
        stdscr.attron(curses.color_pair(5))
        stdscr.addstr(footer_y, 4, "↑↓ Navigate  •  Enter Select  •  q Quit")
        stdscr.attroff(curses.color_pair(5))

        stdscr.refresh()

        # Handle input
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % len(options)
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            return selected
        elif key in (27, ord("q")):  # ESC or q
            return current_idx


def run_curses_menu(
    title: str,
    options: list,
    descriptions: list = None,
    current_idx: int = 0,
    show_current: str = None,
) -> int:
    """Wrapper to run curses menu with fallback"""
    # Check if we're in a proper interactive terminal
    if not sys.stdout.isatty() or not sys.stdin.isatty():
        print(
            f"  {Colors.DIM}Non-interactive terminal detected, using text fallback{Colors.RESET}"
        )
        return fallback_menu(title, options, descriptions, current_idx)

    try:
        # Try curses
        return curses.wrapper(
            curses_menu, title, options, descriptions, current_idx, show_current
        )
    except Exception as e:
        # If curses fails, use fallback but print why
        return fallback_menu(title, options, descriptions, current_idx)


def fallback_menu(
    title: str, options: list, descriptions: list = None, current_idx: int = 0
) -> int:
    """Fallback menu that looks good even without curses"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}◆ {title}{Colors.RESET}\n")

    for i, option in enumerate(options):
        if i == current_idx:
            # Selected item
            marker = f"{Colors.GREEN}▶{Colors.RESET}"
            option_text = f"{Colors.BOLD}{Colors.GREEN}{option}{Colors.RESET}"
            current_tag = (
                f" {Colors.MAGENTA}[current]{Colors.RESET}" if current_idx == i else ""
            )
            print(f"  {marker} {option_text}{current_tag}")
        else:
            # Unselected item
            marker = "○"
            option_text = option
            current_tag = (
                f" {Colors.MAGENTA}[current]{Colors.RESET}" if current_idx == i else ""
            )
            print(f"  {marker} {option_text}{current_tag}")

        # Description
        if descriptions and i < len(descriptions):
            print(f"     {Colors.DIM}{descriptions[i]}{Colors.RESET}")

    print(
        f"\n  {Colors.DIM}Use ↑↓ arrow keys or type number (1-{len(options)}){Colors.RESET}"
    )
    print()

    while True:
        try:
            choice = input(f"{Colors.YELLOW}  Select: {Colors.RESET}").strip()
            if not choice:
                return current_idx
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return idx
            print(f"  {Colors.RED}Please enter 1-{len(options)}{Colors.RESET}")
        except ValueError:
            # Check for arrow key escape sequences (if terminal sends them as input)
            if choice == "\x1b[A":  # Up arrow
                return (current_idx - 1) % len(options)
            elif choice == "\x1b[B":  # Down arrow
                return (current_idx + 1) % len(options)
            print(f"  {Colors.RED}Please enter a number{Colors.RESET}")
        except KeyboardInterrupt:
            return current_idx


# ============================================================================
# Setup Functions
# ============================================================================


def print_welcome_banner():
    """Print welcome banner"""
    banner = f"""
{Colors.GOLD}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.GOLD}{Colors.BOLD}║{Colors.RESET}                                                              {Colors.GOLD}{Colors.BOLD}║{Colors.RESET}
{Colors.GOLD}{Colors.BOLD}║{Colors.RESET}  ⚡️ {Colors.BOLD}Welcome to the Other Side, Builder{Colors.RESET}{Colors.GOLD}{" " * 27}║{Colors.RESET}
{Colors.GOLD}{Colors.BOLD}║{Colors.RESET}                                                              {Colors.GOLD}{Colors.BOLD}║{Colors.RESET}
{Colors.GOLD}{Colors.BOLD}║{Colors.RESET}  {Colors.DIM}You found Blitz — where ideas actually become real.{Colors.RESET}{Colors.GOLD}        ║{Colors.RESET}
{Colors.GOLD}{Colors.BOLD}║{Colors.RESET}  {Colors.DIM}No more abandoned projects. No more decision fatigue.{Colors.RESET}{Colors.GOLD}       ║{Colors.RESET}
{Colors.GOLD}{Colors.BOLD}║{Colors.RESET}  {Colors.DIM}Just describe what you want, and watch it happen.{Colors.RESET}{Colors.GOLD}          ║{Colors.RESET}
{Colors.GOLD}{Colors.BOLD}║{Colors.RESET}                                                              {Colors.GOLD}{Colors.BOLD}║{Colors.RESET}
{Colors.GOLD}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def check_claude_code() -> bool:
    """Check if Claude Code is installed"""
    claude_dir = Path.home() / ".claude"
    return claude_dir.exists()


def verify_claude_code() -> bool:
    """Verify Claude Code actually works by running --version"""
    try:
        result = subprocess.run(["claude", "--version"], capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False


def get_current_prefs() -> dict:
    """Load current preferences if they exist"""
    prefs_file = Path.home() / ".blitz" / "preferences.json"
    if prefs_file.exists():
        try:
            return json.loads(prefs_file.read_text())
        except:
            pass
    return {"tone": "sassy", "trust_mode": "notify", "onboarded": False}


def select_tone(current: str = "sassy") -> str:
    """Select tone with arrow keys"""
    tones = [
        (
            "sassy",
            "Sassy & Fun",
            "Professional with personality. 'Your MVP is ALIVE! 🚀'",
        ),
        (
            "chill",
            "Chill & Casual",
            "Like a smart friend. 'Cool, structure's locked in.'",
        ),
        ("pro", "Professional", "Straight to business. 'Project structure complete.'"),
        ("minimal", "Minimal", "Just the facts. Updates only when you ask."),
    ]

    # Find current index
    current_idx = 0
    for i, (key, _, _) in enumerate(tones):
        if key == current:
            current_idx = i
            break

    options = [t[1] for t in tones]
    descriptions = [t[2] for t in tones]

    choice = run_curses_menu(
        "Pick Your Vibe",
        options,
        descriptions,
        current_idx,
        show_current="current" if current else None,
    )

    selected = tones[choice][0]
    print(
        f"\n  {Colors.GREEN}✓{Colors.RESET} Tone: {Colors.BOLD}{tones[choice][1]}{Colors.RESET}"
    )
    return selected


def select_trust_mode(current: str = "notify") -> str:
    """Select trust mode with arrow keys"""
    modes = [
        (
            "notify",
            "Notify Mode",
            "Blitz tells you what it's about to do, waits for OK",
        ),
        (
            "auto",
            "Auto Mode ★ LOCKED",
            "Blitz executes directly, tells you after it's done [3+ projects]",
        ),
        (
            "ghost",
            "Ghost Mode ★ LOCKED",
            "Blitz works silently, daily summary only [10+ projects]",
        ),
    ]

    # Find current index
    current_idx = 0
    for i, (key, _, _) in enumerate(modes):
        if key == current:
            current_idx = i
            break

    options = [m[1] for m in modes]
    descriptions = [m[2] for m in modes]

    choice = run_curses_menu(
        "Choose Your Trust Mode",
        options,
        descriptions,
        current_idx,
        show_current="current" if current else None,
    )

    selected = modes[choice][0]
    print(
        f"\n  {Colors.GREEN}✓{Colors.RESET} Trust Mode: {Colors.BOLD}{modes[choice][1]}{Colors.RESET}"
    )
    return selected


def save_preferences(tone: str, trust_mode: str):
    """Save user preferences"""
    blitz_home = Path.home() / ".blitz"
    prefs_file = blitz_home / "preferences.json"

    prefs = {
        "trust_mode": trust_mode,
        "tone": tone,
        "onboarded": True,
        "version": "3.1",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "settings": {
            "auto_switch_threshold": True,
            "ghost_summary_time": "09:00",
            "progress_update_interval": 300,
        },
    }

    blitz_home.mkdir(parents=True, exist_ok=True)
    prefs_file.write_text(json.dumps(prefs, indent=2))

    print(f"  {Colors.DIM}Config saved: {prefs_file}{Colors.RESET}")


def print_completion():
    """Print completion message"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}◆ You're In! 🎉{Colors.RESET}\n")
    print(f"  {Colors.BOLD}Next steps:{Colors.RESET}")
    print("  1. Start a new Claude Code session")
    print("  2. Say: 'Build me a trading bot' or whatever you want")
    print("  3. Answer 3-4 quick questions")
    print("  4. Watch your team work ⚡️")
    print()
    print(f"  {Colors.DIM}Reconfigure anytime: blitz config{Colors.RESET}")
    print()
    print(
        f"{Colors.GOLD}{Colors.BOLD}  Welcome to the other side. Let's build something awesome.{Colors.RESET}"
    )
    print()


def run_setup():
    """Main setup flow"""
    # Always show the banner
    print_welcome_banner()

    # Load current preferences (for reconfig)
    current = get_current_prefs()
    is_reconfig = current.get("onboarded", False)

    # Check Claude Code
    print(f"{Colors.CYAN}{Colors.BOLD}◆ Checking Prerequisites{Colors.RESET}")
    if check_claude_code():
        print(f"  {Colors.GREEN}✓{Colors.RESET} Claude Code detected")
        if not verify_claude_code():
            print(
                f"  {Colors.RED}✗{Colors.RESET} Claude Code found but not working properly"
            )
            print(
                f"  {Colors.DIM}Try: claude --version or reinstall: https://claude.ai/code{Colors.RESET}\n"
            )
            print(
                f"  {Colors.YELLOW}Setup blocked - please fix Claude Code first{Colors.RESET}\n"
            )
            sys.exit(1)
        print(f"  {Colors.GREEN}✓{Colors.RESET} Claude Code verified\n")
    else:
        print(f"  {Colors.YELLOW}⚠{Colors.RESET} Claude Code not found")
        print(f"  {Colors.DIM}Install: https://claude.ai/code{Colors.RESET}\n")
        print(
            f"  {Colors.YELLOW}Setup blocked - Claude Code is required{Colors.RESET}\n"
        )
        sys.exit(1)

    # Select preferences
    if is_reconfig:
        print(f"{Colors.CYAN}{Colors.BOLD}◆ Reconfiguring Blitz{Colors.RESET}\n")

    tone = select_tone(current.get("tone", "sassy"))
    trust_mode = select_trust_mode(current.get("trust_mode", "notify"))

    # Save
    print(f"\n{Colors.CYAN}{Colors.BOLD}◆ Saving Configuration{Colors.RESET}")
    save_preferences(tone, trust_mode)
    print(f"  {Colors.GREEN}✓{Colors.RESET} Saved!\n")

    # Completion
    print_completion()


if __name__ == "__main__":
    try:
        run_setup()
    except KeyboardInterrupt:
        print(
            f"\n\n{Colors.DIM}Setup cancelled. Run 'blitz config' to try again.{Colors.RESET}"
        )
        sys.exit(0)

#!/usr/bin/env python3
"""
Blitz v3 Setup Wizard
Interactive onboarding with curses arrow key navigation
"""

import os
import sys
import json
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

def curses_menu(stdscr, title: str, options: list, descriptions: list = None, 
                current_idx: int = 0, show_current: str = None, 
                allow_back: bool = True, skip_option: bool = False) -> int:
    """
    Display an interactive menu with arrow key navigation
    
    Args:
        stdscr: curses window
        title: Menu title
        options: List of option strings
        descriptions: Optional list of descriptions for each option
        current_idx: Default selected index
        show_current: Text to show as [current] next to current selection
        allow_back: If True, allow going back (returns -1)
        skip_option: If True, show "Skip / Keep Current" option
    
    Returns:
        Selected index, or -1 for back, or -2 for skip
    """
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    
    # Enable colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)      # Title
    curses.init_pair(2, curses.COLOR_GREEN, -1)     # Selected
    curses.init_pair(3, curses.COLOR_WHITE, -1)     # Normal
    curses.init_pair(4, curses.COLOR_YELLOW, -1)    # Highlight
    curses.init_pair(5, 245, -1)                    # Dim
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)   # Accent
    curses.init_pair(7, curses.COLOR_CYAN, -1)     # Skip option
    
    # Add skip option to the list if enabled
    all_options = options[:]
    all_descriptions = descriptions[:] if descriptions else None
    
    if skip_option:
        all_options.append("Skip / Keep Current")
        if all_descriptions:
            all_descriptions.append("Use your current setting (skip this step)")
    
    # Adjust selected index if current is out of bounds
    if current_idx >= len(all_options):
        current_idx = 0
    
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
        for i, option in enumerate(all_options):
            y = start_y + i * 2
            is_skip_option = skip_option and i == len(options)
            
            if i == selected:
                # Selected item
                arrow = "▶"
                color = curses.color_pair(7) if is_skip_option else curses.color_pair(2)
                stdscr.attron(color | curses.A_BOLD)
                stdscr.addstr(y, 4, f"{arrow} {option}")
                stdscr.attroff(color | curses.A_BOLD)
                
                # Description
                if all_descriptions and i < len(all_descriptions):
                    stdscr.attron(curses.color_pair(5))
                    stdscr.addstr(y + 1, 8, all_descriptions[i])
                    stdscr.attroff(curses.color_pair(5))
            else:
                # Unselected item
                arrow = "○"
                color = curses.color_pair(7) if is_skip_option else curses.color_pair(3)
                stdscr.attron(color)
                stdscr.addstr(y, 4, f"{arrow} {option}")
                stdscr.attroff(color)
                
                # Description
                if all_descriptions and i < len(all_descriptions):
                    stdscr.attron(curses.color_pair(5))
                    stdscr.addstr(y + 1, 8, all_descriptions[i])
                    stdscr.attroff(curses.color_pair(5))
        
        # Draw footer
        footer_y = height - 2
        stdscr.attron(curses.color_pair(5))
        
        # Build footer text based on options
        footer_parts = ["↑↓ Navigate", "Enter Select"]
        if skip_option:
            footer_parts.append("s Skip")
        if allow_back:
            footer_parts.append("b Back")
        footer_parts.append("q Quit")
        
        footer_text = "  •  ".join(footer_parts)
        stdscr.addstr(footer_y, 4, footer_text)
        stdscr.attroff(curses.color_pair(5))
        
        stdscr.refresh()
        
        # Handle input
        key = stdscr.getch()
        
        if key in (curses.KEY_UP, ord('k')):
            selected = (selected - 1) % len(all_options)
        elif key in (curses.KEY_DOWN, ord('j')):
            selected = (selected + 1) % len(all_options)
        elif key in (curses.KEY_ENTER, 10, 13):
            # If skip option selected
            if skip_option and selected == len(options):
                return -2  # Skip signal
            return selected
        elif allow_back and key in (curses.KEY_BACKSPACE, ord('b'), ord('B')):
            return -1  # Back signal
        elif key in (27, ord('q'), ord('Q')):  # ESC or q
            return current_idx

def run_curses_menu(title: str, options: list, descriptions: list = None, 
                    current_idx: int = 0, show_current: str = None,
                    allow_back: bool = True, skip_option: bool = False) -> tuple:
    """Wrapper to run curses menu with fallback.
    
    Returns:
        tuple: (selected_index, action) where action is 'select', 'back', 'skip', or 'quit'
    """
    # Check if we're in a proper interactive terminal
    if not sys.stdout.isatty() or not sys.stdin.isatty():
        return fallback_menu(title, options, descriptions, current_idx, skip_option)
    
    try:
        # Try curses
        result = curses.wrapper(
            curses_menu, title, options, descriptions, current_idx, show_current,
            allow_back, skip_option
        )
        if result == -1:
            return (current_idx, 'back')
        elif result == -2:
            return (current_idx, 'skip')
        return (result, 'select')
    except Exception as e:
        # If curses fails, use fallback but print why
        return fallback_menu(title, options, descriptions, current_idx, skip_option)

def fallback_menu(title: str, options: list, descriptions: list = None, 
                  current_idx: int = 0, skip_option: bool = False, allow_back: bool = True) -> tuple:
    """Fallback menu that looks good even without curses.
    
    Returns:
        tuple: (selected_index, action) where action is 'select', 'back', 'skip', or 'quit'
    """
    # Add skip option if enabled
    all_options = options[:]
    all_descriptions = descriptions[:] if descriptions else []
    
    if skip_option:
        all_options.append("Skip / Keep Current")
        all_descriptions.append("Use your current setting (skip this step)")
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}◆ {title}{Colors.RESET}\n")
    
    for i, option in enumerate(all_options):
        if i == current_idx:
            # Selected item
            marker = f"{Colors.GREEN}▶{Colors.RESET}"
            option_text = f"{Colors.BOLD}{Colors.GREEN}{option}{Colors.RESET}"
            print(f"  {marker} {option_text}")
        else:
            # Unselected item
            marker = "○"
            option_text = option
            print(f"  {marker} {option_text}")
        
        # Description
        if all_descriptions and i < len(all_descriptions):
            print(f"     {Colors.DIM}{all_descriptions[i]}{Colors.RESET}")
    
    print(f"\n  {Colors.DIM}↑↓ or number to select{Colors.RESET}")
    if skip_option:
        print(f"  {Colors.DIM}s to skip this step{Colors.RESET}")
    if allow_back:
        print(f"  {Colors.DIM}b to go back{Colors.RESET}")
    print()
    
    while True:
        try:
            choice = input(f"{Colors.YELLOW}  Select: {Colors.RESET}").strip().lower()
            
            # Handle special commands
            if choice in ('q', 'quit', 'exit'):
                return (current_idx, 'quit')
            if choice in ('b', 'back') and allow_back:
                return (current_idx, 'back')
            if choice in ('s', 'skip') and skip_option:
                return (current_idx, 'skip')
            
            # Empty input = accept current
            if not choice:
                if skip_option and current_idx >= len(options):
                    return (current_idx, 'skip')
                return (current_idx, 'select')
            
            # Try to parse as number
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(all_options):
                    if skip_option and idx == len(options):
                        return (idx, 'skip')
                    return (idx, 'select')
                print(f"  {Colors.RED}Please enter 1-{len(all_options)}{Colors.RESET}")
            except ValueError:
                # Arrow key handling is limited in fallback mode
                print(f"  {Colors.RED}Please enter a number, or b/s/q{Colors.RESET}")
        except KeyboardInterrupt:
            return (current_idx, 'quit')

# ============================================================================
# Setup Functions
# ============================================================================

def print_welcome_banner():
    """Print welcome banner"""
    banner = f"""
{Colors.GOLD}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.GOLD}{Colors.BOLD}║{Colors.RESET}                                                              {Colors.GOLD}{Colors.BOLD}║{Colors.RESET}
{Colors.GOLD}{Colors.BOLD}║{Colors.RESET}  ⚡️ {Colors.BOLD}Welcome to the Other Side, Builder{Colors.RESET}{Colors.GOLD}{' ' * 27}║{Colors.RESET}
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

def get_current_prefs() -> dict:
    """Load current preferences if they exist"""
    prefs_file = Path.home() / ".blitz" / "preferences.json"
    if prefs_file.exists():
        try:
            return json.loads(prefs_file.read_text())
        except:
            pass
    return {"tone": "sassy", "trust_mode": "notify", "onboarded": False}

def select_tone(current: str = "sassy", skip_if_set: bool = False) -> tuple:
    """Select tone with arrow keys.
    
    Returns:
        tuple: (selected_tone_key, changed: bool)
    """
    tones = [
        ("sassy", "Sassy & Fun", "Professional with personality. 'Your MVP is ALIVE! 🚀'"),
        ("chill", "Chill & Casual", "Like a smart friend. 'Cool, structure's locked in.'"),
        ("pro", "Professional", "Straight to business. 'Project structure complete.'"),
        ("minimal", "Minimal", "Just the facts. Updates only when you ask."),
    ]
    
    # Find current index
    current_idx = 0
    for i, (key, _, _) in enumerate(tones):
        if key == current:
            current_idx = i
            break
    
    # If skip_if_set and already configured, skip this step
    if skip_if_set and current:
        return (current, False)
    
    options = [t[1] for t in tones]
    descriptions = [t[2] for t in tones]
    
    # Allow back only if this isn't the first step in a flow
    choice_idx, action = run_curses_menu(
        "Pick Your Vibe",
        options,
        descriptions,
        current_idx,
        show_current="current" if current else None,
        allow_back=False,  # First step, can't go back
        skip_option=skip_if_set  # Allow skipping if already set
    )
    
    if action == 'skip':
        print(f"\n  {Colors.DIM}✓ Keeping current: {Colors.BOLD}{current}{Colors.RESET}")
        return (current, False)
    elif action == 'quit':
        return (None, False)
    
    selected = tones[choice_idx][0]
    changed = selected != current
    print(f"\n  {Colors.GREEN}✓{Colors.RESET} Tone: {Colors.BOLD}{tones[choice_idx][1]}{Colors.RESET}")
    return (selected, changed)

def select_trust_mode(current: str = "notify", skip_if_set: bool = False) -> tuple:
    """Select trust mode with arrow keys.
    
    Returns:
        tuple: (selected_mode_key, changed: bool)
    """
    modes = [
        ("notify", "Notify Mode", "Blitz tells you what it's about to do, waits for OK"),
        ("auto", "Auto Mode", "Blitz executes directly, tells you after it's done [3+ projects]"),
        ("ghost", "Ghost Mode", "Blitz works silently, daily summary only [10+ projects]"),
    ]
    
    # Find current index
    current_idx = 0
    for i, (key, _, _) in enumerate(modes):
        if key == current:
            current_idx = i
            break
    
    # If skip_if_set and already configured, skip this step
    if skip_if_set and current:
        return (current, False)
    
    options = [m[1] for m in modes]
    descriptions = [m[2] for m in modes]
    
    choice_idx, action = run_curses_menu(
        "Choose Your Trust Mode",
        options,
        descriptions,
        current_idx,
        show_current="current" if current else None,
        allow_back=True,  # Can go back to tone selection
        skip_option=skip_if_set
    )
    
    if action == 'skip':
        print(f"\n  {Colors.DIM}✓ Keeping current: {Colors.BOLD}{current}{Colors.RESET}")
        return (current, False)
    elif action == 'quit':
        return (None, False)
    
    selected = modes[choice_idx][0]
    changed = selected != current
    print(f"\n  {Colors.GREEN}✓{Colors.RESET} Trust Mode: {Colors.BOLD}{modes[choice_idx][1]}{Colors.RESET}")
    return (selected, changed)

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
            "progress_update_interval": 300
        }
    }
    
    blitz_home.mkdir(parents=True, exist_ok=True)
    prefs_file.write_text(json.dumps(prefs, indent=2))
    
    print(f"  {Colors.DIM}Config saved: {prefs_file}{Colors.RESET}")

def print_summary_screen(tone: str, trust_mode: str, current_tone: str = None, current_trust: str = None):
    """Display one-screen summary before final save with review option"""
    tone_names = {
        "sassy": "Sassy & Fun",
        "chill": "Chill & Casual", 
        "pro": "Professional",
        "minimal": "Minimal"
    }
    trust_names = {
        "notify": "Notify Mode",
        "auto": "Auto Mode",
        "ghost": "Ghost Mode"
    }
    
    tone_changed = current_tone is None or tone != current_tone
    trust_changed = current_trust is None or trust_mode != current_trust
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.RESET}                    ◆ Review Your Setup                   {Colors.CYAN}{Colors.BOLD}║{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    # Tone
    tone_label = f"{Colors.GREEN}✓{Colors.RESET} " if tone_changed else f"{Colors.DIM}={Colors.RESET} "
    print(f"  {tone_label}{Colors.BOLD}Vibe:{Colors.RESET} {tone_names.get(tone, tone)}")
    if tone_changed and current_tone:
        print(f"        {Colors.DIM}(was: {tone_names.get(current_tone, current_tone)}){Colors.RESET}")
    
    # Trust Mode
    trust_label = f"{Colors.GREEN}✓{Colors.RESET} " if trust_changed else f"{Colors.DIM}={Colors.RESET} "
    print(f"  {trust_label}{Colors.BOLD}Trust Mode:{Colors.RESET} {trust_names.get(trust_mode, trust_mode)}")
    if trust_changed and current_trust:
        print(f"        {Colors.DIM}(was: {trust_names.get(current_trust, current_trust)}){Colors.RESET}")
    
    print()
    
    # Options
    print(f"  {Colors.YELLOW}→{Colors.RESET} Enter  - Looks good, save it")
    print(f"  {Colors.YELLOW}→{Colors.RESET} t       - Change tone")
    print(f"  {Colors.YELLOW}→{Colors.RESET} m       - Change trust mode")
    print(f"  {Colors.YELLOW}→{Colors.RESET} q       - Quit without saving")
    print()

def run_summary_review(tone: str, trust_mode: str, current_tone: str, current_trust: str) -> str:
    """Run the summary review loop.
    
    Returns:
        'save', 'tone', 'trust', or 'quit'
    """
    print_summary_screen(tone, trust_mode, current_tone, current_trust)
    
    while True:
        choice = input(f"{Colors.YELLOW}  Choice: {Colors.RESET}").strip().lower()
        
        if choice in ('', 'y', 'yes', 's', 'save'):
            return 'save'
        elif choice in ('t', 'tone', 'vibe'):
            return 'tone'
        elif choice in ('m', 'mode', 'trust'):
            return 'trust'
        elif choice in ('q', 'quit', 'exit'):
            return 'quit'
        else:
            print(f"  {Colors.RED}Enter to save, or t/m/q{Colors.RESET}")

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
    print(f"{Colors.GOLD}{Colors.BOLD}  Welcome to the other side. Let's build something awesome.{Colors.RESET}")
    print()

def run_setup(quick: bool = False):
    """Main setup flow.
    
    Args:
        quick: If True, skip prompts for already-configured settings (for reconfig)
    """
    # Always show the banner
    print_welcome_banner()
    
    # Load current preferences (for reconfig)
    current = get_current_prefs()
    is_reconfig = current.get("onboarded", False)
    
    # Store original values for comparison
    original_tone = current.get("tone", "sassy")
    original_trust = current.get("trust_mode", "notify")
    
    # Check Claude Code
    print(f"{Colors.CYAN}{Colors.BOLD}◆ Checking Prerequisites{Colors.RESET}")
    if check_claude_code():
        print(f"  {Colors.GREEN}✓{Colors.RESET} Claude Code detected\n")
    else:
        print(f"  {Colors.YELLOW}⚠{Colors.RESET} Claude Code not found")
        print(f"  {Colors.DIM}Install: https://claude.ai/code{Colors.RESET}\n")
    
    # Determine skip mode for reconfig
    skip_if_set = quick and is_reconfig
    
    # Show appropriate header
    if is_reconfig:
        if skip_if_set:
            print(f"{Colors.CYAN}{Colors.BOLD}◆ Quick Reconfig{Colors.RESET}")
            print(f"  {Colors.DIM}Press Enter to keep current, or change anything you want{Colors.RESET}\n")
        else:
            print(f"{Colors.CYAN}{Colors.BOLD}◆ Reconfiguring Blitz{Colors.RESET}\n")
    
    # Select preferences with back/skip support
    current_tone = current.get("tone", "sassy")
    current_trust = current.get("trust_mode", "notify")
    
    # Step 1: Tone
    if skip_if_set:
        print(f"{Colors.DIM}◆ Skipping tone (current: {current_tone}) - press Enter or 'c' to change{Colors.RESET}")
    
    tone, tone_changed = select_tone(current_tone, skip_if_set=skip_if_set)
    if tone is None:  # User quit
        print(f"\n{Colors.DIM}Setup cancelled.{Colors.RESET}")
        return
    
    # Step 2: Trust Mode (can go back to tone)
    while True:
        current_trust = current.get("trust_mode", "notify")
        trust_mode, trust_changed = select_trust_mode(current_trust, skip_if_set=skip_if_set)
        if trust_mode is None:  # User quit
            print(f"\n{Colors.DIM}Setup cancelled.{Colors.RESET}")
            return
        
        # Handle back navigation
        if trust_mode == -1:  # Back signal
            # Go back to tone selection
            tone, tone_changed = select_tone(current.get("tone", "sassy"), skip_if_set=False)
            if tone is None:
                print(f"\n{Colors.DIM}Setup cancelled.{Colors.RESET}")
                return
            continue
        
        break
    
    # Step 3: Summary screen (preview before save)
    if is_reconfig:
        review_choice = run_summary_review(tone, trust_mode, original_tone, original_trust)
        
        if review_choice == 'quit':
            print(f"\n{Colors.DIM}Setup cancelled.{Colors.RESET}")
            return
        elif review_choice == 'tone':
            tone, _ = select_tone(tone, skip_if_set=False)
            if tone is None:
                print(f"\n{Colors.DIM}Setup cancelled.{Colors.RESET}")
                return
            # After changing tone, show summary again
            review_choice = run_summary_review(tone, trust_mode, original_tone, original_trust)
            if review_choice == 'quit':
                print(f"\n{Colors.DIM}Setup cancelled.{Colors.RESET}")
                return
        elif review_choice == 'trust':
            trust_mode, _ = select_trust_mode(trust_mode, skip_if_set=False)
            if trust_mode is None:
                print(f"\n{Colors.DIM}Setup cancelled.{Colors.RESET}")
                return
            # After changing trust, show summary again
            review_choice = run_summary_review(tone, trust_mode, original_tone, original_trust)
            if review_choice == 'quit':
                print(f"\n{Colors.DIM}Setup cancelled.{Colors.RESET}")
                return
    
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
        print(f"\n\n{Colors.DIM}Setup cancelled. Run 'blitz config' to try again.{Colors.RESET}")
        sys.exit(0)

#!/usr/bin/env python3
"""
Daily copy script - copies image_organizer.py and config.json to one set per day.
Run this via Windows Task Scheduler daily.
"""

import shutil
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
BASE_DIR = Path(__file__).parent
SOURCE_FILES = ["image_organizer.py", "config.json"]
STATE_FILE = BASE_DIR / ".copy_state.json"
LOG_FILE = BASE_DIR / "daily_copy.log"
SET_PREFIX = "set_"
TOTAL_SETS = 95  # set_001 to set_095


def log_event(message, level="INFO"):
    """Write to log file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(log_entry.strip())


def get_processed_sets():
    """Get list of all sets that have been processed (have both files)."""
    processed = []
    for i in range(1, TOTAL_SETS + 1):
        set_folder = BASE_DIR / f"{SET_PREFIX}{i:03d}"
        if set_folder.exists():
            has_all_files = all((set_folder / f).exists() for f in SOURCE_FILES)
            if has_all_files:
                processed.append(i)
    return processed


def find_missed_sets():
    """Find gaps - sets that should have been processed but weren't."""
    processed = get_processed_sets()
    if not processed:
        return list(range(1, TOTAL_SETS + 1))
    
    last_processed = max(processed)
    missed = []
    
    for i in range(1, last_processed):
        if i not in processed:
            missed.append(i)
    
    return missed


def audit_and_log():
    """Log audit of processed vs missed sets."""
    processed = get_processed_sets()
    missed = find_missed_sets()
    last_set = get_last_copied_set()
    
    log_event("=" * 50)
    log_event("AUDIT REPORT")
    log_event("=" * 50)
    log_event(f"Last recorded set: {last_set:03d}")
    log_event(f"Total sets with files: {len(processed)}")
    log_event(f"Processed sets: {', '.join(f'{s:03d}' for s in processed) if processed else 'None'}")
    
    if missed:
        log_event(f"MISSED SETS: {', '.join(f'{s:03d}' for s in missed)}", "WARNING")
    else:
        log_event("No missed sets detected (up to last processed)")
    
    remaining = TOTAL_SETS - last_set
    log_event(f"Remaining sets to process: {remaining}")
    log_event("=" * 50)


def get_last_copied_set():
    """Read state file to get last copied set number."""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            return state.get("last_set", 0)
    return 0


def save_state(set_number):
    """Save current state to file."""
    state = {
        "last_set": set_number,
        "last_run": datetime.now().isoformat()
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def copy_to_set(set_number):
    """Copy source files to specified set folder."""
    set_folder = BASE_DIR / f"{SET_PREFIX}{set_number:03d}"
    
    if not set_folder.exists():
        print(f"Set folder {set_folder} does not exist, skipping...")
        return False
    
    copied = []
    for filename in SOURCE_FILES:
        source = BASE_DIR / filename
        destination = set_folder / filename
        
        if source.exists():
            shutil.copy2(source, destination)
            copied.append(filename)
            print(f"Copied {filename} to {set_folder}")
        else:
            print(f"Source file {filename} not found!")
    
    return len(copied) > 0


def run_organizer(set_number):
    """Spawn image_organizer.py in the set folder."""
    set_folder = BASE_DIR / f"{SET_PREFIX}{set_number:03d}"
    organizer_script = set_folder / "image_organizer.py"
    
    if not organizer_script.exists():
        print(f"Organizer script not found in {set_folder}")
        return False
    
    try:
        # Spawn the script as a separate process (non-blocking)
        subprocess.Popen(
            [sys.executable, str(organizer_script)],
            cwd=str(set_folder),
            creationflags=subprocess.CREATE_NEW_CONSOLE  # Opens in new window on Windows
        )
        print(f"Spawned image_organizer.py in {set_folder}")
        return True
    except Exception as e:
        print(f"Failed to spawn organizer: {e}")
        return False


def main():
    log_event("Daily copy script started")
    
    # Run audit first to log current state
    audit_and_log()
    
    last_set = get_last_copied_set()
    next_set = last_set + 1
    
    if next_set > TOTAL_SETS:
        log_event(f"All {TOTAL_SETS} sets have been processed. Done!")
        return
    
    log_event(f"Processing set_{next_set:03d}...")
    
    if copy_to_set(next_set):
        save_state(next_set)
        log_event(f"Successfully copied files to set_{next_set:03d}")
        # Spawn the organizer in the new set folder
        if run_organizer(next_set):
            log_event(f"Spawned organizer for set_{next_set:03d}")
        else:
            log_event(f"Failed to spawn organizer for set_{next_set:03d}", "ERROR")
    else:
        log_event(f"Failed to copy files to set_{next_set:03d}", "ERROR")


if __name__ == "__main__":
    main()

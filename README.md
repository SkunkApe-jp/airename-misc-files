# AI Image Organizer - Daily Copy Script

This repository contains helper scripts for running [AI Image Organizer](https://github.com/SkunkApe-jp/skunkapes-groq-image-rename) across multiple folder sets on a scheduled basis using Windows Task Scheduler.

## Files

### `daily_copy.py`
Main Python script that:
- Copies `image_organizer.py` and `config.json` to one set folder per day
- Tracks progress via `.copy_state.json`
- Spawns the organizer script in a new window
- Logs all activity to `daily_copy.log`
- Audits and reports any missed sets

**Configuration:**
- Edit `TOTAL_SETS` in the script (default: 95 sets)
- `SOURCE_FILES` lists what gets copied (default: `image_organizer.py`, `config.json`)

### `run_daily_copy.bat`
Batch wrapper for easy Task Scheduler setup:
```batch
@echo off
cd /d "C:\path\to\your\sets"
python daily_copy.py
```

### `global_memory.json`
Sample global memory file used by the image organizer to track category paths across runs. Stored in `%APPDATA%\image_organizer\` when in use.

## Related Helper Script

### `organize_images.py` (from [AI Image Organizer repo](https://github.com/SkunkApe-jp/skunkapes-groq-image-rename/tree/main/misc%20scripts))

Prepares your images by organizing them into numbered sets before running the daily copy script.

**What it does:**
- Moves image files from a source folder into numbered sets (`set_001`, `set_002`, ...)
- Supports: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.ico`
- Handles name conflicts by appending `_1`, `_2`, etc.

**Usage:**
```bash
# Organize 50 images per folder
python organize_images.py -n 50

# Custom source and target directories
python organize_images.py -n 25 -s "C:\path\to\images" -t organized
```

**Arguments:**
- `-n, --number` (required): Images per folder
- `-s, --source` (optional): Source directory (default: `.`)
- `-t, --target` (optional): Output directory (default: `files`)

**Workflow:**
1. Use `organize_images.py` to split images into numbered sets
2. Place `daily_copy.py` and `run_daily_copy.bat` in the target directory
3. Set up Windows Task Scheduler to run `daily_copy.py` daily
4. Each day it processes one set folder automatically

## Windows Task Scheduler Setup

1. Open Task Scheduler
2. Create Basic Task:
   - **Name:** `Daily Set Copy`
   - **Trigger:** Daily (set your preferred time)
   - **Action:** Start a program
   - **Program:** `C:\Users\%USERNAME%\airename-misc-files\run_daily_copy.bat`
   - **Start in:** Your working directory with set folders

3. Optional: Enable "Run whether user is logged on or not" for headless operation

## How It Works

```
Day 1: Task runs → copies files to set_001 → spawns organizer → logs activity
Day 2: Task runs → copies files to set_002 → spawns organizer → logs activity
...
```

The script maintains state in `.copy_state.json` so it resumes correctly even if the computer was off.

## Log File

`daily_copy.log` contains:
- Timestamps of each run
- Audit reports showing processed/missed sets
- Success/failure status

## Requirements

- Python 3.x
- Windows (uses `CREATE_NEW_CONSOLE` flag)
- `image_organizer.py` and `config.json` in the working directory

## Notes

- The organizer script creates category folders **inside** each set folder
- Global memory tracks paths in `%APPDATA%\image_organizer\global_memory.json`
- Set folders must follow naming: `set_001`, `set_002`, etc.

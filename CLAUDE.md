# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Thattan (தட்டான்) is a Tamil99 typing-tutor desktop app built with Python + PySide6 (Qt). It teaches the Tamil99 keyboard layout keystroke-by-keystroke, tracking accuracy/speed and persisting progress locally.

## Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run the app (must run from repo root — no setup.py/pyproject.toml, package isn't pip-installed)
python -m thattan

# Tests (PySide6 not required for the test suite — core/ui logic is tested without Qt)
pip install pytest
python -m pytest tests/ -v
python -m pytest tests/test_session.py -v          # single file
python -m pytest tests/test_session.py::TestSessionProperties::test_index_starts_at_zero  # single test

# Packaging (Linux AppImage, via PyInstaller)
pip install pyinstaller
./build_appimage.sh          # output: release/Thattan-x86_64.AppImage
# thattan.spec is the underlying PyInstaller spec (onedir on Linux, onefile on Windows)
```

CI (`.github/workflows/tests.yml`) runs pytest on 3.11/3.12/3.13 without installing PySide6 — so any code imported by `tests/` must not have a hard, module-level dependency on Qt. `.github/workflows/release.yml` builds the AppImage on tag pushes (`v*`).

## Architecture

Three layers, imported top-down: `app.py` → `ui/` → `core/`. `core/` has no PySide6 imports; `ui/` is all Qt widgets.

- **`thattan/app.py`** — entry point (`run()`). Configures logging, loads the bundled `TAU-Marutham.ttf` font (with emoji-font fallbacks), constructs `LevelRepository` and `ProgressStore`, then hands both to `MainWindow`.
- **`thattan/core/levels.py`** — `LevelRepository` loads every `data/levels/level*.yaml` at startup (sorted numerically by the `N` in `levelN`). Each YAML has `title` + `content` (list or newline-separated string); the number of entries in `content` is that level's task count — there is no separate "task count" config anywhere else.
- **`thattan/core/progress.py`** — `ProgressStore` persists per-level progress (`completed`, `best_wpm`, `best_accuracy`) and gamification state (`total_score`, `current_streak`, `best_streak`) to `~/.thattan/progress.json`. Loaded once at startup, saved after every update call.
- **`thattan/core/session.py`** — `TypingSession` walks through a level's task list one string at a time. `submit(typed)` diffs `typed` against the target character-by-character and returns a `TaskResult`. Speed metrics follow the Tux Typing convention: **CPM** = correct chars/min, **net WPM** = `(total_chars − 5×errors) / 5 / minutes` (displayed value, penalizes errors), **gross WPM** = no penalty (available via `aggregate_gross_wpm()` but not surfaced in the UI).
- **`thattan/core/keystroke_tracker.py`** — `Tamil99KeyboardLayout` is a static mapping from Tamil99 m17n keystroke rules (`data/m17n/ta-tamil99.mim` is the reference source) to Latin key sequences (`CHAR_TO_KEYSTROKES`, `CONSONANT_KEYS`, `VOWEL_SIGN_KEYS`). `get_keystroke_sequence(text)` decomposes Tamil text into `(key, needs_shift)` tuples the UI uses to drive keyboard highlighting; this decomposition logic is duplicated in `MainWindow._build_keystroke_to_char_map` (mirrors the same char-combining rules to map keystroke index → source character index for rendering). If the Tamil99 keystroke mapping ever changes, both places need updating. `KeystrokeTracker` is a separate, currently UI-unused per-keystroke stats accumulator (correct/incorrect counts, response times, common mistakes).
- **`thattan/ui/main_window.py`** (~2300 lines, by far the largest file) — `MainWindow` owns nearly all application state and behavior: a `QStackedWidget` toggling between a home screen (level list + gamification stats) and a typing screen (practice card + on-screen keyboard + finger guidance). Typing input is captured via a hidden, zero-height `QLineEdit` (`input_box`) intercepted through `eventFilter`/`_on_key_press` rather than normal text editing — key handling, Tamil composition, and keyboard-highlight state all flow through there. Layout is resolution-responsive: `_rescale_typing_screen` recomputes every font size/margin as a fraction of window size relative to a 1920×1080 reference, and `_adjust_adaptive_layout` reflows the hands-image/keyboard split on resize.
- **`thattan/ui/home_widgets.py`, `custom_overlay.py`, `about_overlay.py`, `typing_widgets.py`** — reusable widgets (`GlassCard`, `HomeStatCard`, `HomeLevelRowCard`, `HomeProgressBar`, overlays, letter-sequence display) composed by `main_window.py`.
- **`thattan/ui/colors.py`** — `HomeColors` palette constants + `blend_hex`; the only `ui/` module with no PySide6 dependency (hence directly unit-testable).
- **`thattan/ui/level_cards.py`** — `LevelCard`/`LevelMapWidget`, not imported anywhere; superseded by `HomeLevelRowCard` in `home_widgets.py`. Treat as dead code, not a second UI path.

### Environment variables
- `THATTAN_UNLOCK_ALL=1` unlocks all levels regardless of progress (used for manual/dev testing of later levels).

### Data files
- `thattan/data/levels/level{0..4}.yaml` — practice content, loaded by `LevelRepository`.
- `thattan/data/m17n/ta-tamil99.mim` — reference m17n Tamil99 keyboard definition; `keystroke_tracker.py`'s mapping is a hand-ported subset of this, not a runtime parser of it.
- `~/.thattan/progress.json` — user progress, not part of the repo.

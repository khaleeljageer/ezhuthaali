# Thattan Roadmap

This document captures the current state of the project and a proposed plan for future improvements and features.

## Project snapshot

**Thattan (தட்டான்)** is a PySide6 desktop app teaching Tamil99 keyboard typing through progressive practice levels.

- `core/` — `levels.py` (YAML loader), `session.py` (WPM/accuracy scoring), `progress.py` (JSON persistence to `~/.thattan/progress.json`), `keystroke_tracker.py` (per-keystroke Tamil99 mapping) — all well-tested, no Qt dependency.
- `ui/` — `main_window.py` is a ~2,380-line God object: owns keyboard rendering, finger-guidance, theming, event handling, and screen navigation all in one class.
- 5 levels of content, but only `level0.yaml` (30 tasks) is populated — levels 1–4 are empty files.
- CI runs pytest across Python 3.11–3.13; release workflow builds a Linux AppImage only.
- No `pyproject.toml`, no linter/formatter/type-checker wired into CI despite a `py.typed` marker implying typed-package intent.
- Single light theme; gamification (streak/score) exists in `ProgressStore` but is only lightly surfaced in the UI.

## Gaps that stood out

1. **Content gap is the biggest functional hole** — 4 of 5 levels ship empty, so the app can't deliver on its "progressive training" pitch past level 0.
2. **`main_window.py` at 2,380 lines** mixes rendering, layout math, color theory, keyboard-layout logic, and app state — hard to test, hard to extend, high risk for regressions.
3. No lint/type-check gate in CI (`ruff`/`mypy` absent) even though the package declares `py.typed`.
4. Distribution is Linux-only (AppImage); no Windows/macOS build path despite Qt being cross-platform.
5. No UI-level tests (understandable for Qt, but nothing like `pytest-qt` either).

## Roadmap

### Phase 1 — Fix the core promise (content + stability)
- Populate `level1.yaml`–`level4.yaml` with real progressive Tamil99 practice content (this is the #1 thing blocking the app from being useful past level 0).
- Add a `pyproject.toml` with `ruff` + `mypy`, wire into CI as a required check.
- Split `main_window.py`: pull out keyboard-rendering/finger-guidance into its own `ui/keyboard_widget.py`, color/theme math into `colors.py`, screen-navigation into a controller — reduces regression risk before adding features.

### Phase 2 — Learning experience improvements
- Per-key accuracy heatmap (which keys the user fumbles most) — `keystroke_tracker.py` already tracks per-key correctness, just needs a stats view.
- Adaptive practice: auto-generate drill lines weighted toward the user's weakest keys.
- Session history/trends (accuracy & WPM over time), not just best-ever values.
- Sound/haptic-style feedback on errors (optional, toggleable).
- Dark theme (README markets "modern" UI; `colors.py` is a natural extension point — single `HomeColors` class, straightforward to add a second palette + toggle).

### Phase 3 — Reach & distribution
- Windows/macOS packaging (PyInstaller spec already exists — just needs platform-specific CI jobs, since AppImage is Linux-only).
- Settings screen: font size, keyboard-hint toggle, unlock-all-levels (currently only a hidden `THATTAN_UNLOCK_ALL` env var) exposed as a real preference.
- Export progress/stats (CSV/JSON) for users who want to track improvement externally.

### Phase 4 — Stretch features
- Additional layouts beyond Tamil99 (InScript, Bamini) — `Tamil99KeyboardLayout` would need to become one implementation of a layout interface.
- Multiplayer/leaderboard-style typing races (would need a backend — bigger scope decision).
- Custom lesson editor so users/teachers can author their own level YAML from the UI instead of hand-editing files.

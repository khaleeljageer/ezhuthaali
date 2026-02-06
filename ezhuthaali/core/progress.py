from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Tuple


@dataclass
class LevelProgress:
    completed: int = 0
    best_wpm: float = 0.0
    best_accuracy: float = 0.0


def _default_gamification() -> Dict[str, int]:
    return {"total_score": 0, "current_streak": 0, "best_streak": 0}


class ProgressStore:
    def __init__(self) -> None:
        self._file_path = Path.home() / ".ezhuthaali" / "progress.json"
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        self._progress, self._gamification = self._load()

    def get_level_progress(self, level_key: str) -> LevelProgress:
        return self._progress.get(level_key, LevelProgress())

    def get_gamification(self) -> Tuple[int, int, int]:
        """Return (total_score, current_streak, best_streak)."""
        g = self._gamification
        return (
            int(g.get("total_score", 0)),
            int(g.get("current_streak", 0)),
            int(g.get("best_streak", 0)),
        )

    def update_level_progress(
        self,
        level_key: str,
        completed: int,
        wpm: float,
        accuracy: float,
    ) -> None:
        current = self._progress.get(level_key, LevelProgress())
        current.completed = max(current.completed, completed)
        current.best_wpm = max(current.best_wpm, wpm)
        current.best_accuracy = max(current.best_accuracy, accuracy)
        self._progress[level_key] = current
        self._save()

    def update_gamification(
        self,
        total_score: int,
        current_streak: int,
        best_streak: int,
    ) -> None:
        self._gamification["total_score"] = total_score
        self._gamification["current_streak"] = current_streak
        self._gamification["best_streak"] = max(self._gamification.get("best_streak", 0), best_streak)
        self._save()

    def reset_level(self, level_key: str) -> None:
        """Clear progress for a single level (e.g. before restart)."""
        self._progress[level_key] = LevelProgress()
        self._save()

    def reset(self) -> None:
        self._progress = {}
        self._gamification = _default_gamification()
        self._save()

    def _load(self) -> Tuple[Dict[str, LevelProgress], Dict[str, int]]:
        progress: Dict[str, LevelProgress] = {}
        gamification = _default_gamification()
        if not self._file_path.exists():
            return progress, gamification
        try:
            payload = json.loads(self._file_path.read_text())
        except json.JSONDecodeError:
            return progress, gamification

        for key, value in payload.get("levels", {}).items():
            progress[key] = LevelProgress(
                completed=int(value.get("completed", 0)),
                best_wpm=float(value.get("best_wpm", 0.0)),
                best_accuracy=float(value.get("best_accuracy", 0.0)),
            )
        g = payload.get("gamification", {})
        if isinstance(g, dict):
            gamification["total_score"] = int(g.get("total_score", 0))
            gamification["current_streak"] = int(g.get("current_streak", 0))
            gamification["best_streak"] = int(g.get("best_streak", 0))
        return progress, gamification

    def _save(self) -> None:
        payload = {
            "levels": {key: asdict(value) for key, value in self._progress.items()},
            "gamification": dict(self._gamification),
        }
        self._file_path.write_text(json.dumps(payload, indent=2))

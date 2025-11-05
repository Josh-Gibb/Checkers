# record.py
from __future__ import annotations
import os
import json
import tempfile
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple

# Path used to persist records (can be overridden by env var)
RECORDS_FILE = os.getenv("CHECKERS_RECORDS_FILE", "records.json")


@dataclass
class Record:
    player: str                # e.g. username of the local player
    opponent: str              # e.g. "AI" or another username
    winner: Optional[str]      # "player", "opponent", or "draw" / None if unknown
    mode: str                  # "cpu" or "pvp"
    date: str                  # ISO timestamp
    moves: Optional[int] = None
    duration_seconds: Optional[int] = None
    meta: Optional[Dict[str, Any]] = None


def _load_records(file_path: str = RECORDS_FILE) -> List[Dict[str, Any]]:
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        # If the file is corrupted or unreadable, return empty list.
        return []


def _save_records(records: List[Dict[str, Any]], file_path: str = RECORDS_FILE) -> None:
    # Write to a temp file then atomically replace to avoid half-writes.
    dir_name = os.path.dirname(os.path.abspath(file_path)) or "."
    fd, tmp_path = tempfile.mkstemp(prefix="records-", dir=dir_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmpf:
            json.dump(records, tmpf, indent=2, ensure_ascii=False)
            tmpf.flush()
            os.fsync(tmpf.fileno())
        os.replace(tmp_path, file_path)
    finally:
        # if os.replace failed and tmp_path remains, try to clean it.
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


def add_record(
    player: str,
    opponent: str,
    winner: Optional[str],
    mode: str = "cpu",
    moves: Optional[int] = None,
    duration_seconds: Optional[int] = None,
    meta: Optional[Dict[str, Any]] = None,
    file_path: str = RECORDS_FILE,
) -> Record:
    """Add a new record and persist it.

    winner should be:
      - "player" if the local player won
      - "opponent" if opponent won
      - "draw" or None if draw/unknown
    """
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    rec = Record(
        player=player,
        opponent=opponent,
        winner=winner,
        mode=mode,
        date=now,
        moves=moves,
        duration_seconds=duration_seconds,
        meta=meta or {},
    )
    records = _load_records(file_path)
    records.append(asdict(rec))
    _save_records(records, file_path)
    return rec


def get_all_records(file_path: str = RECORDS_FILE) -> List[Record]:
    raw = _load_records(file_path)
    return [Record(**r) for r in raw]


def get_user_records(username: str, file_path: str = RECORDS_FILE) -> List[Record]:
    return [r for r in get_all_records(file_path) if r.player == username or r.opponent == username]


def get_recent(n: int = 10, file_path: str = RECORDS_FILE) -> List[Record]:
    records = get_all_records(file_path)
    records.sort(key=lambda r: r.date, reverse=True)
    return records[:n]


def get_win_counts(file_path: str = RECORDS_FILE) -> Dict[str, int]:
    """Return a dict mapping player -> wins count (only counts 'player' wins in records where player field matches)."""
    counts: Dict[str, int] = {}
    for r in get_all_records(file_path):
        # Count full-player wins: if r.winner == "player" we credit r.player
        if r.winner == "player":
            counts[r.player] = counts.get(r.player, 0) + 1
        elif r.winner == "opponent":
            counts[r.opponent] = counts.get(r.opponent, 0) + 1
    return counts


def get_top_winners(n: int = 10, file_path: str = RECORDS_FILE) -> List[Tuple[str, int]]:
    counts = get_win_counts(file_path)
    items = list(counts.items())
    items.sort(key=lambda kv: kv[1], reverse=True)
    return items[:n]


def clear_records(file_path: str = RECORDS_FILE) -> None:
    _save_records([], file_path)
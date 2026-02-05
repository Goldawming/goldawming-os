from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime, timezone
from typing import Any, Dict

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class SessionStore:
    def __init__(self, base_dir: Path, session: str):
        self.base_dir = base_dir
        self.session = session
        self.session_dir = self.base_dir / session
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.timeline_path = self.session_dir / "timeline.jsonl"

    def append(self, event: Dict[str, Any]) -> None:
        event = dict(event)
        event.setdefault("ts", utc_now_iso())
        with self.timeline_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\\n")

    def read_events(self) -> list[Dict[str, Any]]:
        if not self.timeline_path.exists():
            return []
        events: list[Dict[str, Any]] = []
        with self.timeline_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return events

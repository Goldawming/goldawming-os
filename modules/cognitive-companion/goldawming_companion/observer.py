from __future__ import annotations
import subprocess
from pathlib import Path
from typing import Optional, List
from .redaction import redact
from .store import SessionStore

def run_command(cmd: str) -> tuple[int, str]:
    # MVP: run via shell for convenience. Operator types commands explicitly.
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out

def snapshot_tail(path: Path, lines: int = 80) -> str:
    if not path.exists() or not path.is_file():
        return ""
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            content = f.read().splitlines()
        return "\\n".join(content[-lines:])
    except Exception:
        return ""

class Observer:
    def __init__(self, store: SessionStore, allow_tails: Optional[List[Path]] = None):
        self.store = store
        self.allow_tails = allow_tails or []

    def checkpoint(self, title: str) -> None:
        self.store.append({"type": "checkpoint", "title": title})

    def note(self, note: str) -> None:
        self.store.append({"type": "note", "note": note})

    def command(self, cmd: str) -> None:
        self.store.append({"type": "command", "cmd": cmd})
        rc, output = run_command(cmd)
        self.store.append({"type": "result", "cmd": cmd, "rc": rc, "output": redact(output)})

    def tails(self) -> None:
        for p in self.allow_tails:
            content = snapshot_tail(p)
            if content:
                self.store.append({"type": "log_tail", "path": str(p), "output": redact(content)})

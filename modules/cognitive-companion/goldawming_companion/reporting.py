from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from .store import SessionStore

def generate_report(base_dir: Path, session: str) -> Path:
    store = SessionStore(base_dir, session)
    events = store.read_events()

    cmds = [e for e in events if e.get("type") == "command"]
    results = [e for e in events if e.get("type") == "result"]
    notes = [e for e in events if e.get("type") == "note"]
    checkpoints = [e for e in events if e.get("type") == "checkpoint"]
    tails = [e for e in events if e.get("type") == "log_tail"]

    out_path = base_dir / session / "report.md"
    lines: List[str] = []
    lines.append(f"# Session Report: {session}\\n")
    lines.append("## Summary\\n")
    lines.append(f"- Commands executed: {len(cmds)}")
    lines.append(f"- Results captured: {len(results)}")
    lines.append(f"- Notes: {len(notes)}")
    lines.append(f"- Checkpoints: {len(checkpoints)}")
    lines.append(f"- Log tails captured: {len(tails)}\\n")

    if checkpoints:
        lines.append("## Checkpoints\\n")
        for c in checkpoints:
            lines.append(f"- **{c.get('title','')}** ({c.get('ts','')})")
        lines.append("")

    if notes:
        lines.append("## Operator Notes\\n")
        for n in notes:
            lines.append(f"- {n.get('note','')} ({n.get('ts','')})")
        lines.append("")

    if tails:
        lines.append("## Evidence (Log Snapshots)\\n")
        for t in tails[-5:]:
            lines.append(f"### `{t.get('path','')}` — {t.get('ts','')}\\n")
            lines.append("```text")
            excerpt = (t.get("output","") or "").strip()
            if len(excerpt) > 1200:
                excerpt = excerpt[:1200] + "\\n...[truncated]"
            lines.append(excerpt)
            lines.append("```\\n")

    if results:
        lines.append("## Evidence (Command Outputs)\\n")
        for r in results[-10:]:
            cmd = r.get("cmd", "")
            rc = r.get("rc", "")
            ts = r.get("ts", "")
            out = (r.get("output", "") or "").strip()
            if len(out) > 1200:
                out = out[:1200] + "\\n...[truncated]"
            lines.append(f"### `{cmd}` (rc={rc}) — {ts}\\n")
            lines.append("```text")
            lines.append(out)
            lines.append("```\\n")

    out_path.write_text("\\n".join(lines), encoding="utf-8")
    return out_path

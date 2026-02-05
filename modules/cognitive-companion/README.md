# Goldawming OS — Cognitive Companion (MVP-1)

A **read-only** real-time operational companion for a human operator.

This repo delivers **MVP-1**:
- Observe terminal output (stdout/stderr) from commands you run **inside the tool**
- (Optional) snapshot allowlisted log files you explicitly approve
- Maintain an append-only session timeline (JSONL)
- Redact common secret patterns before writing/printing
- Generate a checkpoint report (Markdown)

**Non-goals (by design):**
- No remote control / TeamViewer features
- No autonomous execution
- No hidden telemetry
- No screen capture or keylogging
- No offensive functionality

## Quick start

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Start a session (interactive)
python -m goldawming_companion observe --session demo

# Inside the prompt:
#   $ whoami
#   $ uname -a
#   $ :note check kernel build
#   $ :checkpoint baseline collected
#   $ :exit

# Generate a report
python -m goldawming_companion report --session demo
```

## Structure
- `docs/` — specifications, governance, threat model
- `goldawming_companion/` — CLI + core library
- `sessions/` — session artifacts (gitignored)

## Safety & privacy
All sources are **allowlisted**.
Redaction runs before persistence/printing.
Everything is auditable in `sessions/<session>/timeline.jsonl`.

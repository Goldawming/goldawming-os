# Security & Privacy (MVP-1)

## Data handling
Session data is stored locally under `sessions/<session>/`. Treat it as sensitive.

## Redaction
A best-effort redaction pass runs before storing/printing:
- PEM blocks
- JWT-like strings
- common API token patterns
- password assignments in output

No redaction is perfect. A qualified human must assume leaks are possible.

## Logging policy
- append-only JSONL timeline
- no hidden telemetry
- no network calls in MVP-1

## Reporting
Reports include evidence excerpts. Avoid sharing reports publicly if they may contain secrets.

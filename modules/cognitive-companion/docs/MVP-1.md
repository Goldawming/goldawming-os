# MVP-1 Plan

## CLI
- `observe --session <name> [--tail <path> ...]`
  - interactive prompt
  - `:note <text>`
  - `:checkpoint <title>`
  - `:tail` (snapshot allowlisted logs)
  - `:exit`

- `report --session <name>`
  - builds `sessions/<name>/report.md`

## Outputs
- `sessions/<name>/timeline.jsonl`
- `sessions/<name>/report.md`

## Next iterations
- plugin packs (audit/ops)
- stronger command execution model (no shell)
- streaming tail with rate limits
- local UI timeline viewer

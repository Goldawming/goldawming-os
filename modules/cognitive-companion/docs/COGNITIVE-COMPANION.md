# Cognitive Companion
## Specification (Goldawming OS)

### Purpose
A **read-only, human-paired** system that observes operational context in real time and provides:
- explanation
- correlation
- suggestions
- risk flags
- decision prompts

It does **not** act autonomously.

---

## Core Principles

### 1) Human Authority
Humans own intent, judgment, and responsibility. The companion provides analysis and advice only.

### 2) Qualified Human Filter
Outputs are **untrusted by default**. A qualified human validates any critical conclusion or action.

### 3) Read-Only by Design
The companion cannot click, type, or execute actions outside the explicit operator flow.
Commands run only because the **operator typed them** (inside the tool), and they are logged.

### 4) Transparency and Traceability
Every observation and recommendation is recorded (timeline). No silent behavior.

### 5) Privacy by Default
Only allowlisted sources may be observed. Redaction runs before printing/persisting.

---

## Capabilities (Allowed)

### Real-time observation
- stdout/stderr of operator-run commands inside the session
- optional allowlisted log snapshots (file paths you explicitly approve)

### Context management
- session timeline (append-only JSONL)
- operator notes and checkpoints

### Advisory output (MVP direction)
- what happened / why it matters
- what to check next
- risk hints and pitfalls
- questions to ask before acting

---

## Prohibited Capabilities (Non-negotiable)
- remote desktop control
- screen capture
- keylogging
- autonomous command execution
- stealth data collection
- scanning/attacking networks or systems

---

## Threat Model (MVP-1)

### Main risks
1. Secret leakage (tokens/keys/passwords in outputs/logs)
2. Over-trust (operator treats suggestions as truth)
3. Scope creep (turning helper into spyware/agent)
4. Unsafe retention (logs stored too long/shared)

### Mitigations
- allowlist sources only
- redaction before persist/print
- append-only timeline for auditability
- explicit “advice is not truth” stance
- clear non-goals in docs + code

---

## MVP-1 Acceptance Criteria

### Must
- start/stop a session
- capture stdout/stderr for commands executed in-session
- store events to `sessions/<name>/timeline.jsonl`
- redact secrets before storing/printing
- generate `report.md` summarizing the session

### Must Not
- execute commands automatically
- read arbitrary files without allowlist
- access network by default
- capture screen or keystrokes

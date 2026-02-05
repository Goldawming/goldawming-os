import re
from typing import Iterable, Tuple

# Best-effort patterns. Not perfect. Assume leaks are possible.
_PATTERNS: Iterable[Tuple[str, str]] = [
    (r"-----BEGIN [A-Z ]+-----[\s\S]+?-----END [A-Z ]+-----", "[REDACTED_PEM]"),
    (r"\beyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\b", "[REDACTED_JWT]"),
    (r"\b(sk-[A-Za-z0-9]{20,})\b", "[REDACTED_OPENAI_KEY]"),
    (r"\b(ghp_[A-Za-z0-9]{20,})\b", "[REDACTED_GITHUB_TOKEN]"),
    (r"\b(xox[baprs]-[A-Za-z0-9-]{10,})\b", "[REDACTED_SLACK_TOKEN]"),
    (r"(?i)\b(password|passwd|pwd)\s*[:=]\s*([^\s]+)", r"\1=[REDACTED_PASSWORD]"),
    (r"\b(AKIA[0-9A-Z]{16})\b", "[REDACTED_AWS_ACCESS_KEY_ID]"),
]

def redact(text: str) -> str:
    if not text:
        return text
    out = text
    for pattern, repl in _PATTERNS:
        out = re.sub(pattern, repl, out)
    return out

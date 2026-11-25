"""Unsent: The Micro-Confession Sprint — make.fun entry.

Writes one two-part micro-confession to /output/entry.txt: a To: line
naming who it was meant for, then the unsent message itself, one line
written exactly as it was typed. The kit gate is UTF-8 text of 1 to
260 characters, not only whitespace. Python 3.13, standard library
only, no network access.
"""

import os
import sys

ENTRY = (
    "To: Mum\n"
    "I still rehearse telling you I dropped out in second year, "
    "then I make tea instead and ask about your garden."
)

MAX_CHARS = 260
MAX_MESSAGE_CHARS = 200


def gate_check(text):
    """Enforce the kit gate exactly; raise ValueError on any failure."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be 1 to 260 characters, got %d" % len(text)
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two parts: a To: line "
                         "and the unsent message, got %d lines"
                         % len(lines))
    if not lines[0].startswith("To: "):
        raise ValueError("entry must start with a To: line")
    if not lines[0][4:].strip():
        raise ValueError("To: line must name someone")
    if "\r" in text:
        raise ValueError("entry must not contain carriage returns")
    if not lines[1].strip():
        raise ValueError("message line must not be blank")
    if len(lines[1]) > MAX_MESSAGE_CHARS:
        raise ValueError(
            "message must be at most 200 characters, got %d"
            % len(lines[1])
        )
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing padding")
    if any(ord(ch) < 32 and ch not in "\n" for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")
    return True


def main():
    gate_check(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)
    print("wrote /output/entry.txt (%d chars)" % len(ENTRY))
    return 0


if __name__ == "__main__":
    sys.exit(main())

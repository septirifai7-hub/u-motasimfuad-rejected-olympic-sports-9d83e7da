"""One-line make.fun entry: Rejected Olympic Sports.

Prints the entry line to stdout and writes it to entry.txt in the
output directory (default /output, or $MAKEFUN_OUTPUT_DIR).

The entry line is validated against the competition gate before it is
written: UTF-8 text, 1 to 200 characters, a single line, not only
whitespace, with no leading or trailing whitespace and no trailing
newline in the file.

The joke is a made-up event plausible enough to sound like a broadcast:
Synchronised Queueing, four athletes standing in line for four hours,
with the twist landing before the line ends — gold goes to whoever
complains the least.
"""

import os
import sys

ENTRY = "Synchronised Queueing: four athletes stand in line for four hours, and the gold goes to whoever complains the least."

MIN_CHARS = 1
MAX_CHARS = 200


def validate(text):
    """Check *text* against the entry gate; raise ValueError if it fails."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, got {len(text)}"
        )
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if any(ord(char) < 0x20 and char not in ("\t",) for char in text):
        raise ValueError("entry must not contain control characters")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ValueError(f"entry must be valid UTF-8 text: {error}") from error
    return text


def write_entry(text, output_dir):
    """Validate *text*, write it to entry.txt in *output_dir*, print it.

    The file holds exactly the entry line: no trailing newline, mode
    0644 so the grader can read it as another user.
    """
    entry = validate(text)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(entry)
    os.chmod(path, 0o644)
    print(entry)
    return path


def main():
    """Validate the entry line, write it to entry.txt, and print it."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(ENTRY, output_dir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"invalid entry: {error}", file=sys.stderr)
        raise SystemExit(1)

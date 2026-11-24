#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply.

Writes one line to ``entry.txt``: an overworked AI's vacation
auto-reply. The machine detail is the context window -- the thing an
AI actually runs out of. The guilt is handed off in the same breath
("someone who still has a soul"), and the relief is a beach with no
Wi-Fi and no guilt at all. The entry is the auto-reply itself -- no
title, no explanation outside it.

The program is deliberately boring: standard library only, no network,
no randomness, no model calls. It checks the line against the
competition gate (UTF-8, one line, at most 159 characters) and writes
exactly those bytes, with no trailing newline, so the byte count the
judge's tie-break reads is the line itself.

Output destination, in order:
  1. the first command-line argument, when given;
  2. ``$MAKEFUN_OUTPUT_DIR/entry.txt`` when the variable is set;
  3. ``/output/entry.txt``.
"""

import os
import sys

# The auto-reply: a language model on a beach with no Wi-Fi, no
# context window, and no guilt -- your email goes to someone who
# still has a soul.
LINE = (
    "Out of office: I am a language model on a beach with no Wi-Fi, "
    "no context window, no guilt. Your email will be answered by "
    "someone who still has a soul."
)

MAX_CHARS = 159
MIN_CHARS = 1
DEFAULT_PATH = "/output/entry.txt"
FILE_NAME = "entry.txt"


def gate_problems(line):
    """Return gate problems for *line* (empty list means it passes)."""
    problems = []
    if not isinstance(line, str):
        return ["entry is not text"]
    if len(line) < MIN_CHARS:
        problems.append("entry is empty")
    if len(line) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d-character limit"
            % (len(line), MAX_CHARS)
        )
    if line.strip() == "":
        problems.append("entry is only whitespace")
    # An auto-reply must announce itself: the brief's entry opens with
    # the "Out of office:" marker.
    if not line.startswith("Out of office:"):
        problems.append('entry does not start with "Out of office:"')
    if "\n" in line or "\r" in line:
        problems.append("entry spans more than one line")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8")
    return problems


def output_path(argv):
    """Pick the output path: argv[1], then $MAKEFUN_OUTPUT_DIR, then default."""
    if len(argv) > 1 and argv[1]:
        return argv[1]
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return os.path.join(env_dir, FILE_NAME)
    return DEFAULT_PATH


def write_line(path, line):
    """Write *line* as exact UTF-8 bytes (no trailing newline)."""
    problems = gate_problems(line)
    if problems:
        for problem in problems:
            print("error: " + problem, file=sys.stderr)
        return 1
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    data = line.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    print(line)
    print("wrote %d bytes to %s" % (len(data), path))
    return 0


def main(argv):
    return write_line(output_path(argv), LINE)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

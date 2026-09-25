#!/usr/bin/env python3
"""Reject KubeJS event handlers that cancel before sending player rejection feedback."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
KUBEJS = ROOT / "kubejs"
EVENT_HANDLER = re.compile(
    r"(?:BlockEvents|ItemEvents)\.[A-Za-z]+\([^=]*?=>\s*\{(?P<body>.*?)\n\}\)",
    re.DOTALL,
)
CANCEL = re.compile(r"\bevent\.cancel\(\)")
FEEDBACK = re.compile(
    r"(?:\b(?:event\.)?player\.tell\s*\(|\bplayer\.tell\s*\(|"
    r"\bshow[A-Za-z0-9_]*Rejection\s*\()"
)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def main() -> int:
    failures: list[str] = []
    scanned = 0
    handlers = 0

    for path in sorted(KUBEJS.rglob("*.js")):
        text = path.read_text(encoding="utf-8")
        scanned += 1
        for match in EVENT_HANDLER.finditer(text):
            handlers += 1
            body = match.group("body")
            cancel = CANCEL.search(body)
            if cancel is None:
                continue
            feedback = FEEDBACK.search(body)
            if feedback is None or feedback.start() < cancel.start():
                continue
            relative = path.relative_to(ROOT).as_posix()
            failures.append(
                f"{relative}:{line_number(text, match.start('body') + cancel.start())}: "
                "event.cancel() occurs before player rejection feedback"
            )

    if failures:
        print("KubeJS rejection-feedback ordering audit FAILED")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print(
        "KubeJS rejection-feedback ordering audit passed: "
        f"{scanned} JavaScript files, {handlers} BlockEvents/ItemEvents handlers checked."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

from __future__ import annotations

import re
from typing import Callable


def parse_hints(raw: str) -> list[str]:
    if not raw:
        return []
    s = raw.replace("\n", ",")
    parts = [p.strip() for p in s.split(",")]
    hints = [p for p in parts if p]
    seen = set()
    out = []
    for h in hints:
        k = h.lower()
        if k not in seen:
            seen.add(k)
            out.append(h)
    return out


def build_matcher(
    hints: list[str],
    mode: str,
    ignore_case: bool,
    use_regex: bool,
    word_boundary: bool,
) -> tuple[Callable[[str], bool], str | None]:
    if not hints:
        return (lambda _t: True), None

    if not use_regex and not word_boundary:
        if ignore_case:
            hs = [h.lower() for h in hints]

            def match(t: str) -> bool:
                tl = t.lower()
                return all(h in tl for h in hs) if mode == "AND" else any(h in tl for h in hs)

            return match, None

        def match(t: str) -> bool:
            return all(h in t for h in hints) if mode == "AND" else any(h in t for h in hints)

        return match, None

    flags = re.IGNORECASE if ignore_case else 0
    patterns: list[re.Pattern] = []

    for h in hints:
        if use_regex:
            p = h
        else:
            p = re.escape(h)

        if word_boundary:
            p = rf"\b(?:{p})\b"

        try:
            patterns.append(re.compile(p, flags))
        except re.error as e:
            return (lambda _t: False), f"Regex error: {e}"

    def match(t: str) -> bool:
        if mode == "AND":
            return all(p.search(t) is not None for p in patterns)
        return any(p.search(t) is not None for p in patterns)

    return match, None

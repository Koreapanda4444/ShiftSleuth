from __future__ import annotations


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


def match_hints(text: str, hints: list[str], mode: str, ignore_case: bool) -> bool:
    if not hints:
        return True

    if ignore_case:
        t = text.lower()
        hs = [h.lower() for h in hints]
    else:
        t = text
        hs = hints

    if mode == "AND":
        return all(h in t for h in hs)
    return any(h in t for h in hs)

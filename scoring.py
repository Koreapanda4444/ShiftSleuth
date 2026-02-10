from __future__ import annotations

import math


ENGLISH_FREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
    0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
    0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
]


def letter_counts_az(text: str) -> tuple[list[int], int]:
    counts = [0] * 26
    total = 0
    for ch in text:
        o = ord(ch)
        if 65 <= o <= 90:
            counts[o - 65] += 1
            total += 1
        elif 97 <= o <= 122:
            counts[o - 97] += 1
            total += 1
    return counts, total


def chi_square_score(text: str) -> float:
    counts, total = letter_counts_az(text)
    if total == 0:
        return float("inf")

    score = 0.0
    for i in range(26):
        exp = ENGLISH_FREQ[i] * total
        if exp > 0:
            diff = counts[i] - exp
            score += (diff * diff) / exp
    return score


def confidence_percent(scores: list[float]) -> list[float]:
    finite = [s for s in scores if math.isfinite(s)]
    if not finite:
        return [0.0 for _ in scores]

    m = min(finite)
    adj = []
    for s in scores:
        if math.isfinite(s):
            adj.append(s - m)
        else:
            adj.append(float("inf"))

    finite_adj = [a for a in adj if math.isfinite(a)]
    mx = max(finite_adj) if finite_adj else 1.0
    if mx <= 0:
        return [100.0 if a == 0 else 0.0 for a in adj]

    k = 5.0
    weights = []
    for a in adj:
        if math.isfinite(a):
            weights.append(math.exp(-k * (a / mx)))
        else:
            weights.append(0.0)

    s = sum(weights)
    if s <= 0:
        return [0.0 for _ in scores]

    return [w / s * 100.0 for w in weights]

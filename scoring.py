from __future__ import annotations


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


def letter_freq_az(text: str) -> tuple[list[float], int]:
    counts, total = letter_counts_az(text)
    if total == 0:
        return [0.0] * 26, 0
    freqs = [c / total for c in counts]
    return freqs, total


def alpha_ratio(text: str) -> float:
    if not text:
        return 0.0
    _, total = letter_counts_az(text)
    return total / len(text)

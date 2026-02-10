from __future__ import annotations


def _shift_upper(ch: str, shift: int) -> str:
    base = ord("A")
    return chr((ord(ch) - base + shift) % 26 + base)


def _shift_lower(ch: str, shift: int) -> str:
    base = ord("a")
    return chr((ord(ch) - base + shift) % 26 + base)


def caesar(text: str, shift: int, *, decrypt: bool = False) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(shift, int):
        raise TypeError("shift must be an int")

    s = shift % 26
    if decrypt:
        s = (-s) % 26

    out_chars: list[str] = []
    for ch in text:
        o = ord(ch)
        if 65 <= o <= 90:
            out_chars.append(_shift_upper(ch, s))
        elif 97 <= o <= 122:
            out_chars.append(_shift_lower(ch, s))
        else:
            out_chars.append(ch)

    return "".join(out_chars)


def encrypt(text: str, shift: int) -> str:
    return caesar(text, shift, decrypt=False)


def decrypt(text: str, shift: int) -> str:
    return caesar(text, shift, decrypt=True)


__all__ = ["caesar", "encrypt", "decrypt"]

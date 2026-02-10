from __future__ import annotations

from matplotlib.figure import Figure

from scoring import ENGLISH_FREQ, letter_counts_az


def _freqs(text: str) -> tuple[list[float], int]:
    counts, total = letter_counts_az(text)
    if total <= 0:
        return [0.0] * 26, 0
    return [c / total for c in counts], total


def build_frequency_figure(input_text: str, selected_text: str) -> tuple[Figure, object]:
    fig = Figure(figsize=(6.2, 2.6), dpi=100)
    ax = fig.add_subplot(111)
    update_frequency_axes(ax, input_text, selected_text)
    fig.tight_layout()
    return fig, ax


def update_frequency_axes(ax, input_text: str, selected_text: str) -> None:
    fin, _ = _freqs(input_text)
    fsel, _ = _freqs(selected_text)
    fref = ENGLISH_FREQ

    ax.clear()

    x = list(range(26))
    ax.plot(x, fin, label="Input")
    ax.plot(x, fsel, label="Selected")
    ax.plot(x, fref, label="English")

    ax.set_ylim(0, max(0.13, max(fin + fsel + fref) * 1.1))
    ax.set_xticks(x)
    ax.set_xticklabels([chr(65 + i) for i in range(26)], fontsize=8)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.2)

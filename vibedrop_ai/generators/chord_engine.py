"""
Chord progression generator.

Builds diatonic 7th-chord progressions for any root note,
using interval templates from music_theory.py.
"""

import random
from dataclasses import dataclass
from typing import List

from vibedrop_ai.music_theory import (
    MINOR_CHORD_TEMPLATES,
    MAJOR_CHORD_TEMPLATES,
    build_chord,
)


@dataclass
class ChordEvent:
    start_bar: float
    duration_bars: float
    notes: List[int]


def generate_chord_prog(
    root_note: int,
    bars: int,
    mode: str = "minor",
) -> List[ChordEvent]:
    """Generate a random diatonic chord progression.

    Args:
        root_note: MIDI note number for the key root (e.g. 60 = C4).
        bars:      Number of bars (one chord per bar).
        mode:      ``"minor"`` or ``"major"``.

    Returns:
        A list of :class:`ChordEvent` objects.
    """
    templates = (
        MINOR_CHORD_TEMPLATES if mode == "minor" else MAJOR_CHORD_TEMPLATES
    )

    chord_pool = [
        build_chord(root_note + t["degree"], t["intervals"])
        for t in templates
    ]

    events: list[ChordEvent] = []
    for bar_index in range(bars):
        chord_notes = random.choice(chord_pool)

        events.append(
            ChordEvent(
                start_bar=bar_index,
                duration_bars=1,
                notes=chord_notes,
            )
        )

    return events
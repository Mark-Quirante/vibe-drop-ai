from dataclasses import dataclass
from typing import List
from vibedrop_ai.config import ROOT_NOTE

@dataclass
class ChordEvent:
    start_bar: float
    duration_bars: float
    notes: List[int]

# chords
def _cm7() -> list[int]:
    return [ROOT_NOTE + i for i in (0, 3, 7, 10)]


def _fm7() -> list[int]:
    return [ROOT_NOTE + i for i in (5, 8, 12, 15)]


def _abmaj7() -> list[int]:
    return [ROOT_NOTE + i for i in (8, 12, 15, 19)]


def _gm7() -> list[int]:
    return [ROOT_NOTE + i for i in (7, 10, 14, 17)]


# generate chord progression
def generate_cm_chord_prog(bars):
    base_progression = [
        _cm7(),
        _fm7(),
        _abmaj7(),
        _gm7(),
    ]

    events: list[ChordEvent] = []
    for bar_index in range(bars):
        chord_notes = base_progression[bar_index % len(base_progression)]
        events.append(
            ChordEvent(
                start_bar=bar_index,
                duration_bars=1,
                notes=chord_notes,
            )
        )

    return events
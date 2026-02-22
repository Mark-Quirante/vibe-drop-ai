"""
Music theory constants and helpers.

Pure interval math — no MIDI I/O or config dependencies.
"""

from __future__ import annotations

# ── Note names (chromatic, sharps only) ──────────────────────────────
NOTE_NAMES: list[str] = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B",
]

# ── Scale interval templates (semitones from root) ───────────────────
SCALES: dict[str, tuple[int, ...]] = {
    "minor_pentatonic": (0, 3, 5, 7, 10),
    "major_pentatonic": (0, 2, 4, 7, 9),
    "natural_minor":    (0, 2, 3, 5, 7, 8, 10),
    "natural_major":    (0, 2, 4, 5, 7, 9, 11),
}

# ── Chord templates for natural-minor diatonic 7ths ─────────────────
# Each entry: degree = semitone offset of the chord root from the key root,
#             intervals = chord tones relative to *that* chord root.
MINOR_CHORD_TEMPLATES: list[dict] = [
    {"name": "im7",     "degree": 0,  "intervals": (0, 3, 7, 10)},
    {"name": "iidim7",  "degree": 2,  "intervals": (0, 3, 6, 10)},
    {"name": "IIImaj7", "degree": 3,  "intervals": (0, 4, 7, 11)},
    {"name": "ivm7",    "degree": 5,  "intervals": (0, 3, 7, 10)},
    {"name": "vm7",     "degree": 7,  "intervals": (0, 3, 7, 10)},
    {"name": "VImaj7",  "degree": 8,  "intervals": (0, 4, 7, 11)},
    {"name": "VII7",    "degree": 10, "intervals": (0, 4, 7, 10)},
]

MAJOR_CHORD_TEMPLATES: list[dict] = [
    {"name": "Imaj7",   "degree": 0,  "intervals": (0, 4, 7, 11)},
    {"name": "ii7",     "degree": 2,  "intervals": (0, 3, 7, 10)},
    {"name": "iii7",    "degree": 4,  "intervals": (0, 3, 7, 10)},
    {"name": "IVmaj7",  "degree": 5,  "intervals": (0, 4, 7, 11)},
    {"name": "V7",      "degree": 7,  "intervals": (0, 4, 7, 10)},
    {"name": "vi7",     "degree": 9,  "intervals": (0, 3, 7, 10)},
    {"name": "viidim7", "degree": 11, "intervals": (0, 3, 6, 10)},
]


# ── Helpers ──────────────────────────────────────────────────────────

def note_name_to_midi(name: str, octave: int = 4) -> int:
    """Convert a note name + octave to a MIDI note number.

    >>> note_name_to_midi("C", 4)
    60
    >>> note_name_to_midi("G#", 3)
    56
    """
    return 12 * (octave + 1) + NOTE_NAMES.index(name)


def build_scale(root_midi: int, scale_key: str) -> list[int]:
    """Return MIDI note numbers for a scale starting at *root_midi*.

    >>> build_scale(60, "minor_pentatonic")
    [60, 63, 65, 67, 70]
    """
    return [root_midi + i for i in SCALES[scale_key]]


def build_chord(root_midi: int, intervals: tuple[int, ...]) -> list[int]:
    """Return MIDI note numbers for a chord.

    >>> build_chord(60, (0, 4, 7))
    [60, 64, 67]
    """
    return [root_midi + i for i in intervals]

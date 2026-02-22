"""
Melody generator.

Produces a pentatonic melody with stepwise bias and rhythmic variety
for any root note and scale type.
"""

from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
import random

from vibedrop_ai.config import TICKS_PER_BEAT, ROOT_NOTE
from vibedrop_ai.music_theory import build_scale


def generate_melody(
    output: str,
    bpm: int = 85,
    bars: int = 4,
    root_note: int = ROOT_NOTE,
    scale_key: str = "minor_pentatonic",
    ticks_per_beat: int = TICKS_PER_BEAT,
) -> None:
    """Generate a melody and save it as a MIDI file.

    Args:
        output:     File path for the ``.mid`` output.
        bpm:        Tempo in beats per minute.
        bars:       Number of bars to generate.
        root_note:  MIDI note number for the key root (e.g. 60 = C4).
        scale_key:  Key into :data:`music_theory.SCALES` (e.g.
                    ``"minor_pentatonic"``, ``"major_pentatonic"``).
        ticks_per_beat: MIDI resolution.
    """
    scale = build_scale(root_note, scale_key)

    mid = MidiFile(ticks_per_beat=ticks_per_beat)
    track = MidiTrack()
    mid.tracks.append(track)

    # tempo
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm), time=0))

    # rhythm
    eighth = ticks_per_beat // 2
    durations = [eighth, eighth, eighth * 2]

    total_beats = bars * 4
    total_ticks = total_beats * ticks_per_beat

    current_time = 0
    last_note = random.choice(scale)

    while current_time < total_ticks:
        # chance of rest (space)
        if random.random() < 0.20:
            current_time += random.choice(durations)
            continue
        dur = random.choice(durations)

        # stepwise bias
        step_options = [n for n in scale if abs(n - last_note) <= 5]
        note = random.choice(step_options) if step_options else random.choice(scale)

        # emit note
        track.append(Message('note_on', note=note, velocity=90, time=0))
        track.append(Message('note_off', note=note, velocity=0, time=dur))

        last_note = note
        current_time += dur

    mid.save(output)
    print("Saved melody to", output)
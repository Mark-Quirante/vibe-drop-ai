from dataclasses import dataclass
from mido import MidiFile, MidiTrack, Message
from vibedrop_ai.generators.chord_engine import ChordEvent
from vibedrop_ai.config import TimeSignature

def beats_to_ticks(beats, ts: TimeSignature, ticks_per_quarter):
    quarter_notes_per_beat = 4 / ts.denominator
    return int(beats * quarter_notes_per_beat * ticks_per_quarter)


def bars_to_ticks(bars, ts: TimeSignature, ticks_per_quarter):
    total_beats = bars * ts.numerator
    return beats_to_ticks(total_beats, ts, ticks_per_quarter)


def write_chord_track(
    mid: MidiFile,
    chords: list[ChordEvent],
    ts,
    ticks_per_quarter: int,
) -> None:
    track = MidiTrack()
    mid.tracks.append(track)

    chords = sorted(chords, key=lambda ev: ev.start_bar)

    last_tick = 0
    for event in chords:
        chord_start_ticks = bars_to_ticks(event.start_bar, ts, ticks_per_quarter)
        chord_duration_ticks = bars_to_ticks(event.duration_bars, ts, ticks_per_quarter)

        delta = chord_start_ticks - last_tick
        if delta < 0:
            delta = 0

        # NOTE ONs
        for i, note in enumerate(event.notes):
            time = delta if i == 0 else 0
            track.append(Message("note_on", note=note, velocity=80, time=time))

        # NOTE OFFs
        for i, note in enumerate(event.notes):
            time = chord_duration_ticks if i == 0 else 0
            track.append(Message("note_off", note=note, velocity=0, time=time))

        last_tick = chord_start_ticks + chord_duration_ticks
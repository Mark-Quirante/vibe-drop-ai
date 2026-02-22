"""Generate a 4-bar RnB chord progression and export as MIDI."""

import os
from mido import MidiFile
from vibedrop_ai.config import TICKS_PER_BEAT, DEFAULT_TIME_SIGNATURE, OUTPUT_DIR, ROOT_NOTE
from vibedrop_ai.generators.chord_engine import generate_chord_prog
from vibedrop_ai.music.midi_io import write_chord_track

OUTPUT_PATH = os.path.join(OUTPUT_DIR, "poc_chords_only.mid")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)

    chords = generate_chord_prog(root_note=ROOT_NOTE, bars=4)
    write_chord_track(
        mid,
        chords,
        DEFAULT_TIME_SIGNATURE,
        TICKS_PER_BEAT,
    )

    mid.save(OUTPUT_PATH)
    print("Saved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()

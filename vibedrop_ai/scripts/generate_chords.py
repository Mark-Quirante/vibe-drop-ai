# scripts/generate_chords_only.py

from mido import MidiFile
from vibedrop_ai.config import TICKS_PER_BEAT, DEFAULT_TIME_SIGNATURE
from vibedrop_ai.generators.chord_engine import generate_cm_chord_prog
from vibedrop_ai.music.midi_io import write_chord_track

OUTPUT_PATH = r"C:\FL-Sample-Library\Vibe Drop AI\poc_chords_only.mid"


def main():
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)

    chords = generate_cm_chord_prog(bars=4)
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

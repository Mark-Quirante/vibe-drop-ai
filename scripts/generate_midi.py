"""Generate a C-Minor pentatonic melody and export as MIDI."""

import os
from vibedrop_ai.config import OUTPUT_DIR
from vibedrop_ai.generators.poc_melody import generate_melody

OUTPUT_PATH = os.path.join(OUTPUT_DIR, "poc_melody.mid")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generate_melody(output=OUTPUT_PATH)


if __name__ == "__main__":
    main()

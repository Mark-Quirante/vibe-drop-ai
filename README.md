# 🎹 Vibe Drop AI (v0.2.0)

> An AI-assisted MIDI generator for RnB and Lo-Fi production.

Vibe Drop AI creates soulful chord progressions and pentatonic melodies, allowing producers to generate inspiration algorithmically and drag the results directly into their DAW.

## ✨ Features

* **Vibe Drop UI:** A modern Graphical User Interface to control all parameters without touching code.
* **Universal Key Support:** Generate music in any of the 12 chromatic keys (C through B).
* **Major & Minor Modes:** Now supports both Major and Minor scales and chord progressions.
* **RnB Chord Engine:** Generates 4-bar progressions using rich voicings (m7, maj7, dimb5).
* **Generative Melody:** Uses stepwise bias and rhythmic variety to create natural-sounding pentatonic leads.

## 🛠 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/vibedrop-ai.git
cd vibedrop-ai
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install -e .
```

## 🚀 Usage

### 1. Launch Vibe Drop UI (Recommended)

To open the graphical dashboard:

```bash
python vibedrop_ui.py
```

From the UI, you can select the Key, Mode (Major/Minor), BPM, and Bar length, then click "Generate" to save MIDI files to your desired folder.

### 2. Generate via CLI

You can still use the traditional script-based generation:

```bash
# Generate a 4-bar RnB chord progression
python scripts/generate_chords.py

# Generate a C-Minor pentatonic melody
python scripts/generate_midi.py
```


Generated MIDI files are saved to the `output/` directory by default.

## ⚙️ Configuration

You can tweak the "vibe" in `vibedrop_ai/config.py`:

| Variable | Default | Description |
|---|---|---|
| `ROOT_NOTE` | `60` (C4) | Base key for all generated content |
| `TICKS_PER_BEAT` | `480` | MIDI resolution — divisible by both 2 and 3 for straight and swung timing |
| `DEFAULT_TIME_SIGNATURE` | `4/4` | Toggle between 4/4 or 6/8 "swing" feels |
| `OUTPUT_DIR` | `<project_root>/output/` | Where generated `.mid` files are written |

## 📝 Recent Changes (v0.2.0)

* **Portable Output Paths:** Replaced hardcoded Windows paths with OS-agnostic defaults using `os.path`.
* **Scripts at Project Root:** Moved entry-point scripts to `scripts/` for standard `python scripts/…` invocation.
* **Modularized MIDI I/O:** MIDI writing logic lives in `midi_io.py` for better reusability.
* **Config Centralization:** Constants like `TICKS_PER_BEAT`, `ROOT_NOTE`, and `OUTPUT_DIR` are sourced from a single `config.py`.
* **Chord Pool:** Standardized `CHORD_POOL` featuring Cm7, Ddimb5, Emaj7, Fm7, Gm7, Abmaj7, and Bb7.
* **Stepwise Melody Bias:** Pentatonic melody engine avoids erratic jumps for more musical results.

## 📁 Project Structure

```
vibedrop-ai/
├── scripts/                  # Entry-point scripts
│   ├── generate_chords.py
│   └── generate_midi.py
├── vibedrop_ai/              # Core package
│   ├── config.py             # Global constants
│   ├── generators/           # Music-theory & randomness engines
│   │   ├── chord_engine.py
│   │   └── poc_melody.py
│   └── music/                # Low-level MIDI file I/O
│       └── midi_io.py
├── output/                   # Generated MIDI files (git-ignored)
├── requirements.txt
└── README.md
```

## 🗺 Roadmap

| Version | Milestone |
|---|---|
| **v0.3.0** | Add more scales (Dorian, Phrygian) and "Vibe" presets (Neo-Soul, Jazz) |
| **v1.0.0** | FL Studio Python Scripting integration for direct-to-piano-roll generation |

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

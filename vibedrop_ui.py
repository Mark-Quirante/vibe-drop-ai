"""
Vibe Drop AI — GUI Dashboard

Launch with:  python vibedrop_ui.py
"""

import os
import customtkinter as ctk
from tkinter import filedialog
from mido import MidiFile

from vibedrop_ai.config import (
    TICKS_PER_BEAT,
    DEFAULT_TIME_SIGNATURE,
    OUTPUT_DIR,
)
from vibedrop_ai.music_theory import NOTE_NAMES, note_name_to_midi
from vibedrop_ai.generators.chord_engine import generate_chord_prog
from vibedrop_ai.generators.poc_melody import generate_melody
from vibedrop_ai.music.midi_io import write_chord_track


# ── Theme ────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT = "#7C3AED"       # vibrant purple
ACCENT_HOVER = "#6D28D9"
BG_DARK = "#0F0F14"
BG_CARD = "#1A1A24"
FG_TEXT = "#E4E4ED"
FG_DIM = "#8888A0"


class VibeDropApp(ctk.CTk):
    """Single-window dashboard for chord & melody generation."""

    def __init__(self) -> None:
        super().__init__()

        # ── Window setup ─────────────────────────────────────────────
        self.title("🎹 Vibe Drop AI")
        self.geometry("520x680")
        self.minsize(460, 620)
        self.configure(fg_color=BG_DARK)

        # ── Header ───────────────────────────────────────────────────
        header = ctk.CTkLabel(
            self,
            text="🎹  Vibe Drop AI",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=FG_TEXT,
        )
        header.pack(pady=(24, 2))

        subtitle = ctk.CTkLabel(
            self,
            text="RnB & Lo-Fi MIDI Generator",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=FG_DIM,
        )
        subtitle.pack(pady=(0, 18))

        # ── Main card ────────────────────────────────────────────────
        card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=16)
        card.pack(padx=28, pady=(0, 12), fill="x")

        row = 0

        # Key selector
        self._add_label(card, "Key", row)
        self.key_var = ctk.StringVar(value="C")
        self.key_menu = ctk.CTkOptionMenu(
            card,
            variable=self.key_var,
            values=NOTE_NAMES,
            width=180,
            fg_color=ACCENT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
        )
        self.key_menu.grid(row=row, column=1, padx=16, pady=12, sticky="e")
        row += 1

        # Mode selector
        self._add_label(card, "Mode", row)
        self.mode_var = ctk.StringVar(value="Minor")
        self.mode_menu = ctk.CTkOptionMenu(
            card,
            variable=self.mode_var,
            values=["Minor", "Major"],
            width=180,
            fg_color=ACCENT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
        )
        self.mode_menu.grid(row=row, column=1, padx=16, pady=12, sticky="e")
        row += 1

        # BPM slider
        self._add_label(card, "BPM", row)
        bpm_frame = ctk.CTkFrame(card, fg_color="transparent")
        bpm_frame.grid(row=row, column=1, padx=16, pady=12, sticky="e")

        self.bpm_label = ctk.CTkLabel(
            bpm_frame, text="85", width=36,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ACCENT,
        )
        self.bpm_label.pack(side="right", padx=(8, 0))

        self.bpm_slider = ctk.CTkSlider(
            bpm_frame,
            from_=40, to=200,
            number_of_steps=160,
            width=140,
            progress_color=ACCENT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            command=self._on_bpm_change,
        )
        self.bpm_slider.set(85)
        self.bpm_slider.pack(side="right")
        row += 1

        # Bars selector
        self._add_label(card, "Bars", row)
        self.bars_var = ctk.StringVar(value="4")
        self.bars_menu = ctk.CTkOptionMenu(
            card,
            variable=self.bars_var,
            values=["2", "4", "8"],
            width=180,
            fg_color=ACCENT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
        )
        self.bars_menu.grid(row=row, column=1, padx=16, pady=12, sticky="e")
        row += 1

        # configure card columns
        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=0)

        # ── Output path card ─────────────────────────────────────────
        out_card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=16)
        out_card.pack(padx=28, pady=(0, 12), fill="x")

        out_label = ctk.CTkLabel(
            out_card, text="Output Folder",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=FG_DIM,
        )
        out_label.grid(row=0, column=0, padx=16, pady=(12, 4), sticky="w")

        path_frame = ctk.CTkFrame(out_card, fg_color="transparent")
        path_frame.grid(row=1, column=0, padx=16, pady=(0, 12), sticky="ew")
        out_card.columnconfigure(0, weight=1)

        self.path_var = ctk.StringVar(value=OUTPUT_DIR)
        self.path_entry = ctk.CTkEntry(
            path_frame,
            textvariable=self.path_var,
            width=300,
        )
        self.path_entry.pack(side="left", fill="x", expand=True)

        browse_btn = ctk.CTkButton(
            path_frame,
            text="Browse",
            width=70,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self._browse_folder,
        )
        browse_btn.pack(side="right", padx=(8, 0))

        # ── Generate buttons ─────────────────────────────────────────
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=28, pady=(4, 8), fill="x")

        self.chord_btn = ctk.CTkButton(
            btn_frame,
            text="🎶  Generate Chords",
            height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            corner_radius=12,
            command=self._generate_chords,
        )
        self.chord_btn.pack(fill="x", pady=(0, 8))

        self.melody_btn = ctk.CTkButton(
            btn_frame,
            text="🎵  Generate Melody",
            height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            corner_radius=12,
            command=self._generate_melody,
        )
        self.melody_btn.pack(fill="x")

        # ── Status bar ───────────────────────────────────────────────
        self.status = ctk.CTkLabel(
            self,
            text="Ready — choose your vibe and hit generate.",
            font=ctk.CTkFont(size=12),
            text_color=FG_DIM,
        )
        self.status.pack(side="bottom", pady=(8, 16))

    # ── Helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _add_label(parent: ctk.CTkFrame, text: str, row: int) -> None:
        lbl = ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=FG_DIM,
        )
        lbl.grid(row=row, column=0, padx=16, pady=12, sticky="w")

    def _on_bpm_change(self, value: float) -> None:
        self.bpm_label.configure(text=str(int(value)))

    def _browse_folder(self) -> None:
        folder = filedialog.askdirectory(initialdir=self.path_var.get())
        if folder:
            self.path_var.set(folder)

    def _get_params(self) -> dict:
        """Read all widget values into a param dict."""
        root = note_name_to_midi(self.key_var.get(), octave=4)
        return {
            "root_note": root,
            "mode": self.mode_var.get().lower(),
            "bpm": int(self.bpm_slider.get()),
            "bars": int(self.bars_var.get()),
            "output_dir": self.path_var.get(),
        }

    def _set_status(self, msg: str, error: bool = False) -> None:
        color = "#EF4444" if error else "#22C55E"
        self.status.configure(text=msg, text_color=color)

    # ── Generation callbacks ─────────────────────────────────────────

    def _generate_chords(self) -> None:
        try:
            p = self._get_params()
            os.makedirs(p["output_dir"], exist_ok=True)

            out_path = os.path.join(p["output_dir"], "chords.mid")
            mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)

            chords = generate_chord_prog(
                root_note=p["root_note"],
                bars=p["bars"],
                mode=p["mode"],
            )
            write_chord_track(mid, chords, DEFAULT_TIME_SIGNATURE, TICKS_PER_BEAT)
            mid.save(out_path)

            self._set_status(f"✅  Chords saved → {out_path}")
        except Exception as exc:
            self._set_status(f"❌  {exc}", error=True)

    def _generate_melody(self) -> None:
        try:
            p = self._get_params()
            os.makedirs(p["output_dir"], exist_ok=True)

            out_path = os.path.join(p["output_dir"], "melody.mid")

            scale_key = (
                "minor_pentatonic" if p["mode"] == "minor" else "major_pentatonic"
            )

            generate_melody(
                output=out_path,
                bpm=p["bpm"],
                bars=p["bars"],
                root_note=p["root_note"],
                scale_key=scale_key,
            )
            self._set_status(f"✅  Melody saved → {out_path}")
        except Exception as exc:
            self._set_status(f"❌  {exc}", error=True)


if __name__ == "__main__":
    app = VibeDropApp()
    app.mainloop()

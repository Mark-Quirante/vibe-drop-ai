from mido import Message, MidiFile, MidiTrack
import random

output_path="C:\\FL-Sample-Library\Vibe Drop AI\poc_melody.mid"

def generate_melody(
        output=output_path,
        bpm=85,
        bars=4,
        ticks_per_beat=480,
):
    # Cmin pentatonic scale
    scale = [60, 63, 65, 67, 70] # C4 Eb4 F4 G4 Bb4

    mid=MidiFile(ticks_per_beat=ticks_per_beat)
    track = MidiTrack()
    mid.tracks.append(track)

    # tempo
    from mido import MetaMessage, bpm2tempo
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
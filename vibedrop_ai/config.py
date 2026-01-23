"""
config file used when generating chords or melodies
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class TimeSignature:
    numerator: int # beats per bar
    denominator: int # note value that represents 1 beat (4 = quarter, 8 = eighth)

"""
A standard MIDI resolution that divides cleanly into all common rhythmic
subdivisions (1/4, 1/8, 1/16, triplets, swing). 480 is divisible by both
2 and 3 many times, making it ideal for both straight and swung timing.

Using 480 keeps all rhythm logic tied to musical beats instead of real-time milliseconds.
"""

TICKS_PER_BEAT = 480

"""
In MIDI notes follow a formula when assigned a value between (0-127)

note_value = 12 * (octave_number + 1) + Semitone

where the value of semitone is (chart below)
                                C = 0
                                C# = 1
                                D = 2
                                D# = 3
                                E = 4
                                F = 5
                                F# = 6
                                G = 7
                                G# = 8
                                A = 9
                                A# = 10
                                B = 11
        
example: C4
note_value = 12 * (4 + 1) + 0
note_value = 60 -> C4
"""

ROOT_NOTE = 60 # C4

"""
Default time signature of generated notes
"""
# can be changed to 6/8
DEFAULT_TIME_SIGNATURE = TimeSignature(4,4)


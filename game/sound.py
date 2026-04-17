"""
Programmatic sound synthesis for Flappy Bird.

All sounds are generated at runtime using only Python built-ins (array, math)
and pygame.mixer.Sound(buffer=...).  No audio files are needed, which keeps
the project pygbag/WASM compatible (pygbag only supports OGG files; by
generating PCM buffers directly we bypass that restriction entirely).

Mixer settings: 22050 Hz, signed 16-bit, mono, 512-sample buffer.
"""

from __future__ import annotations

import array
import math

import pygame


_SAMPLE_RATE = 22050
_MAX_AMP = 32767  # max value for signed 16-bit PCM


class SoundManager:
    """Generates and plays all game sounds.

    Falls back to silent no-ops if pygame.mixer fails to initialise
    (e.g. headless CI environments or systems with no audio device).
    """

    def __init__(self) -> None:
        self._enabled = False
        try:
            # pre_init must have been called before pygame.init() in main.py.
            # If mixer is not yet running, initialise it now with our settings.
            if not pygame.mixer.get_init():
                pygame.mixer.init(_SAMPLE_RATE, -16, 1, 512)
            self._enabled = True
        except pygame.error:
            return  # audio unavailable — all play_*() calls become no-ops

        self._flap = self._build_flap()
        self._score = self._build_score()
        self._hit = self._build_hit()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def play_flap(self) -> None:
        if self._enabled:
            self._flap.play()

    def play_score(self) -> None:
        if self._enabled:
            self._score.play()

    def play_hit(self) -> None:
        if self._enabled:
            self._hit.stop()   # interrupt any previous hit sound
            self._hit.play()

    # ------------------------------------------------------------------
    # Sound builders
    # ------------------------------------------------------------------

    def _build_flap(self) -> pygame.mixer.Sound:
        """Short rising frequency sweep: 400 → 700 Hz over 120 ms."""
        duration_ms = 120
        n = int(_SAMPLE_RATE * duration_ms / 1000)
        buf = array.array("h", [0] * n)
        for i in range(n):
            t = i / _SAMPLE_RATE
            progress = i / n
            freq = 400 + 300 * progress          # linear sweep up
            envelope = math.exp(-t * 18)          # fast decay
            phase = 2 * math.pi * freq * t
            buf[i] = int(_MAX_AMP * 0.6 * envelope * math.sin(phase))
        return pygame.mixer.Sound(buffer=buf)

    def _build_score(self) -> pygame.mixer.Sound:
        """Two-note ascending ding: 880 Hz → 1100 Hz, 150 ms each."""
        note_ms = 150
        n_note = int(_SAMPLE_RATE * note_ms / 1000)
        n_total = n_note * 2
        buf = array.array("h", [0] * n_total)

        for note_idx, freq in enumerate((880, 1100)):
            offset = note_idx * n_note
            for i in range(n_note):
                t = i / _SAMPLE_RATE
                # Smooth bell-shaped envelope: attack then decay
                envelope = math.sin(math.pi * i / n_note) ** 0.5
                phase = 2 * math.pi * freq * t
                buf[offset + i] = int(_MAX_AMP * 0.55 * envelope * math.sin(phase))

        return pygame.mixer.Sound(buffer=buf)

    def _build_hit(self) -> pygame.mixer.Sound:
        """Descending distorted buzz: 300 → 80 Hz over 300 ms."""
        duration_ms = 300
        n = int(_SAMPLE_RATE * duration_ms / 1000)
        buf = array.array("h", [0] * n)
        for i in range(n):
            t = i / _SAMPLE_RATE
            progress = i / n
            freq = 300 - 220 * progress           # sweep down
            envelope = math.exp(-t * 7)            # slower decay for impact feel
            phase = 2 * math.pi * freq * t
            raw = math.sin(phase)
            # Soft clip for a rougher, buzzy timbre
            clipped = max(-0.6, min(0.6, raw * 2.0)) / 0.6
            buf[i] = int(_MAX_AMP * 0.7 * envelope * clipped)
        return pygame.mixer.Sound(buffer=buf)

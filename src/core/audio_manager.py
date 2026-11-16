"""Audio Manager for Paper Warfire.
Gracefully handles SFX and BGM:
- If audio files exist in assets/audio/ (e.g. shot.wav, hit.wav, click.wav), plays them.
- If assets are not yet added, silently ignores without raising any errors.
"""

import os
from typing import Dict, Optional
import pygame

class AudioManager:
    _instance: Optional["AudioManager"] = None
    _sounds: Dict[str, pygame.mixer.Sound] = {}
    _bgm_loaded: Optional[str] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_audio()
        return cls._instance

    def _init_audio(self) -> None:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception:
            pass

    def play_sfx(self, sfx_name: str, volume: float = 1.0) -> None:
        """Plays a sound effect if available in assets/audio/."""
        if not pygame.mixer.get_init():
            return

        if sfx_name not in self._sounds:
            audio_dir = os.path.join("assets", "audio")
            for ext in (".wav", ".ogg", ".mp3"):
                path = os.path.join(audio_dir, f"{sfx_name}{ext}")
                if os.path.exists(path):
                    try:
                        sound = pygame.mixer.Sound(path)
                        self._sounds[sfx_name] = sound
                        break
                    except Exception:
                        pass

        sound = self._sounds.get(sfx_name)
        if sound:
            sound.set_volume(volume)
            sound.play()

    def play_bgm(self, bgm_name: str, loop: bool = True, volume: float = 0.5) -> None:
        """Plays background music if available in assets/audio/."""
        if not pygame.mixer.get_init():
            return

        audio_dir = os.path.join("assets", "audio")
        for ext in (".ogg", ".mp3", ".wav"):
            path = os.path.join(audio_dir, f"{bgm_name}{ext}")
            if os.path.exists(path):
                try:
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.set_volume(volume)
                    pygame.mixer.music.play(-1 if loop else 0)
                    self._bgm_loaded = bgm_name
                    break
                except Exception:
                    pass

    def stop_bgm(self) -> None:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()


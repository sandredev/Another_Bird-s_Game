import pygame as pg

import pygame as pg

class Sounds:
    def __init__(self):
        pg.mixer.init()

        self.sfx = {}
        self.music = {}  # Ahora guardará Sound en vez de solo rutas

        self.sfx_volume = 0.7
        self.music_volume = 0.4

    def set_sfx(self, sfx_dict):
        """Recibe diccionario de efectos y los convierte a Sound."""
        self.sfx = {name: pg.mixer.Sound(path) for name, path in sfx_dict.items()}
        for snd in self.sfx.values():
            snd.set_volume(self.sfx_volume)

    def set_music(self, music_dict):
        """Recibe diccionario de canciones y las convierte a Sound para reproducir varias a la vez."""
        self.music = {name: pg.mixer.Sound(path) for name, path in music_dict.items()}
        for snd in self.music.values():
            snd.set_volume(self.music_volume)

    # ───────────────────────────────
    # Efectos y música
    # ───────────────────────────────
    def play_sfx(self, name, loops=0):
        """Reproduce un efecto de sonido."""
        if name in self.sfx:
            self.sfx[name].play(loops=loops)

    def play_music(self, name, loops=-1):
        """Reproduce música usando Sound, permitiendo varias al mismo tiempo."""
        if name in self.music:
            self.music[name].play(loops=loops)

    def stop_music(self, name=None):
        """Detiene una música específica o todas si name es None."""
        if name:
            if name in self.music:
                self.music[name].stop()
        else:
            for snd in self.music.values():
                snd.stop()



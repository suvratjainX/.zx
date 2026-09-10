import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

pygame.mixer.init()

_loaded = {}
_current = None

def load(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    sound = pygame.mixer.Sound(path)
    _loaded[path] = sound
    return sound

def play(path, loops=0):
    global _current

    if path not in _loaded:
        load(path)

    _current = _loaded[path]
    _current.play(loops=loops)

def stop():
    pygame.mixer.stop()

def pause():
    pygame.mixer.pause()

def resume():
    pygame.mixer.unpause()

def volume(value):
    pygame.mixer.music.set_volume(float(value))

def playing():
    return pygame.mixer.get_busy()

def wait():
    while pygame.mixer.get_busy():
        pygame.time.wait(100)
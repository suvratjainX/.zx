import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

pygame.mixer.init()

def play(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def stop():
    pygame.mixer.music.stop()

def pause():
    pygame.mixer.music.pause()

def resume():
    pygame.mixer.music.unpause()

def volume(v):
    pygame.mixer.music.set_volume(v)
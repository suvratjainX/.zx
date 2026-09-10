import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

cache = {}

def image(path):

    if path not in cache:

        cache[path] = pygame.image.load(
            path
        ).convert_alpha()

    return cache[path]
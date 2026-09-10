import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

def key(name):

    return pygame.key.get_pressed()[
        getattr(
            pygame,
            "K_" + name
        )
    ]
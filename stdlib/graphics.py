import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

from stdlib.window import get_screen

from engine.sprites import Sprite

def rect(
    x,
    y,
    w,
    h,
    color
):

    pygame.draw.rect(
        get_screen(),
        color,
        (x,y,w,h)
    )

def circle(
    x,
    y,
    r,
    color
):

    pygame.draw.circle(
        get_screen(),
        color,
        (x,y),
        r
    )

def text(
    msg,
    x,
    y,
    size=24,
    color=(255,255,255)
):

    font = pygame.font.SysFont(
        None,
        size
    )

    surf = font.render(
        msg,
        True,
        color
    )

    get_screen().blit(
        surf,
        (x,y)
    )

def sprite(
    file,
    x=0,
    y=0
):

    return Sprite(
        file,
        x,
        y
    )
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from stdlib.window import get_screen

_buttons = []
_labels = []

class Button:

    def __init__(
        self,
        text,
        x,
        y,
        width=200,
        height=50,
        color=(60,60,60),
        text_color=(255,255,255),
        callback=None
    ):

        self.text = text

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.color = color

        self.text_color = text_color

        self.callback = callback

        _buttons.append(self)

    def draw(self):

        screen = get_screen()

        pygame.draw.rect(
            screen,
            self.color,
            (
                self.x,
                self.y,
                self.width,
                self.height
            )
        )

        font = pygame.font.SysFont(
            None,
            28
        )

        text = font.render(
            self.text,
            True,
            self.text_color
        )

        screen.blit(
            text,
            (
                self.x + 10,
                self.y + 10
            )
        )

    def click(self):

        if self.callback:

            self.callback()

class Label:

    def __init__(
        self,
        text,
        x,
        y,
        size=24,
        color=(255,255,255)
    ):

        self.text = text

        self.x = x
        self.y = y

        self.size = size

        self.color = color

        _labels.append(self)

    def draw(self):

        screen = get_screen()

        font = pygame.font.SysFont(
            None,
            self.size
        )

        surf = font.render(
            self.text,
            True,
            self.color
        )

        screen.blit(
            surf,
            (
                self.x,
                self.y
            )
        )

def label(
    text,
    x,
    y,
    size=24,
    color=(255,255,255)
):

    return Label(
        text,
        x,
        y,
        size,
        color
    )

def button(
    text,
    x,
    y,
    width=200,
    height=50,
    callback=None
):

    return Button(
        text,
        x,
        y,
        width,
        height,
        callback=callback
    )

def draw():

    for lbl in _labels:

        lbl.draw()

    for btn in _buttons:

        btn.draw()

def handle_event(event):

    if event.type == pygame.MOUSEBUTTONDOWN:

        mx, my = pygame.mouse.get_pos()

        for btn in _buttons:

            if (
                btn.x <= mx <= btn.x + btn.width
                and
                btn.y <= my <= btn.y + btn.height
            ):

                btn.click()
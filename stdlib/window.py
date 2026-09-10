import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import ctypes

pygame.init()

# =========================
# ZX ROOT
# =========================

if getattr(sys, "frozen", False):

    ZX_ROOT = os.path.dirname(
        os.path.dirname(
            sys.executable
        )
    )

else:

    ZX_ROOT = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )

# =========================
# GLOBALS
# =========================

screen = None

clock = pygame.time.Clock()

fps = 60

background_color = (20, 20, 20)

window_width = 1280

window_height = 720

window_title = ""

ZX_VERSION = ""

# =========================
# WINDOW CREATION
# =========================

def create(
    title="ZX Window",
    width=1280,
    height=720,
    icon=None,
    resizable=False,
    fullscreen=False,
    target_fps=60
):

    global screen
    global fps
    global window_width
    global window_height
    global window_title

    fps = target_fps

    window_width = width
    window_height = height
    window_title = title

    flags = 0

    if resizable:
        flags |= pygame.RESIZABLE

    if fullscreen:
        flags |= pygame.FULLSCREEN

    screen = pygame.display.set_mode(
        (width, height),
        flags
    )

    pygame.display.set_caption(
        f"{title}"
    )

    # -------------------------
    # Windows App ID
    # -------------------------

    try:

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "ZX.Language.Engine.5"
        )

    except:
        pass

    # -------------------------
    # Default ZX Icon
    # -------------------------

    try:

        default_icon = os.path.join(
            ZX_ROOT,
            "assets",
            "zx.png"
        )

        if os.path.isfile(default_icon):

            icon_surface = pygame.image.load(
                default_icon
            ).convert_alpha()

            icon_surface = pygame.transform.smoothscale(
                icon_surface,
                (64, 64)
            )

            pygame.display.set_icon(
                icon_surface
            )

    except Exception as e:

        print(
            "ZX icon error:",
            e
        )

    # -------------------------
    # User Override Icon
    # -------------------------

    if icon:

        try:

            custom_icon = pygame.image.load(
                icon
            ).convert_alpha()

            custom_icon = pygame.transform.smoothscale(
                custom_icon,
                (64, 64)
            )

            pygame.display.set_icon(
                custom_icon
            )

            print(
                "Custom icon loaded"
            )

        except Exception as e:

            print(
                "Custom icon error:",
                e
            )

# =========================
# SCREEN
# =========================

def get_screen():

    return screen

# =========================
# BACKGROUND
# =========================

def set_background(color):

    global background_color

    background_color = color

def get_background():

    return background_color

# =========================
# FPS
# =========================

def set_fps(value):

    global fps

    fps = value

def get_fps():

    return fps

# =========================
# WINDOW INFO
# =========================

def width():

    return window_width

def height():

    return window_height

def size():

    return (
        window_width,
        window_height
    )

# =========================
# INPUT
# =========================

def key(name):

    try:

        return pygame.key.get_pressed()[
            getattr(
                pygame,
                "K_" + name.lower()
            )
        ]

    except:

        return False

def mouse_pos():

    return pygame.mouse.get_pos()

def mouse_x():

    return pygame.mouse.get_pos()[0]

def mouse_y():

    return pygame.mouse.get_pos()[1]

def mouse_pressed():

    return pygame.mouse.get_pressed()[0]

def mouse_right():

    return pygame.mouse.get_pressed()[2]

# =========================
# EVENTS
# =========================

def events():

    return pygame.event.get()

# =========================
# WINDOW CONTROL
# =========================

def title(text):

    pygame.display.set_caption(text)

def toggle_fullscreen():

    try:

        pygame.display.toggle_fullscreen()

    except:

        pass

# =========================
# CLEAR SCREEN
# =========================

def clear():

    if screen:

        screen.fill(
            background_color
        )

# =========================
# UPDATE
# =========================

def update():

    pygame.display.flip()

# =========================
# GUI SUPPORT
# =========================

def _handle_gui(event):

    try:

        import stdlib.gui as gui

        gui.handle_event(event)

    except:
        pass

def _draw_gui():

    try:

        import stdlib.gui as gui

        gui.draw()

    except:
        pass

# =========================
# MAIN LOOP
# =========================

def run(update_func=None):

    running = True

    while running:

        for event in pygame.event.get():

            _handle_gui(event)

            if event.type == pygame.QUIT:

                running = False

        if screen:

            screen.fill(
                background_color
            )

        if update_func:

            update_func()

        _draw_gui()

        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()

# =========================
# ZX SHORTCUTS
# =========================

def quit():

    pygame.quit()

    raise SystemExit
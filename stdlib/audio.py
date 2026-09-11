print("audio.py loading...")
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import threading
import time
import random
from threading import Lock
from pathlib import Path

DEBUG = False

try:
    config = Path("C:/ZX/audio_debug.txt").read_text().lower()
    DEBUG = "debug=true" in config
except:
    pass

# ==================================================
# INIT
# ==================================================

pygame.mixer.init()
pygame.mixer.set_num_channels(64)

_music_state = "stopped"  # playing paused stopped
_queue_lock = Lock()
_current_music = None
_music_queue = []
_loop = False
_paused = False
print("_paused created")
_music_volume = 1.0
_sound_volume = 1.0
_sound_cache = {}

# ==================================================
# INTERNAL
# ==================================================

def _clamp(value):
    return max(0.0, min(1.0, float(value)))

# ==================================================
# MUSIC
# ==================================================

def music(file, loops=0):
    global _current_music
    global _music_state

    if DEBUG:
        print("=== MUSIC ===")
        print("File:", file)
        print("Loops:", loops)

    if not os.path.exists(file):
        raise FileNotFoundError(file)

    pygame.mixer.music.load(file)

    if DEBUG:
        print("Loaded")

    pygame.mixer.music.set_volume(_music_volume)

    pygame.mixer.music.play(loops=loops)

    if DEBUG:
        print("Busy after play:", pygame.mixer.music.get_busy())

    _current_music = file
    _music_state = "playing"

    if DEBUG:
        print("State:", _music_state)
        print("================")

    return True


def play(file):
    return music(file)


def stop():
    global _music_state

    pygame.mixer.music.stop()
    _music_state = "stopped"


def pause():
    global _music_state

    if DEBUG:
        print("=== PAUSE ===")
        print("Busy:", pygame.mixer.music.get_busy())
        print("State before:", _music_state)

    pygame.mixer.music.pause()
    _music_state = "paused"

    if DEBUG:
        print("State after:", _music_state)
        print("================")


def resume():
    global _music_state

    if DEBUG:
        print("=== RESUME ===")
        print("Busy before:", pygame.mixer.music.get_busy())
        print("State before:", _music_state)

    pygame.mixer.music.unpause()
    _music_state = "playing"

    if DEBUG:
        print("Busy after:", pygame.mixer.music.get_busy())
        print("State after:", _music_state)
        print("================")


def toggle_pause():
    if paused():
        resume()
    else:
        pause()


def restart():
    if _current_music:
        music(
            _current_music,
            -1 if _loop else 0
        )


def seek(seconds):
    if not _current_music:
        return

    pygame.mixer.music.load(_current_music)

    pygame.mixer.music.play(
        loops=-1 if _loop else 0,
        start=float(seconds)
    )

    global _music_state
    _music_state = "playing"


def playing():
    return _music_state == "playing"


def paused():
    return _music_state == "paused"


def stopped():
    return _music_state == "stopped"


def current():
    return _current_music


def busy():
    return pygame.mixer.music.get_busy()


def position():
    pos = pygame.mixer.music.get_pos()

    if pos < 0:
        return 0

    return pos / 1000.0


def fadeout(ms=1000):
    pygame.mixer.music.fadeout(int(ms))
    return True

# ==================================================
# VOLUME
# ==================================================

def volume(value):
    global _music_volume
    global _sound_volume

    value = _clamp(value)

    _music_volume = value
    _sound_volume = value

    pygame.mixer.music.set_volume(value)

    return value


def music_volume(value=None):
    global _music_volume

    if value is None:
        return _music_volume

    _music_volume = _clamp(value)
    pygame.mixer.music.set_volume(_music_volume)

    return _music_volume


def sound_volume(value=None):
    global _sound_volume

    if value is None:
        return _sound_volume

    _sound_volume = _clamp(value)

    return _sound_volume


def mute():
    pygame.mixer.music.set_volume(0)


def unmute():
    pygame.mixer.music.set_volume(_music_volume)

# ==================================================
# LOOPING
# ==================================================

def loop(enabled=True):
    global _loop

    _loop = bool(enabled)

    if _current_music and playing():
        restart()

    return _loop

# ==================================================
# SOUND EFFECTS
# ==================================================

def sound(file):
    if not os.path.exists(file):
        raise FileNotFoundError(file)

    if file not in _sound_cache:
        _sound_cache[file] = pygame.mixer.Sound(file)

    snd = _sound_cache[file]

    snd.set_volume(_sound_volume)
    snd.play()

    return snd


def stop_sounds():
    pygame.mixer.stop()


def preload(file):
    if not os.path.exists(file):
        raise FileNotFoundError(file)

    if file not in _sound_cache:
        _sound_cache[file] = pygame.mixer.Sound(file)

    return True


def unload(file):
    if file in _sound_cache:
        del _sound_cache[file]


def clear_cache():
    _sound_cache.clear()

# ==================================================
# FILE INFO
# ==================================================

def length(file):
    if not os.path.exists(file):
        raise FileNotFoundError(file)

    snd = pygame.mixer.Sound(file)

    return snd.get_length()

# ==================================================
# QUEUE
# ==================================================

def queue(file):
    if not os.path.exists(file):
        raise FileNotFoundError(file)

    with _queue_lock:
        _music_queue.append(file)


def clear_queue():
    with _queue_lock:
        _music_queue.clear()


def queue_list():
    with _queue_lock:
        return list(_music_queue)


def queue_size():
    with _queue_lock:
        return len(_music_queue)


def shuffle_queue():
    with _queue_lock:
        random.shuffle(_music_queue)


def skip():
    with _queue_lock:

        if _music_queue:
            nxt = _music_queue.pop(0)
            music(nxt)
        else:
            stop()

# ==================================================
# ADVANCED
# ==================================================

def crossfade(file, ms=1000):
    fadeout(ms)

    time.sleep(ms / 1000)

    music(file)


def pause_all():
    pause()
    pygame.mixer.pause()


def resume_all():
    resume()
    pygame.mixer.unpause()

# ==================================================
# CHANNELS
# ==================================================

def channels():
    return pygame.mixer.get_num_channels()


def set_channels(count):
    pygame.mixer.set_num_channels(int(count))


def initialized():
    return pygame.mixer.get_init() is not None

# ==================================================
# QUEUE THREAD
# ==================================================

def _queue_worker():
    global _music_state

    while True:

        if (
            _music_state == "playing"
            and not pygame.mixer.music.get_busy()
        ):
            _music_state = "stopped"

        if (
            _music_state == "stopped"
            and not _loop
        ):
            with _queue_lock:

                if _music_queue:
                    try:
                        nxt = _music_queue.pop(0)
                        music(nxt)

                    except Exception:
                        pass

        time.sleep(0.1)

threading.Thread(
    target=_queue_worker,
    daemon=True
).start()

# ==================================================
# WEBVIEW BRIDGE
# ==================================================

def js_play(file):
    music(file)


def js_pause():
    pause()


def js_resume():
    resume()


def js_stop():
    stop()

# ==================================================
# INFO
# ==================================================

def info():
    return {
        "current": _current_music,
        "state": _music_state,
        "queue": queue_size(),
        "loop": _loop,
        "music_volume": _music_volume,
        "sound_volume": _sound_volume
    }
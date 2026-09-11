import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import threading
import time

# ==========================================
# INIT
# ==========================================

pygame.mixer.init()

_current_music = None
_music_queue = []
_loop = False
_paused = False

_music_volume = 1.0
_sound_volume = 1.0

_sound_cache = {}

# ==========================================
# INTERNAL
# ==========================================

def _clamp(value):
    return max(0.0, min(1.0, float(value)))

# ==========================================
# MUSIC
# ==========================================

def music(file, loops=0):
    global _current_music
    global _paused

    if not os.path.exists(file):
        raise FileNotFoundError(file)

    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(_music_volume)
    pygame.mixer.music.play(loops=loops)

    _current_music = file
    _paused = False

    return True


def stop():
    global _paused

    pygame.mixer.music.stop()
    _paused = False


_paused = False

def pause():
    global _paused

    pygame.mixer.music.pause()
    _paused = True


def resume():
    global _paused

    pygame.mixer.music.unpause()
    _paused = False


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


def playing():
    return pygame.mixer.music.get_busy()


def paused():
    return _paused


def busy():
    return pygame.mixer.music.get_busy()


def current():
    return _current_music


def position():
    pos = pygame.mixer.music.get_pos()

    if pos < 0:
        return 0

    return pos / 1000.0


def fadeout(ms=1000):
    pygame.mixer.music.fadeout(int(ms))


# ==========================================
# VOLUME
# ==========================================

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


# ==========================================
# LOOPING
# ==========================================

def loop(enabled=True):
    global _loop

    _loop = bool(enabled)

    if _current_music:
        restart()


# ==========================================
# SOUND EFFECTS
# ==========================================

def sound(file):
    if not os.path.exists(file):
        raise FileNotFoundError(file)

    if file not in _sound_cache:
        _sound_cache[file] = pygame.mixer.Sound(file)

    s = _sound_cache[file]

    s.set_volume(_sound_volume)
    s.play()

    return s


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


# ==========================================
# QUEUE
# ==========================================

def queue(file):
    if not os.path.exists(file):
        raise FileNotFoundError(file)

    _music_queue.append(file)


def clear_queue():
    _music_queue.clear()


def queue_list():
    return list(_music_queue)


def queue_size():
    return len(_music_queue)


def skip():
    if _music_queue:
        nxt = _music_queue.pop(0)
        music(
            nxt,
            -1 if _loop else 0
        )
    else:
        stop()


# ==========================================
# FILE INFO
# ==========================================

def length(file):
    if not os.path.exists(file):
        raise FileNotFoundError(file)

    snd = pygame.mixer.Sound(file)
    return snd.get_length()


# ==========================================
# QUEUE THREAD
# ==========================================

def _queue_worker():
    while True:

        if (
            not _loop
            and not _paused
            and not pygame.mixer.music.get_busy()
            and _music_queue
        ):
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

# ==========================================
# WEBVIEW HELPERS
# ==========================================

def js_play(file):
    music(file)

def js_pause():
    pause()

def js_resume():
    resume()

def js_stop():
    stop()

# ==========================================
# EXTRA HELPERS
# ==========================================

def channels():
    return pygame.mixer.get_num_channels()


def set_channels(count):
    pygame.mixer.set_num_channels(int(count))


def initialized():
    return pygame.mixer.get_init() is not None
from core.parser import translate

from pathlib import Path

DEBUG = False

try:
    config = Path("C:/ZX/debug.txt").read_text()

    if "debug_mode=true" in config.lower():
        DEBUG = True

except:
    pass

# Built-in ZX modules
import stdlib.window as window
import stdlib.graphics as graphics
import stdlib.audio as audio
import stdlib.files as files
import stdlib.internet as internet
import stdlib.webapp as webapp

# Existing modules
import stdlib.sound as sound
import stdlib.gui as gui
import stdlib.fs as fs
import stdlib.mathx as mathx
import stdlib.network as network


def zx_input(prompt=""):
    value = input(prompt)

    try:
        return int(value)
    except:
        pass

    try:
        return float(value)
    except:
        pass

    return value


def end():
    raise SystemExit


def run(code):
    py_code = translate(code)

    env = {
        "__builtins__": __builtins__,

        # ZX Builtins
        "say": print,
        "input": zx_input,
        "end": end,

        # Python Basics
        "range": range,
        "len": len,
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        "list": list,
        "dict": dict,
        "tuple": tuple,
        "set": set,
        "enumerate": enumerate,
        "zip": zip,
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,

        # ZX Modules
        "window": window,
        "graphics": graphics,
        "audio": audio,
        "files": files,
        "internet": internet,
        "webapp": webapp,
        # Legacy Modules
        "sound": sound,
        "gui": gui,
        "fs": fs,
        "mathx": mathx,
        "network": network,
    }

    if DEBUG:
        print("=== ZX ENV ===")
        print(sorted(env.keys()))
        print()
        print("=== GENERATED PYTHON ===")
        print(py_code)
        print("========================")

    exec(py_code, env)
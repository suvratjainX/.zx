import stdlib.audio
import stdlib.files
import stdlib.fs
import stdlib.graphics
import stdlib.gui
import stdlib.internet
import stdlib.mathx
import stdlib.network
import stdlib.sound
import stdlib.webapp
import stdlib.window

from core.parser import translate

from pathlib import Path
import sys
import traceback
import time
import random
import json

# ==========================================
# DEBUG CONFIG
# ==========================================

DEBUG = False

try:
    config = Path("C:/ZX/debug.txt").read_text(
        encoding="utf-8"
    )

    if "debug_mode=true" in config.lower():
        DEBUG = True

except:
    pass

# ==========================================
# PYINSTALLER SUPPORT
# ==========================================

if getattr(sys, "frozen", False):
    ZX_ROOT = Path(sys._MEIPASS)
else:
    ZX_ROOT = Path(__file__).resolve().parent.parent

if str(ZX_ROOT) not in sys.path:
    sys.path.insert(0, str(ZX_ROOT))

# ==========================================
# INPUT
# ==========================================

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

# ==========================================
# END PROGRAM
# ==========================================

def end():
    raise SystemExit

# ==========================================
# ZX EXECUTION
# ==========================================

def run(code):

    py_code = translate(code)

    env = {
        "__builtins__": __builtins__,

        # ZX builtins
        "say": print,
        "input": zx_input,
        "end": end,

        # Python helpers
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

        "sorted": sorted,
        "reversed": reversed,

        "type": type,
        "isinstance": isinstance,

        "print": print,

        # useful modules
        "time": time,
        "random": random,
        "json": json,
    }

    if DEBUG:

        print("\n=== ZX ROOT ===")
        print(ZX_ROOT)

        print("\n=== SYS PATH ===")
        for p in sys.path:
            print(p)

        print("\n=== GENERATED PYTHON ===")
        print(py_code)

        print("\n========================\n")

    try:
        exec(py_code, env)

    except SystemExit:
        raise

    except KeyboardInterrupt:
        print("\nProgram interrupted.")

    except Exception as e:

        if DEBUG:
            print("\n=== TRACEBACK ===")
            traceback.print_exc()
        else:
            print(f"Runtime error: {e}")
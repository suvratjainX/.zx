from core.parser import translate
from pathlib import Path
import sys
import os

DEBUG = False

try:
    config = Path("C:/ZX/debug.txt").read_text()
    if "debug_mode=true" in config.lower():
        DEBUG = True
except:
    pass


# Make ZX root importable
ZX_ROOT = Path(__file__).resolve().parent.parent

if str(ZX_ROOT) not in sys.path:
    sys.path.insert(0, str(ZX_ROOT))


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
    }

    if DEBUG:
        print("=== ZX ENV ===")
        print(sorted(env.keys()))
        print()

        print("=== GENERATED PYTHON ===")
        print(py_code)
        print()

        print("========================")

    try:
        import sys
        print(sys.path)
        exec(py_code, env)
    except Exception as e:
        print(f"Runtime error: {e}")
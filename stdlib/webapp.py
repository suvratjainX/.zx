import os

# Must be before importing webview
os.environ["PYWEBVIEW_GUI"] = "edgechromium"

import webview
import importlib.util

from core.parser import translate

_windows = []
_main_window = None


class ZXBridge:
    pass


def _load_backend(backend_file):
    bridge = ZXBridge()

    if not backend_file:
        return bridge

    if not os.path.exists(backend_file):
        raise FileNotFoundError(
            f"Backend not found: {backend_file}"
        )

    ext = os.path.splitext(
        backend_file
    )[1].lower()

    # Python backend
    if ext == ".py":
        spec = importlib.util.spec_from_file_location(
            "zx_backend",
            backend_file
        )

        mod = importlib.util.module_from_spec(
            spec
        )

        spec.loader.exec_module(mod)

        for name in dir(mod):
            obj = getattr(mod, name)

            if callable(obj) and not name.startswith("_"):
                setattr(
                    bridge,
                    name,
                    obj
                )

    # ZX backend
    elif ext == ".zx":

        with open(
            backend_file,
            encoding="utf-8"
        ) as f:

            zx_code = f.read()

        py_code = translate(zx_code)

        env = {}

        exec(py_code, env)

        for name, obj in env.items():

            if callable(obj) and not name.startswith("_"):

                setattr(
                    bridge,
                    name,
                    obj
                )

    else:
        raise ValueError(
            f"Unsupported backend type: {ext}"
        )

    return bridge


def _fix_html_path(path):

    if not path:
        return None

    if path.startswith(
        ("http://", "https://")
    ):
        return path

    return os.path.abspath(path)


def create_window(
    html_file=None,
    backend_file=None,
    title="ZX App",
    width=1200,
    height=800,
    resizable=True
):

    global _main_window

    bridge = _load_backend(
        backend_file
    )

    html_file = _fix_html_path(
        html_file
    )

    window = webview.create_window(
        title=title,
        url=html_file,
        js_api=bridge,
        width=width,
        height=height,
        resizable=resizable
    )

    if _main_window is None:
        _main_window = window

    _windows.append(window)

    return window


def open_url(
    url,
    title="ZX App",
    width=1200,
    height=800
):

    global _main_window

    window = webview.create_window(
        title=title,
        url=url,
        width=width,
        height=height
    )

    if _main_window is None:
        _main_window = window

    _windows.append(window)

    return window


def run(
    html_file,
    backend_file=None,
    title="ZX App",
    width=1200,
    height=800
):

    create_window(
        html_file=html_file,
        backend_file=backend_file,
        title=title,
        width=width,
        height=height
    )

    webview.start()


def start():
    webview.start()


def active_window():
    return _main_window


def windows():
    return _windows


def set_title(title):

    if _main_window:
        _main_window.set_title(
            title
        )


def evaluate_js(code):

    if _main_window:
        return _main_window.evaluate_js(
            code
        )


def load_url(url):

    if _main_window:
        _main_window.load_url(
            url
        )


def load_html(html):

    if _main_window:
        _main_window.load_html(
            html
        )


def resize(
    width,
    height
):

    if _main_window:
        _main_window.resize(
            width,
            height
        )


def fullscreen():

    if _main_window:
        _main_window.toggle_fullscreen()


def destroy():

    if _main_window:
        _main_window.destroy()


def exists():
    return _main_window is not None


def width():

    if _main_window:
        return _main_window.width


def height():

    if _main_window:
        return _main_window.height
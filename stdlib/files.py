from pathlib import Path

def read(path):
    return Path(path).read_text(
        encoding="utf-8"
    )

def write(path,text):
    Path(path).write_text(
        text,
        encoding="utf-8"
    )

def exists(path):
    return Path(path).exists()

def delete(path):
    Path(path).unlink()

def list(path="."):
    return [x.name for x in Path(path).iterdir()]
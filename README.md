# ZX Programming Language

ZX is a beginner-friendly programming language built on top of Python. It provides a simpler syntax while still allowing access to Python modules and custom libraries.

---

# Features

- Simple syntax
- Fast execution
- Built-in modules
- Window creation
- Graphics and audio support
- File system access
- Networking support
- Web applications using HTML + ZX backend
- Compiles into a standalone executable

---

# Installation

## 1. Install Python

Download Python from:

https://www.python.org/downloads/

Recommended:

- Python 3.13.x

Verify installation:

```bash
python --version
```

Example output:

```text
Python 3.13.7
```

---

## 2. Clone ZX

```bash
git clone https://github.com/suvratjainX/.zx.git
cd .zx
```

---

## 3. Install Dependencies

```bash
Coming Soon
```

Or manually:

```bash
pip install pygame pywebview requests
```

---

# Running ZX Files

ZX source files use the `.zx` extension.

Example:

```zx
say("Hello World")
```

Save as:

```text
hello.zx
```

Run:

```bash
zx hello.zx
```

Output:

```text
Hello World
```

---

# Adding ZX To PATH

Adding ZX to PATH allows you to run:

```bash
zx program.zx
```

from any folder.

Windows searches folders listed in the PATH environment variable for executables.

## Method 1 (Recommended)

Create:

```text
C:\ZX
```

Place inside:

```text
Contents of .zx
```

Then:

1. Open Start Menu
2. Search:

```text
Environment Variables
```

3. Open:

```text
Edit the system environment variables
```

4. Click:

```text
Environment Variables
```

5. Select:

```text
Path
```

6. Click:

```text
Edit
```

7. Click:

```text
New
```

8. Add:

```text
C:\ZX
```

9. Save everything
10. Open a new terminal

Windows will now find `zx.exe` automatically.

Verify:

```bash
Coming Soon
```

or

```bash
where zx
```

---

# Project Structure

```text
ZX/
│
├── zx.py
├── dist/
│   └── zx.exe
│
├── core/
│   ├── parser.py
│   ├── runtime.py
│   └── ...
│
├── stdlib/
│   ├── window.py
│   ├── graphics.py
│   ├── audio.py
│   ├── files.py
│   ├── internet.py
│   ├── webapp.py
│   └── ...
│
├── examples/
│   └── Coming Soon
│
└── ...
```

---

# Basic Syntax

## Variables

```zx
name = "Alex"
age = 16
```

## Output

```zx
say("Hello")
```

## Input

```zx
name = input("Name: ")
```

## Functions

```zx
func greet(name):
    say("Hello " + name)

greet("Alex")
```

## Loops

```zx
repeat 5:
    say("ZX")
```

```zx
forever:
    say("Running")
```

## Conditions

```zx
if age > 18:
    say("Adult")
```

---

# Importing Modules

```zx
import audio
import graphics
import webapp
```

With alias:

```zx
import graphics as gfx
```

---

# Creating Desktop Windows

```zx
import window

window.create(
    title="ZX Window",
    width=800,
    height=600
)
```

---

# HTML + ZX Applications

Directory:

```text
project/
├── main.zx
├── index.html
└── backend.py
```

Example:

```zx
import webapp

webapp.run(
    "index.html",
    "backend.py"
)
```

---

# Backend Example

```python
def chat(message):
    return "You said: " + message
```

---

# HTML Example

```html
<input id="msg">
<button onclick="send()">Send</button>

<script>
async function send() {
    const text =
        document.getElementById("msg").value;

    const result =
        await pywebview.api.chat(text);

    alert(result);
}
</script>
```

---

# Building ZX Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile zx.py
```

Output:

```text
dist/zx.exe
```

Custom icon:

```cmd
pyinstaller --onefile ^
    --icon assets/zx.ico ^
    zx.py
```

Git Bash:

```bash
pyinstaller --onefile \
    --icon assets/zx.ico \
    zx.py
```

---

# Debug Mode

Create:

```text
C:\ZX\debug.txt
```

Contents:

```text
debug_mode=true
```

ZX will print:

- Generated Python
- Runtime environment
- Loaded modules

---

# Example Program

```zx
func greet(name):
    say("Hello " + name)

name = input("Name: ")

greet(name)
```

---

# License

MIT License

---

# Created With

- Python
- PyGame
- PyWebView

ZX is designed to make desktop app development and scripting easier while keeping the power of Python underneath.
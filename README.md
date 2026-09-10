# Build Cmd

```rm -rf build dist *.spec

pyinstaller --onefile \
  --collect-submodules stdlib \
  --hidden-import stdlib.webapp \
  zx.py```# .zx

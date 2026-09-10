import sys
import os
print(os.getcwd())

from core.runtime import run

VERSION = "ZX Language v5"


def print_help():
    print(VERSION)
    print()
    print("Usage:")
    print("  zx file.zx")
    print()
    print("Examples:")
    print("  zx main.zx")
    print("  zx projects/hello.zx")


def main():

    if len(sys.argv) < 2:
        print_help()
        return 0

    arg = sys.argv[1]

    if arg in ("--help", "-h"):
        print_help()
        return 0

    if arg in ("--version", "-v"):
        print(VERSION)
        return 0

    file_path = os.path.abspath(arg)

    if not os.path.isfile(file_path):
        print(f"File not found: {arg}")
        return 1

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        run(source)
        return 0

    except KeyboardInterrupt:
        print("\nExecution cancelled.")
        return 130

    except Exception as e:
        print(f"Runtime error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
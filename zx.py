import sys
from core.runtime import run

def main():

    if len(sys.argv) < 2:

        print("ZX Language v5")
        print()
        print("Usage:")
        print("  zx file.zx")
        return

    file = sys.argv[1]

    try:

        with open(file, encoding="utf-8") as f:

            run(f.read())

    except FileNotFoundError:

        print(f"File not found: {file}")

if __name__ == "__main__":
    main()
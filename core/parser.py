import re


def translate(code):
    lines = []

    for line in code.splitlines():

        stripped = line.strip()

        # --------------------------------
        # import audio
        # import audio as music
        # --------------------------------

        m = re.match(
            r"^import\s+(\w+)(?:\s+as\s+(\w+))?$",
            stripped
        )

        if m:
            module, alias = m.groups()

            if alias is None:
                alias = module

            line = (
                f'{alias} = __import__('
                f'"stdlib.{module}", '
                f'fromlist=["*"])'
            )

            lines.append(line)
            continue

        # --------------------------------
        # func
        # --------------------------------

        if stripped.startswith("func "):
            line = line.replace(
                "func ",
                "def ",
                1
            )

        # --------------------------------
        # forever
        # --------------------------------

        elif stripped == "forever:":

            indent = line[:len(line) - len(line.lstrip())]

            line = f"{indent}while True:"

        # --------------------------------
        # repeat
        # --------------------------------

        elif stripped.startswith("repeat "):

            amount = stripped[7:-1]

            indent = line[:len(line) - len(line.lstrip())]

            line = (
                f"{indent}"
                f"for _ in range({amount}):"
            )

        # --------------------------------
        # end
        # --------------------------------

        elif stripped == "end":

            indent = line[:len(line) - len(line.lstrip())]

            line = indent + "end()"

        # --------------------------------
        # contains any
        # --------------------------------

        m = re.match(
            r"^(\s*)(if|elif)\s+(.+?)\s+contains\s+any\s+(.+):$",
            line
        )

        if m:

            indent, keyword, left, right = m.groups()

            line = (
                f"{indent}{keyword} "
                f"any(word in {left} "
                f"for word in {right}):"
            )

        else:

            # ----------------------------
            # contains
            # ----------------------------

            m = re.match(
                r"^(\s*)(if|elif)\s+(.+?)\s+contains\s+(.+):$",
                line
            )

            if m:

                indent, keyword, left, right = m.groups()

                line = (
                    f"{indent}{keyword} "
                    f"{right} in {left}:"
                )

        # --------------------------------
        # say()
        # --------------------------------

        line = line.replace(
            "say(",
            "print("
        )

        lines.append(line)

    return "\n".join(lines)
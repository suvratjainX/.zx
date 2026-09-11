import re


def translate(code):
    lines = []

    for line in code.splitlines():
        stripped = line.strip()

        # =================================
        # import audio
        # import audio as music
        # =================================

        m = re.match(
            r'^import\s+(\w+)(?:\s+as\s+(\w+))?$',
            stripped
        )

        if m:
            module, alias = m.groups()

            if alias is None:
                alias = module

            lines.append(
                f"{alias} = __import__('stdlib.{module}', fromlist=['*'])"
            )
            continue

        # =================================
        # python import passthrough
        # from x import y
        # import os
        # =================================

        if stripped.startswith('from '):
            lines.append(line)
            continue

        if (
            stripped.startswith('import ')
            and ' as ' not in stripped
        ):
            parts = stripped.split()

            if len(parts) == 2:
                module = parts[1]

                if module not in (
                    'audio',
                    'files',
                    'fs',
                    'graphics',
                    'gui',
                    'internet',
                    'mathx',
                    'network',
                    'sound',
                    'webapp',
                    'window'
                ):
                    lines.append(line)
                    continue

        # =================================
        # func
        # =================================

        if stripped.startswith('func '):
            line = line.replace(
                'func ',
                'def ',
                1
            )

        # =================================
        # forever
        # =================================

        elif stripped == 'forever:':
            indent = line[:len(line) - len(line.lstrip())]
            line = f'{indent}while True:'

        # =================================
        # repeat
        # =================================

        elif stripped.startswith('repeat ') and stripped.endswith(':'):
            amount = stripped[7:-1]

            indent = line[:len(line) - len(line.lstrip())]

            line = (
                f'{indent}'
                f'for _ in range({amount}):'
            )

        # =================================
        # end
        # =================================

        elif stripped == 'end':
            indent = line[:len(line) - len(line.lstrip())]
            line = indent + 'end()'

        # =================================
        # contains any
        # =================================

        m = re.match(
            r'^(\s*)(if|elif)\s+(.+?)\s+contains\s+any\s+(.+):$',
            line
        )

        if m:
            indent, keyword, left, right = m.groups()

            line = (
                f'{indent}{keyword} '
                f'any(word in {left} for word in {right}):'
            )

        else:

            # =================================
            # contains with AND support
            # query contains "play" and "gospel"
            # =>
            # "play" in query and "gospel" in query
            # =================================

            m = re.match(
                r'^(\s*)(if|elif)\s+(.+?)\s+contains\s+(.+):$',
                line
            )

            if m:
                indent, keyword, left, right = m.groups()

                parts = [
                    p.strip()
                    for p in re.split(
                        r'\s+and\s+',
                        right
                    )
                ]

                condition = ' and '.join(
                    f'{part} in {left}'
                    for part in parts
                )

                line = (
                    f'{indent}'
                    f'{keyword} '
                    f'{condition}:'
                )

        # =================================
        # say()
        # =================================

        line = line.replace(
            'say(',
            'print('
        )

        lines.append(line)

    return '\n'.join(lines)
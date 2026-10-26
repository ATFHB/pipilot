
from pathlib import Path
import re

SOURCE = Path("documentation/documentation/asciidoc")
OUTPUT = Path("data/processed")

OUTPUT.mkdir(parents=True, exist_ok=True)

extensions = {".adoc", ".asciidoc", ".md"}

include_pattern = re.compile(
    r"^\s*include::([^\[]+)\[.*\]\s*$"
)


def expand_file(file_path, stack=None):
    if stack is None:
        stack = []

    file_path = file_path.resolve()

    if file_path in stack:
        return "\n[Include cycle detected]\n"

    if not file_path.is_file():
        return f"\n[Include file not found: {file_path.name}]\n"

    stack = stack + [file_path]
    output_lines = []

    text = file_path.read_text(encoding="utf-8", errors="replace")

    for line in text.splitlines():
        match = include_pattern.match(line)

        if not match:
            output_lines.append(line)
            continue

        include_name = match.group(1).strip()
        include_path = (file_path.parent / include_name).resolve()

        if not include_path.is_file():
            include_path = (SOURCE / include_name).resolve()

        if include_path.is_file():
            included_text = expand_file(include_path, stack)
            output_lines.append(included_text)
        else:
            output_lines.append(
                f"[Include file not found: {include_name}]"
            )

    return "\n".join(output_lines)


count = 0

for source_file in SOURCE.rglob("*"):
    if not source_file.is_file():
        continue

    if source_file.suffix.lower() not in extensions:
        continue

    relative_path = source_file.relative_to(SOURCE)
    output_file = OUTPUT / relative_path

    output_file.parent.mkdir(parents=True, exist_ok=True)

    full_content = expand_file(source_file)
    output_file.write_text(full_content, encoding="utf-8")

    count += 1

print(f"Processed files: {count}")
print(f"Output folder: {OUTPUT}")

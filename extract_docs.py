
from pathlib import Path
import shutil
import hashlib
import csv

SOURCE = Path("documentation/documentation/asciidoc")
RAW = Path("data/raw")
SAMPLE = Path("data/sample")

RAW.mkdir(parents=True, exist_ok=True)
SAMPLE.mkdir(parents=True, exist_ok=True)

extensions = {".adoc", ".asciidoc", ".md"}

files = [
    p for p in SOURCE.rglob("*")
    if p.is_file() and p.suffix.lower() in extensions
]

manifest_rows = []

for source_file in files:
    relative_path = source_file.relative_to(SOURCE)
    destination = RAW / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source_file, destination)

    content = source_file.read_bytes()
    digest = hashlib.sha256(content).hexdigest()

    manifest_rows.append([
        str(relative_path),
        str(source_file),
        len(content),
        digest
    ])

manifest = Path("data/manifest.csv")

with manifest.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["file", "source_path", "bytes", "sha256"])
    writer.writerows(manifest_rows)

for source_file in files[:3]:
    relative_path = source_file.relative_to(SOURCE)
    destination = SAMPLE / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, destination)

print(f"Found {len(files)} documentation files.")
print(f"Copied files to: {RAW}")
print(f"Manifest created: {manifest}")
print(f"Sample files copied: {min(3, len(files))}")

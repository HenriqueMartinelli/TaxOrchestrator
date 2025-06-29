import uuid
from pathlib import Path

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def unique_filename(filename: str) -> str:
    return f"{uuid.uuid4()}_{filename}"

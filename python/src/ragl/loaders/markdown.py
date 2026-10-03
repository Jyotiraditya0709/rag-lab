from pathlib import Path

from ragl.models import Document


def load_markdown(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")

    return Document(
        source=str(path),
        text=text,
        title=path.stem,
    )

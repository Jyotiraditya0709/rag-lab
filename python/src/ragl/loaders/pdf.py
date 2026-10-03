from pathlib import Path

from pypdf import PdfReader

from ragl.models import Document


def load_pdf(path: Path) -> Document:
    reader = PdfReader(path)
    text = "\n\n".join(page.extract_text() or "" for page in reader.pages)

    return Document(
        source=str(path),
        text=text,
        title=path.stem,
    )

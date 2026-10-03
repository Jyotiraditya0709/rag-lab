from pathlib import Path

from pypdf import PdfWriter

from ragl.loaders.pdf import load_pdf


def test_load_pdf(tmp_path: Path) -> None:
    path = tmp_path / "example.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    with path.open("wb") as file:
        writer.write(file)

    document = load_pdf(path)

    assert document.source == str(path)
    assert document.title == "example"

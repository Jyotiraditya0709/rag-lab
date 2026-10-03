from pathlib import Path

from ragl.loaders.markdown import load_markdown


def test_load_markdown(tmp_path: Path) -> None:
    path = tmp_path / "example.md"
    text = "# RAG Lab\n\nThis is a test document."
    path.write_text(text, encoding="utf-8")

    document = load_markdown(path)

    assert document.source == str(path)
    assert document.text == text
    assert document.title == "example"

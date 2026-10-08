from ragl.generators.openai import valid_citations


def test_drops_out_of_range_and_duplicate_citations() -> None:
    assert valid_citations([2, 7, 0, 2, 1], source_count=5) == [1, 2]


def test_no_citations_for_a_refusal() -> None:
    assert valid_citations([], source_count=5) == []

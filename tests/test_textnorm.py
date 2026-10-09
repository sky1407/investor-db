import pytest

from investordb.textnorm import contains_quote, html_to_text, normalize


def test_html_to_text_drops_scripts_and_styles():
    html = (
        "<html><head><style>p{}</style><script>var fund='x'</script></head><body><p>Hello</p></body></html>"
    )
    text = html_to_text(html)
    assert "Hello" in text
    assert "fund" not in text
    assert "p{}" not in text


def test_html_to_text_keeps_meta_description():
    html = '<meta name="description" content="Venture fund for CEE"><body>x</body>'
    assert "Venture fund for CEE" in html_to_text(html)


def test_block_tags_do_not_glue_words():
    assert normalize(html_to_text("<p>seed</p><p>fund</p>")) == "seed fund"


def test_entities_are_decoded():
    assert "Rock & Roll" in html_to_text("<p>Rock &amp; Roll</p>")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Investičný  fond\n\tSlovenska", "investicny fond slovenska"),
        ("„rizikový kapitál“", '"rizikovy kapital"'),
        ("0,5\u00a0\u2013\u00a03 mil. €", "0,5 - 3 mil. €"),
        ("in\u00adves\u00adtor", "investor"),
    ],
)
def test_normalize(raw, expected):
    assert normalize(raw) == expected


def test_contains_quote_survives_formatting_differences():
    page = html_to_text("<p>Fond investuje do <strong>začínajúcich</strong>\n firiem v&nbsp;SR.</p>")
    assert contains_quote(page, "Fond investuje do začinajúcich firiem v SR.")


def test_contains_quote_rejects_paraphrase():
    page = "Fond investuje do začínajúcich firiem v SR."
    assert not contains_quote(page, "Fond investuje do startupov v SR.")


def test_contains_quote_rejects_empty_quote():
    assert not contains_quote("anything", "   ")

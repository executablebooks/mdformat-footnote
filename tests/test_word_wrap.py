import mdformat


def test_word_wrap():
    input_text = """\
[^a]

[^a]: Ooh no, the first line of this first paragraph is still wrapped too wide
    unfortunately. Should fix this.

    But this second paragraph is wrapped exactly as expected. Woohooo, awesome!
"""
    expected_output = """\
[^a]

[^a]: Ooh no, the first line of this first
    paragraph is still wrapped too wide
    unfortunately. Should fix this.

    But this second paragraph is wrapped
    exactly as expected. Woohooo,
    awesome!
"""
    output = mdformat.text(input_text, options={"wrap": 40}, extensions={"footnote"})
    assert output == expected_output

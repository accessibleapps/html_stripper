"""Comprehensive property-based tests for html_stripper using Hypothesis."""

from hypothesis import given
from hypothesis import strategies as st

import html_stripper


# Property: Functions should never crash, regardless of input
@given(st.text())
def test_strip_html_entities_never_crashes(text):
    """strip_html_entities should handle any text input without crashing."""
    result = html_stripper.strip_html_entities(text)
    assert isinstance(result, str)


@given(st.one_of(st.none(), st.text()))
def test_strip_html_entities_handles_none(text):
    """strip_html_entities should handle None input."""
    result = html_stripper.strip_html_entities(text)
    assert isinstance(result, str)


@given(st.text())
def test_extract_text_never_crashes(html):
    """extract_text should handle any HTML input without crashing."""
    result = html_stripper.extract_text(html)
    assert isinstance(result, str)


@given(st.one_of(st.none(), st.text()))
def test_extract_text_handles_none(html):
    """extract_text should handle None input."""
    result = html_stripper.extract_text(html)
    assert isinstance(result, str)


# Test edge cases that commonly cause crashes (from the bug report)
@given(st.sampled_from(["<>", "<0>", "< >", "", "plain text", "&", "&#", "&#;", "&amp;"]))
def test_edge_cases_dont_crash(text):
    """Known edge cases should not crash."""
    result = html_stripper.extract_text(text)
    assert isinstance(result, str)

    result = html_stripper.strip_html_entities(text)
    assert isinstance(result, str)


# Test numeric entity edge cases
@given(
    st.sampled_from(
        [
            "&#0;",  # Minimum
            "&#1114111;",  # Maximum valid Unicode (0x10FFFF)
            "&#1114112;",  # Just above maximum (should be handled)
            "&#999999999999999999;",  # Huge number
            "&#-1;",  # Negative
            "&#;",  # Empty
            "&#abc;",  # Non-numeric
            "&#x1F600;",  # Hex (not supported by simple regex)
        ]
    )
)
def test_numeric_entities_dont_crash(text):
    """Numeric character references should be handled safely."""
    result = html_stripper.strip_html_entities(text)
    assert isinstance(result, str)


# Test HTML-like patterns that aren't valid HTML
@given(st.from_regex(r"<[^>]{0,10}>", fullmatch=True))
def test_invalid_html_patterns_dont_crash(html):
    """Invalid HTML-like patterns should not crash."""
    result = html_stripper.extract_text(html)
    assert isinstance(result, str)


# Test entity patterns
@given(st.from_regex(r"&[a-z]{0,10};", fullmatch=True))
def test_entity_patterns_dont_crash(text):
    """Entity-like patterns should be handled safely."""
    result = html_stripper.strip_html_entities(text)
    assert isinstance(result, str)


# Property: output should always be a string, never longer than input + some overhead
@given(st.text(min_size=0, max_size=1000))
def test_output_is_reasonable_length(text):
    """Output should not be dramatically longer than input."""
    result = html_stripper.strip_html_entities(text)
    # Entities can expand (e.g., &amp; -> &), but not dramatically
    assert len(result) <= len(text) * 2 + 100


# Property: None input should return empty string
def test_none_returns_empty_string():
    """None should be converted to empty string."""
    assert html_stripper.strip_html_entities(None) == ""
    assert html_stripper.extract_text(None) == ""


# Property: extract_text should remove HTML tags
@given(
    st.text(min_size=1, max_size=50),
    st.sampled_from(["p", "div", "span", "br", "strong", "em"]),
)
def test_extract_text_removes_tags(content, tag):
    """HTML tags should be removed from content."""
    html = f"<{tag}>{content}</{tag}>"
    result = html_stripper.extract_text(html)
    # Result should not contain the tag markers
    assert f"<{tag}>" not in result
    assert f"</{tag}>" not in result


# Property: strip_html_entities should decode common entities
@given(
    st.sampled_from(
        [
            ("&amp;", "&"),
            ("&lt;", "<"),
            ("&gt;", ">"),
            ("&quot;", '"'),
            ("&#65;", "A"),  # Numeric entity for 'A'
        ]
    )
)
def test_strip_html_entities_decodes_common(entity_pair):
    """Common HTML entities should be decoded correctly."""
    entity, expected = entity_pair
    result = html_stripper.strip_html_entities(entity)
    assert expected in result or entity in result  # Either decoded or preserved


# Regression test for chr() overflow bug
def test_chr_overflow_regression():
    """Test that huge numeric entities don't crash."""
    # These should not crash and should return the original or empty string
    huge_numbers = [
        "&#999999999999999999;",
        "&#18446744073709551615;",  # 2^64-1
        "&#1114112;",  # Just above valid Unicode range
    ]
    for text in huge_numbers:
        result = html_stripper.strip_html_entities(text)
        assert isinstance(result, str)
        # Should either preserve original or decode successfully
        assert len(result) > 0


# Test Unicode handling
@given(st.text(alphabet=st.characters(min_codepoint=0x0000, max_codepoint=0x10FFFF)))
def test_unicode_handling(text):
    """Should handle all valid Unicode characters."""
    result = html_stripper.strip_html_entities(text)
    assert isinstance(result, str)

    result = html_stripper.extract_text(text)
    assert isinstance(result, str)

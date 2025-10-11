from __future__ import annotations

import re
from html import entities
from html.parser import HTMLParser
from typing import Optional

__version__ = 0.1
__doc__ = """Strip html down to text in various ways."""


def strip_html_entities(s: Optional[str]) -> str:
    """Converts any html entities in s to their unicode-decoded equivalents and returns a string."""
    if s is None:
        s = ""
    entity_re = re.compile(r"&(#\d+|\w+);")

    def matchFunc(match: re.Match[str]) -> str:
        r"""Nested function to handle a match object.
        If we match &blah; and it's not found, &blah; will be returned.
        if we match #\d+, chr(digits) will be returned.
        Else, a string will be returned."""
        if match.group(1).startswith("#"):
            # Parse numeric character reference
            try:
                codepoint = int(match.group(1)[1:])
                # Validate Unicode range
                if 0 <= codepoint <= 0x10FFFF:
                    return chr(codepoint)
                # Invalid codepoint, return original
                return match.group(0)
            except (ValueError, OverflowError):
                # Invalid numeric entity, return original
                return match.group(0)
        replacement = entities.entitydefs.get(match.group(1), f"&{match.group(1)};")
        return replacement

    return entity_re.sub(matchFunc, s)


class _DeHTMLParser(HTMLParser):
    def __init__(self) -> None:
        HTMLParser.__init__(self)
        self.__text: list[str] = []

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if len(text) > 0:
            text = re.sub("[ \t\r\n]+", " ", text)
            self.__text.append(text + " ")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag == "p":
            self.__text.append("\n\n")
        elif tag == "br":
            self.__text.append("\n")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag == "br":
            self.__text.append("\n\n")

    def text(self) -> str:
        return "".join(self.__text).strip()


def extract_text(html: Optional[str]) -> str:
    """Extract plain text from HTML, preserving paragraph and line breaks."""
    if html is None:
        html = ""
    parser = _DeHTMLParser()
    parser.feed(html)
    parser.close()
    return parser.text()

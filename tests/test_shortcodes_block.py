from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from conftest import Formatter


def test_block_body_preserved_verbatim(fmt: Formatter) -> None:
    start = """\
        {% mermaid() %}
        graph TD
          A["velodex[x]"] --> B[*]
          A --> C
        {% end %}
        """
    assert fmt(dedent(start)) == dedent(start)


def test_block_start_args_sorted_body_kept(fmt: Formatter) -> None:
    long_body = f"body *keeps* [markdown](y) then {'more words that push well past column one twenty ' * 3}"
    assert len(long_body) > 120
    start = f'{{% demo(cls="x", author="Bob") %}}\n{long_body}\n{{% end %}}\n'
    expected = f'{{% demo(author="Bob", cls="x") %}}\n{long_body}\n{{% end %}}\n'
    assert fmt(start) == expected


def test_block_escaped(fmt: Formatter) -> None:
    start = """\
        {%/* quote() */%}
        not *rendered*
        {%/* end */%}
        """
    assert fmt(dedent(start)) == dedent(start)


def test_block_nested(fmt: Formatter) -> None:
    start = """\
        {% outer() %}
        before
        {% inner() %}
        deep
        {% end %}
        after
        {% end %}
        """
    assert fmt(dedent(start)) == dedent(start)


def test_block_empty_body(fmt: Formatter) -> None:
    start = """\
        {% note() %}
        {% end %}
        """
    assert fmt(dedent(start)) == dedent(start)


def test_block_terminates_paragraph(fmt: Formatter) -> None:
    start = """\
        text before
        {% demo(id="x") %}
        body
        {% end %}
        """
    expected = """\
        text before

        {% demo(id="x") %}
        body
        {% end %}
        """
    assert fmt(dedent(start)) == dedent(expected)


def test_block_body_with_foreign_marker_kept(fmt: Formatter) -> None:
    start = """\
        {% x() %}
        {%/* end */%}
        {% end %}
        """
    assert fmt(dedent(start)) == dedent(start)


def test_block_too_short_marker_is_text(fmt: Formatter) -> None:
    assert fmt("{%}\n") == "{%}\n"


def test_block_multiline_start_tag_collapses(fmt: Formatter) -> None:
    start = """\
        {% demo(
          author="Bob",
          cite="x"
        ) %}
        body stays put
        {% end %}
        """
    expected = """\
        {% demo(author="Bob", cite="x") %}
        body stays put
        {% end %}
        """
    assert fmt(dedent(start)) == dedent(expected)


def test_block_unclosed_start_tag_is_text(fmt: Formatter) -> None:
    assert fmt("{% demo(\nnever closed here\n") == "{% demo( never closed here\n"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("{% quote() %}\nno end here\n", "{% quote() %} no end here\n", id="unterminated"),
        pytest.param(
            "{% invalid here %}\nbody\n{% end %}\n",
            "{% invalid here %} body {% end %}\n",
            id="invalid_start",
        ),
    ],
)
def test_block_not_recognized(fmt: Formatter, text: str, expected: str) -> None:
    assert fmt(text) == expected


def test_block_in_list_indented_body(fmt: Formatter) -> None:
    start = """\
        - item

          {% demo() %}
          body
          {% end %}
        """
    assert fmt(dedent(start)) == dedent(start)

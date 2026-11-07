from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from conftest import Formatter


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param('{{ youtube(id="x") }}\n', '{{ youtube(id="x") }}\n', id="simple"),
        pytest.param("{{  youtube( id='x' ) }}\n", '{{ youtube(id="x") }}\n', id="normalized"),
        pytest.param(
            '{{ youtube(id="x", autoplay=true) }}\n',
            '{{ youtube(autoplay=true, id="x") }}\n',
            id="args_sorted",
        ),
        pytest.param('{{/* youtube(id="x") */}}\n', '{{/* youtube(id="x") */}}\n', id="escaped"),
        pytest.param('a {{ ref(page="x") }} b\n', 'a {{ ref(page="x") }} b\n', id="in_paragraph"),
    ],
)
def test_inline_shortcode(fmt: Formatter, text: str, expected: str) -> None:
    assert fmt(text) == expected


def test_inline_shortcode_not_wrapped(fmt: Formatter) -> None:
    start = (
        'Prefix {{ screen(name="project", alt="A very long alt text that certainly goes well beyond '
        'the one hundred and twenty character wrap boundary for sure") }} suffix\n'
    )
    shortcode_line = next(line for line in fmt(start).splitlines() if line.startswith("{{"))
    assert shortcode_line == (
        '{{ screen(alt="A very long alt text that certainly goes well beyond the one hundred and '
        'twenty character wrap boundary for sure", name="project") }}'
    )


def test_inline_shortcode_escaping_not_applied(fmt: Formatter) -> None:
    assert fmt("x {{/* note() */}} y\n") == "x {{/* note() */}} y\n"


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("{{ not a shortcode }}\n", id="invalid_call"),
        pytest.param("{{ foo }}\n", id="missing_parens"),
        pytest.param("text {{ and }} more\n", id="bare_double_braces"),
    ],
)
def test_inline_shortcode_invalid_left_untouched(fmt: Formatter, text: str) -> None:
    assert fmt(text) == text


def test_inline_shortcode_unterminated_is_text(fmt: Formatter) -> None:
    assert fmt("a {{ foo(x=1)\n") == "a {{ foo(x=1)\n"


def test_inline_shortcode_unterminated_string_is_text(fmt: Formatter) -> None:
    assert fmt('{{ foo(a="x) }}\n') == '{{ foo(a="x) }}\n'


def test_inline_shortcode_in_link_label(fmt: Formatter) -> None:
    start = '[{{ icon(name="x") }}](@/page.md)\n'
    assert fmt(start) == start


def test_inline_shortcode_in_list(fmt: Formatter) -> None:
    start = """\
        - Item 1 {{ ref(page="1") }}
        - Item 2 {{ ref(page="2") }}
        """
    assert fmt(dedent(start)) == dedent(start)

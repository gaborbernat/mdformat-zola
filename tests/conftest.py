from __future__ import annotations

from typing import TYPE_CHECKING, Final, Protocol

import mdformat
import mdformat.plugins
import pytest

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

# Every installed extension, matching how the mdformat CLI runs on a real Zola site.
_EXTENSIONS: Final[list[str]] = sorted(mdformat.plugins.PARSER_EXTENSIONS)


class Formatter(Protocol):
    def __call__(
        self,
        text: str,
        *,
        wrap: int | str = 120,
        codeformatters: Sequence[str] = (),
        plugin: Mapping[str, str | Sequence[str]] | None = None,
    ) -> str: ...


@pytest.fixture
def fmt() -> Formatter:
    def format_markdown(
        text: str,
        *,
        wrap: int | str = 120,
        codeformatters: Sequence[str] = (),
        plugin: Mapping[str, str | Sequence[str]] | None = None,
    ) -> str:
        options = {"wrap": wrap} if plugin is None else {"wrap": wrap, "plugin": {"zola": plugin}}
        return mdformat.text(text, options=options, extensions=_EXTENSIONS, codeformatters=codeformatters)

    return format_markdown

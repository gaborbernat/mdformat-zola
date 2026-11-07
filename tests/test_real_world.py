from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Final

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

_FIXTURES: Final[list[Path]] = sorted((Path(__file__).parent / "fixtures").glob("*.md"))


@pytest.mark.parametrize("fixture", _FIXTURES, ids=lambda p: p.stem)
def test_fixture_is_stable(fmt: Callable[..., str], fixture: Path) -> None:
    formatted = fmt(fixture.read_text(encoding="utf-8"))
    assert fmt(formatted) == formatted


@pytest.mark.parametrize("fixture", _FIXTURES, ids=lambda p: p.stem)
def test_fixture_preserves_shortcodes_and_bodies(fmt: Callable[..., str], fixture: Path) -> None:
    out = fmt(fixture.read_text(encoding="utf-8"))
    assert "{% mermaid() %}" in out
    assert '  A["node[0]"] --> B[*]' in out  # block body kept byte-for-byte, no escaping
    assert '{{/* youtube(id="x") */}}' in out  # escaped inline stays escaped, star intact
    assert '{%/* quote(author="Nobody") */%}' in out
    assert "This body is shown literally, *stars* and all." in out
    assert "[internal link](@/docs/_index.md#anchor)" in out
    assert "```rust,linenos,linenostart=10,hl_lines=1 3-4,name=main.rs" in out
    assert "## Diagrams {#diagrams .lead}" in out

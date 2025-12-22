"""Lightweight Charts JavaScript asset loading."""

from __future__ import annotations

from functools import lru_cache
from importlib.resources import files


@lru_cache(maxsize=1)
def getLwcJs() -> str:
    """Load the bundled Lightweight Charts JavaScript.

    Returns:
        The LWC JavaScript source code.

    Raises:
        FileNotFoundError: If the JS file is not found (package not built correctly).
    """
    jsPath = files("litecharts.js").joinpath("lightweight-charts.js")

    try:
        return jsPath.read_text(encoding="utf-8")
    except FileNotFoundError:
        msg = (
            "Lightweight Charts JS not found. "
            "This usually means the package was not built correctly. "
            "Try reinstalling: pip install --force-reinstall litecharts"
        )
        raise FileNotFoundError(msg) from None

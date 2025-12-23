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


def getLwcScript() -> str:
    """Get the LWC library wrapped in a script tag.

    Use this once per page when rendering multiple chart fragments.
    Include in <head> before any chart fragments.

    Returns:
        HTML script tag containing the LWC library.
    """
    return f"<script>{getLwcJs()}</script>"


def getPluginScripts() -> str:
    """Get all plugin scripts wrapped in script tags.

    Use this once per page when rendering chart fragments that may use plugins.
    Include in <head> after getLwcScript() and before any chart fragments.

    Returns:
        HTML script tags containing all plugin code.
    """
    from .plugins.draw_rectangle import RECTANGLE_PRIMITIVE_JS

    return f"<script>{RECTANGLE_PRIMITIVE_JS}</script>"


def getDefaultStyles(containerId: str) -> str:
    """Get default CSS styles for a chart container.

    With native LWC panes, minimal styling is needed as LWC manages
    pane layout internally. Returns an empty string for compatibility.

    Args:
        containerId: The chart container ID (e.g., chart.id).

    Returns:
        CSS rules for the container (currently empty).
    """
    # Native LWC panes handle layout internally, no CSS needed
    return f"/* styles for #container_{containerId} */"

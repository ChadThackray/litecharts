"""Rectangle drawing primitive plugin for litecharts.

This plugin adds the ability to draw colored rectangles on the chart,
useful for highlighting trade zones, support/resistance areas, etc.

The rectangle primitive is rendered behind the candles (zOrder: 'bottom').
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..series import BaseSeries
    from ..types import OhlcInput, RectangleOptions, SingleValueInput


# JavaScript primitive class for drawing rectangles.
# This is embedded directly in the HTML output.
RECTANGLE_PRIMITIVE_JS = """
class RectanglePrimitiveRenderer {
    constructor(data) {
        this._data = data;
    }
    draw(target) {
        target.useBitmapCoordinateSpace(scope => {
            const ctx = scope.context;
            this._data.rectangles.forEach(rect => {
                if (rect.x1 === null || rect.x2 === null ||
                    rect.y1 === null || rect.y2 === null) return;
                const x1 = Math.round(rect.x1 * scope.horizontalPixelRatio);
                const x2 = Math.round(rect.x2 * scope.horizontalPixelRatio);
                const y1 = Math.round(rect.y1 * scope.verticalPixelRatio);
                const y2 = Math.round(rect.y2 * scope.verticalPixelRatio);
                const left = Math.min(x1, x2);
                const right = Math.max(x1, x2);
                const top = Math.min(y1, y2);
                const bottom = Math.max(y1, y2);
                ctx.fillStyle = rect.color || 'rgba(0, 255, 0, 0.2)';
                ctx.fillRect(left, top, right - left, bottom - top);
            });
        });
    }
}

class RectanglePrimitivePaneView {
    constructor(source) {
        this._source = source;
        this._data = { rectangles: [] };
    }
    update() {
        const timeScale = this._source._chart.timeScale();
        const series = this._source._series;
        this._data.rectangles = this._source._rectangles.map(rect => {
            return {
                x1: timeScale.timeToCoordinate(rect.startTime),
                x2: timeScale.timeToCoordinate(rect.endTime),
                y1: series.priceToCoordinate(rect.startPrice),
                y2: series.priceToCoordinate(rect.endPrice),
                color: rect.color
            };
        });
    }
    renderer() {
        return new RectanglePrimitiveRenderer(this._data);
    }
    zOrder() {
        return 'bottom';
    }
}

class RectanglePrimitive {
    constructor(chart, series, rectangles) {
        this._chart = chart;
        this._series = series;
        this._rectangles = rectangles;
        this._paneViews = [new RectanglePrimitivePaneView(this)];
    }
    updateAllViews() {
        this._paneViews.forEach(pv => pv.update());
    }
    paneViews() {
        return this._paneViews;
    }
}
"""


def extractRectangles(
    series: BaseSeries[SingleValueInput] | BaseSeries[OhlcInput],
) -> list[RectangleOptions]:
    """Extract rectangle data from a series.

    Args:
        series: The series to extract rectangles from.

    Returns:
        List of rectangle options.
    """
    return series.rectangles


def renderRectangleJs(
    chartVar: str,
    seriesVar: str,
    rectangles: list[RectangleOptions],
) -> str:
    """Generate JS code to create and attach the rectangle primitive.

    Args:
        chartVar: The JS variable name of the chart.
        seriesVar: The JS variable name of the series.
        rectangles: List of rectangle options.

    Returns:
        JavaScript code string.
    """
    # Rectangles are already in camelCase format from the series
    jsRectangles = []
    for rect in rectangles:
        jsRect = {
            "startTime": rect.get("startTime"),
            "endTime": rect.get("endTime"),
            "startPrice": rect.get("startPrice"),
            "endPrice": rect.get("endPrice"),
            "color": rect.get("color", "rgba(0, 255, 0, 0.2)"),
        }
        jsRectangles.append(jsRect)

    rectanglesJson = json.dumps(jsRectangles)
    primitiveVar = f"rectPrimitive_{seriesVar}"

    return f"""// Rectangle primitive for {seriesVar}
    const {primitiveVar} = new RectanglePrimitive(
        {chartVar}, {seriesVar}, {rectanglesJson}
    );
    {seriesVar}.attachPrimitive({primitiveVar});"""

## Lightweight-Charts API Notes

The current lightweight-charts library uses a **generic `addSeries()` method** with series definition objects, NOT type-specific methods like `addCandlestickSeries()`.

### Correct API Pattern

```javascript
// Series definitions are exported from LightweightCharts:
// - CandlestickSeries, LineSeries, AreaSeries, BarSeries, HistogramSeries, BaselineSeries

// Adding series to chart (default pane):
const series = chart.addSeries(LightweightCharts.CandlestickSeries, {options});

// Adding series with pane index:
const series = chart.addSeries(LightweightCharts.LineSeries, {options}, paneIndex);

// Adding panes:
const pane = chart.addPane();  // Returns IPaneApi

// Adding series to a specific pane:
const series = pane.addSeries(LightweightCharts.AreaSeries, {options});
```

### Key IPaneApi Methods
- `addSeries(definition, options)` - Add any series type
- `getSeries()` - Get all series in the pane
- `paneIndex()` - Get pane's index
- `getHeight()`, `setHeight()` - Manage pane height
- `getStretchFactor()`, `setStretchFactor()` - Manage relative sizing

### Key IChartApiBase Methods
- `addSeries(definition, options, paneIndex)` - Add series to a specific pane
- `addPane(preserveEmptyPane?)` - Create new panes
- `panes()` - Get all panes
- `removePane(index)` - Remove a pane

### WRONG (Old API - no longer works):
```javascript
pane.addCandlestickSeries({options})  // TypeError: not a function
chart.addLineSeries({options})        // TypeError: not a function
```

### Markers API (v5)

In LWC v5, markers are no longer set directly on the series. They use a separate primitive:

```javascript
// CORRECT (v5):
LightweightCharts.createSeriesMarkers(series, [
    { time: 1609459200, position: 'aboveBar', shape: 'arrowDown', color: '#f44336' }
]);

// WRONG (v4 - no longer works):
series.setMarkers([...])  // Method doesn't exist in v5
```

Note: Marker position/shape values use camelCase: `aboveBar`, `belowBar`, `inBar`, `arrowUp`, `arrowDown`.

### litecharts Python API Patterns

- `createSeriesMarkers(series, markers)` returns a `SeriesMarkersApi` handle (not `None`) — each call creates an independent marker group
- Handle methods: `.setMarkers(markers)`, `.markers()`, `.detach()`
- `series.markers` flattens all groups into a single list; `series.markerGroups` returns the list of `SeriesMarkersApi` handles
- Display methods (`toHtml`, `show`, `save`) accept an optional `style: StyleOptions` parameter for HTML document styling (e.g. `{"padding": 0}`). Default padding is 20px. No effect on `toFragment()`
- `chart.fitContent()` sets a flag that renders `timeScale().fitContent()` in JS output
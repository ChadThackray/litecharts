---
layout: home

hero:
  name: litecharts
  text: Python Charts Made Simple
  tagline: Thin Python wrapper for TradingView Lightweight Charts
  actions:
    - theme: brand
      text: Get Started
      link: /guide/getting-started
    - theme: alt
      text: View on GitHub
      link: https://github.com/ChadThackray/litecharts

features:
  - title: Simple API
    details: Create interactive financial charts with just a few lines of Python code.
  - title: Multiple Series Types
    details: Candlestick, Line, Area, Bar, Histogram, and Baseline series out of the box.
  - title: Pandas & NumPy Support
    details: Pass DataFrames or arrays directly - no manual conversion needed.
  - title: Jupyter Integration
    details: Works seamlessly in Jupyter notebooks or opens in your browser.
---

<div class="home-chart">

## See it in action

<ChartExample src="/litecharts/examples/basic.html" :height="440" />

</div>

<style>
.home-chart {
  max-width: 840px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}
</style>

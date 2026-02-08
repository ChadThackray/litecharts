import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'litecharts',
  description: 'Python wrapper for TradingView Lightweight Charts',

  base: '/litecharts/',

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/logo.svg' }],
  ],

  themeConfig: {
    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Examples', link: '/examples/basic' },
      { text: 'GitHub', link: 'https://github.com/ChadThackray/litecharts' },
    ],

    sidebar: [
      {
        text: 'Introduction',
        items: [
          { text: 'Getting Started', link: '/guide/getting-started' },
          { text: 'Installation', link: '/guide/installation' },
        ]
      },
      {
        text: 'Basics',
        items: [
          { text: 'Creating Charts', link: '/guide/creating-charts' },
          { text: 'Series Types', link: '/guide/series-types' },
          { text: 'Data Formats', link: '/guide/data-formats' },
        ]
      },
      {
        text: 'Advanced',
        items: [
          { text: 'Multi-Pane Charts', link: '/guide/multi-pane' },
          { text: 'Markers', link: '/guide/markers' },
          { text: 'Customization', link: '/guide/customization' },
        ]
      },
      {
        text: 'Examples',
        items: [
          { text: 'Basic Chart', link: '/examples/basic' },
          { text: 'Multi-Pane', link: '/examples/multi-pane' },
          { text: 'Overlay', link: '/examples/pandas' },
          { text: 'Markers', link: '/examples/markers' },
        ]
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/ChadThackray/litecharts' },
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2025 Chad Thackray',
    },

    search: {
      provider: 'local',
    },
  },
})

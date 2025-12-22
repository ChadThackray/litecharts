import DefaultTheme from 'vitepress/theme'
import ChartExample from './components/ChartExample.vue'
import type { Theme } from 'vitepress'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ChartExample', ChartExample)
  },
} satisfies Theme

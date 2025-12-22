<script setup lang="ts">
interface Props {
  src: string
  height?: number
}

const props = withDefaults(defineProps<Props>(), {
  height: 420,
})
</script>

<template>
  <div class="chart-example">
    <iframe
      :src="src"
      :height="height"
      frameborder="0"
      scrolling="no"
    />
  </div>
</template>

<style scoped>
.chart-example {
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
}

.chart-example iframe {
  width: 100%;
  display: block;
  border: none;
}
</style>

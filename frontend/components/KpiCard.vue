<template>
  <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
    <h3 class="text-sm font-medium text-gray-400 uppercase">
      {{ title }}
    </h3>
    <p class="text-3xl font-bold text-white mt-2">
      {{ value }}
    </p>
    <p v-if="change" class="text-sm text-green-400 mt-1">
      {{ change }} vs período anterior
    </p>
  </div>
</template>

<script setup>

defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  change: {
    type: String,
    required: false
  }
})
</script>
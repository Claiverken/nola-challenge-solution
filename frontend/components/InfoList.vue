<template>
  <div class="bg-gray-800 p-6 rounded-lg shadow-lg h-full overflow-y-auto">

    <h3 v-if="title" class="text-lg font-bold text-white mb-4">
      {{ title }}
    </h3>

    <div v-if="loading" class="text-gray-300">A carregar...</div>
    <div v-else-if="error" class="text-red-400">{{ error }}</div>
    <div v-else-if="!items || items.length === 0" class="text-gray-400">
      Nenhum dado encontrado.
    </div>
    <ul v-else class="space-y-3">
      <li v-for="(item, index) in items" :key="index" class="border-b border-gray-700 pb-2">
        <div class="flex justify-between items-center">
          <span class="text-white font-medium">{{ item.linha_principal }}</span>
          <span class="text-lg font-bold text-blue-400">{{ item.metrica_principal }}</span>
        </div>
        <span class="text-sm text-gray-400">{{ item.sub_linha }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: false // <-- MUDANÇA 2: required: true mudou para false
  },
  items: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})
</script>
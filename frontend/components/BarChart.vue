<template>
  <div class="bg-gray-800 p-6 rounded-lg shadow-lg h-full">
    <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

// Registamos as partes do Chart.js
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
)

// Agora o componente aceita OS DADOS e AS OPÇÕES
const props = defineProps({
  chartData: {
    type: Object,
    required: true
  },
  chartOptions: {
    type: Object,
    // Torna as opções opcionais, embora as vamos passar
    default: () => ({ responsive: true, maintainAspectRatio: false })
  }
})

// NOTA: As 'chartOptions' que defini aqui antes foram REMOVIDAS.
// Agora, usamos as que vêm do 'app.vue'.
</script>
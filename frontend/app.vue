<template>
  <div class="bg-gray-900 min-h-screen p-8">

    <div class="flex flex-col md:flex-row justify-between items-center mb-8">
      <h1 class="text-4xl font-bold text-white">
        Painel Nola
      </h1>
      <div class="flex items-center space-x-4 mt-4 md:mt-0">

        <div>
          <label for="store_filter" class="text-sm font-medium text-gray-400">Loja</label>
          <select
            v-model="globalStoreFilter"
            id="store_filter"
            class="bg-gray-700 text-white p-2 rounded-lg shadow-inner max-w-[150px]"
          >
            <option value="all">Geral (Todas as Lojas)</option>
            <option v-for="store in storeList" :key="store.id" :value="store.id">
              {{ store.name.substring(0, 20) + '...' }}
            </option>
          </select>
        </div>

        <div>
          <label for="start_date" class="text-sm font-medium text-gray-400">De</label>
          <input
            v-model="startDateFilter"
            type="date"
            id="start_date"
            class="bg-gray-700 text-white p-2 rounded-lg shadow-inner"
          >
        </div>
        <div>
          <label for="end_date" class="text-sm font-medium text-gray-400">Até</label>
          <input
            v-model="endDateFilter"
            type="date"
            id="end_date"
            class="bg-gray-700 text-white p-2 rounded-lg shadow-inner"
          >
        </div>

        <button
          @click="fetchAllData"
          :disabled="globalLoading"
          class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-500"
        >
          {{ globalLoading ? 'A filtrar...' : 'Aplicar' }}
        </button>
        <button
          @click="clearAndFetch"
          :disabled="globalLoading"
          class="bg-gray-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-gray-700 disabled:bg-gray-500"
        >
            Limpar
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-if="loadingKpis" class="text-white col-span-3">A carregar KPIs...</div>
      <KpiCard v-if="kpiData" title="Total de Vendas" :value="kpiData.total_sales" />
      <KpiCard v-if="kpiData" title="Faturamento Total" :value="formatCurrency(kpiData.total_revenue)" />
      <KpiCard v-if="kpiData" title="Ticket Médio" :value="formatCurrency(kpiData.average_ticket)" />
    </div>

    <div class="mt-8">
      <div class="flex space-x-1 border-b border-gray-700">
        <button
          @click="activeTab = 'geral'"
          :class="[
            'py-2 px-4 font-medium rounded-t-lg',
            activeTab === 'geral' ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'
          ]"
        >
          Visão Geral
        </button>
        <button
          @click="activeTab = 'operacional'"
          :class="[
            'py-2 px-4 font-medium rounded-t-lg',
            activeTab === 'operacional' ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'
          ]"
        >
          Análise Operacional
        </button>
        <button
          @click="activeTab = 'clientes'"
          :class="[
            'py-2 px-4 font-medium rounded-t-lg',
            activeTab === 'clientes' ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'
          ]"
        >
          Análise de Clientes
        </button>
      </div>

      <div v-if="activeTab === 'geral'" class="pt-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="h-96">
            <div v-if="loadingTopProducts" class="text-white">A carregar Top Produtos...</div>
            <BarChart
              v-if="topProductsChartData"
              :chart-data="topProductsChartData"
              :chart-options="topProductsChartOptions"
            />
          </div>
          <div class="h-96">
            <div v-if="loadingTimeSeries" class="text-white">A carregar Série Temporal...</div>
            <LineChart
              v-if="lineChartData"
              :chart-data="lineChartData"
              :chart-options="lineChartOptions"
            />
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'operacional'" class="pt-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6"> <div class="h-96">
            <div v-if="loadingTopItems" class="text-white">A carregar Top Itens...</div>
            <BarChart
              v-if="topItemsChartData"
              :chart-data="topItemsChartData"
              :chart-options="topItemsChartOptions"
            />
          </div>
          <div class="h-96 bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-bold text-white">
                Piores Bairros (Entrega)
              </h3>
              <select
                v-model="deliveryMinFilter"
                @change="fetchDeliveryPerformance"
                class="bg-gray-700 text-white p-1 rounded-lg text-sm"
              >
                <option v-for="n in 10" :key="n" :value="n">
                  Min. {{ n }} entrega{{ n > 1 ? 's' : '' }}
                </option>
              </select>
            </div>
            <div class="flex-grow overflow-y-auto">
              <InfoList
                title=""
                :items="deliveryPerformanceList"
                :loading="loadingDelivery"
              />
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'clientes'" class="pt-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6"> <div class="h-96 bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col">
            <h3 class="text-lg font-bold text-white mb-4">
              Clientes em Risco (Hoje)
            </h3>
            <p class="text-sm text-gray-400 mb-4">Clientes com 3+ compras que não voltam há 30+ dias.</p>
            <div class="flex-grow overflow-y-auto">
              <InfoList
                title=""
                :items="customerSegmentList"
                :loading="loadingCustomers"
              />
            </div>
          </div>
          <div class="h-96 bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-bold text-white">
                Top Clientes (por Gasto)
              </h3>
              <select
                v-model="topCustomersLimit"
                @change="fetchTopCustomers"
                class="bg-gray-700 text-white p-1 rounded-lg text-sm"
              >
                <option :value="10">Top 10</option>
                <option :value="20">Top 20</option>
                <option :value="50">Top 50</option>
              </select>
            </div>
            <div class="flex-grow overflow-y-auto">
              <InfoList
                title=""
                :items="topCustomersList"
                :loading="loadingTopCustomers"
              />
            </div>
          </div>
        </div>
      </div>

    </div> </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

// --- IMPORTA TODOS OS COMPONENTES ---
import KpiCard from './components/KpiCard.vue'
import BarChart from './components/BarChart.vue'
import LineChart from './components/LineChart.vue'
import InfoList from './components/InfoList.vue'

// ===== MUDANÇA: ESTADO DO SEPARADOR ATIVO =====
const activeTab = ref('geral') // Começa no separador 'geral'

// --- ESTADO DOS FILTROS ---
const startDateFilter = ref('')
const endDateFilter = ref('')
const globalLoading = ref(false)
const globalStoreFilter = ref('all') // Filtro Global de Loja

// Filtros específicos
const topCustomersLimit = ref(10) // Específico para Top Clientes
const deliveryMinFilter = ref(1) // Específico para Piores Bairros

// --- API Base URL ---
const apiBaseUrl = process.env.NUXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1'

// --- ESTADO (Loading & Dados) ---
const kpiData = ref(null); const loadingKpis = ref(true);
const topProductsData = ref(null); const loadingTopProducts = ref(true);
const timeSeriesData = ref(null); const loadingTimeSeries = ref(true);
const topItemsData = ref(null); const loadingTopItems = ref(true);
const deliveryData = ref(null); const loadingDelivery = ref(true);
const customerData = ref(null); const loadingCustomers = ref(true); // Para Clientes em Risco
const topCustomersData = ref(null); const loadingTopCustomers = ref(true); // Para Top Clientes
const storeList = ref([]) // Lista de lojas

// --- FUNÇÕES DE ARRANQUE ---
onMounted(() => {
  fetchAllData() // Chama todos os dados globais (incluindo Top Clientes)
  fetchCustomerSegments() // Chama os dados de cliente (separadamente)
  fetchStores() // Busca a lista de lojas
})

// --- FUNÇÕES GLOBAIS DE FILTRO ---
async function fetchAllData() {
  if (globalLoading.value) return
  console.log("A buscar dados GLOBAIS com os filtros:", globalStoreFilter.value, startDateFilter.value, endDateFilter.value)
  globalLoading.value = true

  // Chama TODOS os 6 endpoints globais
  await Promise.all([
    fetchKpis(),
    fetchTopProducts(),
    fetchTimeSeries(),
    fetchTopItems(),
    fetchDeliveryPerformance(),
    fetchTopCustomers()
  ])

  globalLoading.value = false
}

function clearAndFetch() {
  // Limpa os filtros globais
  startDateFilter.value = ''
  endDateFilter.value = ''
  globalStoreFilter.value = 'all'
  fetchAllData()
}

// --- FUNÇÕES DE FETCH ESPECÍFICAS ---

function formatCurrency(value) {
  if (typeof value !== 'number') return value
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

async function fetchStores() {
  try {
    const response = await axios.get(`${apiBaseUrl}/stores`)
    storeList.value = response.data
  } catch (err) {
    console.error('Erro ao buscar lojas:', err)
  }
}

// 1. KPIs (Global)
async function fetchKpis() {
  try {
    loadingKpis.value = true
    const params = {}
    if (startDateFilter.value) params.start_date = startDateFilter.value;
    if (endDateFilter.value) params.end_date = endDateFilter.value;
    if (globalStoreFilter.value !== 'all') params.store_id = globalStoreFilter.value;

    const response = await axios.get(`${apiBaseUrl}/kpis/main`, { params })
    kpiData.value = response.data
  } catch (err) { console.error('Erro KPIs:', err) }
    finally { loadingKpis.value = false }
}

// 2. Top Produtos (Global)
async function fetchTopProducts() {
  try {
    loadingTopProducts.value = true
    const params = { limit: 10, channel_type: 'D' }
    if (startDateFilter.value) params.start_date = startDateFilter.value;
    if (endDateFilter.value) params.end_date = endDateFilter.value;
    if (globalStoreFilter.value !== 'all') params.store_id = globalStoreFilter.value;

    const response = await axios.get(`${apiBaseUrl}/analytics/top-products`, { params })
    topProductsData.value = response.data
  } catch (err) { console.error('Erro Top Produtos:', err) }
    finally { loadingTopProducts.value = false }
}

// 3. Série Temporal (Global)
async function fetchTimeSeries() {
  try {
    loadingTimeSeries.value = true
    const params = {
      metric: 'average_ticket',
      group_by: 'channel'
    }

    if (startDateFilter.value && endDateFilter.value) {
      params.start_date = startDateFilter.value;
      params.end_date = endDateFilter.value;
      params.time_unit = 'day';
    } else {
      params.time_unit = 'month';
    }

    if (globalStoreFilter.value !== 'all') params.store_id = globalStoreFilter.value;

    const response = await axios.get(`${apiBaseUrl}/analytics/time-series`, { params })
    timeSeriesData.value = response.data.data
  } catch (err) { console.error('Erro Série Temporal:', err) }
    finally { loadingTimeSeries.value = false }
}

// 4. Top Itens (Global)
async function fetchTopItems() {
  try {
    loadingTopItems.value = true
    const params = { limit: 10 }
    if (startDateFilter.value) params.start_date = startDateFilter.value;
    if (endDateFilter.value) params.end_date = endDateFilter.value;
    if (globalStoreFilter.value !== 'all') params.store_id = globalStoreFilter.value;

    const response = await axios.get(`${apiBaseUrl}/analytics/top-items`, { params })
    topItemsData.value = response.data
  } catch (err) { console.error('Erro Top Itens:', err) }
    finally { loadingTopItems.value = false }
}

// 5. Performance de Entrega (Global)
async function fetchDeliveryPerformance() {
  try {
    loadingDelivery.value = true
    const params = {
      limit: 10,
      min_deliveries: deliveryMinFilter.value // Usa o filtro do widget
    }
    if (startDateFilter.value) params.start_date = startDateFilter.value;
    if (endDateFilter.value) params.end_date = endDateFilter.value;
    if (globalStoreFilter.value !== 'all') params.store_id = globalStoreFilter.value;

    const response = await axios.get(`${apiBaseUrl}/analytics/delivery-performance`, { params })
    deliveryData.value = response.data
  } catch (err) { console.error('Erro Entrega:', err) }
    finally { loadingDelivery.value = false }
}

// 6. Top Clientes (Global)
async function fetchTopCustomers() {
  try {
    loadingTopCustomers.value = true
    const params = {
      limit: topCustomersLimit.value,
      sort_by: 'monetary_value'
    }
    if (startDateFilter.value) params.start_date = startDateFilter.value;
    if (endDateFilter.value) params.end_date = endDateFilter.value;
    if (globalStoreFilter.value !== 'all') params.store_id = globalStoreFilter.value;

    const response = await axios.get(`${apiBaseUrl}/analytics/top-customers`, { params })
    topCustomersData.value = response.data
  } catch (err) { console.error('Erro Top Clientes:', err) }
    finally { loadingTopCustomers.value = false }
}

// 7. Clientes em Risco (Específico - SEMPRE HOJE)
async function fetchCustomerSegments() {
  try {
    loadingCustomers.value = true
    const params = { min_recency_days: 30, min_frequency: 3, limit: 50 }

    const response = await axios.get(`${apiBaseUrl}/analytics/customer-segments`, { params })
    customerData.value = response.data
  } catch (err) { console.error('Erro Clientes:', err) }
    finally { loadingCustomers.value = false }
}

// --- DADOS COMPUTADOS (para os 7 widgets) ---

// (Todo o código das 'computed properties' e 'options' fica 100% igual)
const topProductsChartData = computed(() => {
  if (!topProductsData.value || topProductsData.value.length === 0) return null
  const sortedData = [...topProductsData.value].reverse()
  const labels = sortedData.map(prod => prod.product_name.substring(0, 20) + '...')
  const data = sortedData.map(prod => prod.total_sold)
  return {
    labels: labels,
    datasets: [{
      label: 'Total de Vendas',
      backgroundColor: '#4A90E2', data: data, indexAxis: 'y',
    }]
  }
})
const topProductsChartOptions = {
  responsive: true, maintainAspectRatio: false, indexAxis: 'y',
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Top 10 Produtos (Delivery)', color: 'white', font: { size: 16 } },
  },
  scales: {
    y: { ticks: { color: 'white' }, grid: { display: false } },
    x: { beginAtZero: true, ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } }
  }
}
const lineChartData = computed(() => {
  if (!timeSeriesData.value || timeSeriesData.value.length === 0) return null;
  const allDates = [...new Set(timeSeriesData.value.map(d => d.date))].sort();
  const allGroups = [...new Set(timeSeriesData.value.map(d => d.group))];
  const colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B', '#BD10E0', '#9013FE'];
  const datasets = allGroups.map((group, index) => {
    const color = colors[index % colors.length];
    const data = allDates.map(date => {
      const dataPoint = timeSeriesData.value.find(d => d.date === date && d.group === group);
      return dataPoint ? dataPoint.value : null;
    });
    return {
      label: group, data: data, borderColor: color, backgroundColor: color, fill: false, tension: 0.1
    };
  });
  return { labels: allDates, datasets: datasets };
});
const lineChartOptions = {
  responsive: true, maintainAspectRatio: false,
  plugins: {
    legend: { display: true, position: 'top', labels: { color: 'white' } },
    title: { display: true, text: 'Ticket Médio por Canal', color: 'white', font: { size: 16 } },
  },
  scales: {
    y: { beginAtZero: false, ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
    x: { ticks: { color: 'white' }, grid: { display: false } }
  }
};
const topItemsChartData = computed(() => {
  if (!topItemsData.value || topItemsData.value.length === 0) return null
  const sortedData = [...topItemsData.value].reverse()
  const labels = sortedData.map(item => item.item_name)
  const data = sortedData.map(item => item.total_sold)
  return {
    labels: labels,
    datasets: [{
      label: 'Total de Vendas',
      backgroundColor: '#50E3C2', // Cor Verde
      data: data,
      indexAxis: 'y',
    }]
  }
})
const topItemsChartOptions = {
  responsive: true, maintainAspectRatio: false, indexAxis: 'y',
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Top 10 Itens Adicionais', color: 'white', font: { size: 16 } },
  },
  scales: {
    y: { ticks: { color: 'white' }, grid: { display: false } },
    x: { beginAtZero: true, ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } }
  }
}
const deliveryPerformanceList = computed(() => {
  if (!deliveryData.value) return []
  return deliveryData.value.map(item => ({
    linha_principal: `${item.neighborhood}, ${item.city}`,
    metrica_principal: `${item.avg_delivery_minutes.toFixed(1)} min`,
    sub_linha: `${item.total_deliveries} entregas`
  }))
})
const customerSegmentList = computed(() => {
  if (!customerData.value) return []
  return customerData.value.map(item => ({
    linha_principal: item.customer_name || `Cliente #${item.customer_id}`,
    metrica_principal: `${item.recency_days} dias`,
    sub_linha: `${item.frequency} compras | ${formatCurrency(item.monetary_value)}`
  }))
})

const topCustomersList = computed(() => {
  if (!topCustomersData.value) return []
  return topCustomersData.value.map(item => ({
    linha_principal: item.customer_name || `Cliente #${item.customer_id}`,
    metrica_principal: formatCurrency(item.monetary_value),
    sub_linha: `${item.frequency} compras`
  }))
})

</script>
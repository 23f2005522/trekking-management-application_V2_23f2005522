<script setup>
import { onMounted, onBeforeUnmount, watch, ref, nextTick } from 'vue'
import { useAdminStore } from '@/stores/admin/adminStore'
import { useFlashStore } from '@/stores/flashStore'
import { storeToRefs } from 'pinia'
import Loader from '@/components/Loader.vue'
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  DoughnutController,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js'

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  DoughnutController,
  ArcElement,
  Tooltip,
  Legend
)

const adminStore = useAdminStore()
const flashStore = useFlashStore()
const { report, loadingReport } = storeToRefs(adminStore)

const bookingsChartRef = ref(null)
const treksChartRef = ref(null)
let bookingsChart = null
let treksChart = null

const trekStatusColors = {
  open: '#198754',
  ongoing: '#ffc107',
  completed: '#0d6efd',
  pending: '#dc3545',
  approved: '#0dcaf0',
}

const destroyCharts = () => {
  if (bookingsChart) {
    bookingsChart.destroy()
    bookingsChart = null
  }
  if (treksChart) {
    treksChart.destroy()
    treksChart = null
  }
}

const renderCharts = async () => {
  if (!report.value?.charts) return

  await nextTick()
  destroyCharts()

  const bookingsData = report.value.charts.bookings_per_month || []
  if (bookingsChartRef.value) {
    bookingsChart = new Chart(bookingsChartRef.value, {
      type: 'bar',
      data: {
        labels: bookingsData.map((item) => item.label),
        datasets: [{
          label: 'Bookings',
          data: bookingsData.map((item) => item.count),
          backgroundColor: '#198754',
          borderRadius: 8,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    })
  }

  const trekStatus = report.value.charts.treks_by_status || {}
  const labels = Object.keys(trekStatus)
  if (treksChartRef.value && labels.length) {
    treksChart = new Chart(treksChartRef.value, {
      type: 'doughnut',
      data: {
        labels: labels.map((key) => key.charAt(0).toUpperCase() + key.slice(1)),
        datasets: [{
          data: labels.map((key) => trekStatus[key]),
          backgroundColor: labels.map((key) => trekStatusColors[key] || '#6c757d'),
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } },
      },
    })
  }
}

watch(report, () => {
  renderCharts()
})

onMounted(async () => {
  try {
    await adminStore.fetchReport()
    await renderCharts()
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to load report.', 'error')
  }
})

onBeforeUnmount(() => {
  destroyCharts()
})
</script>

<template>
  <div>

    <h2 class="fw-bold mb-4 d-flex align-items-center gap-2 text-dark">
      <i class="bi bi-graph-up-arrow text-primary"></i>
      Trekking Statistics & Reports
    </h2>

    <Loader v-if="loadingReport" />

    <div v-else-if="report">

      <!-- overview -->
      <h4 class="mb-3 d-flex align-items-center gap-2 fw-semibold text-secondary">
        <i class="bi bi-grid-1x2-fill text-muted"></i> Overview
      </h4>

      <div class="row g-3 mb-5">
        <div class="col-md-3">
          <div class="card status-card bg-gradient bg-primary text-white border-0 shadow-sm">
            <div class="card-body d-flex align-items-center justify-content-between p-4">
              <div>
                <h3 class="fw-bold mb-1">{{ report.overview.total_trekkers }}</h3>
                <small class="text-white-50 text-uppercase fw-bold tracking-wider">Total Trekkers</small>
              </div>
              <i class="bi bi-people-fill fs-1 opacity-75"></i>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card status-card bg-gradient bg-success text-white border-0 shadow-sm">
            <div class="card-body d-flex align-items-center justify-content-between p-4">
              <div>
                <h3 class="fw-bold mb-1">{{ report.overview.total_staff }}</h3>
                <small class="text-white-50 text-uppercase fw-bold tracking-wider">Total Staff</small>
              </div>
              <i class="bi bi-person-badge-fill fs-1 opacity-75"></i>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card status-card bg-gradient bg-info text-white border-0 shadow-sm">
            <div class="card-body d-flex align-items-center justify-content-between p-4">
              <div>
                <h3 class="fw-bold mb-1">{{ report.overview.total_treks }}</h3>
                <small class="text-white-50 text-uppercase fw-bold tracking-wider">Total Treks</small>
              </div>
              <i class="bi bi-compass-fill fs-1 opacity-75"></i>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card status-card bg-gradient bg-warning text-dark border-0 shadow-sm">
            <div class="card-body d-flex align-items-center justify-content-between p-4">
              <div>
                <h3 class="fw-bold mb-1">{{ report.overview.total_bookings }}</h3>
                <small class="text-dark-50 text-uppercase fw-bold tracking-wider">Total Bookings</small>
              </div>
              <i class="bi bi-journal-bookmark-fill fs-1 opacity-75"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- charts -->
      <h4 class="mb-3 d-flex align-items-center gap-2 fw-semibold text-secondary">
        <i class="bi bi-bar-chart-line text-muted"></i> Visual Analytics
      </h4>

      <div class="row g-4 mb-5">
        <div class="col-lg-7">
          <div class="card status-card border-0 shadow-sm h-100">
            <div class="card-body">
              <h5 class="fw-semibold mb-3">Bookings per Month</h5>
              <div class="chart-wrap">
                <canvas ref="bookingsChartRef"></canvas>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-5">
          <div class="card status-card border-0 shadow-sm h-100">
            <div class="card-body">
              <h5 class="fw-semibold mb-3">Treks by Status</h5>
              <div class="chart-wrap">
                <canvas ref="treksChartRef"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- trek status -->
      <h4 class="mb-3 d-flex align-items-center gap-2 fw-semibold text-secondary">
        <i class="bi bi-activity text-muted"></i> Trek Status
      </h4>

      <div class="row g-3 mb-5">
        <div v-for="(value, key) in report.trek_status" :key="key" class="col-md-2">
          <div class="card status-card bg-gradient bg-secondary text-white border-0 shadow-sm">
            <div class="card-body text-center p-3">
              <i class="bi bi-tags fs-3 mb-2 opacity-75 d-block"></i>
              <h4 class="fw-bold mb-1">{{ value }}</h4>
              <small class="text-capitalize text-white-50 fw-semibold">{{ key }}</small>
            </div>
          </div>
        </div>
      </div>

      <!-- booking status -->
      <h4 class="mb-3 d-flex align-items-center gap-2 fw-semibold text-secondary">
        <i class="bi bi-calendar-check text-muted"></i> Booking Status
      </h4>

      <div class="row g-3 mb-5">
        <div v-for="(value, key) in report.booking_status" :key="key" class="col-md-4">
          <div class="card status-card bg-gradient bg-dark text-white border-0 shadow-sm">
            <div class="card-body d-flex align-items-center justify-content-between p-4">
              <div>
                <h4 class="fw-bold mb-1">{{ value }}</h4>
                <small class="text-capitalize text-white-50 fw-semibold">{{ key }}</small>
              </div>
              <i class="bi bi-bookmark-plus fs-2 opacity-50"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- payment statistics -->
      <h4 class="mb-3 d-flex align-items-center gap-2 fw-semibold text-secondary">
        <i class="bi bi-credit-card-2-back text-muted"></i> Payment Statistics
      </h4>

      <div class="row g-3 mb-5">
        <div class="col-md-4">
          <div class="card status-card border-start border-success border-4 shadow-sm bg-white">
            <div class="card-body d-flex align-items-center justify-content-between p-4">
              <div>
                <h4 class="fw-bold text-success mb-1">{{ report.payment_statistics.paid }}</h4>
                <small class="text-muted fw-semibold">Paid Bookings</small>
              </div>
              <i class="bi bi-check-circle-fill text-success fs-2"></i>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card status-card border-start border-warning border-4 shadow-sm bg-white">
            <div class="card-body d-flex align-items-center justify-content-between p-4">
              <div>
                <h4 class="fw-bold text-warning mb-1">{{ report.payment_statistics.pending }}</h4>
                <small class="text-muted fw-semibold">Pending Bookings</small>
              </div>
              <i class="bi bi-hourglass-split text-warning fs-2"></i>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card status-card bg-gradient bg-danger text-white border-0 shadow-sm">
            <div class="card-body d-flex align-items-center justify-content-between p-4">
              <div>
                <h4 class="fw-bold mb-1">₹ {{ report.payment_statistics.revenue }}</h4>
                <small class="text-white-50 fw-semibold">Total Revenue</small>
              </div>
              <i class="bi bi-currency-rupee fs-2 opacity-75"></i>
            </div>
          </div>
        </div>
      </div>

      <div class="card status-card border-0 shadow-sm mb-4">
        <div class="card-header bg-white border-bottom-0 py-3">
          <h5 class="mb-0 fw-bold d-flex align-items-center gap-2 text-dark">
            <i class="bi bi-fire text-danger"></i> Top 5 Most Popular Treks
          </h5>
        </div>

        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light text-secondary">
              <tr>
                <th width="10%">#</th>
                <th width="60%">Trek Name</th>
                <th width="30%">Total Bookings</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(trek, index) in report.popular_treks" :key="trek.trek_name">
                <td>
                  <span class="badge rounded-circle p-2 d-inline-flex align-items-center justify-content-center"
                    :class="index === 0 ? 'bg-warning text-dark' : index === 1 ? 'bg-secondary text-white' : 'bg-light text-dark'"
                    style="width: 28px; height: 28px;">
                    {{ index + 1 }}
                  </span>
                </td>
                <td class="fw-semibold text-dark">{{ trek.trek_name }}</td>
                <td>
                  <span
                    class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-3 py-2 fw-bold">
                    {{ trek.booking_count }} Bookings
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.status-card {
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.status-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
}

.tracking-wider {
  letter-spacing: 0.05rem;
}

.chart-wrap {
  position: relative;
  height: 280px;
}
</style>

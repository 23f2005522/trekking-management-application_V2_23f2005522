<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import Loader from '@/components/Loader.vue'
import { useFlashStore } from '@/stores/flashStore'
import { useTrekHistoryStore } from '@/stores/trekker/trekHistoryStore'

const historyStore = useTrekHistoryStore()
const flashStore = useFlashStore()

const EXPORT_COOLDOWN_SEC = 10
const cooldownSeconds = ref(0)
let cooldownTimer = null

function startButtonCooldown() {
  cooldownSeconds.value = EXPORT_COOLDOWN_SEC

  if (cooldownTimer) clearInterval(cooldownTimer)

  cooldownTimer = setInterval(() => {
    cooldownSeconds.value -= 1

    if (cooldownSeconds.value <= 0) {
      clearInterval(cooldownTimer)
      cooldownTimer = null
    }
  }, 1000)
}

function isExportDisabled() {
  return historyStore.exporting || cooldownSeconds.value > 0  // slow API response + Spam protection
}

onMounted(async () => {
  try {
    await historyStore.fetchHistory()
    await historyStore.fetchExportJobs()
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to fetch trekking history.', 'error')
  }
})

onUnmounted(() => {
  if (cooldownTimer) clearInterval(cooldownTimer)
})

function getBadgeClass(status) {
  const classes = {
    booked: 'bg-success',
    pending: 'bg-warning text-dark',
    completed: 'bg-primary',
    canceled: 'bg-danger',
    open: 'bg-success',
    ongoing: 'bg-warning text-dark',
    closed: 'bg-secondary',
    processing: 'bg-info',
    failed: 'bg-danger',
  }

  return classes[String(status).toLowerCase()] || 'bg-secondary'
}

function formatDate(date) {
  if (!date) return '-'

  return new Date(date).toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

async function handleExport() {
  if (isExportDisabled()) return

  startButtonCooldown()

  try {
    const data = await historyStore.startExport()
    flashStore.show(data.message || 'Export started.', 'success')
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to start export.', 'error')
  }
}

async function handleDownload(jobId) {
  try {
    await historyStore.downloadExport(jobId)
    flashStore.show('CSV downloaded successfully.', 'success')
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to download export.', 'error')
  }
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold mb-0">Trekking History</h2>

      <button
        class="btn btn-success"
        :disabled="isExportDisabled()"
        @click="handleExport"
      >
        <span v-if="cooldownSeconds > 0">
          <span class="spinner-border spinner-border-sm me-1"></span>
          Wait {{ cooldownSeconds }}s...
        </span>
        <span v-else-if="historyStore.exporting">
          <span class="spinner-border spinner-border-sm me-1"></span>
          Exporting...
        </span>
        <span v-else>
          <i class="bi bi-download me-1"></i>
          Export CSV
        </span>
      </button>
    </div>

    <div v-if="historyStore.loadingHistory" class="text-center py-5">
      <Loader />
    </div>

    <div v-else>
      <div class="card shadow-sm">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Trek</th>
                <th>Trek Dates</th>
                <th>Price</th>
                <th>Trek Status</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="trek in historyStore.history" :key="trek.booking_id">
                <td>
                  <div class="fw-semibold fs-6">
                    {{ trek.name }}
                  </div>

                  <small class="text-muted">
                    location : {{ trek.location }}
                  </small>

                  <br />

                  <span class="badge bg-info me-1 text-capitalize">
                    {{ trek.difficulty }}
                  </span>

                  <span class="badge bg-secondary"> {{ trek.duration }} Days </span>
                </td>

                <td>
                  <div>
                    <strong>Start:</strong>
                    {{ formatDate(trek.starting_date) }}
                  </div>

                  <div>
                    <strong>End:</strong>
                    {{ formatDate(trek.ending_date) }}
                  </div>
                </td>

                <td>
                  <span class="fw-bold text-success"> ₹{{ trek.price }} </span>
                </td>

                <td>
                  <span class="badge text-uppercase" :class="getBadgeClass(trek.status)">
                    {{ trek.status }}
                  </span>
                </td>
              </tr>

              <tr v-if="historyStore.history.length === 0">
                <td colspan="4" class="text-center py-4 text-muted">No trekking history found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Export History -->
    <div class="mt-5">
      <h4 class="fw-semibold mb-3">
        <i class="bi bi-clock-history me-2"></i>
        Export History
      </h4>

      <div class="card shadow-sm">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Job ID</th>
                <th>Created</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="job in historyStore.exportJobs" :key="job.id">
                <td>#{{ job.id }}</td>
                <td>{{ job.created_at }}</td>
                <td>
                  <span class="badge text-uppercase" :class="getBadgeClass(job.status)">
                    {{ job.status }}
                  </span>
                </td>
                <td>
                  <button
                    v-if="job.status === 'completed'"
                    class="btn btn-sm btn-outline-success"
                    @click="handleDownload(job.id)"
                  >
                    <i class="bi bi-download me-1"></i>
                    Download
                  </button>
                  <span v-else-if="job.status === 'processing' || job.status === 'pending'" class="text-muted">
                    <span class="spinner-border spinner-border-sm me-1"></span>
                    Processing...
                  </span>
                  <span v-else-if="job.status === 'failed'" class="text-danger">Failed</span>
                  <span v-else class="text-muted">Pending...</span>
                </td>
              </tr>
              <tr v-if="historyStore.exportJobs.length === 0">
                <td colspan="4" class="text-center py-3 text-muted">No exports yet.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="alert alert-primary d-flex align-items-center gap-2 mt-4">
      <i class="bi bi-info-circle"></i>

      <span>
        Click <strong>Export CSV</strong> to generate a background job. You will get a live
        notification when the file is ready to download.
      </span>
    </div>
  </div>
</template>

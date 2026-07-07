<script setup>
import { onMounted } from 'vue'
import Loader from '@/components/Loader.vue'
import { useFlashStore } from '@/stores/flashStore'
import { useTrekHistoryStore } from '@/stores/trekker/trekHistoryStore'

const historyStore = useTrekHistoryStore()
const flashStore = useFlashStore()

onMounted(async () => {
  try {
    await historyStore.fetchHistory()
    
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to fetch trekking history.', 'danger')
  }
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
  }

  return classes[String(status).toLowerCase()] || 'bg-secondary'
}

function formatDate(date) {
  console.log(date)
  if (!date) return '-'

  return new Date(date).toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}
</script>

<template>
  <div>
    <h2 class="fw-bold mb-4">Trekking History</h2>

    <div v-if="historyStore.loadingHistory" class="text-center py-5">
      <Loader />
    </div>

    <div v-else class="card shadow-sm">
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
              <!-- Trek -->
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

              <!-- Dates -->
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

              <!-- Price -->
              <td>
                <span class="fw-bold text-success"> ₹{{ trek.price }} </span>
              </td>



              <!-- Trek Status -->
              <td>
                <span class="badge text-uppercase" :class="getBadgeClass(trek.status)">
                  {{ trek.status }}
                </span>
              </td>
            </tr>

            <tr v-if="historyStore.history.length === 0">
              <td colspan="5" class="text-center py-4 text-muted">No trekking history found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="alert alert-primary d-flex align-items-center gap-2 mt-4">
      <i class="bi bi-info-circle"></i>

      <span>
        This page displays every trek you have booked along with its current booking and trek
        status.
      </span>
    </div>
  </div>
</template>

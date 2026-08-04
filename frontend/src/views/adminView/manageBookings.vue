<script setup>
import { onMounted } from 'vue'
import Loader from '@/components/Loader.vue'
import { useBookingStore } from '@/stores/admin/bookingStore'
import { useFlashStore } from '@/stores/flashStore'

const bookingStore = useBookingStore()
const flashStore = useFlashStore()

const getStatusBadgeClass = (status, context = 'booking') => {
  const normalizedStatus = String(status || '').toLowerCase()

  const statusClassMap = {
    booked: 'bg-info text-dark',
    completed: context === 'export' ? 'bg-success' : 'bg-primary',
    canceled: 'bg-danger',
    pending: 'bg-warning text-dark',
    paid: 'bg-success',
    failed: 'bg-danger',
    processing: 'bg-info text-dark',
  }

  return statusClassMap[normalizedStatus] || 'bg-secondary'
}

const formatStatusLabel = (status) => {
  const normalizedStatus = String(status || '').trim().toLowerCase()
  return normalizedStatus || 'n/a'
}

const applyFilters = async () => {
  try {
    await bookingStore.fetchAllBookings()
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to fetch bookings.', 'error')
  }
}

const clearFilters = async () => {
  bookingStore.resetFilters()
  await applyFilters()
}

const handleExport = async () => {
  try {
    const data = await bookingStore.startBookingsExport()
    flashStore.show(data.message || 'Export started.', 'success')
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to start export.', 'error')
  }
}

const handleDownload = async (jobId) => {
  try {
    await bookingStore.downloadExport(jobId)
    flashStore.show('CSV downloaded successfully.', 'success')
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to download export.', 'error')
  }
}

onMounted(async () => {
  try {
    await bookingStore.fetchAllBookings()
    await bookingStore.fetchExportJobs()
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to fetch bookings.', 'error')
  }
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-2">
      <div>
        <h1 class="fw-bold mb-1">Manage Bookings</h1>
        <p class="text-muted mb-0">View, filter, and export all trek bookings.</p>
      </div>
      <button
        class="btn btn-success"
        :disabled="bookingStore.exporting"
        @click="handleExport"
      >
        <span v-if="bookingStore.exporting">
          <span class="spinner-border spinner-border-sm me-1"></span>
          Exporting...
        </span>
        <span v-else>
          <i class="bi bi-download me-1"></i>
          Export CSV
        </span>
      </button>
    </div>
    <hr />

    <div class="card shadow-sm mb-4 border-0">
      <div class="card-body">
        <div class="row g-3 align-items-end">
          <div class="col-md-4">
            <label class="form-label small text-muted">Search</label>
            <input
              v-model="bookingStore.filters.search"
              type="text"
              class="form-control"
              placeholder="Trekker, email, trek name, booking ID..."
              @keyup.enter="applyFilters"
            />
          </div>
          <div class="col-md-2">
            <label class="form-label small text-muted">Booking status</label>
            <select v-model="bookingStore.filters.status" class="form-select">
              <option value="">All</option>
              <option value="booked">Booked</option>
              <option value="completed">Completed</option>
              <option value="canceled">Canceled</option>
            </select>
          </div>
          <div class="col-md-2">
            <label class="form-label small text-muted">Payment</label>
            <select v-model="bookingStore.filters.payment_status" class="form-select">
              <option value="">All</option>
              <option value="pending">Pending</option>
              <option value="paid">Paid</option>
              <option value="failed">Failed</option>
            </select>
          </div>
          <div class="col-md-2">
            <label class="form-label small text-muted">From date</label>
            <input v-model="bookingStore.filters.from_date" type="date" class="form-control" />
          </div>
          <div class="col-md-2">
            <label class="form-label small text-muted">To date</label>
            <input v-model="bookingStore.filters.to_date" type="date" class="form-control" />
          </div>
          <div class="col-12 d-flex gap-2">
            <button class="btn btn-success" @click="applyFilters">
              <i class="bi bi-funnel me-1"></i>
              Apply filters
            </button>
            <button class="btn btn-outline-secondary" @click="clearFilters">Clear</button>
            <small class="text-muted ms-auto align-self-center">
              Showing <strong>{{ bookingStore.allBookings.length }}</strong> booking(s)
            </small>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm border-0 mb-4">
      <div v-if="bookingStore.loadingBookings" class="d-flex justify-content-center align-items-center p-5">
        <Loader />
      </div>

      <div v-else class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="bg-success text-white">
            <tr>
              <th scope="col">Booking ID</th>
              <th scope="col">Trekker</th>
              <th scope="col">Trek</th>
              <th scope="col">Booking Date</th>
              <th scope="col">Amount Paid</th>
              <th scope="col">Payment Status</th>
              <th scope="col">Trek Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="booking in bookingStore.allBookings" :key="booking.id">
              <td>{{ booking.id }}</td>
              <td>
                {{ booking.username }}
                <div class="text-muted small">{{ booking.user_email }}</div>
              </td>
              <td>{{ booking.trek_name }}</td>
              <td>{{ booking.booking_date }}</td>
              <td>₹{{ booking.amount_paid }}</td>
              <td>
                <span
                  :class="['badge text-uppercase', getStatusBadgeClass(booking.payment_status)]"
                >
                  {{ formatStatusLabel(booking.payment_status) }}
                </span>
              </td>
              <td>
                <span
                  :class="['badge text-uppercase', getStatusBadgeClass(booking.status)]"
                >
                  {{ formatStatusLabel(booking.status) }}
                </span>
              </td>
            </tr>

            <tr v-if="bookingStore.allBookings.length === 0">
              <td colspan="7" class="text-center text-muted py-4">No bookings found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <h4 class="fw-semibold mb-3">
      <i class="bi bi-clock-history me-2"></i>
      Export History
    </h4>
    <div class="card shadow-sm border-0">
      <div class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Job ID</th>
              <th>Created</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="job in bookingStore.exportJobs" :key="job.id">
              <td>#{{ job.id }}</td>
              <td>{{ job.created_at }}</td>
              <td>
                <span
                  :class="['badge text-uppercase', getStatusBadgeClass(job.status, 'export')]"
                >
                  {{ formatStatusLabel(job.status) }}
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
                <span v-else-if="job.status === 'failed'" class="text-danger">Failed</span>
                <span v-else class="text-muted">Processing...</span>
              </td>
            </tr>
            <tr v-if="bookingStore.exportJobs.length === 0">
              <td colspan="4" class="text-center py-3 text-muted">No exports yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  border-radius: 15px;
}

.table td,
.table th {
  vertical-align: middle;
}

.badge {
  padding: 0.45rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.03em;
}
</style>

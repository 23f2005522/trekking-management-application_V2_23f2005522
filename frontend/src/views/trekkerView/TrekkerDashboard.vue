<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTrekkerStore } from '@/stores/trekker/trekkerStore'
import { useFlashStore } from '@/stores/flashStore'
import Loader from '@/components/Loader.vue'

const router = useRouter()
const trekkerStore = useTrekkerStore()
const flashStore = useFlashStore()

const getStatusBadgeClass = (status) => {
  const normalizedStatus = String(status || '').toLowerCase()

  const statusClassMap = {
    booked: 'bg-success',
    completed: 'bg-primary',
    canceled: 'bg-danger',
    pending: 'bg-warning text-dark',
    paid: 'bg-success',
    open: 'bg-success',
    ongoing: 'bg-warning text-dark',
    closed: 'bg-secondary',
  }

  return statusClassMap[normalizedStatus] || 'bg-secondary'
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(Number(price || 0))
}

onMounted(async () => {
  try {
    await trekkerStore.fetchDashboardData()
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to load dashboard data.', 'error')
  }
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-4">
      <div>
        <h2 class="fw-bold mb-1">Welcome, {{ trekkerStore.trekkerProfile?.username || 'Trekker' }}!</h2>
        <p class="text-muted mb-0">Track bookings and discover newly opened treks.</p>
      </div>

      <button class="btn btn-success" @click="router.push('/trekker/profile')">
        <i class="bi bi-person me-1"></i>
        Manage Profile
      </button>
    </div>

    <div v-if="trekkerStore.loadingDashboard" class="text-center text-muted py-5">
      <Loader/>
    </div>

    <div v-else>
      <div class="row g-4 mb-4">
        <div class="col-md-6 col-xl-3">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <p class="text-muted mb-1">Total Bookings</p>
                  <h2 class="fw-bold mb-0">{{ trekkerStore.dashboardStats?.total_bookings || 0 }}</h2>
                </div>
                <i class="bi bi-calendar-check fs-2 text-success"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-xl-3">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <p class="text-muted mb-1">Active Bookings</p>
                  <h2 class="fw-bold mb-0">{{ trekkerStore.dashboardStats?.active_bookings || 0 }}</h2>
                </div>
                <i class="bi bi-backpack2 fs-2 text-primary"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-xl-3">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <p class="text-muted mb-1">Completed</p>
                  <h2 class="fw-bold mb-0">{{ trekkerStore.dashboardStats?.completed_bookings || 0 }}</h2>
                </div>
                <i class="bi bi-check2-circle fs-2 text-success"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-xl-3">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <p class="text-muted mb-1">Canceled</p>
                  <h2 class="fw-bold mb-0">{{ trekkerStore.dashboardStats?.canceled_bookings || 0 }}</h2>
                </div>
                <i class="bi bi-x-circle fs-2 text-danger"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card shadow-sm mb-4">
        <div class="card-header bg-white d-flex justify-content-between align-items-center">
          <h5 class="mb-0">Recently Opened Treks</h5>

          <button class="btn btn-outline-success btn-sm" @click="router.push('/trekker/treks')">
            Show More Treks
          </button>
        </div>

        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Trek</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Duration</th>
                <th>Slots Left</th>
                <th>Price</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="trek in trekkerStore.recentOpenTreks" :key="trek.id">
                <td class="fw-semibold">{{ trek.name }}</td>
                <td>{{ trek.location }}</td>
                <td class="text-capitalize">{{ trek.difficulty }}</td>
                <td>{{ trek.duration }} Days</td>
                <td>{{ trek.available_slots }}</td>
                <td>{{ formatPrice(trek.price) }}</td>
                <td>
                  <span :class="['badge text-uppercase', getStatusBadgeClass(trek.status)]">
                    {{ trek.status }}
                  </span>
                </td>
              </tr>

              <tr v-if="trekkerStore.recentOpenTreks.length === 0">
                <td colspan="7" class="text-center text-muted py-4">
                  No open treks found.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card shadow-sm">
        <div class="card-header bg-white d-flex justify-content-between align-items-center">
          <h5 class="mb-0">Recent Bookings</h5>

          <button class="btn btn-outline-success btn-sm" @click="router.push('/trekker/bookings')">
            Show All Bookings
          </button>
        </div>

        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Trek</th>
                <th>Booking Date</th>
                <th>Booking Status</th>
                <th>Payment</th>
                <th>Amount</th>
                <th>Trek Status</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="booking in trekkerStore.recentBookings" :key="booking.id">
                <td class="fw-semibold">{{ booking.trek_name }}</td>
                <td>{{ booking.booking_date }}</td>
                <td>
                  <span :class="['badge text-uppercase', getStatusBadgeClass(booking.status)]">
                    {{ booking.status }}
                  </span>
                </td>
                <td>
                  <span :class="['badge text-uppercase', getStatusBadgeClass(booking.payment_status)]">
                    {{ booking.payment_status }}
                  </span>
                </td>
                <td>{{ formatPrice(booking.amount_paid) }}</td>
                <td class="text-capitalize">{{ booking.trek_status }}</td>
              </tr>

              <tr v-if="trekkerStore.recentBookings.length === 0">
                <td colspan="6" class="text-center text-muted py-4">
                  No bookings yet.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

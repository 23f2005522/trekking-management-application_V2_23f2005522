<script setup>
import Loader from '@/components/Loader.vue'
import { useAdminStore } from '@/stores/admin/adminStore'
import { useFlashStore } from '@/stores/flashStore'
import { onMounted } from 'vue'

const adminStore = useAdminStore()
const flashStore = useFlashStore()

onMounted(async () => {
  try {
    await adminStore.fetchAdminData()
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to load dashboard data.', 'error')
  }
})
</script>

<template>
  <div>
    <div v-if="adminStore.loadingAdmin">
      <Loader />
    </div>

    <!-- Main Content -->
    <div v-else class="MainContent">
      <h1 class="fw-bold">Admin Dashboard</h1>
      <h2>welcome, {{ adminStore.admin?.username || 'Admin' }}</h2>

      <p class="text-muted">
        Welcome back, Admin! Here's what's happening with your trekking platform.
      </p>

      <div class="row g-4 mt-2">
        <div class="col-md-6 col-lg-3">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted">Total Treks</h6>

                  <h1 class="text-success fw-bold">
                    {{ adminStore.dashboardData?.total_treks || 0 }}
                  </h1>

                  <small class="text-success"> +3 this month </small>
                </div>

                <i class="bi bi-signpost-2 fs-1 text-success"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted">Total Users</h6>

                  <h1 class="text-success fw-bold">
                    {{ adminStore.dashboardData?.total_trekkers || 0 }}
                  </h1>

                  <small class="text-success"> +15 this month </small>
                </div>

                <i class="bi bi-person fs-1 text-success"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted">Total Staff</h6>

                  <h1 class="text-success fw-bold">
                    {{ adminStore.dashboardData?.total_staff || 0 }}
                  </h1>

                  <small class="text-success"> +2 this month </small>
                </div>

                <i class="bi bi-people fs-1 text-success"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted">Total Bookings</h6>

                  <h1 class="text-success fw-bold">
                    {{ adminStore.dashboardData?.total_bookings || 0 }}
                  </h1>

                  <small class="text-success"> +20 this month </small>
                </div>

                <i class="bi bi-calendar-check fs-1 text-success"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted">Total Revenue</h6>

                  <h1 class="text-success fw-bold">
                    {{ adminStore.dashboardData?.total_revenue_till_data || 0 }}
                  </h1>

                  <small class="text-success"> +20 this month </small>
                </div>

                <i class="bi bi-calendar-check fs-1 text-success"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted">Total Approved Treks</h6>

                  <h1 class="text-success fw-bold">
                    {{ adminStore.dashboardData?.treks_approved || 0 }}
                  </h1>

                  <small class="text-success"> +20 this month </small>
                </div>

                <i class="bi bi-check2-circle fs-1 text-success"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-3">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted">Total Pending Treks</h6>

                  <h1 class="text-success fw-bold">
                    {{ adminStore.dashboardData?.treks_pending || 0 }}
                  </h1>

                  <small class="text-success"> +20 this month </small>
                </div>

                <i class="bi bi-ban fs-1 text-success"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Bookings -->

      <div class="card shadow-sm mt-5">
        <div class="card-header bg-white">
          <h4 class="mb-0">Recent Bookings</h4>
        </div>

        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Booking ID</th>
                <th>User</th>
                <th>Trek</th>
                <th>Booking Date</th>
                <th>Booking Status</th>
                <th>Payment Status</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="booking in adminStore.dashboardData?.recent_bookings || []"
                :key="booking.id"
              >
                <td>{{ booking.id }}</td>
                <td>{{ booking.user.username }}</td>
                <td>{{ booking.trek.name }}</td>
                <td>{{ booking.booking_date }}</td>
                <td 
                    :class="{
                    'bg-success': booking.booking_status === 'booked',
                    'bg-secondary': booking.booking_status === 'completed',
                    'bg-danger': booking.booking_status === 'canceled',
                    'text-white': booking.booking_status === 'booked' || booking.booking_status === 'canceled',
                  }"
                >{{ booking.booking_status }}</td>
                <td
                  :class="{
                    'bg-success': booking.payment_status === 'paid',
                    'bg-warning': booking.payment_status === 'pending',
                    'bg-danger': booking.payment_status === 'failed',
                    'text-white': booking.payment_status === 'paid' || booking.payment_status === 'failed',
                  }"
                >{{ booking.payment_status }}</td>


              </tr>
            </tbody>
          </table>
        </div>

        <div class="card-footer bg-white text-end">
          <router-link to="/admin/bookings" class="text-success text-decoration-none fw-semibold">
            View All Bookings

            <i class="bi bi-arrow-right"></i>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  border-radius: 15px;
}
</style>

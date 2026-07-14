<script setup>
import { onMounted } from 'vue'
import Loader from '@/components/Loader.vue'
import { useBookingStore } from '@/stores/admin/bookingStore'
import { useFlashStore } from '@/stores/flashStore'

const bookingStore = useBookingStore()
const flashStore = useFlashStore()

onMounted(async () => {
  try {
    await bookingStore.fetchAllBookings()
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to fetch bookings.', 'error')
  }
})
</script>

<template>
  <div>
    <h1 class="fw-bold">Manage Bookings</h1>
    <p class="text-muted">View and manage all trek bookings.</p>
    <hr />

    <!-- search -->
    <div class="card shadow-sm mb-4 border-0">
      <div class="card-body">
        <div class="row align-items-center">
          <div class="col-md-8">
            <div class="input-group">
              <span class="input-group-text bg-white border-end-0">
                <i class="bi bi-search text-success"></i>
              </span>

              <input
                v-model="bookingStore.bookingSearchQuery"
                type="text"
                class="form-control border-start-0"
                placeholder="Search by trekkerName, trek Name, Trek Status, or booking ID..."
              />
            </div>
          </div>

          <div class="col-md-4 text-end">
            <small class="text-muted">
              Showing
              <strong>{{ bookingStore.filteredBookings.length || 0 }}</strong>
              of
              <strong>{{ bookingStore.allBookings.length || 0 }}</strong>
              Bookings
            </small>
          </div>
        </div>
      </div>
    </div>

    <!-- bookings table -->
    <div class="card shadow-sm border-0">
      <div v-if="bookingStore.loadingBookings" class="d-flex justify-content-center align-items-center p-5">
        <Loader />
      </div>

      <table v-else class="table table-hover mb-0">
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
            <tr v-for="booking in bookingStore.filteredBookings" :key="booking.id">
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
                  class="badge p-2"
                  :class="{
                    'bg-success': booking.payment_status === 'paid',
                    'bg-warning text-dark': booking.payment_status === 'pending',
                    'bg-danger': booking.payment_status === 'failed',
                    'bg-secondary': booking.payment_status === 'completed',
                  }"
                >
                  {{ booking.payment_status }}
                </span>
              </td>
              <td>
                <span
                  class="badge p-2"
                  :class="{
                    'bg-success': booking.status === 'booked',
                    'bg-secondary': booking.status === 'completed',
                    'bg-danger': booking.status === 'canceled',
                  }"
                >
                  {{ booking.status }}
                </span>
              </td>
            </tr>

            <tr v-if="bookingStore.filteredBookings.length === 0">
              <td colspan="7" class="text-center text-muted py-4">No bookings found.</td>
            </tr>
          </tbody>
        </table>
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
  padding: 8px 12px;
}
</style>
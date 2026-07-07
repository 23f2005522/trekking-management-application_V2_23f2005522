<script setup>
import { onMounted } from 'vue'
import { useBookingStore } from '@/stores/trekker/bookingStore'
import { useFlashStore } from '@/stores/flashStore'
import Loader from '@/components/Loader.vue'

const bookingStore = useBookingStore()
const flashStore = useFlashStore()

onMounted(async () => {
  try {
    await bookingStore.fetchBookings()
  } catch (error) {
    flashStore.show(
      error.response?.data?.message || 'Failed to fetch bookings.',
      'danger'
    )
  }
})

async function handleCancelBooking(id) {
  if (!confirm('Are you sure you want to cancel this booking?')) return

  try {
    const response = await bookingStore.cancelBooking(id)

    flashStore.show(response.message, 'success')
  } catch (error) {
    flashStore.show(
      error.response?.data?.message || 'Failed to cancel booking.',
      'danger'
    )
  }
}

function getBadgeClass(status) {
  const statusMap = {
    pending: 'bg-warning text-dark',
    booked: 'bg-success',
    completed: 'bg-primary',
    canceled: 'bg-danger',
    paid: 'bg-success',
    failed: 'bg-danger',
    open: 'bg-success',
    ongoing: 'bg-warning text-dark',
    closed: 'bg-secondary',
    approved: 'bg-info text-dark',
  }

  return statusMap[String(status).toLowerCase()] || 'bg-secondary'
}
</script>

<template>
  <div>

    <h2 class="fw-bold mb-4">
      My Bookings
    </h2>

    <div
      v-if="bookingStore.loadingBookings"
      class="text-center py-5"
    >
      <Loader />
    </div>

    <div
      v-else
      class="card shadow-sm"
    >
      <div class="table-responsive">

        <table class="table table-hover align-middle mb-0">

          <thead class="table-light">

            <tr>
              <th>Trek Name</th>
              <th>Booking Date</th>
              <th>Booking Status</th>
              <th>Payment</th>
              <th>Trek Status</th>
              <th>Action</th>
            </tr>

          </thead>

          <tbody>

            <tr
              v-for="booking in bookingStore.bookings"
              :key="booking.id"
            >

              <td>
                {{ booking.trek_name }}
              </td>

              <td>
                {{ booking.booking_date }}
              </td>

              <td>

                <span
                  class="badge text-uppercase"
                  :class="getBadgeClass(booking.status)"
                >
                  {{ booking.status }}
                </span>

              </td>

              <td>

                <span
                  class="badge text-uppercase"
                  :class="getBadgeClass(booking.payment_status)"
                >
                  {{ booking.payment_status }}
                </span>

              </td>

              <td>

                <span
                  class="badge text-uppercase"
                  :class="getBadgeClass(booking.trek_status)"
                >
                  {{ booking.trek_status }}
                </span>

              </td>

              <td>

                <button
                  v-if="
                    booking.status.toLowerCase() === 'booked' ||
                    booking.status.toLowerCase() === 'pending'
                  "
                  class="btn btn-outline-danger btn-sm"
                  :disabled="bookingStore.cancelBookingLoading"
                  @click="handleCancelBooking(booking.id)"
                >
                  Cancel Booking
                </button>

                <span
                  v-else
                  class="text-muted"
                >
                  —
                </span>

              </td>

            </tr>

            <tr
              v-if="bookingStore.bookings.length === 0"
            >
              <td
                colspan="6"
                class="text-center py-4 text-muted"
              >
                No bookings found.
              </td>
            </tr>

          </tbody>

        </table>

      </div>
    </div>

  </div>
</template>
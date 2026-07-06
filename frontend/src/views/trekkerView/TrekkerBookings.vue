<script setup>
const bookings = [
  {
    id: 1,
    trekName: 'Kedarkantha Trek',
    bookingDate: '10 May 2026',
    trekDates: '15 Jan - 20 Jan 2026',
    status: 'Booked',
  },
  {
    id: 2,
    trekName: 'Everest Base Camp',
    bookingDate: '02 Jun 2026',
    trekDates: '10 Apr - 16 Apr 2026',
    status: 'Booked',
  },
  {
    id: 3,
    trekName: 'Hampta Pass',
    bookingDate: '18 Jun 2026',
    trekDates: '05 Aug - 09 Aug 2026',
    status: 'Pending',
  },
]
</script>

<template>
  <div>
    <h2 class="fw-bold mb-4">My Bookings</h2>

    <div class="card shadow-sm">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th>Trek Name</th>
              <th>Trek Dates</th>
              <th>Booking Date</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="booking in bookings" :key="booking.id">
              <td>{{ booking.trekName }}</td>
              <td>{{ booking.trekDates }}</td>
              <td>{{ booking.bookingDate }}</td>
              <td>
                <span
                  class="badge"
                  :class="booking.status === 'Booked' ? 'bg-success' : 'bg-warning text-dark'"
                >
                  {{ booking.status }}
                </span>
              </td>
              <td>
                <button class="btn btn-outline-primary btn-sm">View Details</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

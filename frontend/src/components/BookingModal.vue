<script setup>
import { useFlashStore } from '@/stores/flashStore'
import { useTrekStore } from '@/stores/trekker/trekStore'

const trekStore = useTrekStore()
const flashStore = useFlashStore()

async function confirmBooking() {
  try {
    await trekStore.bookTrek()
    await trekStore.fetchTreks()
    flashStore.show('Trek booked.', 'success')
  } catch (error) {
    flashStore.show(
      error.response?.data?.message || 'An error occurred while booking the trek.',
      'error'
    )
  }
}
</script>

<template>
  <div
    class="modal fade"
    id="bookingModal"
    tabindex="-1"
    aria-labelledby="bookingModalLabel"
    aria-hidden="true"
    data-bs-backdrop="static"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header bg-success text-white">
          <h5 class="modal-title" id="bookingModalLabel">
            <i class="bi bi-backpack2-fill me-2"></i>
            Confirm Trek Booking
          </h5>

          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body" v-if="trekStore.selectedTrek">
          <div class="row">
            <!-- Image -->
            <div class="col-md-5">
              <img
                :src="
                  trekStore.selectedTrek.image_url ||
                  trekStore.selectedTrek.image ||
                  'https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png'
                "
                class="img-fluid rounded shadow-sm"
                style="height: 260px; width: 100%; object-fit: cover"
              />
              <div>
                {{ trekStore.selectedTrek.description || 'No description available.' }}
              </div>
            </div>

            <!-- Details -->
            <div class="col-md-7">
              <h3 class="fw-bold mb-3">
                {{ trekStore.selectedTrek.name }}
              </h3>

              <table class="table table-borderless mb-3">
                <tbody>
                  <tr>
                    <th width="35%">
                      <i class="bi bi-geo-alt-fill text-danger me-2"></i>
                      Location
                    </th>

                    <td>
                      {{ trekStore.selectedTrek.location }}
                    </td>
                  </tr>

                  <tr>
                    <th>
                      <i class="bi bi-bar-chart-fill text-warning me-2"></i>
                      Difficulty
                    </th>

                    <td class="text-capitalize">
                      {{ trekStore.selectedTrek.difficulty }}
                    </td>
                  </tr>

                  <tr>
                    <th>
                      <i class="bi bi-calendar-week-fill text-primary me-2"></i>
                      Duration
                    </th>

                    <td>{{ trekStore.selectedTrek.duration }} Days</td>
                  </tr>

                  <tr>
                    <th>
                      <i class="bi bi-people-fill text-success me-2"></i>
                      Slots Left
                    </th>

                    <td>
                      {{ trekStore.selectedTrek.available_slots }}
                    </td>
                  </tr>

                  <tr>
                    <th>
                      <i class="bi bi-currency-rupee text-success me-2"></i>
                      Price
                    </th>

                    <td class="fw-bold fs-5 text-success">₹ {{ trekStore.selectedTrek.price }}</td>
                  </tr>
                </tbody>
              </table>

              <div class="alert alert-warning mb-0">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                Once booked, your request will appear in
                <strong>My Bookings</strong>.
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">
            Cancel
          </button>

          <button type="button" class="btn btn-success" @click="confirmBooking">
            <i class="bi bi-check-circle-fill me-2"></i>
            Confirm Booking
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

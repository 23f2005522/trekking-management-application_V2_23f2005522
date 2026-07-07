<script setup>
import { onMounted } from 'vue'
import { useTrekStore } from '@/stores/trekker/trekStore' // Ensure this matches your store's export and file name!
import Loader from '@/components/Loader.vue'
import BookingModal from '@/components/BookingModal.vue'

// Initialize your store
const trekStore = useTrekStore()

// Fetch treks when the component mounts
onMounted(() => {
  trekStore.fetchTreks()
})

function openBookingModal(trek) {
  trekStore.selectedTrek = trek
  console.log('Opening modal for:', trek.name)
  // Add your modal triggering logic here (e.g., Bootstrap modal show toggles)
}
</script>

<template>
  <div>
    <!-- Booking Modal -->
    <BookingModal />

    <div class="d-flex flex-wrap gap-3 mb-4">
      <input
        type="text"
        class="form-control"
        placeholder="Search treks Names..."
        v-model="trekStore.filters.search"
        style="max-width: 320px"
      />

      <select v-model="trekStore.filters.difficulty" class="form-select" style="max-width: 180px">
        <option value="">Difficulty: All</option>
        <option value="easy">Easy</option>
        <option value="moderate">Moderate</option>
        <option value="hard">Hard</option>
      </select>

      <select v-model="trekStore.filters.location" class="form-select" style="max-width: 180px">
        <option value="">Location: All</option>
        <option value="Nepal">Nepal</option>
        <option value="Uttarakhand">Uttarakhand</option>
        <option value="Himachal">Himachal</option>
      </select>

      <select v-model="trekStore.filters.duration" class="form-select" style="max-width: 180px">
        <option value="">Duration: All</option>
        <option value="3">3 Days</option>
        <option value="5">5 Days</option>
        <option value="8">8 Days</option>
      </select>
    </div>

    <div v-if="trekStore.loadingTreks" class="text-center my-5">
      <Loader />
    </div>

    <div v-else class="row g-4">
      <div v-for="trek in trekStore.availableTreks" :key="trek.id" class="col-12 col-md-6 col-xl-4">
        <div class="card h-100 shadow-sm">
          <img
            :src="
              trek.image ||
              'https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png'
            "
            class="card-img-top trek-image"
            :alt="trek.name"
          />

          <div class="card-body">
            <h5 class="fw-bold mb-3">{{ trek.name }}</h5>
            <p class="mb-2"><strong>Location:</strong> {{ trek.location }}</p>
            <p class="mb-2"><strong>Difficulty:</strong> {{ trek.difficulty }}</p>
            <p class="mb-2"><strong>Duration:</strong> {{ trek.duration }} Days</p>
            <p class="mb-3">Slots Left: {{ trek.available_slots }}</p>

            <button
              class="btn btn-success w-100"
              data-bs-toggle="modal"
              data-bs-target="#bookingModal"
              @click="openBookingModal(trek)"
            >
              <i class="bi bi-backpack2 me-2"></i>
              Show Details 
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trek-image {
  height: 170px;
  object-fit: cover;
}
</style>

<script setup>
import { onMounted } from 'vue'
import { useTrekStore } from '@/stores/trekker/trekStore'
import { useFlashStore } from '@/stores/flashStore'
import Loader from '@/components/Loader.vue'
import BookingModal from '@/components/BookingModal.vue'

const trekStore = useTrekStore()
const flashStore = useFlashStore()

const placeholderImage =
  'https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png'

onMounted(async () => {
  try {
    await trekStore.fetchTreks()
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to fetch treks.', 'error')
  }
})

function getTrekImage(trek) {
  return trek.image_url || trek.image || placeholderImage
}

function getDifficultyClass(difficulty) {
  const map = {
    easy: 'bg-success',
    moderate: 'bg-warning text-dark',
    difficult: 'bg-danger',
  }
  return map[String(difficulty || '').toLowerCase()] || 'bg-secondary'
}

</script>

<template>
  <div>
    <BookingModal />

    <h2 class="fw-bold mb-1">Browse Treks</h2>
    <p class="text-muted mb-4">Pick an open trek and book your next adventure.</p>

    <div class="d-flex flex-wrap gap-3 mb-4">
      <input
        v-model="trekStore.filters.search"
        type="text"
        class="form-control"
        placeholder="Search trek names..."
        style="max-width: 320px"
      />

      <select v-model="trekStore.filters.difficulty" class="form-select" style="max-width: 180px">
        <option value="">Difficulty: All</option>
        <option value="easy">Easy</option>
        <option value="moderate">Moderate</option>
        <option value="difficult">Difficult</option>
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

    <div v-else-if="trekStore.availableTreks.length === 0" class="text-center text-muted py-5">
      No open treks found. Try changing your filters.
    </div>

    <div v-else class="row g-4">
      <!-- display all treks  -->
      <div
        v-for="trek in trekStore.availableTreks"
        :key="trek.id"
        class="col-12 col-md-6 col-xl-4"
      >
        <div class="card trek-overlay-card border-0 shadow-sm h-100">
          <img
            class="card-img trek-overlay-image"
            :src="getTrekImage(trek)"
            :alt="trek.name"
          />

          <div class="card-img-overlay trek-overlay-panel d-flex flex-column justify-content-end">
            <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
              <h4 class="card-title text-white fw-bold mb-0">{{ trek.name }}</h4>
              <span :class="['badge text-capitalize', getDifficultyClass(trek.difficulty)]">
                {{ trek.difficulty }}
              </span>
            </div>

            <p class="card-text text-white-50 mb-2 small">
              <i class="bi bi-geo-alt-fill me-1"></i>{{ trek.location }}
              <span class="mx-2">|</span>
              <i class="bi bi-calendar-week me-1"></i>{{ trek.duration }} Days
            </p>

            <p class="card-text text-white mb-3 small trek-description">
              {{ trek.description || 'Explore this trek and book your slot today.' }}
            </p>

            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
              <span class="badge bg-light text-success">
                <i class="bi bi-people-fill me-1"></i>
                {{ trek.available_slots }} slots left
              </span>
              <span class="text-white fw-semibold">
                <i class="bi bi-currency-rupee"></i>{{ trek.price }}
              </span>
            </div>

            <button
              type="button"
              class="btn btn-success"
              data-bs-toggle="modal"
              data-bs-target="#bookingModal"
              @click="trekStore.selectedTrek = trek"
            >
              <i class="bi bi-backpack2 me-2"></i>
              Book Trek
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trek-overlay-card {
  min-height: 360px;
  overflow: hidden;
  border-radius: 16px;
}

.trek-overlay-image {
  width: 100%;
  height: 100%;
  min-height: 360px;
  object-fit: cover;
}

.trek-overlay-panel {
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.88) 0%,
    rgba(0, 0, 0, 0.55) 55%,
    rgba(0, 0, 0, 0.15) 100%
  );
  border-radius: 16px;
}

.trek-description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

<script setup>
const treks = [
  {
    id: 1,
    name: 'Everest Base Camp',
    location: 'Nepal',
    difficulty: 'Hard',
    duration: '12 Days',
    slotsLeft: 8,
    image: 'https://images.unsplash.com/photo-1486911278844-a81c5267e227?auto=format&fit=crop&w=700&q=80',
  },
  {
    id: 2,
    name: 'Roopkund Trek',
    location: 'Uttarakhand',
    difficulty: 'Moderate',
    duration: '7 Days',
    slotsLeft: 7,
    image: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=700&q=80',
  },
  {
    id: 3,
    name: 'Hampta Pass',
    location: 'Himachal',
    difficulty: 'Moderate',
    duration: '5 Days',
    slotsLeft: 0,
    image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=700&q=80',
  },
]
</script>

<template>
  <div>
    <div class="d-flex flex-wrap gap-3 mb-4">
      <input type="text" class="form-control" placeholder="Search treks..." style="max-width: 320px;" />

      <select class="form-select" style="max-width: 180px;">
        <option>Difficulty: All</option>
        <option>Easy</option>
        <option>Moderate</option>
        <option>Hard</option>
      </select>

      <select class="form-select" style="max-width: 180px;">
        <option>Location: All</option>
        <option>Nepal</option>
        <option>Uttarakhand</option>
        <option>Himachal</option>
      </select>
    </div>

    <div class="row g-4">
      <div v-for="trek in treks" :key="trek.id" class="col-12 col-md-6 col-xl-4">
        <div class="card h-100 shadow-sm">
          <img :src="trek.image" class="card-img-top trek-image" :alt="trek.name" />

          <div class="card-body">
            <h5 class="fw-bold mb-3">{{ trek.name }}</h5>
            <p class="mb-2">{{ trek.location }}</p>
            <p class="mb-2">{{ trek.difficulty }}</p>
            <p class="mb-2">{{ trek.duration }}</p>
            <p class="mb-3">Slots Left: {{ trek.slotsLeft }}</p>

            <button
              class="btn w-100"
              :class="trek.slotsLeft > 0 ? 'btn-outline-primary' : 'btn-outline-secondary'"
              :disabled="trek.slotsLeft === 0"
            >
              View Details
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

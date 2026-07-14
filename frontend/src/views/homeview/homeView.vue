<script setup>
import router from '@/router';

</script>

<template>
  <!-- Hero Section -->
  <section class="bg-success text-white py-5">
    <div class="container">
      <div class="row align-items-center">

        <div class="col-lg-6">
          <h1 class="display-3 fw-bold">
            Explore The Mountains
          </h1>

          <p class="lead mt-4">
            Discover breathtaking trekking experiences and manage your adventures effortlessly.
          </p>

          <button 
          @click="router.push('/trekker/treks')"
          class="btn btn-warning btn-lg">
            Explore Treks
          </button>
        </div>

        <div class="col-lg-6 text-center">
          <img
            src="/src/assets/mountains.jpg"
            class="img-fluid rounded shadow"
            alt="Mountains"
          />
        </div>

      </div>
    </div>
  </section>

  <!-- Features -->
  <section class="py-5">
    <div class="container">

      <h2 class="text-center mb-5">
        Why Choose TrekMaster?
      </h2>

      <div class="row g-4">

        <div class="col-md-4">
          <div class="card shadow h-100">
            <div class="card-body text-center">
              <h3>🏕 Guided Treks</h3>
              <p>
                Professionally managed trekking experiences.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow h-100">
            <div class="card-body text-center">
              <h3>🧭 Easy Booking</h3>
              <p>
                Reserve your next adventure with ease.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow h-100">
            <div class="card-body text-center">
              <h3>🌄 Beautiful Destinations</h3>
              <p>
                Explore stunning mountain ranges and valleys.
              </p>
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- Popular Treks -->
  <section class="py-5">
    <div class="container">

      <h2 class="text-center mb-5">
        Popular Treks
      </h2>

      <div class="row g-4">

        <div class="col-md-4">
          <div class="card shadow h-100">
            <img
              src="https://picsum.photos/400/250?1"
              class="card-img-top"
            />

            <div class="card-body">
              <h4>Everest Base Camp</h4>

              <p>
                Experience the beauty of the Himalayas with our premium trekking package.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow h-100">
            <img
              src="https://picsum.photos/400/250?2"
              class="card-img-top"
            />

            <div class="card-body">
              <h4>Kedarkantha Trek</h4>

              <p>
                A beginner-friendly trek famous for snow and panoramic views.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow h-100">
            <img
              src="https://picsum.photos/400/250?3"
              class="card-img-top"
            />

            <div class="card-body">
              <h4>Valley of Flowers</h4>

              <p>
                Witness breathtaking landscapes and colorful meadows.
              </p>
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- Testimonials -->
  <section class="bg-light py-5">

    <div class="container">

      <h2 class="text-center mb-5">
        What Our Trekkers Say
      </h2>

      <div class="row g-4">

        <div class="col-md-4">
          <div class="card shadow h-100">
            <div class="card-body">
              <p>
                "Amazing experience! Everything was well organized and the guides were very helpful."
              </p>

              <h6>- Rahul Sharma</h6>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow h-100">
            <div class="card-body">
              <p>
                "One of the best trekking communities I have ever joined."
              </p>

              <h6>- Priya Das</h6>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow h-100">
            <div class="card-body">
              <p>
                "Beautiful destinations and excellent management."
              </p>

              <h6>- Arjun Singh</h6>
            </div>
          </div>
        </div>

      </div>

    </div>

  </section>

  <!-- Call To Action -->
  <section class="py-5 text-center">

    <div class="container">

      <h2 class="mb-4">
        Ready For Your Next Adventure?
      </h2>

      <p class="lead">
        Join thousands of trekkers and start exploring today.
      </p>

      <button class="btn btn-success btn-lg">
        Start Your Journey
      </button>

    </div>

  </section>
</template>

<style scoped>
section {
  scroll-margin-top: 80px;
}
</style>
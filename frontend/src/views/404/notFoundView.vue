<template>
  <div class="container py-5">

    <div class="row justify-content-center align-items-center min-vh-75">

      <div class="col-lg-8 text-center">

        <!-- Icon -->
        <i class="bi bi-compass display-1 text-success"></i>

        <!-- Error Code -->
        <h1 class="display-1 fw-bold text-success mt-3">
          404
        </h1>

        <!-- Heading -->
        <h2 class="fw-bold mb-3">
          Oops! You've Lost the Trail
        </h2>

        <!-- Description -->
        <p class="lead text-muted mb-4">
          The page you're looking for doesn't exist or may have been moved.
          Let's help you get back to your next adventure.
        </p>

        <!-- Buttons -->
        <div class="d-flex justify-content-center gap-3 flex-wrap">

          <router-link
            to="/"
            class="btn btn-success btn-lg">

            <i class="bi bi-house-door me-2"></i>
            Back to Home

          </router-link>

          <button
            class="btn btn-outline-success btn-lg"
            @click="$router.back()">

            <i class="bi bi-arrow-left me-2"></i>
            Go Back

          </button>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
</script>

<style scoped>
.min-vh-75{
    min-height:75vh;
}

.display-1{
    font-size:7rem;
}
</style>
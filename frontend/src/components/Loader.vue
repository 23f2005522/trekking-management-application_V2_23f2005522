<template>
  <div class="loader-overlay">

    <div class="text-center">

      <div class="loader-icon mb-4">
        <i class="bi bi-mountains display-1 text-success"></i>
      </div>

      <div
        class="spinner-border text-success mb-4"
        role="status"
        style="width: 4rem; height: 4rem;"
      >
        <span class="visually-hidden">Loading...</span>
      </div>

      <h3 class="fw-bold">
        TrekMaster
      </h3>

      <p class="text-muted mb-3">
        Preparing your adventure...
      </p>

      <div class="d-flex justify-content-center gap-4 fs-3">

        <i class="bi bi-signpost-2 text-success bounce"></i>

        <i class="bi bi-backpack2 text-warning bounce delay-1"></i>

        <i class="bi bi-compass text-primary bounce delay-2"></i>

      </div>

    </div>

  </div>
</template>

<script setup>
</script>

<style scoped>

.loader-overlay{
    position:fixed;
    inset:0;
    background:white;
    display:flex;
    justify-content:center;
    align-items:center;
    z-index:9999;
}

.loader-icon{
    animation:float 2s ease-in-out infinite;
}

@keyframes float{

    0%,100%{
        transform:translateY(0px);
    }

    50%{
        transform:translateY(-12px);
    }

}

.bounce{
    animation:bounce 1.3s infinite;
}

.delay-1{
    animation-delay:.2s;
}

.delay-2{
    animation-delay:.4s;
}

@keyframes bounce{

    0%,100%{
        transform:translateY(0);
    }

    50%{
        transform:translateY(-8px);
    }

}

</style>
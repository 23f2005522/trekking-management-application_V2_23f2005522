<script setup></script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-success shadow">
    <div class="container">
      <router-link class="navbar-brand fw-bold d-flex align-items-center" to="/">
        <img src="@/assets/hiking.png" style="width: 40px; height: 40px" class="me-2" />

        TrekMaster
      </router-link>

      <button class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#nav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div id="nav" class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/login" class="btn btn-outline-light"> Login </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

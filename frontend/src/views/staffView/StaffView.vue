<script setup>

import StaffSidebar from "./StaffSidebar.vue";


</script>

<template>
<div class="container-fluid">

    <div class="row">

        <div class="col-auto p-0">
            <StaffSidebar />
        </div>

        <div class="col">

            <router-view />

        </div>

    </div>

</div>
</template>
<script setup>
import { useFlashStore } from "@/stores/flashStore";

const flashStore = useFlashStore();
</script>

<template>
  <Transition name="flash">

    <div
      v-if="flashStore.state.message"
      class="position-fixed top-0 end-0 p-3"
      style="z-index: 1055; width: 350px;"
    >

      <div
        class="alert alert-dismissible shadow"
        :class="{
          'alert-success': flashStore.state.type === 'success',
          'alert-danger': flashStore.state.type === 'error',
          'alert-warning': flashStore.state.type === 'warning',
          'alert-info': flashStore.state.type === 'info'
        }"
      >

        {{ flashStore.state.message }}

        <button
          type="button"
          class="btn-close"
          @click="flashStore.clear()"
        ></button>

      </div>

    </div>

  </Transition>
</template>

<style scoped>
.flash-enter-active,
.flash-leave-active {
  transition: all 0.3s ease;
}

.flash-enter-from,
.flash-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.flash-enter-to,
.flash-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
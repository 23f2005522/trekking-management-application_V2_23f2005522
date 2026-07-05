<script setup>
import { useTrekStore } from '@/stores/trekStore'


const props = defineProps({
  trekId: {
    type: [String, Number, null],
    required: true,
    default: null,
  },
})


const trekStore = useTrekStore()


</script>

<template>
  <div
    class="modal fade"
    id="deleteTrekModal"
    tabindex="-1"
    aria-labelledby="deleteTrekModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="deleteTrekModalLabel">Delete Trek</h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">Are you sure you want to delete this trek?</div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-danger" @click="trekStore.deleteTrek(props.trekId)">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useTrekStore } from '@/stores/admin/trekStore'
import { useFlashStore } from '@/stores/flashStore'

const props = defineProps({
  trekId: {
    type: [String, Number, null],
    required: true,
    default: null,
  },
})

const trekStore = useTrekStore()
const flashStore = useFlashStore()

const handleDelete = async () => {
  if (!props.trekId) return

  try {
    const data = await trekStore.deleteTrek(props.trekId)
    flashStore.show(data?.message || 'Trek deleted successfully.', 'success')
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Error deleting trek.', 'error')
  }
}
</script>

<template>
  <div
    class="modal fade"
    id="deleteTrekModal"
    tabindex="-1"
    aria-labelledby="deleteTrekModalLabel"
    aria-hidden="true"
    data-bs-backdrop="static"
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
          <button type="button" class="btn btn-danger" @click="handleDelete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

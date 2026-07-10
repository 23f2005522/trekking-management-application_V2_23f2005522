import { defineStore } from "pinia";
import { reactive } from "vue";

export const useFlashStore = defineStore("flash", () => {

    // state
    const state = reactive({
        message: "",
        type: "success",
    });

    let timer = null;

    // actions
    function show(message, type = "success", duration = 3000) {

        state.message = message;
        state.type = type;

        clearTimeout(timer);

        timer = setTimeout(() => {
            state.message = "";
            state.type = "success";
        }, duration);
    }

    function clear() {
        clearTimeout(timer);
        state.message = "";
        state.type = "success";
    }


    return {
        state,
        show,
        clear,
    };
});
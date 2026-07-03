import { defineStore } from "pinia";
import { ref, reactive } from "vue";


export const useUserStore = defineStore("user", () => {

    // state
    const user = reactive(null);

    // getters 


    // actions



    return {
        // state
        user,

        // getters


        // actions
    }
})
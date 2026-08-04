import { defineStore } from "pinia";
import { ref } from "vue";
import axiosInstance from "@/utils/axioUtil";

export const useBookingStore = defineStore("Booking", () => {
    const allBookings = ref([]);
    const loadingBookings = ref(false);
    const exportJobs = ref([]);
    const exporting = ref(false);

    const filters = ref({
        search: "",
        status: "",
        payment_status: "",
        from_date: "",
        to_date: "",
    });

    function buildFilterParams() {
        const params = {};
        if (filters.value.search.trim()) params.search = filters.value.search.trim();
        if (filters.value.status) params.status = filters.value.status;
        if (filters.value.payment_status) params.payment_status = filters.value.payment_status;
        if (filters.value.from_date) params.from_date = filters.value.from_date;
        if (filters.value.to_date) params.to_date = filters.value.to_date;
        return params;
    }

    async function fetchAllBookings() {
        loadingBookings.value = true;
        try {
            const { data } = await axiosInstance.get("/admin/bookings", {
                params: buildFilterParams(),
            });
            allBookings.value = data.bookings;
            return data;
        } finally {
            loadingBookings.value = false;
        }
    }

    function resetFilters() {
        filters.value = {
            search: "",
            status: "",
            payment_status: "",
            from_date: "",
            to_date: "",
        };
    }

    async function fetchExportJobs() {
        const { data } = await axiosInstance.get("/admin/export-jobs");
        exportJobs.value = data.export_jobs || [];
        return data;
    }

    async function startBookingsExport() {
        if (exporting.value) return;

        exporting.value = true;
        try {
            const { data } = await axiosInstance.post("/admin/export-bookings");
            await fetchExportJobs();
            return data;
        } catch (error) {
            await fetchExportJobs();
            throw error;
        } finally {
            exporting.value = false;
        }
    }

    async function downloadExport(jobId) {
        const response = await axiosInstance.get(`/admin/export/${jobId}/download`, {
            responseType: "blob",
        });

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `admin_bookings_${jobId}.csv`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    }

    return {
        allBookings,
        loadingBookings,
        filters,
        exportJobs,
        exporting,
        fetchAllBookings,
        resetFilters,
        fetchExportJobs,
        startBookingsExport,
        downloadExport,
    };
});

import router from "@/router";

router
export default function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');
    localStorage.removeItem('username');
    router.push({ name: 'login' });
}     

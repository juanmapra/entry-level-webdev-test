import { createRouter, createWebHistory } from "vue-router";
import UsersTable from "../views/UsersTable.vue";
import UserDetails from '../views/UserDetails.vue';

const routes = [
    {
        path: '/',
        redirect: '/users'
    },
    {
        path: '/users',
        name: 'UsersTable',
        component: UsersTable
    },
    {
        path: '/users/:_id',
        name: 'userDetails',
        component: UserDetails,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;
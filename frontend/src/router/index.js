import { createRouter, createWebHistory } from "vue-router";
import ChatView from "@/views/ChatView.vue"; 
import UserView from "@/views/UserView.vue";

// Available pages
const routes = [
  { path: "/", component: ChatView },
  { path: "/user", component: UserView }
];

const router = createRouter({
  history: createWebHistory(), // Enables modern browser history mode
  routes
});

export default router;

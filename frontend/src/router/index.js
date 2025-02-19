import { createRouter, createWebHistory } from "vue-router";
import ChatView from "@/views/ChatView.vue"; 

// Available pages
const routes = [
  { path: "/", component: ChatView }
];

const router = createRouter({
  history: createWebHistory(), // Enables modern browser history mode
  routes
});

export default router;

<template>
    <div class="layout">
      <HeaderBar :isSidebarOpen="isSidebarOpen" @toggleSidebar="toggleSidebar" />
      <SidebarMenu :isOpen="isSidebarOpen" @toggleSidebar="toggleSidebar" />
      <main>
        <Chat />
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import HeaderBar from "@/components/HeaderBar.vue";
  import SidebarMenu from "@/components/SidebarMenu.vue";
  import Chat from "@/components/Chat.vue";
  
  const isSidebarOpen = ref(false);
  
  const toggleSidebar = () => {
    isSidebarOpen.value = !isSidebarOpen.value;
  };
  </script>
  
  <style scoped>
  .layout {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  
  main {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
  }
  </style>
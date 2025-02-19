<template>
  <div class="layout">
    <HeaderBar 
      :is-sidebar-open="isSidebarOpen" 
      @toggle-sidebar="handleSidebarToggle" 
    />
    <SidebarMenu 
      :is-open="isSidebarOpen" 
      @toggle-sidebar="handleSidebarToggle" 
    />
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
  
  const handleSidebarToggle = () => {
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
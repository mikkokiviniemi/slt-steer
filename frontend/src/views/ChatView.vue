<template>
  <div class="layout">
    <HeaderBar 
      :is-sidebar-open="isSidebarOpen" 
      @toggle-sidebar="handleSidebarToggle" 
    />
    <SidebarMenu 
      :is-open="isSidebarOpen" 
      @toggle-sidebar="handleSidebarToggle" 
      @open-patient-form="openPatientForm"
    />
    <main>
      <Chat
        :external-show-form="showForm"
        @update:external-show-form="showForm = $event"
      />
    </main>
  </div>
</template>
  
<script setup>
import { ref } from "vue";
import HeaderBar from "@/components/HeaderBar.vue";
import SidebarMenu from "@/components/SidebarMenu.vue";
import Chat from "@/components/Chat.vue";

const isSidebarOpen = ref(false);
const showForm = ref(false);

const handleSidebarToggle = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const openPatientForm = () => {
  showForm.value = true;
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

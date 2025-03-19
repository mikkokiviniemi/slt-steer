<template>
  <aside :class="['sidebar', { open: isOpen }]">
    <ul>
      <li><a href="#">Home</a></li>
      <li><a href="#">Settings</a></li>
      <li><a href="#">Logout</a></li>
      <li><a href="#" @click.prevent="openPatientForm">Esitietolomake</a></li>
    </ul>
  </aside>

  <SettingsModal
    v-if="settingsOpen"
    @close="settingsOpen = false"
  />
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

import { ref } from "vue";
import SettingsModal from "./SettingsModal.vue";

defineProps({
  isOpen: Boolean
});

const emit = defineEmits(["open-patient-form"]);

const openPatientForm = () => {
  emit("open-patient-form");
};

// Temporarily commented out
/*
const emit = defineEmits(["toggle-sidebar"]);

const handleSidebarToggle = () => {
  emit("toggle-sidebar");
};
*/

const settingsOpen = ref(false);
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 90px; /* Match header height */
  left: -250px;
  height: calc(100% - 90px); /* Adjust height to avoid overlapping header */
  background: var(--border-color);
  color: var(--text-light);
  padding: 30px 50px;
  transition: left 0.2s;
  font-size: 1rem;
  font-family: 'Arial', sans-serif; /* Sama fontti kuin chat-ikkunan nappuloissa */
}

/* Responsiivisuus eri näyttöleveydellä */
@media (max-width: 768px) {
  .sidebar {
    top: 80px;
    height: calc(100% - 80px);
  }
}

@media (max-width: 480px) {
  .sidebar {
    top: 70px;
    height: calc(100% - 70px);
  }
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

a {
  color: white;
  text-decoration: none;
  font-size: 16px;
  font-family: 'Arial', sans-serif;
  transition: color 0.2s ease-in-out;
  cursor: pointer;
  padding: 8px 0;

}

a:hover {
  color: #005b96;
}

.sidebar.open {
  left: 0;
}


.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  display: block;
  margin-bottom: 10px;
}
</style>

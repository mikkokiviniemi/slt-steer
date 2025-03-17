<template>
  <aside :class="['sidebar', { open: isOpen }]">
    <ul>
      <li><a href="#"><p>{{ $t("home") }}</p></a></li>
      <li>
        <a
          href="#"
          @click="settingsOpen = true"
        >{{ $t("settings") }}</a>
      </li>
      <li><a href="#">{{ $t("logout") }}</a></li>
    </ul>
  </aside>

  <SettingsModal
    v-if="settingsOpen"
    @close="settingsOpen = false"
  />
</template>

<script setup>
import { ref } from "vue";
import SettingsModal from "./SettingsModal.vue";

defineProps({
  isOpen: Boolean
});

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
  top: 60px;
  left: -250px;
  height: 100%;
  background: var(--border-color); /* Light Blue (Not to be same as Header bar) */
  color: var(--text-light); /* White */
  padding-top: 30px;
  padding-right: 50px;
  padding-bottom: 10px;
  padding-left: 50px;
  transition: left 0.2s;
  font-size: 1rem;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px; /* Adds a 10px gap between each list item */ 
}

a {
  color: white;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.2s ease-in-out;
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
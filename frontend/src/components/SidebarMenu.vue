<template>
  <aside :class="['sidebar', { open: isOpen }]">
    <ul>
      <li><a href="#"><p>{{ $t("home") }}</p></a></li>
      <li>
        <a
          href="#"
          @click="settingsOpen = true"
        >{{ $t("settings.title") }}</a>
      </li>
      <li><a href="#">{{ $t("logout") }}</a></li>
      <li>
        <a
          href="#"
          @click.prevent="openPatientForm"
        >{{ $t("form") }}</a>
      </li>
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

const settingsOpen = ref(false);
</script>

<style scoped>
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
</style>

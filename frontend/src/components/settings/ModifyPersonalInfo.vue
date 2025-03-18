<template>
  <div class="settings-section">
    <h2>{{ $t("modifyPersonalInfo.title") }}</h2>
    <input
      type="text"
      :placeholder="namePlaceholder"
    >
    <input
      type="number"
      :placeholder="agePlaceholder"
    >
    <select>
      <option>{{ $t("modifyPersonalInfo.male") }}</option>
      <option>{{ $t("modifyPersonalInfo.female") }}</option>
      <option>{{ $t("modifyPersonalInfo.other") }}</option>
    </select>
    <button>{{ $t("modifyPersonalInfo.save") }}</button>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

// Käännökset placeholderille
const namePlaceholder = computed(() => t('modifyPersonalInfo.name'));
const agePlaceholder = computed(() => t('modifyPersonalInfo.age'));
</script>

  <style scoped>
@import "@/assets/settingsstyles.css";
  </style>
<template>
  <div class="settings-section">
    <h2>{{ $t("login.title") }}</h2>
    <input
      type="text"
      :placeholder="namePlaceholder"
    >
    <input
      type="password"
      :placeholder="passwordPlaceholder"
    >
    <button>{{ $t("login.logIn") }}</button>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

// Käännökset placeholderille
const namePlaceholder = computed(() => t('login.username'));
const passwordPlaceholder = computed(() => t('login.password'));
</script>

<style scoped>
@import "@/assets/settingsstyles.css";
</style>
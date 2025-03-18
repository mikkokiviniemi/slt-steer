<template>
  <div class="settings-section">
    <h2>{{ $t("accessibility.title") }}</h2>
    <p>{{ $t("accessibility.screenReader") }}</p>
    <label class="checkbox-label">
      <input
        type="checkbox"
        class="checkbox-input"
      >
      <span class="checkbox-custom" />
      {{ $t("accessibility.enable") }}
    </label>
  </div>
</template>

<style scoped>
@import "@/assets/settingsstyles.css";
</style>
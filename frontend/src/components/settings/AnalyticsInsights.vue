<template>
  <div class="settings-section">
    <h2>{{ $t("analytics.title") }}</h2>
    <p>{{ $t("analytics.usageStats") }}</p>
    <label>
      <input type="checkbox"> {{ $t("analytics.enableTracking") }}
    </label>
  </div>
</template>

<style scoped>
@import "@/assets/settingsstyles.css";
</style>
<template>
  <div class="settings-section">
    <h2>{{ $t("personalInfo.title") }}</h2>
    <p><strong>{{ $t("personalInfo.name") }}</strong> John Doe</p>
    <p><strong>{{ $t("personalInfo.age") }}</strong> 25</p>
    <p><strong>{{ $t("personalInfo.gender") }}</strong> {{ $t("modifyPersonalInfo.male") }}</p>
  </div>
</template>
  
  <style scoped>
@import "@/assets/settingsstyles.css";
  </style>
<template>
  <header class="header">
    <!-- Sidebar Toggle Button -->
    <button 
      class="sidebar-toggle" 
      @click="handleSidebarToggle"
    >
      <FontAwesomeIcon :icon="isSidebarOpen ? 'times' : 'bars'" />
    </button>

    <div class="logo-container">
      <img 
        src="@/assets/logo.png" 
        alt="HeartWise Logo" 
        class="logo" 
      >
    </div>

    <div class="language-selector">
      <select 
        v-model="locale" 
        @change="changeLanguage"
      >
        <option value="fi">
          {{ $t("fin") }}
        </option>
        <option value="en">
          {{ $t("eng") }}
        </option>
      </select>
    </div>
  </header>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { watch } from "vue";

defineProps({
  "isSidebarOpen" : Boolean
}); // Prop for sidebar state

const emit = defineEmits(["toggle-sidebar"]);
const { locale } = useI18n();
const handleSidebarToggle = () => {
  emit("toggle-sidebar");
};

const changeLanguage = (event) => {
  const newLocale = event.target.value;
  locale.value = newLocale;
  localStorage.setItem("selectedLanguage", newLocale);
  window.location.reload();
  //console.log("Kieli vaihdettu", locale.value);
}

watch(locale, (newLocale) => {
  localStorage.setItem("selectedLanguage", newLocale);
  location.reload(); // Jeesusteippiratkaisu; päivittää koko sivun
});

</script>

<style scoped>

/* Responsive Design */
@media (max-width: 768px) {
  .header {
    height: 80px; /* Slightly smaller for tablets */
    padding: 12px;
  }

  .sidebar-toggle {
    font-size: 22px;
  }

  .logo {
    max-width: 140px;
    max-height: 60px;
  }

  .language-selector select {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .header {
    height: 70px; /* Smaller header for mobile */
    padding: 10px;
  }

  .sidebar-toggle {
    font-size: 20px;
  }

  .logo {
    max-width: 120px;
    max-height: 50px;
  }

  .language-selector select {
    font-size: 12px;
  }
}
</style>

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
        v-model="selectedLanguage" 
        @change="changeLanguage"
      >
        <option value="fi">
          Finnish
        </option>
        <option value="en">
          English
        </option>
      </select>
    </div>
  </header>
</template>

<script setup>
import { ref } from "vue";

defineProps({
  "isSidebarOpen" : Boolean
}); // Prop for sidebar state

const emit = defineEmits(["toggle-sidebar"]);

const handleSidebarToggle = () => {
  emit("toggle-sidebar");
};

const selectedLanguage = ref("fi");

const changeLanguage = () => {
    console.log("Language changed to:", selectedLanguage.value);    
    // Add logic to change the language globally in your app if needed
}

</script>

<style scoped>
.header {
    display: flex;
    align-items: center;
    justify-content: space-between; /* Pushes items to left, center, right */
    height: 90px; /* Increased height */
    padding: 15px 25px; /* Adjusted padding */
    background-color: var(--primary-color);
    color: var(--text-light);
}

.sidebar-toggle {
  background: none;
  border: none;
  color: var(--text-light);
  font-size: 24px; /* Increased icon size */
  cursor: pointer;
  padding: 15px;
}

.logo-container {
  flex: 1; /* Allows logo to be centered */
  display: flex;
  justify-content: center;
}

.logo {
  width: auto;
  height: 80px; /* Increased logo size */
  max-height: 100%;
}

.language-selector select {
  padding: 8px;
  font-size: 16px;
  background: var(--background-dark);
  color: var(--text-light);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
}

/* When the dropdown is open (focused) */
.language-selector select:focus {
  background: var(--background-light);
  color: var(--primary-color);
  border-color: var(--primary-color);
  outline: none;
}

/* When hovering over the dropdown */
.language-selector select:hover {
  background: var(--background-light);
  color: var(--primary-color);
}

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
    height: 70px;
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
    height: 60px;
  }

  .language-selector select {
    font-size: 12px;
  }
}
</style>

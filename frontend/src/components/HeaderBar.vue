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
    justify-content: space-between; /*Pushes items to left, center, right*/
    height: 60px;
    padding: 10px 20px;
    background-color: var(--primary-color);
    color: var(--text-light);
}

.sidebar-toggle {
  background: none;
  border: none;
  color: var(--text-light);
  font-size: 20px;
  cursor: pointer;
  padding: 10px;
}

.logo-container
{
  flex: 1; /*Allows logo to be centered*/
  display: flex;
  justify-content: center;
}

.logo
{
  width: auto;
  height: 60px; /*Adjust size as needed*/
}

.language-selector select 
{
  padding: 5px;
  font-size: 14px;
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
@media (max-width: 768px) 
{
  .header 
  {
    padding: 10px;
  }

  .sidebar-toggle {
      font-size: 18px;
    }

  .logo 
  {
    width: 100px;
    max-height: 40px;
  }

  .language-selector select 
  {
    font-size: 12px;
  }
}

@media (max-width: 480px) 
{
  .header 
  {
    padding: 8px;
  }

  .sidebar-toggle {
      font-size: 16px;
    }

  .logo 
  {
    width: 100px;
    max-height: 40px;
  }

  .language-selector select 
  {
    font-size: 12px;
  }
}

</style>
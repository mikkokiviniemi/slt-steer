<template>
    <header class="header">
      <!-- Sidebar Toggle Button -->
      <button class="sidebar-toggle" @click="$emit('toggleSidebar')">
        <font-awesome-icon :icon="isSidebarOpen ? 'times' : 'bars'" />
      </button>

      <div class="logo-container">
        <img src="@/assets/logo.png" alt="HeartWise Logo" class="logo" />
      </div>

      <div class="language-selector">
        <select v-model="selectedLanguage" @change="changeLanguage">
          <option value="fi">Finnish</option>
          <option value="en">English</option>
        </select>
      </div>
    </header>
</template>

<script setup>
import { ref } from "vue";

defineProps(["isSidebarOpen"]); // Prop for sidebar state

const selectedLanguage = ref("fi");

const changeLanguage = () => {
    console.log("Language changed to:", selectedLanguage.value);
}
</script>

<style scoped>
.header {
    display: flex;
    align-items: center;
    justify-content: space-between; /*Pushes items to left, center, right*/
    height: 20px;
    padding: 10px 20px;
    background: #333;
    color: rgb(255, 255, 255);
}

.sidebar-toggle {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
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
  height: 40px; /*Adjust size as needed*/
}

.language-selector select 
{
  padding: 5px;
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 768px) 
{
  .header 
  {
    flex-direction: row;
    padding: 10px;
  }

  .hamburger 
  {
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
    flex-direction: row;
    padding: 8px;
  }

  .hamburger 
  {
    font-size: 16px;
  }

  .logo 
  {
    width: 90px;
    max-height: 35px;
  }

  .language-selector select 
  {
    font-size: 12px;
    padding: 3px;
  }
}

</style>
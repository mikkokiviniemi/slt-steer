<template>
    <header class="header">
      <!-- Sidebar Toggle Button -->
      <button class="sidebar-toggle" @click="$emit('toggleSidebar')">
        <font-awesome-icon :icon="isSidebarOpen ? faTimes : faBars" />
      </button>
  
      <div class="logo-container">
        <img src="./assets/logo.png" alt="HeartWise Logo" class="logo" />
      </div>
  
    </header>
  </template>
  
  <script setup>
  // Import the FontAwesomeIcon component
  import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
  // Import the icons you need
  import { faBars, faTimes } from "@fortawesome/free-solid-svg-icons";
  
  // Define props
  defineProps({
    isSidebarOpen: Boolean, // Prop for sidebar state with type validation
  });
  
  </script>
  
  <style scoped>
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between; /* Pushes items to left, center, right */
    height: 60px; /* Adjusted height for better visibility */
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
    padding: 10px; /* Added padding for better click area */
  }
  
  .logo-container {
    flex: 1; /* Allows logo to be centered */
    display: flex;
    justify-content: center;
  }
  
  .logo {
    width: auto;
    height: 60px; /* Adjust size as needed */
  }
  
  .language-selector select {
    padding: 5px;
    font-size: 14px;
    background: #444; /* Added background for better visibility */
    color: white;
    border: 1px solid #666;
    border-radius: 4px;
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .header {
      padding: 10px;
    }
  
    .sidebar-toggle {
      font-size: 18px;
    }
  
    .logo {
      width: 100px;
      max-height: 40px;
    }
  
    .language-selector select {
      font-size: 12px;
    }
  }
  
  @media (max-width: 480px) {
    .header {
      padding: 8px;
    }
  
    .sidebar-toggle {
      font-size: 16px;
    }
  
    .logo {
      width: 90px;
      max-height: 35px;
    }
  
    .language-selector select {
      font-size: 12px;
      padding: 3px;
    }
  }
  </style>
  
<template>
  <aside :class="['sidebar', { open: isOpen }]">
    <button 
      class="close-btn" 
      @click="handleSidebarToggle"
    >
      ✖
    </button>
    <ul>
      <li><a href="#">Home</a></li>
      <!--<li><a href="#">Settings</a></li>
      <li><a href="#">Logout</a></li>-->
    </ul>
  </aside>
</template>
  
  <script setup>
  defineProps({
    isOpen: Boolean
  });

  const emit = defineEmits(["toggle-sidebar"]);

  const handleSidebarToggle = () => {
    emit("toggle-sidebar");
  };
  </script>
  
  <style scoped>
  .sidebar {
    position: fixed;
    left: -250px;
    height: 100%;
    background: var(--primary-color); /* Dark Blue */
    color: var(--text-light); /* White */
    padding: 20px;
    transition: left 0.2s;
    font-size: 1rem;
  }
  
  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 10px; /* Adds a 10px gap between each list item */ 
  }
  a {
    color: white;
    text-decoration: none;
    font-size: 16px;
    transition: color 0.2s ease-in-out;
  }
  a:hover {
    color: #005b96;
  }
  .sidebar.open {
    left: 0;
  }
  
  .close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 18px;
    cursor: pointer;
    display: block;
    margin-bottom: 10px;
  }
  </style>
  
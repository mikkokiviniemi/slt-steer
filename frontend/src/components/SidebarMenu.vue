<template>
    <aside :class="['sidebar', { open: isOpen }]">
      <button class="close-btn" @click="$emit('toggleSidebar')">✖</button>
      <ul>
        <li><a href="#">Home</a></li>
        <li><a href="#">Settings</a></li>
        <li><a href="#">Logout</a></li>
      </ul>
    </aside>
  </template>
  
  <script setup>
  defineProps(["isOpen"]);
  </script>
  
  <style scoped>
  .sidebar {
    position: fixed;
    left: -250px;
    top: 0;
    width: px;
    height: 100%;
    background: #222;
    color: green;
    padding: 20px;
    transition: left 0.3s;
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
  
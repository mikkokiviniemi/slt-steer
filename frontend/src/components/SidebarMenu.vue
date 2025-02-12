<template>
    <aside :class="['sidebar', { open: isOpen }]">
      <ul>
        <li><a href="">Home</a></li>
        <li><a href="">Settings</a></li>
        <li><a href="">Logout</a></li>
        <li class="language-selector">
            <select v-model="selectedLanguage" @change="changeLanguage">
            <option value="fi">Finnish</option>
            <option value="en">English</option>
            </select>
        </li>
      </ul>
    </aside>
  </template>

  <script setup>
  import { ref } from "vue";
  defineProps(["isOpen"]);
  const selectedLanguage = ref("fi");
  
  const changeLanguage = () => {
    console.log("Language changed to:", selectedLanguage.value);
    // Add logic to change the language globally in your app if needed
  };
  </script>

<style scoped>
.sidebar {
  position: fixed;
  left: -250px;
  top: 80px;
  height: 100%;
  background: #222;
  color: #005b96;
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
</style>
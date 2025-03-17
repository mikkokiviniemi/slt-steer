<template>
  <div class="settings-section">
    <h2>Modify Personal Info</h2>
    <input
      type="text"
      placeholder="Name"
    >
    <input
      type="number"
      placeholder="Age"
    >
    <select>
      <option>Male</option>
      <option>Female</option>
      <option>Other</option>
    </select>
    <button>Save</button>
  </div>
</template>
  
  <style scoped>
  .settings-section {
    padding: 20px;
  }
  input, select, button {
    display: block;
    margin: 10px 0;
  }
  </style>
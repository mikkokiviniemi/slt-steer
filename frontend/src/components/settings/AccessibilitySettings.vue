<template>
  <div class="settings-section">
    <h2>Accessibility Settings</h2>
    <p>Enable screen reader support</p>
    <label class="checkbox-label">
      <input type="checkbox" class="checkbox-input" />
      <span class="checkbox-custom"></span>
      Enable
    </label>
  </div>
</template>

<style scoped>
.settings-section {
  padding: 16px;
}

h2 {
  margin: 0 0 16px;
  font-size: 20px;
  color: #333;
}

p {
  margin: 0 0 12px;
  color: #666;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #333;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 16px;
  height: 16px;
  border: 2px solid #666;
  border-radius: 4px;
  position: relative;
  transition: background 0.2s, border-color 0.2s;
}

.checkbox-input:checked + .checkbox-custom {
  background: #007bff;
  border-color: #007bff;
}

.checkbox-input:checked + .checkbox-custom::after {
  content: "";
  position: absolute;
  top: 2px;
  left: 5px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
</style>
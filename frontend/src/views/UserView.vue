<script setup>
import { ref } from "vue";
import { getUser } from "@/services/api.js";

const user = ref(null);
const patientId = ref("");

const fetchUser = async () => {
  if (!patientId.value.trim()) return; // Prevent empty requests
  user.value = await getUser(patientId.value);
};
</script>

<template>
  <div>
    <input 
      v-model="patientId" 
      placeholder="Enter Patient ID"
    >  
    <button @click="fetchUser">
      Fetch
    </button>

    <pre v-if="user">
      {{ user }}
    </pre>
  </div>
</template>

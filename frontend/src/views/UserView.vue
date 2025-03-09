<script>
import { ref, onMounted } from "vue";
import { getUser } from "@/services/api.js";

// Testing file for fetching isnformation of single user

export default {
  setup() {
    const user = ref(null);
    const patientId = "P1001";

    onMounted(async () => {
      user.value = await getUser(patientId);
    });

    return { user };
  },
};
</script>

<template>
  <div>
    <h1>User Profile</h1>
    
    <div v-if="user">
      <p><strong>Name:</strong> {{ user.firstName }} {{ user.lastName }}</p>
      <p><strong>Date of Birth:</strong> {{ user.dateOfBirth }}</p>
      <p><strong>Preferred Language:</strong> {{ user.languageSettings.preferredLanguage }}</p>
      <p><strong>Available Languages:</strong> {{ user.languageSettings.availableLanguages.join(", ") }}</p>
      <p><strong>Weight:</strong> {{ user.weight }} kg</p>
      <p><strong>Height:</strong> {{ user.height }} cm</p>
    </div>

    <div v-else>
      <p>Loading user data...</p>
    </div>
  </div>
</template>

<style scoped>
h1 {
  color: #2c3e50;
}
</style>

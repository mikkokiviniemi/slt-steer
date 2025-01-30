<template>
  <div>
    <h1>Vue + FastAPI</h1>
    <button @click="fetchData">Fetch Data</button>
    <ul v-if="data.length">
      <li v-for="item in data" :key="item">{{ item }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return { data: [] };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/data");
        this.data = response.data.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }
  }
};
</script>

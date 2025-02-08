<template>
  <h1></h1>
  <div class="chat-container">
    <div class="messages">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.from === 'self' ? 'self' : 'other']"
      >
        <div class="message-content">{{ message.text }}</div>
      </div>
    </div>
    <form @submit.prevent="sendMessage" class="input-area">
      <input v-model="newMessage" type="text" placeholder="Type a number..." required />
      <button type="submit">Send</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";


//DATA FROM BACKEND THINGY
export default {
  name: "ChatComponent",
  data() {
    return {
      mapping: [],
      messages: [],
      newMessage: ""
    };
  },
  methods: {
    async fetchMapping() {
      const response = await axios.get("http://127.0.0.1:8000/api/data");
      this.mapping = response.data.data;
    },
    sendMessage() {
      if (this.newMessage.trim() === "") return;
      this.messages.push({ text: this.newMessage, from: "self" });
      const num = parseInt(this.newMessage, 10);
      let responseText = "";
      if (!isNaN(num) && num >= 1 && num <= this.mapping.length) {
        responseText = this.mapping[num - 1];
      } else {
        responseText = "no number";
      }
      this.messages.push({ text: responseText, from: "other" });
      this.newMessage = "";
    }
  },
  mounted() {
    this.fetchMapping();
  }
};
</script>

<style scoped>
.chat-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid;
  border-radius: 4px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  height: 80vh;
  box-sizing: border-box;
}

.messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 10px;
}

.message {
  margin-bottom: 8px;
  word-wrap: break-word;
}

.message.self {
  text-align: right;
}

.message.other {
  text-align: left;
}

.message-content {
  display: inline-block;
  padding: 8px 12px;
  border: 1px solid;
  border-radius: 4px;
  max-width: 80%;
}

.input-area {
  display: flex;
}

.input-area input {
  flex: 1;
  padding: 8px;
  border: 1px solid;
  border-radius: 4px;
  box-sizing: border-box;
}

.input-area button {
  margin-left: 5px;
  padding: 8px 12px;
  border: 1px solid;
  border-radius: 4px;
  background: none;
  cursor: pointer;
}

@media (max-width: 600px) {
  .chat-container {
    height: 90vh;
    padding: 5px;
  }
  .input-area input {
    padding: 6px;
  }
  .input-area button {
    padding: 6px 10px;
  }
  .message-content {
    padding: 6px 10px;
    max-width: 90%;
  }
}
</style>

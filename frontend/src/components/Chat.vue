<template>
  <div class="chat-container">
    <!-- Esitietolomake-modal -->
    <PatientForm 
      v-if="showForm" 
      @close="closePatientForm" 
    />

    <div class="messages">
      <!-- Tervetuloviesti, joka näytetään vain kerran ensimmäisenä viestinä -->
      <div
        v-if="welcomeMessageDisplayed"
        class="message other"
      >
        <div class="message-content">
          {{ $t("welcomeMessage") }}
          <a
            href="#"
            @click.prevent="openPatientForm"
          >{{ $t("fillForm") }}</a>.
          {{ $t("returnLater") }}
        </div>
      </div>

      <!-- Käyttäjän ja botin viestit -->
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.from === 'self' ? 'self' : 'other']"
      >
        <div
          class="message-content"
          v-html="message.text"
        />
      </div>
    </div>

    <form
      class="input-area"
      @submit.prevent="sendMessage"
    >
      <input
        v-model="newMessage"
        type="text"
        :placeholder="$t('prompt')"
        required
      >
      <button type="submit">
        <p>{{ $t("send") }}</p>
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import PatientForm from "./PatientForm.vue";
import { useI18n } from "vue-i18n"; // Lisätty kielituki

export default {
  name: "ChatComponent",
  components: {
    PatientForm,
  },
  props: {
    externalShowForm: Boolean,
  },
  setup() {
    const { t, locale } = useI18n(); // Hae kielituki
    return { t, locale };
  },
  data() {
    return {
      userId: "user123",
      messages: [],
      newMessage: "",
      showForm: false,
      welcomeMessageDisplayed: true, // Tervetuloviesti näytetään vain kerran
    };
  },
  watch: {
    externalShowForm(newVal) {
      this.showForm = newVal;
    },
  },
  methods: {
    openPatientForm() {
      this.showForm = true;
      this.$emit("update:externalShowForm", true);
    },
    closePatientForm() {
      this.showForm = false;
      this.$emit("update:externalShowForm", false);
    },
    async fetchMapping() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/data");
        this.mapping = response.data.data;
      } catch (error) {
        console.error(this.$t("data-error"), error);
      }
    },
    async sendMessage() {
      if (this.newMessage.trim() === "") return;

      // Lisää käyttäjän viesti chattiin
      this.messages.push({ text: this.newMessage, from: "self" });

      try {
        const response = await axios.post("http://127.0.0.1:8000/api/send", {
          message: this.newMessage,
        });

        // Lisää palvelimen vastaus chattiin
        this.messages.push({ text: response.data.reply, from: "other" });
      } catch (error) {
        console.error(this.$t("send-error"), error);
        this.messages.push({ text: this.$t("connection-error"), from: "other" });
      }

      // Tyhjennä syötekenttä
      this.newMessage = "";
    },
  },
};
</script>

<style scoped>
@media (max-width: 600px) {
  .logo {
    width: 150px;
  }

  .chat-container {
    height: 90vh;
    padding: 15px;
  }

  .message-content {
    font-size: 0.9rem;
  }

  .input-area input {
    padding: 8px;
  }

  .input-area button {
    padding: 8px 15px;
  }
}
</style>
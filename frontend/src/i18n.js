//npm install vue-i18n
import { createI18n } from "vue-i18n";
import fi from "./locales/fi.json";
import en from "./locales/en.json";

const savedLanguage = localStorage.getItem("selectedLanguage") || "fi";

const i18n = createI18n({
  legacy: false,  // Käytetään Composition API:ta
  locale: savedLanguage,   // Oletuskieli tai käyttäjän valinta
  fallbackLocale: "en",
  messages: { fi, en }
});

export default i18n;
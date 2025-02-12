import { createApp } from 'vue'
import App from './App.vue'
import router from "./router";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faBars, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(faBars, faTimes);

const app = createApp(App);
app.component("font-awesome-icon", FontAwesomeIcon); // ✅ Register globally
app.use(router);
app.mount('#app')

<template>
  <div>
    <HeaderBar :isSidebarOpen="isSidebarOpen" @toggleSidebar="toggleSidebar" />
    <SidebarMenu :isOpen="isSidebarOpen" @toggleSidebar="toggleSidebar" />
    <ChatComponent/>
  </div>
</template>

<script>
import { ref } from "vue";
import ChatComponent from './components/Chat.vue';
import HeaderBar from "./components/HeaderBar.vue";
import SidebarMenu from "./components/SidebarMenu.vue";

export default {
  components: {
    ChatComponent,
    HeaderBar,
    SidebarMenu,
  },
  setup() {
    const isSidebarOpen = ref(false);

    const toggleSidebar = () => {
      isSidebarOpen.value = !isSidebarOpen.value;
    };

    return {
      isSidebarOpen,
      toggleSidebar,
    };
  },
};

</script>
<style>
body 
{
  margin: 0px;
}
</style>

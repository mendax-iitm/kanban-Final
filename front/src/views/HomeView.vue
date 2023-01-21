<template>
  <div class="container">
    <div v-if="dash">
      <h5>Welcome {{ username }}</h5>
      <NavBar @dashchange="dash = $event" />
      <Dashboard />
    </div>
    <div v-if="!dash">
      <img alt="Vue logo" src="../assets/kanba.webp" />
      <Home msg="Welcome to Kanban App" />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from "@/components/NavBar.vue";
import Home from "@/components/Home.vue";
import Dashboard from "@/components/Dashboard.vue";
export default {
  name: "HomeView",
  data: function () {
    return {
      dash: false,
      username: "",
    };
  },
  components: {
    Home,
    NavBar,
    Dashboard,
  },
  mounted: function () {
    if (localStorage.getItem("access_token")) {
      this.dash = true;
      this.username = localStorage.getItem("username");
    } else {
      this.dash = false;
    }
  },
};
</script>

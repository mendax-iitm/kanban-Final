<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h8 class="text-success">
      Subtracting from your list of priorities is as important as adding to it.
    </h8>
    <div>
      Already a User?
      <router-link class="link-primary" to="/login"> Sign-in</router-link>
    </div>
    <div>
      New User?<router-link class="link-primary" to="/register"
        >Register</router-link
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
  props: {
    msg: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

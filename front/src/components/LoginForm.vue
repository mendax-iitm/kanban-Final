<template>
  <main class="form-signin w-50 m-auto">
    <form @submit.prevent="handleFormSubmit">
      <!-- <img class="mb-4" src="../assets/brand/bootstrap-logo.svg" alt="" width="72" height="57"> -->
      <div v-if="errStatus">
        <br />
        <p class="alert alert-danger">{{ errormsg }}</p>
      </div>
      <h1 class="h3 mb-3 fw-normal">Please sign in</h1>

      <div class="form-floating mb-3">
        <input
          type="text"
          v-model="username"
          class="form-control"
          id="floatingInput"
          placeholder="username"
        />
        <label for="floatingInput">Username</label>
        <div class="error" v-if="!$v.username.required">
          Username is required
        </div>
      </div>

      <div class="form-floating mb-3">
        <input
          type="password"
          v-model="password"
          class="form-control"
          id="floatingPassword"
          placeholder="Password"
        />
        <label for="floatingPassword">Password</label>
        <div class="error" v-if="!$v.password.required">
          Password is required.
        </div>
        <div class="error" v-if="!$v.password.minLength">
          Password must have at least
          {{ $v.password.$params.minLength.min }} letters.
        </div>
      </div>

      <!-- <div class="checkbox mb-3">
        <label>
          <input type="checkbox" value="remember-me" /> Remember me
        </label>
      </div> -->
      <button class="w-100 btn btn-lg btn-primary" type="submit">
        Sign in
      </button>
      <p class="mt-5 mb-3 text-muted">&copy; mendax</p>
    </form>
    <div class="text-center fw-bold">
      New User?<router-link class="link-primary" to="/register"
        >Register</router-link
      >
    </div>
  </main>
</template>

<script>
import router from "@/router";
import { required, minLength } from "vuelidate/lib/validators";
export default {
  name: "LoginForm",
  data: function () {
    return {
      username: "",
      password: "",
      errormsg: "",
      errStatus: false,
    };
  },
  validations: {
    username: { required },
    password: { required, minLength: minLength(6) },
  },
  methods: {
    handleFormSubmit: function () {
      console.log("before touch");
      this.$v.$touch();
      if (this.$v.$error) {
        console.log("fail");
      } else {
        fetch("http://127.0.0.1:8081/api/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              alert("Response not ok");
            }
            return response.json();
          })
          .then((data) => {
            console.log(data.msg);
            if (data.status) {
              console.log(data.status);
              console.log(data.access_token);
              localStorage.setItem("access_token", data.access_token);
              localStorage.setItem("username", this.username);
              router.push("/");
            } else {
              this.errStatus = true;
              this.errormsg = data.msg;
              this.username = null;
              this.password = null;
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
  },
};
</script>
<style scoped>
.error {
  text-align: left;
  color: red;
}
</style>

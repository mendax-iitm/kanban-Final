<template>
  <main class="form-register w-50 m-auto">
    <form @submit.prevent="handleFormRegister">
      <!-- <img class="mb-4" src="../assets/brand/bootstrap-logo.svg" alt="" width="72" height="57"> -->
      <h1 class="h3 mb-3 fw-normal">Register</h1>

      <div class="form-floating">
        <input
          type="text"
          v-model="username"
          class="form-control"
          placeholder="username"
        />
        <label for="floatingInput">Username</label>
        <div class="error" v-if="!$v.username.required">
          Username is required
        </div>
      </div>
      <div class="form-floating">
        <input
          type="email"
          v-model="email"
          class="form-control"
          placeholder="email"
        />
        <label for="floatingInput">Email</label>
        <div class="error" v-if="!$v.email.required">Email is required</div>
        <div class="error" v-if="!$v.email.email">
          Enter correct email format
        </div>
      </div>
      <div class="form-floating">
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
      <div class="form-floating">
        <input
          type="password"
          v-model="repeatPassword"
          class="form-control"
          id="floatingPassword2"
          placeholder="Password"
        />
        <label for="floatingPassword">Type Password Again</label>
        <div class="error" v-if="!$v.repeatPassword.sameAsPassword">
          Passwords must be identical.
        </div>
      </div>

      <!-- <div class="checkbox mb-3">
          <label>
            <input type="checkbox" value="remember-me" /> Remember me
          </label>
        </div> -->
      <button class="w-100 btn btn-lg btn-primary" type="submit">
        Register
      </button>
      <p class="mt-5 mb-3 text-muted">&copy; mendax</p>
    </form>
    <div class="text-center">
      Already a User?
      <router-link class="link-primary" to="/login"> Sign-in</router-link>
    </div>
  </main>
</template>

<script>
import router from "@/router";
import { required, minLength, sameAs, email } from "vuelidate/lib/validators";
export default {
  name: "RegisterForm",
  data: function () {
    return {
      username: "",
      password: "",
      errormsg: "",
      email: "",
      repeatPassword: "",
      errStatus: false,
    };
  },
  validations: {
    username: { required },
    email: { required, email },
    password: { required, minLength: minLength(6) },
    repeatPassword: { sameAsPassword: sameAs("password") },
  },
  methods: {
    handleFormRegister: function () {
      console.log("before touch");
      this.$v.$touch();
      if (this.$v.$error) {
        console.log("fail");
      } else {
        fetch("http://127.0.0.1:8081/api/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
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
            if (data.status) {
              localStorage.setItem("access_token", data.access_token);
              localStorage.setItem("username", this.username);
              router.push("/");
            } else {
              this.errStatus = true;
              this.errormsg = data.msg;
              this.username = null;
              this.password = null;
              this.email = null;
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

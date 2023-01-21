<template>
  <main class="form-signin w-50 m-auto">
    <form @submit.prevent="AddList">
      <h1 class="h3 mb-3 fw-normal">Add List</h1>
      <div v-if="errStatus">
        <br />
        <p class="alert alert-danger">{{ errormsg }}</p>
      </div>
      <div class="form-floating mb-3">
        <input
          type="text"
          v-model="title"
          class="form-control"
          id="floatingInput"
          placeholder="Title"
        />
        <label for="floatingInput">Title</label>
        <div class="error" v-if="!$v.title.required">Title is required</div>
      </div>

      <button class="w-100 btn btn-lg btn-primary" type="submit">
        Add List
      </button>
    </form>
    <div class="text-center fw-bold">
      Don't want to create List?<router-link class="link-primary" to="/"
        >Back to Home</router-link
      >
    </div>
  </main>
</template>

<script>
import router from "@/router";
import { required } from "vuelidate/lib/validators";
export default {
  name: "AddList",
  data: function () {
    return {
      title: "",
      errStatus: false,
      errormsg: "",
    };
  },
  validations: {
    title: { required },
  },
  methods: {
    AddList: function () {
      this.$v.$touch();
      if (this.$v.$error) {
        console.log("fail");
      } else {
        fetch(`http://127.0.0.1:8081/api/list`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
          body: JSON.stringify({
            title: this.title,
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
              router.push("/");
            } else {
              this.errStatus = true;
              this.errormsg = data.error_message;
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

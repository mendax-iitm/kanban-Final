<template>
  <main class="form-signin w-50 m-auto">
    <form @submit.prevent="EditCard">
      <!-- <img class="mb-4" src="../assets/brand/bootstrap-logo.svg" alt="" width="72" height="57"> -->
      <div v-if="errStatus">
        <br />
        <p class="alert alert-danger">{{ errormsg }}</p>
      </div>
      <h1 class="h3 mb-3 fw-normal">Edit card</h1>

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

      <div class="form-floating mb-3">
        <textarea
          type="textarea"
          rows="10"
          v-model="content"
          class="form-control"
          id="floatingContent"
          placeholder="Please enter your Content"
        ></textarea>
        <label for="floatingContent">Content</label>
        <div class="error" v-if="!$v.content.required">
          Content is required.
        </div>
      </div>
      <div class="form-floating mb-3">
        <input
          type="date"
          v-model="deadline"
          class="form-control"
          id="floatingDeadline"
          placeholder="Please enter your Content"
        />
        <label for="floatingDeadline">Deadline</label>
        <div class="error" v-if="!$v.deadline.required">
          Deadline is required.
        </div>
        <div class="error" v-if="!$v.deadline.minValue">
          Deadline cannot be lower than today
        </div>
      </div>
      <div class="form-floating mb-3">
        <select
          name="move-list"
          id="move-list"
          v-model="list_id"
          class="form-control"
        >
          <option v-for="list in list_items" :key="list.id" :value="list.id">
            {{ list.title }}
          </option>
        </select>
        <label for="move_list">Choose a list to move:</label>
      </div>

      <button class="w-100 btn btn-lg btn-primary" type="submit">
        Edit Card
      </button>
    </form>
    <div class="text-center fw-bold">
      Don't want to edit card?<router-link class="link-primary" to="/"
        >Back to Home</router-link
      >
    </div>
  </main>
</template>

<script>
import router from "@/router";
import { required } from "vuelidate/lib/validators";
export default {
  name: "EditCard",
  data: function () {
    return {
      title: "",
      content: "",
      deadline: "",
      list_id: "",
      list_items: [],
      errStatus: false,
      errormsg: null,
    };
  },
  validations: {
    title: { required },
    content: { required },
    deadline: {
      required,
      minValue(val) {
        const today = new Date();

        let day = today.getDate();
        let month = today.getMonth();
        let year = today.getFullYear();
        return new Date(val) > new Date(year, month, day);
      },
    },
  },
  methods: {
    EditCard: function () {
      console.log("before touch");
      this.$v.$touch();
      if (this.$v.$error) {
        console.log("fail");
      } else {
        fetch(`http://127.0.0.1:8081/api/card/${this.$route.params.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
          body: JSON.stringify({
            title: this.title,
            content: this.content,
            deadline: this.deadline,
            list_move_id: this.list_id,
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
              console.log("success");
              router.push("/");
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
  },
  mounted: function () {
    fetch(`http://127.0.0.1:8081/api/editcard/${this.$route.params.id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        Authorization: "Bearer " + localStorage.getItem("access_token"),
      },
    })
      .then((response) => {
        if (!response.ok) {
          alert("Response not ok");
        }
        return response.json();
      })
      .then((data) => {
        if (data.status) {
          this.deadline = data.deadline;
          this.title = data.card_data.title;
          this.content = data.card_data.content;
          this.list_id = data.card_data.list_id;
          this.list_items = data.list_items;
        } else {
          this.errStatus = true;
          this.errormsg = data.msg;
          this.title = null;
          this.content = null;
          this.deadline = null;
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style scoped>
.error {
  text-align: left;
  color: red;
}
</style>

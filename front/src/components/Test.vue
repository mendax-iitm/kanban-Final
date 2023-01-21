<template>
  <main class="form-signin w-50 m-auto" id="page">
    <router-link to="/login">Login</router-link>
    <form @submit.prevent="Testing">
      <!-- <img class="mb-4" src="../assets/brand/bootstrap-logo.svg" alt="" width="72" height="57"> -->

      <h1 class="h3 mb-3 fw-normal">Test API component</h1>
      <div class="form-floating mb-3">
        <input
          type="date"
          v-model="deadline"
          class="form-control"
          id="floatingInput"
          placeholder="username"
        />
        <label for="floatingInput">Input date</label>
      </div>
      <label for="move_list">Choose a list to move:</label>
      <select name="move-list" id="move-list" v-model="list_id">
        <option v-for="list in lists" :key="list.id" :value="list.id">
          {{ list.title }}
        </option>
      </select>
      <h1>{{ list_id }}</h1>
      <!-- <div v-for="card in allcards" :key="card.id">
        {{ card }}
      </div>

      <div v-if="errStatus">
        <br />
        <p class="alert alert-danger">{{ errormsg }}</p>
      </div> -->

      <!-- <div class="form-floating mb-3">
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
        </div> -->

      <!-- <div class="form-floating mb-3">
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
        </div> -->

      <!-- <div class="checkbox mb-3">
          <label>
            <input type="checkbox" value="remember-me" /> Remember me
          </label>
        </div> -->
      <button class="w-100 btn btn-lg btn-primary" type="submit">Test</button>
      <p class="mt-5 mb-3 text-muted">&copy; mendax</p>
    </form>
    <div id="chartContainer" style="width: 30%; float: left">
      I am getting this
      <canvas id="acquisitions"></canvas>
    </div>
  </main>
</template>

<script>
// import router from "@/router";
import Chart from "chart.js/auto";

export default {
  name: "TestingAPI",
  data: function () {
    return {
      allcards: [],
      errormsg: "",
      errStatus: false,
      deadline: "",
      list_id: 2,
      lists: [
        { id: 1, title: "one" },
        { id: 2, title: "two" },
        { id: 3, title: "three" },
        { id: 4, title: "four" },
      ],
      datachart: {
        labels: ["Completed", "Incomplete", "Passed"],
        datasets: [
          {
            label: "No. of tasks",
            backgroundColor: [
              "rgb(75, 192, 192)",
              "rgb(255, 205, 86)",
              "rgb(255, 99, 132)",
            ],
            data: [3, 5, 1],
          },
        ],
      },
      chart: null,
    };
  },

  methods: {
    Testing: function () {
      // console.log("before fetch");
      // fetch("http://127.0.0.1:8081/test123", {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //     "Access-Control-Allow-Origin": "*",
      //     Authorization: "Bearer " + localStorage.getItem("access_token"),
      //   },
      //   body: JSON.stringify({
      //     deadline: this.deadline,
      //   }),
      // })
      //   .then((response) => {
      //     if (!response.ok) {
      //       alert("Response not ok");
      //     }
      //     console.log(response);
      //     return response.json();
      //   })
      //   .then((data) => {
      //     console.log(data);
      //     if (data) {
      //       console.log("here it is");
      //       this.deadline = data.deadline;
      //       // localStorage.setItem("access_token", data.access_token);
      //       // localStorage.setItem("username", this.username);
      //       // this.allcards = data.lists;
      //       // console.log(data.cards[0]["title"]);
      //       // router.push("/");
      //     } else {
      //       this.errStatus = true;
      //       this.errormsg = data.msg;
      //     }
      //   })
      //   .catch((err) => {
      //     console.log(err);
      //   });
      // let csv = "id,title,\n";
      // this.lists.forEach((row) => {
      //   csv += Object.values(row).join(",");
      //   csv += "\n";
      // });
      // const anchor = document.createElement("a");
      // anchor.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
      // anchor.target = "_blank";
      // anchor.download = "nameYourFileHere.csv";
      // anchor.click();
      // const data = [
      //   { year: 2010, count: 10 },
      //   { year: 2011, count: 20 },
      //   { year: 2012, count: 15 },
      //   { year: 2013, count: 25 },
      //   { year: 2014, count: 22 },
      //   { year: 2015, count: 30 },
      //   { year: 2016, count: 28 },
      // ];
      new Chart(document.getElementById("acquisitions"), {
        type: "bar",
        data: {
          labels: this.datachart.labels,
          datasets: [
            {
              label: "Acquisitions by year",
              backgroundColor: [
                "rgb(75, 192, 192)",
                "rgb(255, 205, 86)",
                "rgb(255, 99, 132)",
              ],
              data: [1, 3, 5],
            },
          ],
        },
        options: {
          responsiveness: true,
        },
      });
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

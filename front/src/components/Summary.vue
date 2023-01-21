<template>
  <div class="main">
    <div class="container" id="reportPage">
      <h1 class="justify-content-center">Summary Page</h1>
      <div class="row">
        <div class="col m-1">
          <div class="card shadow" style="width: 10rem; min-height: 8rem">
            <div class="card-header">Lists Created</div>
            <div class="card-body">{{ listsnum }}</div>
          </div>
        </div>
        <div class="col m-1">
          <div class="card shadow" style="width: 10rem; min-height: 8rem">
            <div class="card-header">Cards Created</div>
            <div class="card-body">{{ cardsnum }}</div>
          </div>
        </div>
        <div class="col m-1">
          <div class="card shadow" style="width: 10rem; min-height: 8rem">
            <div class="card-header">Tasks to be done</div>
            <div class="card-body">{{ incomplete }}</div>
          </div>
        </div>
        <div class="col m-1">
          <div class="card shadow" style="width: 10rem; min-height: 8rem">
            <div class="card-header">Task Completed</div>
            <div class="card-body">{{ complete }}</div>
          </div>
        </div>
        <div class="col m-1">
          <div class="card shadow" style="width: 10rem; min-height: 8rem">
            <div class="card-header">Deadline Passed</div>
            <div class="card-body">{{ passed }}</div>
          </div>
        </div>
      </div>
      <div class="row m-3">
        <div
          id="chartContainer"
          class="justify-content-center m-auto"
          style="width: 50rem"
        >
          <!-- <canvas id="myChart"></canvas> -->
          <img alt="Bar chart" :src="'data:image/png;base64,' + img64" />"
        </div>
      </div>
      <div class="row m-3">
        <a @click="downloadPdf" class="nav-links" id="downloadPdf"
          >Download Report Page as PDF</a
        >
      </div>
      <br />
      <button @click="home" class="btn btn-primary">Back to Home Page</button>
    </div>
  </div>
</template>
<script>
// import Chart from "chart.js/auto";

import html2PDF from "jspdf-html2canvas";

export default {
  name: "Summary",
  data: function () {
    return {
      listsnum: 0,
      cardsnum: 0,
      incomplete: 0,
      complete: 0,
      passed: 0,
      img64: null,
    };
  },

  methods: {
    home: function () {
      this.$router.push("/");
    },
    downloadPdf: function () {
      //   console.log("print finished");
      html2PDF(document.getElementById("reportPage"), {
        jsPDF: {
          format: "a4",
        },
        imageType: "image/png",
        output: "./pdf/generate.pdf",
      });
    },
  },

  mounted: function () {
    fetch("http://127.0.0.1:8081/api/allcards", {
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
          let cards = data.all_lists;
          this.cardsnum = cards.length;
          this.listsnum = data.listnum;
          this.img64 = data.img;
          cards.forEach((element) => {
            if (parseInt(element.completed) == 1) {
              this.complete += 1;
            } else if (element.deadline_days < -1) {
              this.passed += 1;
            } else if (element.deadline_days >= -1) {
              this.incomplete += 1;
            }
          });

          //   // localStorage.setItem("access_token", data.access_token);
          //   // localStorage.setItem("username", this.username);
          //   this.lists = data.lists;
          // console.log(data.cards[0]["title"]);
          // router.push("/");
        }
      })
      //   .then(() => {
      //     console.log(this.complete);
      //     console.log(this.incomplete);
      //     console.log(this.passed);
      //     new Chart(document.getElementById("myChart"), {
      //       type: "bar",
      //       data: {
      //         labels: ["Completed", "Incomplete", "Passed"],
      //         datasets: [
      //           {
      //             label: "Tasks",
      //             backgroundColor: [
      //               "rgb(75, 192, 192)",
      //               "rgb(255, 205, 86)",
      //               "rgb(255, 99, 132)",
      //             ],
      //             data: [this.complete, this.incomplete, this.passed],
      //           },
      //         ],
      //       },
      //       options: {
      //         responsiveness: true,
      //         legend: {
      //           display: false,
      //         },
      //       },
      //     });
      //   })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style scoped>
#chartContainer {
  width: 40%;
}
</style>

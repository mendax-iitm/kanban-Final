<template>
  <nav class="navbar navbar-expand-lg bg-light">
    <div class="container">
      <a class="navbar-brand" href="#"
        ><img
          src="../assets/kanba.webp"
          alt="Logo"
          width="50"
          height="50"
          class="d-inline-block align-text-top"
        />
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarText"
        aria-controls="navbarText"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/"
              ><a
                class="nav-link active text-primary"
                aria-current="page"
                href="#"
                >Home</a
              ></router-link
            >
          </li>
          <li class="nav-item">
            <div class="nav-link text-primary" @click="exportAll">Export</div>
          </li>
          <li class="nav-item">
            <router-link to="/summary">
              <a class="nav-link text-primary">Summary</a>
            </router-link>
          </li>
        </ul>
      </div>
      <div id="logout" @click="logout" class="mb-2 nav-link text-primary">
        Logout
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  props: {
    msg: String,
  },
  methods: {
    logout: function () {
      localStorage.clear();
      this.$emit("dashchange", false);
    },
    exportAll: function () {
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
            console.log(cards);
            let csv =
              "title,content,list_title,deadline,completed,completed_time,\n";
            cards.forEach((card) => {
              let li = [];
              li.push(card.title);
              li.push(card.content);
              li.push(card.list_title);
              li.push(card.deadline);
              li.push(card.completed);
              li.push(card.completed_time);
              csv += li.join(",");
              csv += "\n";
            });

            const anchor = document.createElement("a");
            anchor.href =
              "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
            anchor.target = "_blank";
            anchor.download = "Cards_.csv";
            anchor.click();
            // localStorage.setItem("access_token", data.access_token);
            // localStorage.setItem("username", this.username);

            this.lists = data.lists;
            // console.log(data.cards[0]["title"]);

            // router.push("/");
          } else {
            this.errStatus = true;
            this.errormsg = data.msg;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

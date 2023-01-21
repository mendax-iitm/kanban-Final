<template>
  <div class="dashboard">
    <div class="container-fluid">
      <div class="row">
        <div class="col-3" v-for="list in lists" :key="list.id">
          <List
            :id="list.id"
            :title="list.title"
            :user_id="list.user_id"
            @change-title="changelisttitle"
            @delete-list="deletelist"
          ></List>
        </div>

        <div class="col-3 d-flex align-items-center justify-content-center">
          <!-- <br />
          <br />
          <br />
          <br />
          <br />
          <br /> -->
          <i
            @click="addList(id)"
            class="bi bi-plus-circle-fill text-success"
            style="font-size: 5rem"
            data-toggle="tooltip"
            data-placement="bottom"
            title="Add List"
          ></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import List from "./List.vue";
export default {
  name: "Dashboard",
  components: {
    List,
  },
  data: function () {
    return {
      lists: [],
    };
  },
  methods: {
    addList: function () {
      this.$router.push("/addList");
    },
    changelisttitle(id, title) {
      // console.log(this.lists);
      this.lists.forEach(function (list) {
        if (list.id === id) {
          list.title = title;
        }
      });
    },
    deletelist: function (id) {
      this.lists.splice(
        this.lists.findIndex((a) => a.id === id),
        1
      );
    },
  },
  mounted: function () {
    fetch("http://127.0.0.1:8081/api/lists", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        Authorization: "Bearer " + localStorage.getItem("access_token"),
      },
      // body: JSON.stringify({
      //   username: this.username,
      //   password: this.password,
      // }),
    })
      .then((response) => {
        if (!response.ok) {
          alert("Response not ok");
        }
        console.log(response);
        return response.json();
      })
      .then((data) => {
        if (data) {
          console.log("here it is");

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
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>

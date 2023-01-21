<template>
  <div class="card shadow" style="width: 15rem; min-height: 10rem">
    <div class="card-header bg-warning">
      <h5>{{ title }}</h5>
      <div class="col">
        <i
          @click="editList(id)"
          class="bi bi-pencil text-primary h5 mx-2"
          data-toggle="tooltip"
          data-placement="top"
          title="Edit"
        ></i>

        <i
          @click="deleteList(id)"
          class="bi bi-trash text-danger h5 mx-2"
          data-toggle="tooltip"
          data-placement="top"
          title="Delete"
        ></i>
        <i
          @click="exportList()"
          class="bi bi-file-earmark-arrow-down-fill text-success h5 mx-2"
          data-toggle="tooltip"
          data-placement="top"
          title="Export"
        ></i>
        <i
          @click="addCard(id)"
          class="bi bi-plus-square-fill h5 mx-2"
          data-toggle="tooltip"
          data-placement="bottom"
          title="Add Card"
        ></i>
      </div>
    </div>
    <div class="card-body" v-for="card in allcards" :key="card.id">
      <Card
        :card_id="card.id"
        :content="card.content"
        :deadline="card.deadline"
        :title="card.title"
        :completed="card.completed"
        :deadline_days="card.deadline_days"
        @delete-card="deletecard"
      ></Card>

      <div></div>
    </div>
  </div>
</template>
<!-- 2021-11-26 17:53:39.657516 -->
<script>
import Card from "./Card.vue";
export default {
  name: "List",
  props: ["title", "id", "user_id"],
  data: function () {
    return {
      allcards: [],
    };
  },
  components: {
    Card,
  },
  methods: {
    deleteList: function (id) {
      // this.$router.push({
      //   name: "edit-card",
      //   params: { id: id },
      // });

      if (confirm("Do you really want to delete this list")) {
        fetch(`http://127.0.0.1:8081/api/list/${this.id}`, {
          method: "DELETE",
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
              this.$emit("delete-list", id);
            }
          });
      }
    },
    exportList: function () {
      let csv =
        "list_title,card_title,card_content,deadline_weekday,deadline,completed,\n";
      // let days = parseInt(this.deadline_days) + 1;

      this.allcards.forEach((card) => {
        let li = [];
        li = [this.title.toString()];
        li.push(card.title);
        li.push(card.content);
        li.push(card.deadline);
        li.push(card.completed);
        csv += li.join(",");
        csv += "\n";
      });
      const anchor = document.createElement("a");
      anchor.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
      anchor.target = "_blank";
      anchor.download = `List_${this.id}.csv`;
      anchor.click();
    },
    editList: function (id) {
      // this.$router.push({
      //   name: "edit-card",
      //   params: { id: id },
      // });
      let title = prompt("Please input the new title");
      if (title) {
        fetch(`http://127.0.0.1:8081/api/list/${this.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
          body: JSON.stringify({
            title: title,
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
              this.$emit("change-title", id, title);
            }
          });
      }
    },
    deletecard: function (id) {
      this.allcards.splice(
        this.allcards.findIndex((a) => a.id === id),
        1
      );
    },
    addCard: function (id) {
      this.$router.push(`/addCard/${id}`);
    },
  },
  deleteList: function () {},
  mounted: function () {
    console.log("before fetch");

    fetch(`http://127.0.0.1:8081/api/card/list/${this.id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
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
        console.log(data);
        if (data) {
          console.log("here it is");

          // localStorage.setItem("access_token", data.access_token);
          // localStorage.setItem("username", this.username);

          this.allcards = data;
          // console.log(data.cards[0]["title"]);

          // router.push("/");
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

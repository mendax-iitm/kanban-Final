<template>
  <div class="card shadow" style="width: 12rem; min-height: 10rem">
    <h5
      class="card-header"
      :class="{ 'bg-success': done, 'bg-danger': deadpass }"
    >
      {{ title }}
    </h5>
    <div class="card-body">
      <div class="card-text col justify-content-center">
        <div class="row justify-content-center">{{ content }}</div>
        <div class="row mt-5 justify-content-center small text-info fst-italic">
          <em>{{ deadlinestr }}</em>
        </div>
      </div>
    </div>
    <div class="card-footer bg-white">
      <div class="col">
        <i
          @click="editCard(card_id)"
          class="bi bi-pencil text-primary h5 mx-2"
          data-toggle="tooltip"
          data-placement="top"
          title="Edit"
        ></i>

        <i
          @click="deleteCard(card_id)"
          class="bi bi-trash text-danger h5 mx-2"
          data-toggle="tooltip"
          data-placement="top"
          title="Delete"
        ></i>
        <i
          @click="exportCard(card_id)"
          class="bi bi-file-earmark-arrow-down-fill text-success h5 mx-2"
          data-toggle="tooltip"
          data-placement="top"
          title="Export"
        ></i>
      </div>
      <div class="col">
        <!-- Default switch -->
        <div class="form-switch">
          <input
            class="form-check-input"
            type="checkbox"
            role="switch"
            id="flexSwitchCheckDefault"
            @click="completetoggleSwitch"
            :checked="checked"
          />

          <label class="mx-2 form-check-label" for="flexSwitchCheckDefault"
            >Done</label
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Card",
  data() {
    return {
      done: false,
      checked: false,
      deadpass: false,
      deadlinestr: "",
    };
  },
  props: [
    "card_id",
    "title",
    "deadline",
    "content",
    // "created_time",
    // "updated_time",
    "completed",
    // "completed_time",

    // "list_id",
    "deadline_days",
  ],
  methods: {
    deleteCard: function (id) {
      if (confirm("Are you sure you want to delete this card")) {
        fetch(`http://127.0.0.1:8081/api/card/${id}`, {
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
            console.log(response);
            return response.json();
          })
          .then((data) => {
            if (data) {
              console.log("here it is");
              this.$emit("delete-card", id);
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
    editCard: function (id) {
      this.$router.push(`/editCard/${id}`);
    },
    exportCard: function () {
      let csv = "id,title,content,weekday,deadline,completed,\n";
      // let days = parseInt(this.deadline_days) + 1;
      let li = [
        this.card_id.toString(),
        this.title.toString(),
        this.content.toString(),
        this.deadline.toString(),
        this.completed.toString(),
      ];
      csv += li.join(",");
      csv += "\n";

      const anchor = document.createElement("a");
      anchor.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
      anchor.target = "_blank";
      anchor.download = `Card_${this.card_id}.csv`;
      anchor.click();
    },
    completetoggleSwitch: function () {
      fetch(`http://127.0.0.1:8081/api/card/complete/${this.card_id}`, {
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
          console.log(response);
          return response.json();
        })
        .then((data) => {
          if (data.status) {
            this.done = !this.done;
            if (this.done) {
              this.deadpass = false;
              this.deadlinestr = "Completed";
            } else if (this.deadline_days < -1) {
              this.deadpass = true;
              this.deadlinestr = "Deadline has passed";
            } else if (this.deadline_days == -1) {
              this.deadlinestr = "Today is the deadline";
            } else if (this.deadline_days == 0) {
              this.deadlinestr = "Tomorrow is the deadline";
            } else {
              let de = parseInt(this.deadline_days) + 1;
              this.deadlinestr = de + " days left";
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  mounted: function () {
    if (this.completed == 1) {
      this.done = true;
      this.checked = true;
      this.deadlinestr = "Completed";
    } else if (this.deadline_days < -1) {
      this.deadpass = true;
      this.deadlinestr = "Deadline has passed";
    } else if (this.deadline_days == -1) {
      this.deadlinestr = "Today is the deadline";
    } else if (this.deadline_days == 0) {
      this.deadlinestr = "Tomorrow is the deadline";
    } else {
      let de = parseInt(this.deadline_days) + 1;
      this.deadlinestr = de + " days left";
    }
  },
};
</script>

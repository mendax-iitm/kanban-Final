function validateForm() {}

// function validate(event) {
//   v = document.getElementById("email").value;

//   if (v.indexOf("@") == -1) {
//     event.preventDefault();
//     alert("enter a valid email");
//     return false;
//   }

//   return true;
// }

// function show_thankyou(article, response) {
//   var div = document.createElement("div");
//   div.class = "message";
//   div.innerHTML = "Thank you for liking.";
//   article.parentNode.appendChild(div);
// }
// function send_like(event) {
//   article = event.target;
//   article_id = article.dataset.article_id;

//   fetch("/article_like/" + article_id)
//     .then((response) => show_thankyou(article, response))
//     // .then((response) => alert(response))
//     .catch((err) => console.log(err));
// }

// function initialize() {
//   like_buttons = document.querySelectorAll(".like-icon");
//   for (const like_button of like_buttons) {
//     like_button.onclick = send_like;
//   }
// }

function func() {
  document.getElementById("front").style.visibility = "hidden";
  document.getElementById("back").style.visibility = "visible";
  document.getElementById("btn").style.visibility = "visible";
}
// function textupdate() {
//   document.getElementById("frontupdate").value = front;
//   document.getElementById("backupdate").value = back;
// }
// window.onload = textupdate;
// window.onload = (event) => {
//   console.log("page is fully loaded");
// };

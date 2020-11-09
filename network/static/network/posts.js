document.addEventListener("DOMContentLoaded", function () {
  // Like-Unlike
  const user = JSON.parse(document.getElementById("username").textContent);
  document.querySelectorAll(".like").forEach((anchor) => {
    anchor.onclick = function () {
      post_to_like_unlike(this.dataset.post, user);
    };
  });

  // Edit message
  document.querySelectorAll(".ui.teal.button").forEach((button) => {
    button.onclick = function () {
      forms = document.querySelectorAll(".comment");
      forms.forEach((element) => {
        element.style.display = "none";
      });
      const messages = document.querySelectorAll(".extra");
      messages.forEach((element) => {
        element.style.display = "block";
      });
      post_id = this.dataset.comment;
      const message = document.getElementById(`msg_${post_id}`);
      const msg_text = document.getElementById(`text_${post_id}`);

      msg_text.innerHTML = message.innerHTML.trim();
      document.getElementById(`form_${post_id}`).style.display = "block";
      msg_text.focus();
      message.style.display = "none";
      msg_text.addEventListener("keyup", (e) => {
        if (e.key == "Enter") {
          if (e.target.value != 0) {
            message.innerHTML = e.target.value;
          }

          message.style.display = "block";
          document.getElementById(`form_${post_id}`).style.display = "none";
          edit_comment(post_id, message.innerHTML);
        }
      });
    };
  });
});

function post_to_like_unlike(post_id, user) {
  fetch("posts/")
    .then((response) => response.json())
    .then((posts) => {
      posts.forEach((post) => {
        if (post.id == parseInt(post_id)) {
          if (post.likes.includes(user)) {
            unlike(post);
          } else like(post);
        }
      });
    });
}

function like(post) {
  const likes = document.getElementById(post.id).text.trim();
  const heart = '<i class="like liked icon"></i> ';
  document.getElementById(post.id).innerHTML = heart + (parseInt(likes) + 1);
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const request = new Request(`posts/${post.id}`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  fetch(request, {
    method: "PUT",
    mode: "same-origin",
  });
}
function unlike(post) {
  const likes = document.getElementById(post.id).text.trim();
  const heart =
    '<i class="like icon"></i> ';
  document.getElementById(post.id).innerHTML = heart + (parseInt(likes) - 1);
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const request = new Request(`posts/${post.id}`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  fetch(request, {
    method: "PUT",
    mode: "same-origin",
  });
}

function edit_comment(post_id, message) {
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const request = new Request(`/posts/msg/${post_id}`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      message: message,
    }),
  });
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".like-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            let postId = this.dataset.postId;
            let likeUrl = `/feed/like/${postId}/`;  

            fetch(likeUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    this.innerText = "❤️ " + data.like_count;
                } else {
                    this.innerText = "🤍 " + data.like_count;
                }
            })
            .catch(error => console.error("Ошибка:", error));
        });
    });
});


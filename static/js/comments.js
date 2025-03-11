document.addEventListener("DOMContentLoaded", function () {
    // Переключатель для показа/свертывания всего блока комментариев для поста
    document.querySelectorAll(".toggle-comments-btn").forEach(btn => {
        btn.addEventListener("click", function (event) {
            event.preventDefault();
            let commentsSection = this.closest(".post-comments").querySelector(".comments-section");
            if (commentsSection.style.display === "none" || commentsSection.style.display === "") {
                commentsSection.style.display = "block";
                this.textContent = "▲";
            } else {
                commentsSection.style.display = "none";
                this.textContent = "▼";
            }
        });
    });

    // Обработчик для кнопки "Ответить" – показывает/скрывает форму ответа
    document.querySelectorAll(".reply-btn").forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            let replyForm = this.closest(".comment").querySelector(".reply-form");
            if (replyForm.style.display === "none" || replyForm.style.display === "") {
                replyForm.style.display = "flex";
                this.textContent = "Свернуть ответ";
            } else {
                replyForm.style.display = "none";
                this.textContent = "Ответить";
            }
        });
    });

    // Отправка нового (топ-уровня) комментария
    document.querySelectorAll(".btn-submit-comment").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            let postId = this.dataset.postId;
            let textarea = this.closest(".add-comment").querySelector("textarea");
            let content = textarea.value.trim();
            if (!content) {
                alert("Комментарий не может быть пустым");
                return;
            }
            let commentUrl = `/feed/post/${postId}/`;
            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            fetch(commentUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    "content": content
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    textarea.value = "";
                    let commentsSection = this.closest(".post-comments").querySelector(".comments-section");
                    if (commentsSection.style.display === "none" || commentsSection.style.display === "") {
                        commentsSection.style.display = "block";
                        let toggleBtn = this.closest(".post-comments").querySelector(".toggle-comments-btn");
                        if (toggleBtn) toggleBtn.textContent = "▲";
                    }
                    let newComment = document.createElement("div");
                    newComment.className = "comment";
                    newComment.innerHTML = `
                        <div class="comment-header">
                            <img src="${data.avatar_url}" alt="Аватар" class="comment-avatar">
                            <span class="comment-author">${data.first_name} ${data.last_name}</span>
                            <span class="comment-date">${data.created_at}</span>
                        </div>
                        <p class="comment-content">${content}</p>
                        <a href="#" class="reply-btn" data-comment-id="${data.comment_id}">Ответить</a>
                        <div class="reply-form" style="display: none;">
                            <textarea placeholder="Ваш ответ..." required></textarea>
                            <button class="btn-submit-reply" data-post-id="${postId}" data-parent-id="${data.comment_id}">Отправить</button>
                        </div>
                    `;
                    commentsSection.appendChild(newComment);
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error("Ошибка при добавлении комментария:", error));
        });
    });

    // Отправка ответа на комментарий (делегирование события для динамически добавляемых элементов)
    document.addEventListener("click", function (event) {
        if (event.target && event.target.classList.contains("btn-submit-reply")) {
            event.preventDefault();
            let button = event.target;
            let postId = button.dataset.postId;
            let parentId = button.dataset.parentId;
            let textarea = button.closest(".reply-form").querySelector("textarea");
            let content = textarea.value.trim();
            if (!content) {
                alert("Ответ не может быть пустым");
                return;
            }
            let commentUrl = `/feed/post/${postId}/`;
            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            fetch(commentUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    "content": content,
                    "parent_id": parentId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    textarea.value = "";
                    // Находим контейнер для ответов внутри родительского комментария
                    let parentComment = button.closest(".comment");
                    let nestedReplies = parentComment.querySelector(".nested-replies");
                    if (!nestedReplies) {
                        nestedReplies = document.createElement("div");
                        nestedReplies.className = "nested-replies";
                        parentComment.appendChild(nestedReplies);
                    }
                    let newReply = document.createElement("div");
                    newReply.className = "comment reply";
                    newReply.innerHTML = `
                        <div class="comment-header">
                            <img src="${data.avatar_url}" alt="Аватар" class="comment-avatar">
                            <span class="comment-author">${data.first_name} ${data.last_name}</span>
                            <span class="comment-date">${data.created_at}</span>
                        </div>
                        <p class="comment-content">${content}</p>
                        <a href="#" class="reply-btn" data-comment-id="${data.comment_id}">Ответить</a>
                        <div class="reply-form" style="display: none;">
                            <textarea placeholder="Ваш ответ..." required></textarea>
                            <button class="btn-submit-reply" data-post-id="${postId}" data-parent-id="${data.comment_id}">Отправить</button>
                        </div>
                    `;
                    nestedReplies.appendChild(newReply);
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error("Ошибка при добавлении ответа:", error));
        }
    });
});

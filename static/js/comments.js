document.addEventListener("DOMContentLoaded", () => {
    const csrfToken = document
        .querySelector('meta[name="csrf-token"]')
        .getAttribute("content");

    // Обработчик для кнопки "Комментарии" (открытие/закрытие контейнера комментариев)
    document.body.addEventListener("click", (e) => {
        if (e.target.matches(".toggle-comments-btn")) {
            e.preventDefault();
            const postCard = e.target.closest(".post-card");
            const commentsContainer = postCard.querySelector(".comments-container");
            commentsContainer.classList.toggle("open");
        }
    });

    // Обработчик для кнопок "Ответить" (открытие/скрытие формы ответа)
    document.body.addEventListener("click", (e) => {
        if (e.target.matches(".reply-btn")) {
            e.preventDefault();
            const commentElem = e.target.closest(".comment");
            const replyForm = commentElem.querySelector(".reply-form");
            if (replyForm) {
                const isVisible = replyForm.style.display === "block";
                replyForm.style.display = isVisible ? "none" : "block";
                e.target.textContent = isVisible ? "Ответить" : "Свернуть ответ";
            }
        }
    });

    // Добавление нового комментария
    document.querySelectorAll(".btn-submit-comment").forEach((button) => {
        button.addEventListener("click", async (e) => {
            e.preventDefault();
            const postId = button.dataset.postId;
            const postCard = button.closest(".post-card");
            const textarea = button
                .closest(".add-comment")
                .querySelector("textarea");
            const commentsContainer = postCard.querySelector(".comments-container");
            const content = textarea.value.trim();
            if (!content) return alert("Комментарий не может быть пустым");

            try {
                const res = await fetch(`/feed/post/${postId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: new URLSearchParams({ content }),
                });
                const data = await res.json();
                if (!data.success) return alert(data.message);

                // Очищаем поле ввода
                textarea.value = "";

                // Создаём новый элемент комментария
                const newComment = document.createElement("div");
                newComment.classList.add("comment");
                newComment.dataset.commentId = data.comment_id;
                newComment.innerHTML = `
                    <img src="${data.avatar_url}" alt="Аватар" class="comment-avatar">
                    <div class="comment-body">
                        <div class="comment-header">
                            <span class="comment-author">${data.first_name} ${data.last_name}</span>
                            <span class="comment-date">${data.created_at}</span>
                        </div>
                        <p class="comment-content">${content}</p>
                        <a href="#" class="reply-btn" data-comment-id="${data.comment_id}">Ответить</a>
                        <div class="reply-form" style="display: none;">
                            <textarea placeholder="Ваш ответ..." required></textarea>
                            <button class="btn-submit-reply" data-post-id="${postId}" data-parent-id="${data.comment_id}">Отправить</button>
                        </div>
                    </div>
                `;

                // Добавляем новый комментарий в контейнер
                commentsContainer.appendChild(newComment);
            } catch (error) {
                console.error("Ошибка при добавлении комментария:", error);
            }
        });
    });

    // Обработчик для добавления ответа (reply)
    document.body.addEventListener("click", async (e) => {
        if (e.target.matches(".btn-submit-reply")) {
            e.preventDefault();
            const button = e.target;
            const postId = button.dataset.postId;
            const parentId = button.dataset.parentId;
            const replyForm = button.closest(".reply-form");
            const textarea = replyForm.querySelector("textarea");
            const content = textarea.value.trim();
            if (!content) return alert("Ответ не может быть пустым");

            try {
                const res = await fetch(`/feed/post/${postId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: new URLSearchParams({ content, parent_id: parentId }),
                });
                const data = await res.json();
                if (!data.success) return alert(data.message);

                textarea.value = "";

                const parentComment = button.closest(".comment");
                let repliesContainer =
                    parentComment.querySelector(".nested-replies");
                if (!repliesContainer) {
                    repliesContainer = document.createElement("div");
                    repliesContainer.classList.add("nested-replies");
                    parentComment.appendChild(repliesContainer);
                }

                const newReply = document.createElement("div");
                newReply.classList.add("comment", "reply");
                newReply.dataset.commentId = data.comment_id;
                newReply.innerHTML = `
                    <img src="${data.avatar_url}" alt="Аватар" class="comment-avatar">
                    <div class="comment-body">
                        <div class="comment-header">
                            <span class="comment-author">${data.first_name} ${data.last_name}</span>
                            <span class="comment-date">${data.created_at}</span>
                        </div>
                        <p class="comment-content">${content}</p>
                        <a href="#" class="reply-btn" data-comment-id="${data.comment_id}">Ответить</a>
                        <div class="reply-form" style="display: none;">
                            <textarea placeholder="Ваш ответ..." required></textarea>
                            <button class="btn-submit-reply" data-post-id="${postId}" data-parent-id="${data.comment_id}">Отправить</button>
                        </div>
                    </div>
                `;
                repliesContainer.appendChild(newReply);
            } catch (error) {
                console.error("Ошибка при добавлении ответа:", error);
            }
        }
    });
});

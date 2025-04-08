// comments.js

document.addEventListener("DOMContentLoaded", function () {
    // Кнопка «Комментарии» в шапке поста
    document.querySelectorAll(".toggle-comments-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            const card = this.closest(".post-card");
            const commentsContainer = card.querySelector(".comments-container");
            commentsContainer.classList.toggle("open");
        });
    });

    // Открытие/закрытие формы ответа
    document.addEventListener("click", function (e) {
        if (!e.target.classList.contains("reply-btn")) return;
        e.preventDefault();
        const link = e.target;
        const replyForm = link.closest(".comment").querySelector(".reply-form");
        if (!replyForm) return;
        const isOpen = replyForm.style.display === "flex";
        replyForm.style.display = isOpen ? "none" : "flex";
        link.textContent = isOpen ? "Ответить" : "Свернуть ответ";
    });

    // Отправка нового комментария
    document.querySelectorAll(".btn-submit-comment").forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const textarea = this.closest(".add-comment").querySelector("textarea");
            const content = textarea.value.trim();
            if (!content) return alert("Комментарий не может быть пустым");

            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            fetch(`/feed/post/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({ content })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) return alert(data.message);

                // Очищаем форму и показываем контейнер
                textarea.value = "";
                const card = button.closest(".post-card");
                const commentsContainer = card.querySelector(".comments-container");
                commentsContainer.classList.add("open");

                // Добавляем новый комментарий в конец
                const newComment = document.createElement("div");
                newComment.className = "comment";
                newComment.innerHTML = `
                    <img src="${data.avatar_url}" alt="Аватар" class="comment-avatar">
                    <div class="comment-body">
                        <div class="comment-header">
                            <span class="comment-author">${data.first_name} ${data.last_name}</span>
                            <span class="comment-date">${data.created_at}</span>
                        </div>
                        <p class="comment-content">${content}</p>
                        <a href="#" class="reply-btn" data-comment-id="${data.comment_id}">Ответить</a>
                        <div class="reply-form">
                            <textarea placeholder="Ваш ответ..." required></textarea>
                            <button class="btn-submit-reply" data-post-id="${postId}" data-parent-id="${data.comment_id}">Отправить</button>
                        </div>
                    </div>
                `;
                commentsContainer.appendChild(newComment);
            })
            .catch(err => console.error("Ошибка при добавлении комментария:", err));
        });
    });

    // Отправка ответа на комментарий
    document.addEventListener("click", function (e) {
        if (!e.target.classList.contains("btn-submit-reply")) return;
        e.preventDefault();
        const button = e.target;
        const postId = button.dataset.postId;
        const parentId = button.dataset.parentId;
        const textarea = button.closest(".reply-form").querySelector("textarea");
        const content = textarea.value.trim();
        if (!content) return alert("Ответ не может быть пустым");

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch(`/feed/post/${postId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ content, parent_id: parentId })
        })
        .then(res => res.json())
        .then(data => {
            if (!data.success) return alert(data.message);

            textarea.value = "";
            const parentComment = button.closest(".comment");
            let nested = parentComment.querySelector(".nested-replies");
            if (!nested) {
                nested = document.createElement("div");
                nested.className = "nested-replies";
                parentComment.appendChild(nested);
            }
            const newReply = document.createElement("div");
            newReply.className = "comment reply";
            newReply.innerHTML = `
                <img src="${data.avatar_url}" alt="Аватар" class="comment-avatar">
                <div class="comment-body">
                    <div class="comment-header">
                        <span class="comment-author">${data.first_name} ${data.last_name}</span>
                        <span class="comment-date">${data.created_at}</span>
                    </div>
                    <p class="comment-content">${content}</p>
                    <a href="#" class="reply-btn" data-comment-id="${data.comment_id}">Ответить</a>
                    <div class="reply-form">
                        <textarea placeholder="Ваш ответ..." required></textarea>
                        <button class="btn-submit-reply" data-post-id="${postId}" data-parent-id="${data.comment_id}">Отправить</button>
                    </div>
                </div>
            `;
            nested.appendChild(newReply);
        })
        .catch(err => console.error("Ошибка при добавлении ответа:", err));
    });
});

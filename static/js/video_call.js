document.addEventListener("DOMContentLoaded", function () {
    const openVideoCallBtn = document.getElementById("open-video-call");
    const videoCallModal = document.getElementById("video-call-modal");
    const closeModalBtn = document.getElementById("close-modal");
    const videoCallContainer = document.getElementById("video-call-container");

    if (!openVideoCallBtn || !videoCallModal || !videoCallContainer || !closeModalBtn) {
        console.warn("Один из элементов для видеозвонка не найден в DOM.");
        return;
    }

    const chatId = openVideoCallBtn.dataset.chatId;

    fetch(`/chat/check-call/${chatId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.room_url) {
                openVideoCallBtn.textContent = "Присоединиться к звонку";
                openVideoCallBtn.dataset.roomUrl = data.room_url;
            }
        })
        .catch(error => console.error("Ошибка при проверке звонка:", error));

    openVideoCallBtn.addEventListener("click", function () {
        if (openVideoCallBtn.dataset.roomUrl) {
            openVideoCall(openVideoCallBtn.dataset.roomUrl);
        } else {
            fetch(`/chat/create-or-get-call/${chatId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.room_url) {
                    openVideoCallBtn.textContent = "Присоединиться к звонку";
                    openVideoCallBtn.dataset.roomUrl = data.room_url;
                    openVideoCall(data.room_url);
                } else {
                    alert("Ошибка создания видеозвонка");
                }
            })
            .catch(error => console.error("Ошибка:", error));
        }
    });

    closeModalBtn.addEventListener("click", function () {
        fetch(`/chat/delete-call/${chatId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken()
            }
        }).then(response => {
            if (!response.ok) {
                console.warn("Не удалось удалить комнату");
            }
        }).catch(error => {
            console.error("Ошибка при удалении комнаты:", error);
        });
        videoCallModal.classList.remove("show");
        videoCallContainer.innerHTML = "";
    });
    

    function openVideoCall(roomUrl) {
        videoCallContainer.innerHTML = `<iframe src="${roomUrl}" width="100%" height="100%" allow="microphone; camera; fullscreen; display-capture"></iframe>`;
        videoCallModal.classList.add("show");
    }

    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith("csrftoken=")) {
                    cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                    break;
                }
            }
        }
        return cookieValue;
    }

    
});

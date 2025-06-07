document.addEventListener("DOMContentLoaded", function() {
    fetchNotifications();
});

function fetchNotifications() {
    fetch("/notifications/get/")
        .then(response => response.json())
        .then(data => {
            const bellImg = document.getElementById("notification-bell-img");
            const dropdown = document.getElementById("notification-dropdown");
            if (data.length > 0) {
                bellImg.src = "/static/images/notificationsHave.svg"; 
                renderNotifications(data);
            } else {
                bellImg.src = "/static/images/notifications.svg"; 
                dropdown.innerHTML = `<p class="text-gray-500 text-sm">Нет новых уведомлений</p>`;
            }
        })
        .catch(error => console.error("Ошибка загрузки уведомлений:", error));
}

function renderNotifications(notifications) {
    const dropdown = document.getElementById("notification-dropdown");
    dropdown.innerHTML = "";
    notifications.forEach(notification => {
        let notifItem = document.createElement("a");
        notifItem.href = notification.link;
        notifItem.innerText = notification.description;
        notifItem.classList.add("notification-item");
        notifItem.addEventListener("click", function() {
            markNotificationsAsRead();
        });
        dropdown.appendChild(notifItem);
    });
}

function toggleNotifications(event) {
    event.stopPropagation();
    const dropdown = document.getElementById("notification-dropdown");
    dropdown.classList.toggle("show");
    if (!dropdown.classList.contains("show")) {
        markNotificationsAsRead();
    }
}

document.addEventListener("click", function(event) {
    const dropdown = document.getElementById("notification-dropdown");
    const bell = document.getElementById("notification-bell");
    if (!bell.contains(event.target)) {
        dropdown.classList.remove("show");
    }
});

function markNotificationsAsRead() {
    fetch("/notifications/read/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    }).then(() => {
        document.getElementById("notification-bell-img").src = "/static/images/notifications.svg";
        fetchNotifications(); 
    }).catch(error => console.error("Ошибка при отметке уведомлений:", error));
}

function toggleMenu(event) {
    const menu = document.getElementById('profile-menu');
    menu.classList.toggle('show');
    event.stopPropagation();
}

document.addEventListener('click', function(event) {
    const menu = document.getElementById('profile-menu');
    const profileIcon = document.querySelector('.profile-icon');
    if (!profileIcon.contains(event.target) && !menu.contains(event.target)) {
        menu.classList.remove('show');
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach(cookie => {
            let [key, value] = cookie.trim().split("=");
            if (key === name) {
                cookieValue = decodeURIComponent(value);
            }
        });
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function() {
    fetchNotifications();

    const openChatBtn = document.getElementById("open-ai-chat");
    const chatModal = document.getElementById("ai-chat-box");
    const chatModalContent = document.querySelector("#ai-chat-box .chat-modal-content");
    const chatClose = document.getElementById("chat-close");

    openChatBtn.addEventListener("click", function() {
        chatModal.style.display = "flex"; 
        openChatBtn.style.display = "none";
    });

    chatClose.addEventListener("click", function() {
        chatModal.style.display = "none";
        openChatBtn.style.display = "block"; 
    });

    window.addEventListener("click", function(event) {
        if (!chatModalContent.contains(event.target) && event.target !== openChatBtn) {
            chatModal.style.display = "none";
            openChatBtn.style.display = "block";
        }
    });

    const input = document.getElementById("chat-input");
    const sendBtn = document.getElementById("chat-send");

    sendBtn.addEventListener("click", function () {
        const message = input.value;
        if (!message.trim()) return;

        addToChat("Вы", message);

        fetch('/assistant/chat-api/?prompt=' + encodeURIComponent(message))
            .then(res => res.json())
            .then(data => {
                addToChat("AI", data.response);
                input.value = "";
            });
    });

    input.addEventListener("keydown", function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendBtn.click();
        }
    });

    function addToChat(sender, text) {
        const container = document.getElementById("chat-history");
        const message = document.createElement("div");
        message.className = "chat-message";
        message.innerHTML = `<strong>${sender}:</strong> ${text}`;
        container.appendChild(message);
        container.scrollTop = container.scrollHeight;
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const burger = document.getElementById("burger-toggle");
    const nav = document.getElementById("nav-links");

    burger.addEventListener("click", function () {
        nav.classList.toggle("active");
    });
});

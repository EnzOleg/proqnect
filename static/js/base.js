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
                bellImg.src = "/static/images/notifications_.png"; 
                renderNotifications(data);
            } else {
                bellImg.src = "/static/images/notifications.png"; 
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
        document.getElementById("notification-bell-img").src = "/static/images/notifications.png";
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

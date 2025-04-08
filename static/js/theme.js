(function() {
    const root = document.documentElement;
    let savedTheme = localStorage.getItem("theme") || "light";

    // Скрываем страницу во время установки темы
    root.style.visibility = "hidden";
    root.style.opacity = "0";

    // Устанавливаем тему на основе сохраненного значения
    root.setAttribute("data-theme", savedTheme);

    // Обновляем логотип в зависимости от темы
    const logo = document.getElementById("site-logo");
    if (logo) {
        if (savedTheme === "dark") {
            logo.src = "/static/images/proqfigm-dark.svg";  // Темный логотип
        } else {
            logo.src = "/static/images/proqfigm.svg";  // Светлый логотип
        }
    }

    // Показываем страницу после установки темы
    root.style.visibility = "visible";
    root.style.opacity = "1";

    document.addEventListener("DOMContentLoaded", function () {
        const themeSelect = document.getElementById("theme-select");
        if (themeSelect) {
            themeSelect.value = savedTheme;
            themeSelect.addEventListener("change", function () {
                const selectedTheme = this.value;
                
                // Меняем тему на выбранную
                root.setAttribute("data-theme", selectedTheme);
                localStorage.setItem("theme", selectedTheme);

                // Обновляем логотип в зависимости от новой темы
                if (selectedTheme === "dark") {
                    logo.src = "/static/images/proqfigm-dark.svg";
                } else {
                    logo.src = "/static/images/proqfigm.svg";
                }
            });
        }
    });
})();

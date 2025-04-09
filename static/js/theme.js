(function() {
    const root = document.documentElement;
    let savedTheme = localStorage.getItem("theme") || "light";

    root.style.visibility = "hidden";
    root.style.opacity = "0";

    root.setAttribute("data-theme", savedTheme);

    const logo = document.getElementById("site-logo");
    if (logo) {
        if (savedTheme === "dark") {
            logo.src = "/static/images/proqfigm-dark.svg"; 
        } else {
            logo.src = "/static/images/proqfigm.svg";  
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
                
                root.setAttribute("data-theme", selectedTheme);
                localStorage.setItem("theme", selectedTheme);

                if (selectedTheme === "dark") {
                    logo.src = "/static/images/proqfigm-dark.svg";
                } else {
                    logo.src = "/static/images/proqfigm.svg";
                }
            });
        }
    });
})();

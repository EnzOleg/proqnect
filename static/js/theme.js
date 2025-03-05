document.addEventListener("DOMContentLoaded", function () {
    const root = document.documentElement;
    const themeSelect = document.getElementById("theme-select");
    let savedTheme = localStorage.getItem("theme") || "light";

    root.setAttribute("data-theme", savedTheme);

    if (themeSelect) {
        themeSelect.value = savedTheme;
        themeSelect.addEventListener("change", function () {
            root.setAttribute("data-theme", this.value);
            localStorage.setItem("theme", this.value);
        });
    }
});

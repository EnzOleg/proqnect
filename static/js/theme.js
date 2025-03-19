(function() {
    const root = document.documentElement;
    let savedTheme = localStorage.getItem("theme") || "light";

    root.style.visibility = "hidden";
    root.style.opacity = "0";

    root.setAttribute("data-theme", savedTheme);

    root.style.visibility = "visible";
    root.style.opacity = "1";

    document.addEventListener("DOMContentLoaded", function () {
        const themeSelect = document.getElementById("theme-select");
        if (themeSelect) {
            themeSelect.value = savedTheme;
            themeSelect.addEventListener("change", function () {
                root.setAttribute("data-theme", this.value);
                localStorage.setItem("theme", this.value);
            });
        }
    });
})();

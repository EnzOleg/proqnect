document.addEventListener("DOMContentLoaded", function () {
    const navItems = document.querySelectorAll(".nav-item");
    const contents = document.querySelectorAll(".tab-content");

    navItems.forEach(item => {
        item.addEventListener("click", function () {
            navItems.forEach(i => i.classList.remove("active"));
            contents.forEach(c => c.classList.remove("active"));

            this.classList.add("active");

            const targetId = this.getAttribute("data-tab");
            const targetContent = document.getElementById(targetId);

            if (targetContent) {
                targetContent.classList.add("active");
            }
        });
    });
});

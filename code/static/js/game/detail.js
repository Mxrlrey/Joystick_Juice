document.addEventListener("DOMContentLoaded", () => {
    const dropdowns = document.querySelectorAll(".custom-dropdown");

    dropdowns.forEach(dd => {
        const btn = dd.querySelector(".dropdown-btn");
        const content = dd.querySelector(".dropdown-content");
        const hidden = dd.closest("form").querySelector('input[name="status"]');

        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            content.classList.toggle("show");
        });

        content.querySelectorAll(".dropdown-item").forEach(item => {
            item.addEventListener("click", () => {
                hidden.value = item.dataset.value;
                btn.firstChild.textContent = item.textContent;
                content.classList.remove("show");
            });
        });
    });

    window.addEventListener("click", () => {
        dropdowns.forEach(dd => {
            dd.querySelector(".dropdown-content").classList.remove("show");
        });
    });
});
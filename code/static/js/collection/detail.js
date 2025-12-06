document.addEventListener("DOMContentLoaded", function () {

    if (!isOwner) return;

    const grid = document.querySelector(".games-grid");
    if (!grid) return;

    Sortable.create(grid, {
        animation: 150,
        ghostClass: "dragging",
        handle: ".game-card",

        onEnd: function () {
            const ids = [...document.querySelectorAll(".item-card")]
                .map(el => el.dataset.itemId);

            fetch(reorderUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ order: ids })
            });
        }
    });
});

function scrollCarousel(btn, direction) {
    const wrapper = btn.closest(".carousel-wrapper");
    const container = wrapper.querySelector(".carousel-scroll-container");
    const scrollAmount = 250;

    container.scrollBy({
        left: scrollAmount * direction,
        behavior: "smooth"
    });

    setTimeout(() => updateDots(wrapper), 300);
}

function updateDots(wrapper) {
    const container = wrapper.querySelector(".carousel-scroll-container");
    const dots = wrapper.querySelector(".carousel-dots");

    const totalWidth = container.scrollWidth;
    const visibleWidth = container.clientWidth;
    const pages = Math.ceil(totalWidth / visibleWidth);

    dots.innerHTML = "";
    let currentPage = Math.round(container.scrollLeft / visibleWidth);

    for (let i = 0; i < pages; i++) {
        const dot = document.createElement("span");
        if (i === currentPage) dot.classList.add("active");

        dot.addEventListener("click", () => {
            container.scrollTo({
                left: i * visibleWidth,
                behavior: "smooth"
            });
            updateDots(wrapper);
        });

        dots.appendChild(dot);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".carousel-wrapper").forEach(wrapper => {
        updateDots(wrapper);
        wrapper.querySelector(".carousel-scroll-container")
            .addEventListener("scroll", () => updateDots(wrapper));
    });
});
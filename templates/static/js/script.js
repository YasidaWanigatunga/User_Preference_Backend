document.addEventListener("DOMContentLoaded", function () {
    function applyTheme(theme) {
        const body = document.body;
        const card = document.querySelector('.card');

        if (theme === "dark") {
            body.classList.remove("bg-light");
            body.classList.add("bg-dark");
            card.classList.remove("bg-light");
            card.classList.add("bg-dark");
        } else {
            body.classList.remove("bg-dark");
            body.classList.add("bg-light");
            card.classList.remove("bg-dark");
            card.classList.add("bg-light");
        }
    }

    const themeColorSelect = document.getElementById("theme_color");
    if (themeColorSelect) {
        themeColorSelect.addEventListener("change", function () {
            localStorage.setItem("theme_color", this.value);
            applyTheme(this.value);
        });

        applyTheme(localStorage.getItem("theme_color") || themeColorSelect.value);
    } else {
        console.warn("Theme color select element not found.");
    }

    const fontStyleSelect = document.getElementById("font_style");
    if (fontStyleSelect) {
        fontStyleSelect.addEventListener("change", function () {
            document.body.style.fontFamily = this.value;
        });
    }

    function applyLayout(layout) {
        const container = document.querySelector(".container");
        if (layout === "grid") {
            container.classList.remove("layout-list");
            container.classList.add("layout-grid");
        } else {
            container.classList.remove("layout-grid");
            container.classList.add("layout-list");
        }
    }
    const layoutStyleSelect = document.getElementById("layout_style");
    if (layoutStyleSelect) {
        let savedLayout = localStorage.getItem("layout_style") || "list";
        layoutStyleSelect.value = savedLayout;
        applyLayoutStyle(savedLayout);

        layoutStyleSelect.addEventListener("change", function () {
            localStorage.setItem("layout_style", this.value);
            applyLayout(this.value);
        });
        applyLayout(localStorage.getItem("layout_style") || layoutStyleSelect.value);
    } else {
        console.warn("Layout style select element not found.");
    }
});

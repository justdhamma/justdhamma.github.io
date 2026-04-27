function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    if (current === "dark") {
        setTheme("light");
    } else {
        setTheme("dark");
    }
}

(function () {
    const saved = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    if (saved) {
        setTheme(saved);
    } else if (prefersDark) {
        setTheme("dark");
    }
})();
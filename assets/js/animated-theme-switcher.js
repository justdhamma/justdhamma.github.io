(function () {
  const root = document.documentElement;
  const STORAGE_KEY = "theme";
  const themeOptionContainers = document.querySelectorAll(".theme-options-in-row");

  const icons = {
    light: "☀",
    sepia: "☕",
    dark: "🌙"
  };

  const themes = {
    light: {
      bg: "#ffffff",
      text: "#111111",
      border: "#e5e5e5",
      link: "#4772cfff",
      muted: "#666666"
    },
    dark: {
      bg: "#1c1f2b",
      text: "#bdcadb",
      border: "#7d8895ff",
      link: "#3eb1d0",
      muted: "#aaaaaa"
    },
    sepia: {
      bg: "#f3eacb",
      text: "#704214",
      border: "#d6c6a6",
      link: "#704214",
      muted: "#7a6a58"
    }
  };

  function applyTheme(name) {
    const theme = themes[name];
    if (!theme) return;

    Object.keys(theme).forEach(function (key) {
      root.style.setProperty("--" + key, theme[key]);
    });

    localStorage.setItem(STORAGE_KEY, name);

    themeOptionContainers.forEach(function (container) {
      const buttons = container.querySelectorAll("button");

      buttons.forEach(function (button) {
        button.classList.toggle("active", button.dataset.theme === name);
      });
    });
  }

  window.setTheme = function (name) {
    applyTheme(name);
  };

  themeOptionContainers.forEach(function (container) {
    const buttons = container.querySelectorAll("button");

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        setTheme(button.dataset.theme);
      });
    });
  });

  document.addEventListener("DOMContentLoaded", function () {
    const saved = localStorage.getItem(STORAGE_KEY) || "light";
    applyTheme(saved);
  });
})();

(function () {

  const root = document.documentElement;
  const STORAGE_KEY = "theme";

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

    Object.keys(theme).forEach(key => {
      root.style.setProperty("--" + key, theme[key]);
    });

    localStorage.setItem(STORAGE_KEY, name);
  }

  window.setTheme = function (name) {
    applyTheme(name);
  };

  document.addEventListener("DOMContentLoaded", function () {
    const saved = localStorage.getItem(STORAGE_KEY) || "light";
    applyTheme(saved);
  });

})();
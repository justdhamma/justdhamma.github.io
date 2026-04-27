(function () {

  const root = document.documentElement;
  const key = "theme";

  const themes = {
    light: {
      bg: "#ffffff",
      text: "#111111",
      border: "#e5e5e5"
    },
    dark: {
      bg: "#0f0f0f",
      text: "#eaeaea",
      border: "#2a2a2a"
    },
    sepia: {
      bg: "#f4ecd8",
      text: "#3b2f2f",
      border: "#d6c6a6"
    }
  };

  function applyTheme(name) {
    const t = themes[name];
    if (!t) return;

    root.style.setProperty("--bg", t.bg);
    root.style.setProperty("--text", t.text);
    root.style.setProperty("--border", t.border);

    localStorage.setItem(key, name);
  }

  window.setTheme = function (name) {
    applyTheme(name);
  };

  document.addEventListener("DOMContentLoaded", function () {
    const saved = localStorage.getItem(key) || "light";
    applyTheme(saved);
  });

})();
(function () {

  const root = document.documentElement;
  const key = "theme";

  const themes = {
    light: {
      bg: "#ffffff",
      text: "#111111",
      border: "#e5e5e5",
      link: "#2563eb",
      muted: "#666666"
    },
    dark: {
      bg: "#2d3143",
      text: "#bdcadb",
      border: "#2a2a2a",
      link: "#8ab4f8",
      muted: "#aaaaaa"
    },
    sepia: {
      bg: "#f4ecd8",
      text: "#3b2f2f",
      border: "#d6c6a6",
      link: "#8b5e3c",
      muted: "#7a6a58"
    }
  };

  function applyTheme(name) {
    const t = themes[name];
    if (!t) return;

    for (let key in t) {
      root.style.setProperty("--" + key, t[key]);
    }

    localStorage.setItem("theme", name);
  }

  window.setTheme = function (name) {
    applyTheme(name);
  };

  document.addEventListener("DOMContentLoaded", function () {
    const saved = localStorage.getItem("theme") || "light";
    applyTheme(saved);
  });

})();
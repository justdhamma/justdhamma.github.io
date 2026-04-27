(function () {

  const root = document.documentElement;
  const STORAGE_KEY = "theme";

  const toggle = document.getElementById("theme-toggle");
  const menu = document.getElementById("theme-menu");
  const buttons = menu ? menu.querySelectorAll("button") : [];

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

    Object.keys(theme).forEach(key => {
      root.style.setProperty("--" + key, theme[key]);
    });

    localStorage.setItem(STORAGE_KEY, name);

    // update icon
    if (toggle) toggle.textContent = icons[name];

    // highlight active
    buttons.forEach(btn => {
      btn.classList.toggle("active", btn.dataset.theme === name);
    });
  }

  window.setTheme = function (name) {
    applyTheme(name);
    if (menu) menu.classList.remove("show");
  };

  /* dropdown toggle */
  if (toggle && menu) {
    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      menu.classList.toggle("show");
    });

    document.addEventListener("click", function () {
      menu.classList.remove("show");
    });
  }

  /* attach click to buttons */
  buttons.forEach(btn => {
    btn.addEventListener("click", function () {
      setTheme(btn.dataset.theme);
    });
  });

  /* init */
  document.addEventListener("DOMContentLoaded", function () {
    const saved = localStorage.getItem(STORAGE_KEY) || "light";
    applyTheme(saved);
  });

})();
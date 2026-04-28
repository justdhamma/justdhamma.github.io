(function () {
  const root = document.documentElement;
  const STORAGE_KEY = "theme";
  const switchers = document.querySelectorAll(".theme-switcher");

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

    switchers.forEach(function (switcher) {
      const toggle = switcher.querySelector(".theme-toggle-button");
      const buttons = switcher.querySelectorAll(".theme-menu button");

      if (toggle) {
        toggle.textContent = icons[name];
      }

      buttons.forEach(function (button) {
        button.classList.toggle("active", button.dataset.theme === name);
      });
    });
  }

  function closeMenus() {
    switchers.forEach(function (switcher) {
      const menu = switcher.querySelector(".theme-menu");
      if (menu) {
        menu.classList.remove("show");
      }
    });
  }

  window.setTheme = function (name) {
    applyTheme(name);
    closeMenus();
  };

  switchers.forEach(function (switcher) {
    const toggle = switcher.querySelector(".theme-toggle-button");
    const menu = switcher.querySelector(".theme-menu");
    const buttons = switcher.querySelectorAll(".theme-menu button");

    if (toggle && menu) {
      toggle.addEventListener("click", function (event) {
        if (window.innerWidth <= 640) return;

        event.stopPropagation();
        menu.classList.toggle("show");
      });
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        setTheme(button.dataset.theme);
      });
    });
  });

  document.addEventListener("click", function () {
    closeMenus();
  });

  document.addEventListener("DOMContentLoaded", function () {
    const saved = localStorage.getItem(STORAGE_KEY) || "light";
    applyTheme(saved);
  });
})();

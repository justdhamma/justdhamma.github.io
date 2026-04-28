(function () {
  function closeMenu(navbar) {
    navbar.classList.remove("nav-open");
    document.body.classList.remove("nav-menu-open");

    const toggle = navbar.querySelector(".nav-toggle");
    const backdrop = navbar.querySelector(".nav-backdrop");

    if (toggle) {
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
    }

    if (backdrop) {
      backdrop.hidden = true;
    }
  }

  function openMenu(navbar) {
    navbar.classList.add("nav-open");
    document.body.classList.add("nav-menu-open");

    const toggle = navbar.querySelector(".nav-toggle");
    const backdrop = navbar.querySelector(".nav-backdrop");

    if (toggle) {
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Close menu");
    }

    if (backdrop) {
      backdrop.hidden = false;
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const navbars = document.querySelectorAll(".navbar");

    navbars.forEach(function (navbar) {
      const toggle = navbar.querySelector(".nav-toggle");
      const menu = navbar.querySelector(".nav-menu");
      const backdrop = navbar.querySelector(".nav-backdrop");

      if (!toggle || !menu) return;

      toggle.addEventListener("click", function (event) {
        event.stopPropagation();

        if (navbar.classList.contains("nav-open")) {
          closeMenu(navbar);
        } else {
          openMenu(navbar);
        }
      });

      menu.addEventListener("click", function (event) {
        const target = event.target;
        if (target instanceof HTMLAnchorElement) {
          closeMenu(navbar);
        }
      });

      if (backdrop) {
        backdrop.addEventListener("click", function () {
          closeMenu(navbar);
        });
      }
    });

    document.addEventListener("click", function (event) {
      navbars.forEach(function (navbar) {
        if (!navbar.contains(event.target)) {
          closeMenu(navbar);
        }
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        navbars.forEach(closeMenu);
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 640) {
        navbars.forEach(closeMenu);
      }
    });
  });
})();

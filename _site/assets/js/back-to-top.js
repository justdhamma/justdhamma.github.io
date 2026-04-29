(function () {
  const VISIBILITY_THRESHOLD = 180;

  function syncTopButton() {
    const button = document.getElementById("top-toggle");
    if (!button) return;

    const shouldShow = window.scrollY > VISIBILITY_THRESHOLD;
    button.textContent = shouldShow ? "↑" : "☸";
    button.setAttribute("aria-label", shouldShow ? "Scroll to top" : "Dharma wheel");
  }

  window.scrollToTop = function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  };

  document.addEventListener("DOMContentLoaded", syncTopButton);
  window.addEventListener("scroll", syncTopButton, { passive: true });
})();

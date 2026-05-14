(function () {
  const VISIBILITY_THRESHOLD = 180;

  function syncTopButton() {
    const button = document.getElementById("top-toggle");
    if (!button) return;

    const shouldShowTop = window.scrollY > VISIBILITY_THRESHOLD;
    button.textContent = shouldShowTop ? "↑" : "↓";
    button.setAttribute("aria-label", shouldShowTop ? "Scroll to top" : "Scroll to bottom");
    button.onclick = shouldShowTop ? scrollToTop : scrollToBottom;
  }

  window.scrollToTop = function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  };

  window.scrollToBottom = function () {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth"
    });
  };

  document.addEventListener("DOMContentLoaded", syncTopButton);
  window.addEventListener("scroll", syncTopButton, { passive: true });
})();

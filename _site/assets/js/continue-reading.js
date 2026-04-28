(function () {
  const key = "scroll-pos:" + window.location.pathname;
  let ticking = false;

  function saveScroll() {
    localStorage.setItem(key, window.scrollY);
  }

  function restoreScroll() {
    const saved = localStorage.getItem(key);
    if (saved !== null) {
      window.scrollTo(0, parseInt(saved, 10));
    }
  }

  window.addEventListener("scroll", function () {
    if (!ticking) {
      window.requestAnimationFrame(function () {
        saveScroll();
        ticking = false;
      });
      ticking = true;
    }
  });

  document.addEventListener("DOMContentLoaded", restoreScroll);
})();

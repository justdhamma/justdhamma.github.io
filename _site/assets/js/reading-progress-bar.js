(function () {
  const bar = document.getElementById("progress-bar");

  function updateProgress() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;

    bar.style.width = progress + "%";
  }

  window.addEventListener("scroll", updateProgress);
})();
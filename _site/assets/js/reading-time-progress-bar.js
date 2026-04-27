(function () {

  /* -------------------------
     READING TIME
  --------------------------*/
  function readingTime() {
    const content = document.querySelector(".post-content");
    if (!content) return;

    const words = content.innerText.trim().split(/\s+/).length;
    const minutes = Math.ceil(words / 200);

    const el = document.getElementById("reading-time");
    if (el) el.textContent = `${minutes} min read`;
  }

  /* -------------------------
     PROGRESS BAR
  --------------------------*/
  function progressBar() {
    const bar = document.getElementById("progress-bar");
    const content = document.querySelector(".post-content");

    if (!bar || !content) return;

    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;

    const progress = (scrollTop / docHeight) * 100;
    bar.style.width = progress + "%";
  }

  document.addEventListener("DOMContentLoaded", readingTime);
  window.addEventListener("scroll", progressBar);

})();
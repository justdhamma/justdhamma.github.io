(function () {
  function calculateReadingTime() {
    const content = document.querySelector(".post-content");
    if (!content) return;

    const text = content.innerText || "";
    
    // Average reading speed (adjust if you want slower/faster feel)
    const wordsPerMinute = 200;

    const wordCount = text.trim().split(/\s+/).length;
    const minutes = Math.ceil(wordCount / wordsPerMinute);

    const el = document.getElementById("reading-time");
    if (el) {
      el.textContent = `${minutes} min read`;
    }
  }

  document.addEventListener("DOMContentLoaded", calculateReadingTime);
})();
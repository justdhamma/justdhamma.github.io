(function () {
  function syncTranscriptTagSections() {
    const sections = document.querySelectorAll(".transcript-tag-section");
    if (!sections.length) return;

    const hash = window.location.hash;
    const hasTagHash = hash.indexOf("#tag-") === 0;

    sections.forEach(function (section) {
      const shouldShow = !hasTagHash || ("#" + section.id) === hash;
      section.classList.toggle("is-hidden", !shouldShow);
    });
  }

  document.addEventListener("DOMContentLoaded", syncTranscriptTagSections);
  window.addEventListener("hashchange", syncTranscriptTagSections);
})();

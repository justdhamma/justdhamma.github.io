(function () {

  const STORAGE_KEY_PREFIX = "font-size";
  const DEFAULT_SIZES = {
    en: 18,
    ne: 19
  };

  function getContent() {
    return document.querySelector(".post-content");
  }

  function getLanguage() {
    const content = getContent();
    if (content) {
      if (content.classList.contains("ne")) return "ne";
      if (content.classList.contains("en")) return "en";
    }

    if (document.body.classList.contains("lang-ne")) return "ne";
    return "en";
  }

  function getStorageKey() {
    return STORAGE_KEY_PREFIX + "-" + getLanguage();
  }

  function getDefaultSize() {
    return DEFAULT_SIZES[getLanguage()] || DEFAULT_SIZES.en;
  }

  function applyFontSize(size) {
    const content = getContent();
    if (!content) return;

    content.style.fontSize = size + "px";
  }

  function getSavedSize() {
    const saved = parseInt(localStorage.getItem(getStorageKey()), 10);
    return Number.isNaN(saved) ? getDefaultSize() : saved;
  }

  function saveSize(size) {
    localStorage.setItem(getStorageKey(), size);
  }

  // exposed globally for buttons
  window.changeFontSize = function (delta) {
    let current = getSavedSize();
    let next = current + delta;

    // limits (prevents broken layout)
    if (next < 14) next = 14;
    if (next > 28) next = 28;

    applyFontSize(next);
    saveSize(next);
  };

  document.addEventListener("DOMContentLoaded", function () {
    applyFontSize(getSavedSize());
  });

})();

(function () {

  const STORAGE_KEY = "font-size";

  const DEFAULT_SIZE = 19; // matches your reading font size

  function applyFontSize(size) {
    document.querySelector(".post-content").style.fontSize = size + "px";
  }

  function getSavedSize() {
    return parseInt(localStorage.getItem(STORAGE_KEY)) || DEFAULT_SIZE;
  }

  function saveSize(size) {
    localStorage.setItem(STORAGE_KEY, size);
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
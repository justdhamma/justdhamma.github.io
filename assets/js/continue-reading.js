// (function () {

//   const key = "scroll-pos:" + window.location.pathname;

//   /* -------------------------
//      SAVE SCROLL POSITION
//   --------------------------*/
//   function saveScroll() {
//     localStorage.setItem(key, window.scrollY);
//   }

//   /* -------------------------
//      RESTORE SCROLL POSITION
//   --------------------------*/
//   function restoreScroll() {
//     const saved = localStorage.getItem(key);
//     if (saved !== null) {
//       window.scrollTo(0, parseInt(saved, 10));
//     }
//   }

//   /* -------------------------
//      EVENTS
//   --------------------------*/
//   document.addEventListener("DOMContentLoaded", restoreScroll);
//   window.addEventListener("scroll", function () {
//     window.requestAnimationFrame(saveScroll);
//   });

// })();


(function () {

  const key = "scroll-pos:" + window.location.pathname;

  let ticking = false;

  /* -------------------------
     SAVE SCROLL (THROTTLED)
  --------------------------*/
  function saveScroll() {
    localStorage.setItem(key, window.scrollY);
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

  /* -------------------------
     RESTORE SCROLL POSITION
  --------------------------*/
  function restoreScroll() {
    const saved = localStorage.getItem(key);
    if (saved !== null) {
      window.scrollTo(0, parseInt(saved, 10));
    }
  }

  /* -------------------------
     CONTINUE READING HINT
  --------------------------*/
  function showContinueHint() {
    const saved = localStorage.getItem(key);

    if (saved && parseInt(saved, 10) > 100) {
      const el = document.getElementById("continue-reading");
      if (el) el.style.display = "block";
    }
  }

  /* -------------------------
     INIT
  --------------------------*/
  document.addEventListener("DOMContentLoaded", function () {
    restoreScroll();
    showContinueHint();
  });

})();
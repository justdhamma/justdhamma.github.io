(function () {

  /* -------------------------
     BACK TO TOP SMOOTH SCROLL
  --------------------------*/
  window.scrollToTop = function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  };

  /* -------------------------
     SHOW/HIDE BUTTON ON SCROLL
  --------------------------*/
  const btn = document.getElementById("back-to-top");

  function toggleButton() {
    if (!btn) return;

    if (window.scrollY > 300) {
      btn.style.display = "block";
    } else {
      btn.style.display = "none";
    }
  }

  window.addEventListener("scroll", toggleButton);

})();












// (function () {

//   /* -------------------------
//      SMOOTH SCROLL TO TOP
//   --------------------------*/
//   window.scrollToTop = function () {
//     window.scrollTo({
//       top: 0,
//       behavior: "smooth"
//     });
//   };

//   /* -------------------------
//      BACK TO TOP BUTTON
//   --------------------------*/
//   const btn = document.getElementById("back-to-top");

//   function toggleBackToTop() {
//     if (!btn) return;

//     // your requested logic (opacity control)
//     btn.style.opacity = (window.scrollY > 300) ? "1" : "0";

//     // optional: prevent clicking when hidden
//     btn.style.pointerEvents = (window.scrollY > 300) ? "auto" : "none";
//   }

//   /* -------------------------
//      INIT
//   --------------------------*/
//   document.addEventListener("DOMContentLoaded", function () {
//     toggleBackToTop();
//   });

//   window.addEventListener("scroll", function () {
//     window.requestAnimationFrame(toggleBackToTop);
//   });

// })();





// (function () {

//   /* -------------------------
//      SMOOTH SCROLL TO TOP
//   --------------------------*/
//   window.scrollToTop = function () {
//     window.scrollTo({
//       top: 0,
//       behavior: "smooth"
//     });
//   };

//   /* -------------------------
//      BACK TO TOP (scroll-aware)
//   --------------------------*/
//   const btn = document.getElementById("back-to-top");

//   let lastScrollY = window.scrollY;

//   function handleScroll() {
//     if (!btn) return;

//     const currentScrollY = window.scrollY;

//     // Show only after threshold
//     const shouldShow = currentScrollY > 300;

//     // Detect scroll direction
//     const scrollingUp = currentScrollY < lastScrollY;

//     if (shouldShow && scrollingUp) {
//       btn.style.opacity = "1";
//       btn.style.pointerEvents = "auto";
//     } else {
//       btn.style.opacity = "0";
//       btn.style.pointerEvents = "none";
//     }

//     lastScrollY = currentScrollY;
//   }

//   /* -------------------------
//      INIT
//   --------------------------*/
//   document.addEventListener("DOMContentLoaded", function () {
//     handleScroll();
//   });

//   window.addEventListener("scroll", function () {
//     window.requestAnimationFrame(handleScroll);
//   });

// })();
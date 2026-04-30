(function () {
  function getEmbedUrl(url) {
    try {
      const parsed = new URL(url, window.location.origin);
      let videoId = "";

      if (parsed.hostname.includes("youtu.be")) {
        videoId = parsed.pathname.replace("/", "");
      } else {
        videoId = parsed.searchParams.get("v") || "";
      }

      if (!videoId) return "";
      return "https://www.youtube.com/embed/" + videoId;
    } catch (error) {
      return "";
    }
  }

  function initTranscriptEmbed() {
    const trigger = document.querySelector(".transcript-video-trigger");
    const container = document.getElementById("transcript-video-embed");
    if (!trigger || !container) return;

    trigger.addEventListener("click", function () {
      const isOpen = !container.hasAttribute("hidden");

      if (isOpen) {
        container.innerHTML = "";
        container.setAttribute("hidden", "");
        trigger.setAttribute("aria-expanded", "false");
        return;
      }

      const embedUrl = getEmbedUrl(trigger.dataset.youtubeUrl || "");
      if (!embedUrl) return;

      container.innerHTML =
        '<iframe src="' +
        embedUrl +
        '" title="YouTube video player" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>';
      container.removeAttribute("hidden");
      trigger.setAttribute("aria-expanded", "true");
    });
  }

  document.addEventListener("DOMContentLoaded", initTranscriptEmbed);
})();

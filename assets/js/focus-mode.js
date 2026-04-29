function syncReadButton() {
  const button = document.getElementById("focus-toggle");
  if (!button) return;

  const isReadMode = document.body.classList.contains("read-mode");
  button.textContent = "📖";
  button.setAttribute("aria-pressed", isReadMode ? "true" : "false");
  button.setAttribute("aria-label", isReadMode ? "Exit reading mode" : "Enter reading mode");
}

window.toggleFocus = function toggleFocus() {
  document.body.classList.toggle("read-mode");
  document.body.classList.remove("focus-mode");
  syncReadButton();
};

document.addEventListener("DOMContentLoaded", syncReadButton);

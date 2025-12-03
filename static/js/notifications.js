// static/js/notifications.js
document.addEventListener("DOMContentLoaded", () => {
  const bell = document.getElementById("notifToggle");
  const dropdown = document.getElementById("notifDropdown");
  const closeBtn = document.getElementById("notifClose");

  if (!bell || !dropdown) return;

  const openDropdown = () => {
    dropdown.classList.remove("hidden");
  };

  const closeDropdown = () => {
    dropdown.classList.add("hidden");
  };

  bell.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdown.classList.toggle("hidden");
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      closeDropdown();
    });
  }

  // close kung mo-click outside
  document.addEventListener("click", (e) => {
    if (!dropdown.classList.contains("hidden")) {
      if (!dropdown.contains(e.target) && e.target !== bell) {
        closeDropdown();
      }
    }
  });

  // ESC key to close
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeDropdown();
    }
  });
  
  // Add scroll handling for notifications dropdown
  const notificationContainer = dropdown.querySelector('.max-h-80');
  if (notificationContainer) {
    notificationContainer.addEventListener('wheel', (e) => {
      e.stopPropagation();
    });
  }
});
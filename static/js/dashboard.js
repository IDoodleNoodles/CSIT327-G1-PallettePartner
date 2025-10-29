document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const toggleSidebar = document.getElementById('toggleSidebar');
  const sidebarOverlay = document.getElementById('sidebarOverlay');
  const menuLabel = document.getElementById('menuLabel');
  const modal = document.getElementById('createModal');
  const overlay = document.getElementById('overlay');
  const addPostBtn = document.getElementById('addPostBtn');
  const closeModalBtn = document.getElementById('closeModal');

  // Toggle Sidebar Open/Close with Mobile Overlay
  toggleSidebar.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');

    // Handle mobile overlay
    if (window.innerWidth < 1024) {
      if (sidebar.classList.contains('collapsed')) {
        sidebar.style.transform = 'translateX(-100%)';
        sidebarOverlay.classList.add('hidden');
      } else {
        sidebar.style.transform = 'translateX(0)';
        sidebarOverlay.classList.remove('hidden');
      }
    }

    if (sidebar.classList.contains('collapsed')) {
      menuLabel.style.display = 'none';
    } else {
      menuLabel.style.display = 'inline';
    }
  });

  // Close sidebar when clicking overlay
  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', () => {
      sidebar.classList.add('collapsed');
      sidebar.style.transform = 'translateX(-100%)';
      sidebarOverlay.classList.add('hidden');
      menuLabel.style.display = 'none';
    });
  }

  // Handle responsive sidebar on window resize
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024) {
      sidebar.style.transform = 'translateX(0)';
      sidebarOverlay.classList.add('hidden');
    } else if (sidebar.classList.contains('collapsed')) {
      sidebar.style.transform = 'translateX(-100%)';
    }
  });

  // Modal Logic
  if (addPostBtn) {
    addPostBtn.addEventListener('click', () => {
      modal.classList.add('show');
      overlay.classList.add('show');
    });
  }

  const closeModal = () => {
    modal.classList.remove('show');
    overlay.classList.remove('show');
  };

  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeModal);
  }

  if (overlay) {
    overlay.addEventListener('click', closeModal);
  }

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
  });
});
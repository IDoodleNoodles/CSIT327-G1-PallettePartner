document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const toggleSidebar = document.getElementById('toggleSidebar'); // optional
  const sidebarOverlay = document.getElementById('sidebarOverlay');
  const menuLabel = document.getElementById('menuLabel'); // optional
  const modal = document.getElementById('createModal');
  const overlay = document.getElementById('overlay');
  const addPostBtn = document.getElementById('addPostBtn');
  const closeModalBtn = document.getElementById('closeModal');
  const scrollToTopBtn = document.getElementById('scrollToTop');
  const mainContent = document.querySelector('main');

  /* =========================
     Sidebar toggle + overlay
  ========================== */

  if (toggleSidebar && sidebar) {
    toggleSidebar.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');

      // Handle mobile overlay
      if (window.innerWidth < 1024) {
        if (sidebar.classList.contains('collapsed')) {
          sidebar.style.transform = 'translateX(-100%)';
          if (sidebarOverlay) sidebarOverlay.classList.add('hidden');
        } else {
          sidebar.style.transform = 'translateX(0)';
          if (sidebarOverlay) sidebarOverlay.classList.remove('hidden');
        }
      }

      if (menuLabel) {
        if (sidebar.classList.contains('collapsed')) {
          menuLabel.style.display = 'none';
        } else {
          menuLabel.style.display = 'inline';
        }
      }
    });
  }

  // Close sidebar when clicking overlay
  if (sidebarOverlay && sidebar) {
    sidebarOverlay.addEventListener('click', () => {
      sidebar.classList.add('collapsed');
      sidebar.style.transform = 'translateX(-100%)';
      sidebarOverlay.classList.add('hidden');
      if (menuLabel) menuLabel.style.display = 'none';
    });
  }

  // Handle responsive sidebar on window resize
  if (sidebar) {
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 1024) {
        sidebar.style.transform = 'translateX(0)';
        if (sidebarOverlay) sidebarOverlay.classList.add('hidden');
      } else if (sidebar.classList.contains('collapsed')) {
        sidebar.style.transform = 'translateX(-100%)';
      }
    });
  }

  /* ==============
     Modal logic
  ============== */

  if (addPostBtn && modal && overlay) {
    addPostBtn.addEventListener('click', () => {
      modal.classList.add('show');
      overlay.classList.add('show');
    });
  }

  const closeModal = () => {
    if (!modal || !overlay) return;
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

  /* ==================
     Scroll to Top btn
  =================== */

  if (scrollToTopBtn && mainContent) {
    mainContent.addEventListener('scroll', () => {
      if (mainContent.scrollTop > 300) {
        scrollToTopBtn.classList.remove('opacity-0', 'pointer-events-none');
        scrollToTopBtn.classList.add('opacity-100');
      } else {
        scrollToTopBtn.classList.add('opacity-0', 'pointer-events-none');
        scrollToTopBtn.classList.remove('opacity-100');
      }
    });

    scrollToTopBtn.addEventListener('click', () => {
      mainContent.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* =========================
     Floating comments panel
  ========================== */

  const commentsPanel = document.getElementById('commentsPanel');
  const commentsFrame = document.getElementById('commentsFrame');
  const closeCommentsPanel = document.getElementById('closeCommentsPanel');
  const commentsHeader = document.getElementById('commentsPanelHeader');

  if (commentsPanel && commentsFrame && closeCommentsPanel && commentsHeader) {
    // open panel when clicking comment icon
    document.querySelectorAll('.open-comments').forEach(btn => {
      btn.addEventListener('click', () => {
        const url = btn.dataset.commentsUrl;
        if (!url) return;
        commentsFrame.src = url;
        commentsPanel.classList.remove('hidden');
      });
    });

    // close panel
    closeCommentsPanel.addEventListener('click', () => {
      commentsPanel.classList.add('hidden');
      commentsFrame.src = '';
    });

    // draggable behavior
    let isDragging = false;
    let offsetX = 0;
    let offsetY = 0;

    commentsHeader.addEventListener('mousedown', (e) => {
      isDragging = true;
      const rect = commentsPanel.getBoundingClientRect();
      offsetX = e.clientX - rect.left;
      offsetY = e.clientY - rect.top;
      document.body.classList.add('select-none');
    });

    document.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      commentsPanel.style.left = (e.clientX - offsetX) + 'px';
      commentsPanel.style.top = (e.clientY - offsetY) + 'px';
      commentsPanel.style.right = 'auto'; // so left/top take control
    });

    document.addEventListener('mouseup', () => {
      if (!isDragging) return;
      isDragging = false;
      document.body.classList.remove('select-none');
    });
  }
});
// static/js/dashboard.js
document.addEventListener('DOMContentLoaded', () => {
  const sidebarOverlay = document.getElementById('sidebarOverlay');
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.querySelector('main');
  const scrollToTopBtn = document.getElementById('scrollToTop');

  // Scroll to top
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

  // (Optional) close sidebar on overlay click (mobile)
  if (sidebarOverlay && sidebar) {
    sidebarOverlay.addEventListener('click', () => {
      sidebarOverlay.classList.add('hidden');
    });
  }

  // Create Collaboration modal
  const addPostBtn = document.getElementById('addPostBtn');
  const modal = document.getElementById('createModal');
  const overlay = document.getElementById('overlay');
  const closeModalBtn = document.getElementById('closeModal');

  const closeModal = () => {
    if (!modal || !overlay) return;
    modal.style.display = 'none';
    overlay.style.display = 'none';
  };

  if (addPostBtn && modal && overlay) {
    addPostBtn.addEventListener('click', () => {
      modal.style.display = 'block';
      overlay.style.display = 'block';
    });
  }

  if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
  if (overlay) overlay.addEventListener('click', closeModal);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
});
document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const toggleSidebar = document.getElementById('toggleSidebar');
  const backButton = document.getElementById('backButton');
  const menuLabel = document.getElementById('menuLabel');
  const modal = document.getElementById('createModal');
  const overlay = document.getElementById('overlay');
  const addPostBtn = document.getElementById('addPostBtn');
  const closeModalBtn = document.getElementById('closeModal');

  // Toggle Sidebar Open/Close
  toggleSidebar.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    if (sidebar.classList.contains('collapsed')) {
      menuLabel.style.display = 'none';
    } else {
      menuLabel.style.display = 'inline';
    }
  });

  // Back Button Functionality
  backButton.addEventListener('click', () => {
    window.history.back();
  });

  // Modal Logic
  addPostBtn.addEventListener('click', () => {
    modal.classList.add('show');
    overlay.classList.add('show');
  });

  const closeModal = () => {
    modal.classList.remove('show');
    overlay.classList.remove('show');
  };

  closeModalBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', closeModal);

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
  });
});
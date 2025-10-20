// Smooth Navigation, Sidebar, and Modal Initialization
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-item');
    const sidebar = document.getElementById('sidebar');
    const toggleButton = document.getElementById('toggleSidebar');
    const floatingBtn = document.getElementById('addPostBtn');
    const postModal = document.getElementById('createModal');
    const overlay = document.getElementById('overlay');

    // --- Highlight Active Page ---
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href)) {
            link.classList.add('bg-[#111827]', 'text-[#7EBFB3]');
        } else {
            link.classList.remove('bg-[#111827]', 'text-[#7EBFB3]');
        }

        // Smooth fade transition between pages
        link.addEventListener('click', e => {
            e.preventDefault();
            document.body.style.opacity = '0.85';
            setTimeout(() => (window.location.href = link.getAttribute('href')), 150);
        });
    });

    // --- Sidebar Toggle ---
    if (toggleButton && sidebar) {
        toggleButton.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            sidebar.classList.toggle('overflow-hidden');

            // Smooth animation
            sidebar.style.transition = 'width 0.4s ease';
        });
    }

    // --- Floating Button: Open Modal ---
    if (floatingBtn && postModal) {
        floatingBtn.addEventListener('click', () => {
            postModal.classList.add('show');
            if (overlay) overlay.classList.add('show');
        });
    }

    // --- Close Modal ---
    if (overlay && postModal) {
        overlay.addEventListener('click', () => {
            postModal.classList.remove('show');
            overlay.classList.remove('show');
        });
    }

    // Close modal with ESC key
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && postModal?.classList.contains('show')) {
            postModal.classList.remove('show');
            if (overlay) overlay.classList.remove('show');
        }
    });
}

// --- Run after DOM Loads ---
document.addEventListener('DOMContentLoaded', initializeNavigation);
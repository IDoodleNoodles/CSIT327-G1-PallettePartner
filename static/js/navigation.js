// Navigation functionality
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }

        link.addEventListener('click', function (e) {
            e.preventDefault();
            document.body.style.opacity = '0.8';
            setTimeout(() => {
                window.location.href = this.getAttribute('href');
            }, 150);
        });
    });
}
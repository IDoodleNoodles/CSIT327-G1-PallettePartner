// Animations on scroll
function initializeAnimations() {
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    const elementsToAnimate = document.querySelectorAll('.card, .sidebar-section, .portfolio-item');
    elementsToAnimate.forEach(el => observer.observe(el));
}
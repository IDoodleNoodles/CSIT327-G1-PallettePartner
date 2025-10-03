function showView(viewId) {
    const views = document.querySelectorAll('.view');
    views.forEach(view => {
        view.classList.add('hidden');
    });

    const targetView = document.getElementById(viewId);
    if (targetView) {
        targetView.classList.remove('hidden');
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Main initializer
document.addEventListener('DOMContentLoaded', function () {
    // Show landing page by default
    showView('LandingPage');

    // Initialize interactive features
    initializeNavigation();
    initializeFeedFilters();
    initializeCardInteractions();
    initializePortfolioFilters();
    initializeChat();
    initializeTimeline();
    initializeAnimations();
});
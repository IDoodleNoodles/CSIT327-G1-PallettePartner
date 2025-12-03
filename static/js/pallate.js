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

    // Skip feed filters on dashboard since it has its own category filter
    const isDashboardPage = document.getElementById('categoryFilterButton');
    
    // Initialize interactive features (safely check if functions exist)
    if (typeof initializeNavigation === 'function') {
        initializeNavigation();
    }
    
    // Only initialize feed filters if not on dashboard
    if (!isDashboardPage && typeof initializeFeedFilters === 'function') {
        initializeFeedFilters();
    }
    
    if (typeof initializeCardInteractions === 'function') {
        initializeCardInteractions();
    }
    
    if (typeof initializePortfolioFilters === 'function') {
        initializePortfolioFilters();
    }
    
    if (typeof initializeChat === 'function') {
        initializeChat();
    }
    
    if (typeof initializeTimeline === 'function') {
        initializeTimeline();
    }
    
    if (typeof initializeAnimations === 'function') {
        initializeAnimations();
    }
});
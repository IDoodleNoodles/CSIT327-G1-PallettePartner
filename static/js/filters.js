// Feed filter functionality
function initializeFeedFilters() {
    // Check if we're on a page with filter buttons to avoid conflicts
    // Also check if we're on the dashboard page where we have a different category filter
    const simpleCategoryFilter = document.querySelector('.category-filter-btn');
    if (simpleCategoryFilter) return; // We're on dashboard, let simple-category-filter.js handle filtering
    
    const filterButtons = document.querySelectorAll('.filter-btn');
    if (filterButtons.length === 0) return; // No filter buttons, exit early
    
    const cards = document.querySelectorAll('.card');

    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            const filter = this.textContent.toLowerCase();

            cards.forEach(card => {
                if (filter === 'all') {
                    card.style.display = 'block';
                    card.classList.add('fade-in');
                } else {
                    const tags = Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent.toLowerCase());
                    card.style.display = tags.includes(filter) ? 'block' : 'none';
                }
            });
        });
    });
}
// Portfolio filter functionality
function initializePortfolioFilters() {
    const portfolioFilterButtons = document.querySelectorAll('.portfolio-filters .filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');

    portfolioFilterButtons.forEach(button => {
        button.addEventListener('click', function () {
            portfolioFilterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            const filter = this.textContent.toLowerCase();

            portfolioItems.forEach(item => {
                const overlay = item.querySelector('.portfolio-overlay');
                const title = overlay ? overlay.querySelector('h4').textContent.toLowerCase() : '';
                const description = overlay ? overlay.querySelector('p').textContent.toLowerCase() : '';

                if (filter === 'all' || title.includes(filter) || description.includes(filter)) {
                    item.style.display = 'block';
                    item.classList.add('fade-in');
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}
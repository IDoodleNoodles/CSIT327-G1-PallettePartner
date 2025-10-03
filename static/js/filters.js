// Feed filter functionality
function initializeFeedFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
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
// Favorites Toggle with AJAX
document.addEventListener('DOMContentLoaded', function () {
    // Add event listeners to all favorite buttons
    const favoriteLinks = document.querySelectorAll('a[href*="toggle_favorite"]');

    favoriteLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const url = this.href;
            const heartIcon = this.querySelector('span');
            const isCurrentlyFavorited = heartIcon.textContent.trim() === '❤️';

            // Add pulse animation
            heartIcon.style.transition = 'transform 0.2s ease';
            heartIcon.style.transform = 'scale(1.3)';
            setTimeout(() => {
                heartIcon.style.transform = 'scale(1)';
            }, 200);

            // Send AJAX request
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
                .then(response => response.json())
                .then(data => {
                    // Toggle the heart icon based on response
                    if (data.favorited) {
                        heartIcon.textContent = '❤️';
                        this.title = 'Remove from favorites';

                        // Show toast notification
                        showToast('Added to favorites! ❤️', 'success');
                    } else {
                        heartIcon.textContent = '🤍';
                        this.title = 'Add to favorites';

                        showToast('Removed from favorites', 'info');

                        // If on favorites page, remove the card with animation
                        if (window.location.pathname.includes('favorites')) {
                            const card = this.closest('.bg-\\[\\#1A2035\\]');
                            if (card) {
                                card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                                card.style.opacity = '0';
                                card.style.transform = 'scale(0.9)';
                                setTimeout(() => {
                                    card.remove();

                                    // Check if no favorites left
                                    const remainingCards = document.querySelectorAll('.bg-\\[\\#1A2035\\]');
                                    if (remainingCards.length === 0) {
                                        location.reload();
                                    }
                                }, 300);
                            }
                        }
                    }
                })
                .catch(error => {
                    console.error('Error toggling favorite:', error);
                    showToast('Failed to update favorite. Please try again.', 'error');
                    // Fallback to page reload if AJAX fails
                    setTimeout(() => {
                        window.location.href = url;
                    }, 1000);
                });
        });
    });

    // Toast notification function
    function showToast(message, type = 'info') {
        // Remove existing toast
        const existingToast = document.getElementById('toast');
        if (existingToast) {
            existingToast.remove();
        }

        const colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            info: 'bg-blue-500'
        };

        const toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = `fixed bottom-6 left-1/2 transform -translate-x-1/2 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300`;
        toast.style.opacity = '0';
        toast.textContent = message;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '1';
        }, 10);

        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 2000);
    }
});

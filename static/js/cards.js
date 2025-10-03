// Card interactions
function initializeCardInteractions() {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-4px)';
            this.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.5)';
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.4)';
        });

        const likeButtons = card.querySelectorAll('.btn-icon');
        likeButtons.forEach(button => {
            if (button.querySelector('.fa-heart')) {
                button.addEventListener('click', function (e) {
                    e.stopPropagation();
                    const icon = this.querySelector('i');
                    if (icon.classList.contains('fa-heart')) {
                        icon.classList.remove('fa-heart');
                        icon.classList.add('fas', 'fa-heart');
                        this.style.color = '#E74C3C';
                        showNotification('Added to favorites!', 'success');
                    } else {
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                        this.style.color = '';
                        showNotification('Removed from favorites', 'info');
                    }
                });
            }

            if (button.querySelector('.fa-bookmark')) {
                button.addEventListener('click', function (e) {
                    e.stopPropagation();
                    const icon = this.querySelector('i');
                    if (icon.classList.contains('fa-bookmark')) {
                        icon.classList.remove('fa-bookmark');
                        icon.classList.add('fas', 'fa-bookmark');
                        this.style.color = '#F39C12';
                        showNotification('Bookmarked!', 'success');
                    } else {
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                        this.style.color = '';
                        showNotification('Removed bookmark', 'info');
                    }
                });
            }
        });
    });
}
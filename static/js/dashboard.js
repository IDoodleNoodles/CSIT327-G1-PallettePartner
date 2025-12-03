document.addEventListener('DOMContentLoaded', function() {
  const categoryFilterButton = document.getElementById('categoryFilterButton');
  const categoryFilterDropdown = document.getElementById('categoryFilterDropdown');
  const applyCategoryFilter = document.getElementById('applyCategoryFilter');
  const clearCategoryFilter = document.getElementById('clearCategoryFilter');
  const categoryCheckboxes = document.querySelectorAll('input[name="category_filter"]');

  if (categoryFilterButton) {
    categoryFilterButton.addEventListener('click', function(e) {
      e.stopPropagation();
      categoryFilterDropdown.classList.toggle('hidden');
    });
  }

  document.addEventListener('click', function(event) {
    if (categoryFilterDropdown && !categoryFilterButton.contains(event.target) && !categoryFilterDropdown.contains(event.target)) {
      categoryFilterDropdown.classList.add('hidden');
    }
  });

  categoryCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      const span = this.nextElementSibling.querySelector('span');
      if (this.checked) {
        span.classList.add('bg-[#8B5CF6]');
        span.innerHTML = '<svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>';
      } else {
        span.classList.remove('bg-[#8B5CF6]');
        span.innerHTML = '';
      }
    });
  });

  if (clearCategoryFilter) {
    clearCategoryFilter.addEventListener('click', function() {
      categoryCheckboxes.forEach(cb => {
        cb.checked = false;
        const span = cb.nextElementSibling.querySelector('span');
        span.classList.remove('bg-[#8B5CF6]');
        span.innerHTML = '';
      });

      const url = new URL(window.location);
      url.searchParams.delete('categories');
      window.location.href = url.toString();
    });
  }

  // Handle comments panel opening - use event delegation for dynamically loaded content
  document.addEventListener('click', function(e) {
    // Handle comments panel opening
    if (e.target.closest('.open-comments')) {
      const commentsPanel = document.getElementById('commentsPanel');
      const commentsFrame = document.getElementById('commentsFrame');
      const closeCommentsPanel = document.getElementById('closeCommentsPanel');
      
      if (commentsPanel && commentsFrame && closeCommentsPanel) {
        const btn = e.target.closest('.open-comments');
        const url = btn.dataset.commentsUrl;
        if (!url) return;
        commentsFrame.src = url;
        commentsPanel.classList.remove('hidden');
      }
    }
  });

  // Handle closing comments panel
  const closeCommentsPanel = document.getElementById('closeCommentsPanel');
  if (closeCommentsPanel) {
    closeCommentsPanel.addEventListener('click', function() {
      const commentsPanel = document.getElementById('commentsPanel');
      const commentsFrame = document.getElementById('commentsFrame');
      if (commentsPanel && commentsFrame) {
        commentsPanel.classList.add('hidden');
        commentsFrame.src = '';
      }
    });
  }

  if (applyCategoryFilter) {
    applyCategoryFilter.addEventListener('click', function(e) {
      e.preventDefault();

      const checkedCategories = Array.from(categoryCheckboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);

      const loadingIndicator = document.getElementById('loadingIndicator');
      const recentUploadsScroller = document.getElementById('recentUploadsScroller');

      if (loadingIndicator && recentUploadsScroller) {
        recentUploadsScroller.innerHTML = '';
        loadingIndicator.classList.remove('hidden');

        const params = new URLSearchParams();
        if (checkedCategories.length > 0) {
          params.append('categories', checkedCategories.join(','));
        }

        fetch(`/api/fetch-artworks-by-category/?${params.toString()}`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
        .then(response => response.json())
        .then(data => {
          loadingIndicator.classList.add('hidden');

          if (data.artworks && data.artworks.length > 0) {
            let html = '';
            data.artworks.forEach(artwork => {
              const createdDate = new Date(artwork.created_at);
              const createdText = createdDate.toLocaleDateString() +
                ' at ' +
                createdDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

              const firstCategory = artwork.categories && artwork.categories.length > 0
                ? artwork.categories[0]
                : null;
              const extraCount = artwork.categories && artwork.categories.length > 1
                ? artwork.categories.length - 1
                : 0;

              html += `
              <div class="snap-start bg-card-dark border border-border-dark rounded-2xl overflow-hidden shadow-md
                          relative transform hover:scale-[1.01] hover:shadow-[0_8px_20px_rgba(0,0,0,0.3)] transition-all duration-300">

                <div class="flex items-center justify-between px-4 pt-3 pb-2">
                  <div class="flex items-center gap-3">
                    <a href="/artist/${artwork.user_id}/"
                       class="w-10 h-10 rounded-full bg-[#232B46] flex items-center justify-center overflow-hidden text-sm font-semibold text-text-light hover:ring-2 hover:ring-[#8B5CF6] transition">
                      ${(artwork.user_first_name || artwork.user_username || 'U').charAt(0).toUpperCase()}
                    </a>
                    <div>
                      <a href="/artist/${artwork.user_id}/"
                         class="text-sm font-semibold text-white hover:underline">
                        ${artwork.user_first_name || artwork.user_username || 'Unknown'}
                      </a>
                      <p class="text-[11px] text-gray-400">
                        ${createdText}
                      </p>
                    </div>
                  </div>

                  ${firstCategory ? `
                    <span class="px-2 py-1 text-[10px] rounded-full bg-[#8B5CF6]/20 text-[#E9D5FF] border border-[#8B5CF6]/50">
                      ${firstCategory}
                    </span>` : ``}
                </div>

                ${artwork.description ? `
                  <p class="px-4 pb-3 text-sm text-gray-200">
                    ${artwork.description}
                  </p>` : ``}

                <div class="w-full bg-[#020617] max-h-[480px] overflow-hidden">
                  ${artwork.image_url ?
                    `<img src="${artwork.image_url}" alt="${artwork.title}"
                         class="w-full h-full object-cover">`
                    :
                    `<div class="flex items-center justify-center h-48 text-gray-500">
                       <span>Image not available</span>
                     </div>`}
                </div>

                <div class="flex items-center justify-between px-4 py-2 text-[11px] text-gray-400 border-t border-[#1F2937]">
                  <span>
                    ${(artwork.favorite_count || 0)} saves · ${(artwork.comment_count || 0)} comments
                  </span>
                </div>

                <div class="flex items-center justify-between px-4 py-2 border-t border-[#1F2937] text-sm">
                  <div class="flex items-center gap-4">
                    ${artwork.id ? `
                      <a href="/toggle-favorite/${artwork.id}/"
                         class="flex items-center gap-1 text-gray-400 hover:text-[#8B5CF6] transition toggle-favorite"
                         title="Save to favorites" data-artwork-id="${artwork.id}">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                        <span>${artwork.favorite_count || 0}</span>
                      </a>` : ``}

                    ${artwork.id ? `
                      <button type="button"
                              class="open-comments flex items-center gap-1 text-gray-400 hover:text-[#A7F3D0] transition"
                              data-comments-url="/artwork/${artwork.id}/comments/"
                              title="View comments">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                        </svg>
                        <span>${artwork.comment_count || 0}</span>
                      </button>` : ``}
                  </div>

                  <a href="/artist/${artwork.user_id}/"
                     class="text-xs text-gray-400 hover:text-[#A7F3D0] hover:underline">
                    View profile →
                  </a>
                </div>
              </div>`;
            });
            recentUploadsScroller.innerHTML = html;
            
            // Re-initialize favorite toggle functionality for newly loaded content
            initializeFavoriteToggle();
          } else {
            recentUploadsScroller.innerHTML = `
              <div class="text-center text-muted text-sm border border-dashed border-[#374151] rounded-2xl py-10 bg-[#050819]">
                <p class="mb-2">🎨</p>
                <p>No artworks found for the selected categories.</p>
                <p class="text-xs mt-2">Try selecting different categories or upload your own artwork!</p>
              </div>`;
          }
        })
        .catch(error => {
          loadingIndicator.classList.add('hidden');
          console.error('Error:', error);
        });
      }

      categoryFilterDropdown.classList.add('hidden');
    });
  }
  
  // Function to initialize favorite toggle for dynamically loaded content
  function initializeFavoriteToggle() {
    const favoriteLinks = document.querySelectorAll('.toggle-favorite:not(.initialized)');
    
    favoriteLinks.forEach(link => {
      // Mark as initialized to avoid duplicate event listeners
      link.classList.add('initialized');
      
      link.addEventListener('click', function(e) {
        e.preventDefault();
        
        const url = this.href;
        const heartIcon = this.querySelector('svg');
        const countSpan = this.querySelector('span');
        
        // Add pulse animation
        if (heartIcon) {
          heartIcon.style.transition = 'transform 0.2s ease';
          heartIcon.style.transform = 'scale(1.3)';
          setTimeout(() => {
            heartIcon.style.transform = 'scale(1)';
          }, 200);
        }
        
        // Send AJAX request
        fetch(url, {
          method: 'POST', // Changed to POST to match the view
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          }
        })
        .then(response => response.json())
        .then(data => {
          // Update UI to reflect favorite status
          if (heartIcon) {
            if (data.favorited) {
              // Change to filled heart
              heartIcon.outerHTML = `
                <svg class="w-5 h-5 text-[#8B5CF6]" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                </svg>`;
            } else {
              // Change to empty heart
              heartIcon.outerHTML = `
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>`;
            }
          }
          
          // Update favorite count
          if (countSpan) {
            const currentCount = parseInt(countSpan.textContent) || 0;
            countSpan.textContent = data.favorited ? currentCount + 1 : Math.max(0, currentCount - 1);
          }
          
          console.log('Favorite toggled:', data);
        })
        .catch(error => {
          console.error('Error toggling favorite:', error);
          // Fallback to page reload if AJAX fails
          setTimeout(() => {
            window.location.href = url;
          }, 1000);
        });
      });
    });
  }
  
  // Initialize favorite toggle for initially loaded content
  initializeFavoriteToggle();
});
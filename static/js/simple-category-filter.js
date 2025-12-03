// Simple category filter functionality for dashboard
console.log('Simple category filter script loading...');

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('Simple category filter DOMContentLoaded fired');
  
  // Initialize the filter functionality
  initializeCategoryFilter();
});

function initializeCategoryFilter() {
  console.log('Initializing category filter');
  
  // Get all category filter buttons
  var categoryFilterButtons = document.querySelectorAll('.category-filter-btn');
  var loadingIndicator = document.getElementById('loadingIndicator');
  var recentUploadsScroller = document.getElementById('recentUploadsScroller');
  
  console.log('Found category filter buttons:', categoryFilterButtons.length);
  
  // Check if we're on the dashboard page
  if (categoryFilterButtons.length === 0) {
    console.log('No category filter buttons found, exiting');
    return;
  }
  
  console.log('Setting up event listeners for category filter buttons');
  
  // Handle category filter button clicks
  categoryFilterButtons.forEach(function(button) {
    // Remove any existing event listeners to prevent duplicates
    button.removeEventListener('click', handleCategoryFilterClick);
    
    // Add click event listener
    button.addEventListener('click', handleCategoryFilterClick);
  });
  
  // Click handler function
  function handleCategoryFilterClick() {
    var category = this.getAttribute('data-category');
    console.log('Category filter button clicked:', category);
    
    // If "All" category is clicked, remove active state from all other buttons and activate "All"
    if (category === 'all') {
      // Remove active class from all buttons
      document.querySelectorAll('.category-filter-btn').forEach(function(btn) {
        btn.classList.remove('active');
      });
      
      // Activate the "All" button
      this.classList.add('active');
      
      // Show all artworks
      console.log('Showing all artworks');
      window.location.href = window.location.pathname;
      return;
    }
    
    // Deactivate the "All" button when any other category is selected
    var allButton = document.querySelector('.category-filter-btn[data-category="all"]');
    if (allButton) {
      allButton.classList.remove('active');
    }
    
    // Toggle active state for the clicked category
    this.classList.toggle('active');
    
    // Get all active categories
    var activeButtons = document.querySelectorAll('.category-filter-btn.active');
    var activeCategories = [];
    activeButtons.forEach(function(btn) {
      // Only add non-'all' categories
      if (btn.getAttribute('data-category') !== 'all') {
        activeCategories.push(btn.getAttribute('data-category'));
      }
    });
    
    console.log('Active categories:', activeCategories);
    
    // If no categories are selected, show all artworks
    if (activeCategories.length === 0) {
      console.log('No categories selected, showing all artworks');
      // Activate the "All" button
      if (allButton) {
        allButton.classList.add('active');
      }
      window.location.href = window.location.pathname;
      return;
    }
    
    // Filter artworks by selected categories
    filterArtworksByCategory(activeCategories);
  }
  
  // Filter artworks by category (AJAX)
  function filterArtworksByCategory(categories) {
    // Make sure we have the required elements
    if (!recentUploadsScroller) {
      console.error('Recent uploads scroller not found');
      return;
    }
    
    console.log('Filtering artworks by categories:', categories);
    
    // Show loading indicator
    if (loadingIndicator) {
      recentUploadsScroller.innerHTML = '';
      loadingIndicator.classList.remove('hidden');
    }
    
    // Build query parameters
    var params = new URLSearchParams();
    if (categories.length > 0) {
      params.append('categories', categories.join(','));
    }
    
    console.log('Fetching with params:', params.toString());
    
    // Get CSRF token
    var csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
    var csrfToken = csrfTokenElement ? csrfTokenElement.getAttribute('content') : '';
    console.log('CSRF Token:', csrfToken);
    
    // Make the API request
    fetch('/api/fetch-artworks-by-category/?' + params.toString(), {
      method: 'GET',
      headers: { 
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrfToken
      }
    })
    .then(function(response) {
      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);
      
      if (!response.ok) {
        throw new Error('Network response was not ok: ' + response.status + ' ' + response.statusText);
      }
      return response.json();
    })
    .then(function(data) {
      console.log('Received data:', data);
      
      // Hide loading indicator
      if (loadingIndicator) {
        loadingIndicator.classList.add('hidden');
      }
      
      // Check if we have artworks
      if (!data.artworks || data.artworks.length === 0) {
        recentUploadsScroller.innerHTML = `
          <div class="text-center text-muted text-sm border border-dashed border-[#374151] rounded-2xl py-10 bg-[#050819]">
            <p class="mb-2">🎨</p>
            <p>No artworks found for the selected categories.</p>
            <p class="text-xs mt-2">Try selecting different categories or upload your own artwork!</p>
          </div>`;
        return;
      }
      
      // Build HTML for artworks
      var html = '';
      data.artworks.forEach(function(artwork) {
        var createdDate = new Date(artwork.created_at);
        var createdText =
          createdDate.toLocaleDateString() +
          ' at ' +
          createdDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        var categories = artwork.categories || [];
        var categoryChips = categories
          .map(function(cat) {
            return '<span class="px-2 py-1 text-xs rounded-full bg-[#8B5CF6]/20 text-[#E9D5FF] border border-[#8B5CF6]/30 category-tag">' + cat + '</span>';
          })
          .join('');
        
        html += `
          <div class="snap-start grid md:grid-cols-[minmax(0,_1.3fr)_minmax(260px,_1fr)] gap-4 bg-card-dark border border-border-dark rounded-3xl p-4 shadow recent-upload-card">
            <div class="flex flex-col justify-between text-text-light">
              <div>
                <p class="text-xs text-muted mb-1 flex items-center gap-1">
                  <span>📋</span> Project Title
                </p>
                <h3 class="text-base font-semibold text-white">${artwork.title || ''}</h3>
                <p class="text-xs text-gray-400 mt-1 line-clamp-2">
                  ${artwork.description || ''}
                </p>
                ${categories.length ? '<div class="mt-2 flex flex-wrap gap-1">' + categoryChips + '</div>' : ''}
              </div>
              
              <div class="mt-3 text-[11px] text-muted flex items-center gap-1">
                <span>⏱️</span> ${createdText}
              </div>
              
              <div class="mt-3 flex items-center gap-3">
                <a href="/artist/${artwork.user_id}/"
                   class="flex items-center justify-center w-8 h-8 rounded-full bg-[#111827] hover:bg-[#1F2937] transition"
                   title="Artist Profile">
                  <img src="/static/icon/artist_icon.png" class="w-4 h-4" alt="Artist">
                </a>
                
                ${artwork.id ? `
                <a href="/toggle-favorite/${artwork.id}/"
                   class="toggle-favorite flex items-center justify-center w-8 h-8 rounded-full bg-[#111827] hover:bg-[#1F2937] transition"
                   title="Add to favorites">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                  <span class="ml-1 text-[11px] text-gray-300">
                    ${artwork.favorite_count || 0}
                  </span>
                </a>` : ''}
                
                ${artwork.id ? `
                <button type="button"
                        class="open-comments flex items-center gap-1 px-2 py-1 rounded-full bg-[#111827] hover:bg-[#1F2937] transition"
                        data-comments-url="/artwork/${artwork.id}/comments/"
                        title="View comments">
                  <img src="/static/icon/comment_icon.png" class="w-4 h-4" alt="Comments">
                  <span class="text-[11px] text-gray-200">
                    ${artwork.comment_count || 0}
                  </span>
                </button>` : ''}
              </div>
            </div>
            
            <div class="rounded-3xl bg-[#0F172A] flex items-center justify-center overflow-hidden min-h-[210px] relative">
              ${artwork.image_url ? `
                <img src="${artwork.image_url}" alt="${artwork.title || ''}"
                     class="w-full h-full object-cover transition duration-300">
                <div class="absolute inset-0 bg-gradient-to-t from-[#050819] to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300 flex items-end justify-start p-4">
                  <span class="text-white text-sm font-semibold truncate max-w-full">
                    ${artwork.title || ''}
                  </span>
                </div>` : '<span class="text-sm text-gray-300">🖼️ Image here</span>'}
            </div>
          </div>`;
      });
      
      // Update the scroller with new content
      recentUploadsScroller.innerHTML = html;
      
      // Reattach event listeners to the new elements
      reattachEventListeners();
    })
    .catch(function(error) {
      console.error('Error loading artworks by category:', error);
      
      // Hide loading indicator
      if (loadingIndicator) {
        loadingIndicator.classList.add('hidden');
      }
      
      // Show error message
      if (recentUploadsScroller) {
        recentUploadsScroller.innerHTML = `
          <div class="text-center text-red-400 text-sm border border-dashed border-[#374151] rounded-2xl py-10 bg-[#050819]">
            <p class="mb-2">⚠️</p>
            <p>Error loading artworks. Please try again.</p>
            <p class="text-xs mt-2">Details: ${error.message}</p>
          </div>`;
      }
    });
  }
}

// Function to reattach event listeners to newly created elements
function reattachEventListeners() {
  // Reattach event listeners for comments buttons
  const newOpenCommentsButtons = document.querySelectorAll('.open-comments');
  // Remove existing event listeners to prevent duplicates
  newOpenCommentsButtons.forEach(button => {
    button.removeEventListener('click', handleCommentsClick);
    button.addEventListener('click', handleCommentsClick);
  });
  
  // Reattach event listeners for favorite links
  const newFavoriteLinks = document.querySelectorAll('a[href*="toggle_favorite"]');
  newFavoriteLinks.forEach(link => {
    link.removeEventListener('click', handleFavoriteClick);
    link.addEventListener('click', handleFavoriteClick);
  });
  
  // Note: Artist profile links don't need JavaScript handlers as they are regular navigation links
}

// Click handler for comments buttons
function handleCommentsClick(e) {
  e.preventDefault();
  
  const commentsPanel = document.getElementById('commentsPanel');
  const commentsFrame = document.getElementById('commentsFrame');
  
  if (!commentsPanel || !commentsFrame) {
    console.error('Comments panel elements not found');
    return;
  }
  
  // Get the comments URL from the data attribute
  const commentsUrl = this.getAttribute('data-comments-url');
  
  if (commentsUrl) {
    // Set the iframe source to load the comments page
    commentsFrame.src = commentsUrl;
    
    // Show the comments panel
    commentsPanel.classList.remove('hidden');
    
    // Add backdrop and prevent body scrolling
    document.body.style.overflow = 'hidden';
    document.body.insertAdjacentHTML('beforeend', '<div id="commentsBackdrop" class="fixed inset-0 bg-black bg-opacity-50 z-40"></div>');
    
    const backdrop = document.getElementById('commentsBackdrop');
    if (backdrop) {
      // Remove any existing event listeners to prevent duplicates
      backdrop.removeEventListener('click', closeCommentsPanelHandler);
      backdrop.addEventListener('click', closeCommentsPanelHandler);
    }
  } else {
    console.error('No comments URL found for this button');
  }
}

// Click handler for favorite links
function handleFavoriteClick(e) {
  e.preventDefault();
  
  const url = this.href;
  const heartIcon = this.querySelector('svg');
  
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
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    }
  })
    .then(response => response.json())
    .then(data => {
      // Toggle the heart icon based on response
      if (data.favorited) {
        // Change to filled heart
        if (heartIcon) {
          heartIcon.classList.remove('text-gray-400');
          heartIcon.classList.add('text-[#8B5CF6]');
        }
        this.title = 'Remove from favorites';
        
        // Show toast notification
        showToast('Added to favorites!', 'success');
      } else {
        // Change to outlined heart
        if (heartIcon) {
          heartIcon.classList.remove('text-[#8B5CF6]');
          heartIcon.classList.add('text-gray-400');
        }
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
}

// Also initialize on window load to ensure everything is ready
window.addEventListener('load', function() {
  console.log('Window load event fired, initializing category filter');
  initializeCategoryFilter();
});

console.log('Simple category filter script loaded');
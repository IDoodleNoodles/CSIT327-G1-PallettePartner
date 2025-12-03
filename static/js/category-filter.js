// Category filter functionality for dashboard
console.log('Category filter script loading...');

document.addEventListener('DOMContentLoaded', function() {
  console.log('Category filter DOMContentLoaded fired');
  
  // Wait a bit for all elements to be rendered
  setTimeout(function() {
    console.log('Category filter timeout callback executing');
    
    var categoryFilterButton = document.getElementById('categoryFilterButton');
    var categoryFilterDropdown = document.getElementById('categoryFilterDropdown');
    var applyCategoryFilter = document.getElementById('applyCategoryFilter');
    var clearCategoryFilter = document.getElementById('clearCategoryFilter');
    var categoryCheckboxes = document.querySelectorAll('input[name="category_filter"]');
    var loadingIndicator = document.getElementById('loadingIndicator');
    var recentUploadsScroller = document.getElementById('recentUploadsScroller');

    console.log('Looking for category filter elements...');
    console.log('categoryFilterButton:', categoryFilterButton);
    console.log('categoryFilterDropdown:', categoryFilterDropdown);
    console.log('applyCategoryFilter:', applyCategoryFilter);
    console.log('clearCategoryFilter:', clearCategoryFilter);
    console.log('categoryCheckboxes length:', categoryCheckboxes.length);

    // Check if we're on the dashboard page
    if (!categoryFilterButton || !categoryFilterDropdown) {
      console.log('Not on dashboard page or elements not found');
      return; // Not on dashboard page
    }

    console.log('Category filter elements found, setting up event listeners');
    
    // Remove any existing event listeners to prevent duplicates
    categoryFilterButton.removeEventListener('click', toggleDropdown);
    
    // Toggle dropdown visibility
    function toggleDropdown(e) {
      e.stopPropagation();
      console.log('Category filter button clicked');
      
      // Debug: Log the current state before toggling
      console.log('Before toggle - dropdown hidden:', categoryFilterDropdown.classList.contains('hidden'));
      
      categoryFilterDropdown.classList.toggle('hidden');
      
      // Debug: Log the state after toggling
      console.log('After toggle - dropdown hidden:', categoryFilterDropdown.classList.contains('hidden'));
      
      // Debug: Force the dropdown to be visible
      if (!categoryFilterDropdown.classList.contains('hidden')) {
        console.log('Making dropdown visible');
        categoryFilterDropdown.style.display = 'block';
        categoryFilterDropdown.style.visibility = 'visible';
        categoryFilterDropdown.style.opacity = '1';
        
        // Additional debugging to ensure it's visible
        console.log('Dropdown position:', {
          offsetTop: categoryFilterDropdown.offsetTop,
          offsetLeft: categoryFilterDropdown.offsetLeft,
          offsetWidth: categoryFilterDropdown.offsetWidth,
          offsetHeight: categoryFilterDropdown.offsetHeight,
          computedStyle: window.getComputedStyle(categoryFilterDropdown)
        });
      }
    }
    
    categoryFilterButton.addEventListener('click', toggleDropdown);

    // Close dropdown when clicking outside
    document.removeEventListener('click', closeDropdownOnClickOutside);
    
    function closeDropdownOnClickOutside(e) {
      if (categoryFilterDropdown && 
          !categoryFilterDropdown.classList.contains('hidden') &&
          categoryFilterButton && 
          !categoryFilterButton.contains(e.target) && 
          !categoryFilterDropdown.contains(e.target)) {
        console.log('Click outside category filter dropdown, hiding it');
        categoryFilterDropdown.classList.add('hidden');
      }
    }
    
    document.addEventListener('click', closeDropdownOnClickOutside);

    // Handle checkbox changes for visual feedback
    categoryCheckboxes.forEach(function(checkbox) {
      // Remove existing event listeners to prevent duplicates
      checkbox.removeEventListener('change', handleCheckboxChange);
      
      function handleCheckboxChange() {
        var span = this.nextElementSibling.querySelector('span');
        if (!span) return;

        if (this.checked) {
          span.classList.add('bg-[#8B5CF6]');
          span.innerHTML = '<svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>';
        } else {
          span.classList.remove('bg-[#8B5CF6]');
          span.innerHTML = '';
        }
      }
      
      checkbox.addEventListener('change', handleCheckboxChange);
    });

    // Clear filter (reset + reload)
    if (clearCategoryFilter) {
      clearCategoryFilter.removeEventListener('click', clearFilter);
      
      function clearFilter(e) {
        e.preventDefault();
        console.log('Clear category filter clicked');

        categoryCheckboxes.forEach(function(cb) {
          cb.checked = false;
          var span = cb.nextElementSibling.querySelector('span');
          if (span) {
            span.classList.remove('bg-[#8B5CF6]');
            span.innerHTML = '';
          }
        });

        var url = new URL(window.location);
        url.searchParams.delete('categories');
        window.location.href = url.toString();
      }
      
      clearCategoryFilter.addEventListener('click', clearFilter);
    }

    // Apply filter (AJAX)
    if (applyCategoryFilter && loadingIndicator && recentUploadsScroller) {
      applyCategoryFilter.removeEventListener('click', applyFilter);
      
      function applyFilter(e) {
        e.preventDefault();
        console.log('Apply category filter clicked');

        var checkedCategories = [];
        categoryCheckboxes.forEach(function(cb) {
          if (cb.checked) {
            checkedCategories.push(cb.value);
          }
        });

        console.log('Checked categories:', checkedCategories);

        recentUploadsScroller.innerHTML = '';
        loadingIndicator.classList.remove('hidden');

        var params = new URLSearchParams();
        if (checkedCategories.length > 0) {
          params.append('categories', checkedCategories.join(','));
        }

        console.log('Fetching with params:', params.toString());
        
        // Get CSRF token
        var csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        var csrfToken = csrfTokenElement ? csrfTokenElement.getAttribute('content') : '';
        console.log('CSRF Token:', csrfToken);

        fetch('/api/fetch-artworks-by-category/?' + params.toString(), {
          method: 'GET',
          headers: { 
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
          }
        })
        .then(function(res) {
          return res.json();
        })
        .then(function(data) {
          console.log('Received data:', data);
          loadingIndicator.classList.add('hidden');

          if (!data.artworks || data.artworks.length === 0) {
            recentUploadsScroller.innerHTML = `
              <div class="text-center text-muted text-sm border border-dashed border-[#374151] rounded-2xl py-10 bg-[#050819]">
                <p class="mb-2">🎨</p>
                <p>No artworks found for the selected categories.</p>
                <p class="text-xs mt-2">Try selecting different categories or upload your own artwork!</p>
              </div>`;
            return;
          }

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

          recentUploadsScroller.innerHTML = html;
        })
        .catch(function(err) {
          console.error('Error loading artworks by category:', err);
          loadingIndicator.classList.add('hidden');
          recentUploadsScroller.innerHTML = `
            <div class="text-center text-red-400 text-sm border border-dashed border-[#374151] rounded-2xl py-10 bg-[#050819]">
              <p class="mb-2">⚠️</p>
              <p>Error loading artworks. Please try again.</p>
            </div>`;
        });

        categoryFilterDropdown.classList.add('hidden');
      }
      
      applyCategoryFilter.addEventListener('click', applyFilter);
    }
    
    // Add event listener to log when the dropdown is shown
    var observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
          if (!categoryFilterDropdown.classList.contains('hidden')) {
            console.log('Dropdown is now visible');
          } else {
            console.log('Dropdown is now hidden');
          }
        }
      });
    });
    
    if (categoryFilterDropdown) {
      observer.observe(categoryFilterDropdown, {
        attributes: true,
        attributeFilter: ['class']
      });
    }
  }, 100); // Small delay to ensure DOM is fully loaded
});

console.log('Category filter script loaded');
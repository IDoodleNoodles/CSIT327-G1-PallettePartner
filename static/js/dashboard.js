document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const toggleSidebar = document.getElementById('toggleSidebar'); // optional
  const sidebarOverlay = document.getElementById('sidebarOverlay');
  const menuLabel = document.getElementById('menuLabel'); // optional
  const modal = document.getElementById('createModal');
  const overlay = document.getElementById('overlay');
  const addPostBtn = document.getElementById('addPostBtn');
  const closeModalBtn = document.getElementById('closeModal');
  const scrollToTopBtn = document.getElementById('scrollToTop');
  const mainContent = document.querySelector('main');

  /* =========================
     Sidebar toggle + overlay
  ========================== */

  if (toggleSidebar && sidebar) {
    toggleSidebar.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');

      // Handle mobile overlay
      if (window.innerWidth < 1024) {
        if (sidebar.classList.contains('collapsed')) {
          sidebar.style.transform = 'translateX(-100%)';
          if (sidebarOverlay) sidebarOverlay.classList.add('hidden');
        } else {
          sidebar.style.transform = 'translateX(0)';
          if (sidebarOverlay) sidebarOverlay.classList.remove('hidden');
        }
      }

      if (menuLabel) {
        if (sidebar.classList.contains('collapsed')) {
          menuLabel.style.display = 'none';
        } else {
          menuLabel.style.display = 'inline';
        }
      }
    });
  }

  // Close sidebar when clicking overlay
  if (sidebarOverlay && sidebar) {
    sidebarOverlay.addEventListener('click', () => {
      sidebar.classList.add('collapsed');
      sidebar.style.transform = 'translateX(-100%)';
      sidebarOverlay.classList.add('hidden');
      if (menuLabel) menuLabel.style.display = 'none';
    });
  }

  // Handle responsive sidebar on window resize
  if (sidebar) {
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 1024) {
        sidebar.style.transform = 'translateX(0)';
        if (sidebarOverlay) sidebarOverlay.classList.add('hidden');
      } else if (sidebar.classList.contains('collapsed')) {
        sidebar.style.transform = 'translateX(-100%)';
      }
    });
  }

  /* ==============
     Modal logic
  ============== */

  if (addPostBtn && modal && overlay) {
    addPostBtn.addEventListener('click', () => {
      modal.classList.add('show');
      overlay.classList.add('show');
    });
  }

  const closeModal = () => {
    if (!modal || !overlay) return;
    modal.classList.remove('show');
    overlay.classList.remove('show');
  };

  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeModal);
  }

  if (overlay) {
    overlay.addEventListener('click', closeModal);
  }

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
  });

  /* ==================
     Scroll to Top btn
  =================== */

  if (scrollToTopBtn && mainContent) {
    mainContent.addEventListener('scroll', () => {
      if (mainContent.scrollTop > 300) {
        scrollToTopBtn.classList.remove('opacity-0', 'pointer-events-none');
        scrollToTopBtn.classList.add('opacity-100');
      } else {
        scrollToTopBtn.classList.add('opacity-0', 'pointer-events-none');
        scrollToTopBtn.classList.remove('opacity-100');
      }
    });

    scrollToTopBtn.addEventListener('click', () => {
      mainContent.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* =========================
     Floating comments panel
  ========================== */

  const commentsPanel = document.getElementById('commentsPanel');
  const commentsFrame = document.getElementById('commentsFrame');
  const closeCommentsPanel = document.getElementById('closeCommentsPanel');
  const commentsHeader = document.getElementById('commentsPanelHeader');

  if (commentsPanel && commentsFrame && closeCommentsPanel && commentsHeader) {
    // open panel when clicking comment icon
    document.querySelectorAll('.open-comments').forEach(btn => {
      btn.addEventListener('click', () => {
        const url = btn.dataset.commentsUrl;
        if (!url) return;
        commentsFrame.src = url;
        commentsPanel.classList.remove('hidden');
      });
    });

    // close panel
    closeCommentsPanel.addEventListener('click', () => {
      commentsPanel.classList.add('hidden');
      commentsFrame.src = '';
    });

    // draggable behavior
    let isDragging = false;
    let offsetX = 0;
    let offsetY = 0;

    commentsHeader.addEventListener('mousedown', (e) => {
      isDragging = true;
      const rect = commentsPanel.getBoundingClientRect();
      offsetX = e.clientX - rect.left;
      offsetY = e.clientY - rect.top;
      document.body.classList.add('select-none');
    });

    document.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      commentsPanel.style.left = (e.clientX - offsetX) + 'px';
      commentsPanel.style.top = (e.clientY - offsetY) + 'px';
      commentsPanel.style.right = 'auto'; // so left/top take control
    });

    document.addEventListener('mouseup', () => {
      if (!isDragging) return;
      isDragging = false;
      document.body.classList.remove('select-none');
    });
  }

  /* =========================
     Category Filter Logic
  ========================== */
  
  const categoryFilterButton = document.getElementById('categoryFilterButton');
  const categoryFilterDropdown = document.getElementById('categoryFilterDropdown');
  const applyCategoryFilter = document.getElementById('applyCategoryFilter');
  const clearCategoryFilter = document.getElementById('clearCategoryFilter');
  const categoryCheckboxes = document.querySelectorAll('input[name="category_filter"]');
  
  // Always show the filter button, even if there are no categories
  if (categoryFilterButton) {
    categoryFilterButton.style.display = 'flex'; // Ensure it's visible
    
    // Toggle dropdown visibility
    categoryFilterButton.addEventListener('click', function(e) {
      e.stopPropagation();
      categoryFilterDropdown.classList.toggle('hidden');
    });
  }
  
  // Close dropdown when clicking outside
  document.addEventListener('click', function(event) {
    if (categoryFilterDropdown && !categoryFilterButton.contains(event.target) && !categoryFilterDropdown.contains(event.target)) {
      categoryFilterDropdown.classList.add('hidden');
    }
  });
  
  // Update checkbox visuals when clicked
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
  
  // Clear category filter
  if (clearCategoryFilter) {
    clearCategoryFilter.addEventListener('click', function() {
      // Uncheck all checkboxes
      categoryCheckboxes.forEach(cb => {
        cb.checked = false;
        // Update visuals
        const span = cb.nextElementSibling.querySelector('span');
        span.classList.remove('bg-[#8B5CF6]');
        span.innerHTML = '';
      });
      
      // Remove categories from URL
      const url = new URL(window.location);
      url.searchParams.delete('categories');
      
      window.location.href = url.toString();
    });
  }
  
  // AJAX filtering for smoother experience
  if (applyCategoryFilter) {
    applyCategoryFilter.addEventListener('click', function(e) {
      e.preventDefault(); // Prevent default form submission
      
      const checkedCategories = Array.from(categoryCheckboxes).filter(cb => cb.checked).map(cb => cb.value);
      
      // Show loading indicator
      const loadingIndicator = document.getElementById('loadingIndicator');
      const recentUploadsScroller = document.getElementById('recentUploadsScroller');
      
      if (loadingIndicator && recentUploadsScroller) {
        recentUploadsScroller.innerHTML = '';
        loadingIndicator.classList.remove('hidden');
        
        // Fetch filtered artworks
        const params = new URLSearchParams();
        if (checkedCategories.length > 0) {
          params.append('categories', checkedCategories.join(','));
        }
        
        fetch(`/api/fetch-artworks-by-category/?${params.toString()}`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          }
        })
        .then(response => response.json())
        .then(data => {
          loadingIndicator.classList.add('hidden');
          
          if (data.artworks && data.artworks.length > 0) {
            // Render artworks
            let html = '';
            data.artworks.forEach(artwork => {
              html += `
              <div class="snap-start min-w-[350px] md:min-w-[400px] grid md:grid-cols-[minmax(0,_1.3fr)_minmax(260px,_1fr)] gap-4 bg-card-dark border border-border-dark rounded-3xl p-4 shadow recent-upload-card">
                <div class="flex flex-col justify-between text-text-light">
                  <div>
                    <p class="text-xs text-muted mb-1 flex items-center gap-1">
                      <span>📋</span> Project Title
                    </p>
                    <h3 class="text-base font-semibold">${artwork.title}</h3>
                    <p class="text-xs text-gray-400 mt-1 line-clamp-2">
                      ${artwork.description}
                    </p>
                    
                    <!-- Categories -->
                    <div class="mt-2 flex flex-wrap gap-1">
                      ${artwork.categories.map((cat, index) => `
                        <span class="px-2 py-1 text-xs rounded-full bg-[#8B5CF6]/20 text-[#E9D5FF] border border-[#8B5CF6]/30 category-tag">
                          ${cat}
                        </span>
                      `).join('')}
                    </div>
                  </div>
                  
                  <div class="mt-3 text-[11px] text-muted flex items-center gap-1">
                    <span>⏱️</span> ${new Date(artwork.created_at).toLocaleDateString()} at ${new Date(artwork.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                  </div>
                  
                  <div class="mt-3 flex items-center gap-3">
                    <a href="/artist/${artwork.user_id}/" class="flex items-center justify-center w-8 h-8 rounded-full bg-[#111827] hover:bg-[#1F2937] transition" title="Artist Profile">
                      <img src="/static/icon/artist_icon.png" class="w-4 h-4" alt="Artist">
                    </a>
                    
                    <a href="#" class="flex items-center justify-center w-8 h-8 rounded-full bg-[#111827] hover:bg-[#1F2937] transition" title="Add to favorites">
                      <img src="/static/icon/favorite_icon.png" class="w-4 h-4 opacity-40" alt="Favorite">
                    </a>
                    
                    <button type="button" class="open-comments flex items-center gap-1 px-2 py-1 rounded-full bg-[#111827] hover:bg-[#1F2937] transition" title="View comments">
                      <img src="/static/icon/comment_icon.png" class="w-4 h-4" alt="Comments">
                      <span class="text-[11px] text-gray-200">
                        ${artwork.comment_count}
                      </span>
                    </button>
                  </div>
                </div>
                
                <div class="rounded-3xl bg-[#0F172A] flex items-center justify-center overflow-hidden min-h-[210px] relative">
                  ${artwork.image_url ? 
                    `<img src="${artwork.image_url}" alt="${artwork.title}" class="w-full h-full object-cover transition duration-300">
                     <div class="absolute inset-0 bg-gradient-to-t from-[#050819] to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300 flex items-end justify-start p-4">
                       <span class="text-white text-sm font-semibold truncate max-w-full">${artwork.title}</span>
                     </div>` : 
                    `<span class="text-sm text-gray-300">🖼️ Image here</span>`
                  }
                </div>
              </div>`;
            });
            recentUploadsScroller.innerHTML = html;
          } else {
            recentUploadsScroller.innerHTML = `
              <div class="text-center text-muted text-sm border border-dashed border-[#374151] rounded-2xl py-10 bg-[#050819] col-span-full">
                <p class="mb-2">🎨</p>
                <p>No artworks found for the selected categories.</p>
                <p class="text-xs mt-2">Try selecting different categories or upload your own artwork!</p>
              </div>`;
          }
          
          // Re-initialize animations for newly loaded content
          initCardAnimations();
        })
        .catch(error => {
          loadingIndicator.classList.add('hidden');
          console.error('Error:', error);
          recentUploadsScroller.innerHTML = `
            <div class="text-center text-red-400 text-sm border border-dashed border-[#374151] rounded-2xl py-10 bg-[#050819] col-span-full">
              <p class="mb-2">⚠️</p>
              <p>Error loading artworks. Please try again.</p>
            </div>`;
        });
      }
      
      // Hide dropdown after applying
      categoryFilterDropdown.classList.add('hidden');
    });
  }

  /* =========================
     Auto-scroll for Recent Uploads (horizontal)
  ========================== */
  
  const scroller = document.getElementById('recentUploadsScroller');
  if (scroller) {
    let isScrolling = false;
    let scrollInterval = null;
    let idleTimeout = null;
    const IDLE_DELAY = 3000; // 3 seconds of idle before auto-scroll starts
    const SCROLL_SPEED = 0.5; // pixels per frame

    function startAutoScroll() {
      if (scrollInterval) return;
      
      scrollInterval = setInterval(() => {
        if (isScrolling) return;

        // Scroll right smoothly
        scroller.scrollLeft += SCROLL_SPEED;

        // If reached end, scroll back to start
        if (scroller.scrollLeft + scroller.clientWidth >= scroller.scrollWidth - 5) {
          setTimeout(() => {
            scroller.scrollLeft = 0;
          }, 2000); // Pause at end for 2 seconds
        }
      }, 16); // ~60fps
    }

    function stopAutoScroll() {
      if (scrollInterval) {
        clearInterval(scrollInterval);
        scrollInterval = null;
      }
    }

    function resetIdleTimer() {
      isScrolling = true;
      stopAutoScroll();
      
      if (idleTimeout) clearTimeout(idleTimeout);
      
      idleTimeout = setTimeout(() => {
        isScrolling = false;
        startAutoScroll();
      }, IDLE_DELAY);
    }

    // Listen for user interaction
    scroller.addEventListener('mouseenter', resetIdleTimer);
    scroller.addEventListener('mousemove', resetIdleTimer);
    scroller.addEventListener('scroll', resetIdleTimer);
    scroller.addEventListener('wheel', resetIdleTimer);
    scroller.addEventListener('touchstart', resetIdleTimer);
    scroller.addEventListener('touchmove', resetIdleTimer);

    // Start auto-scroll after initial idle period
    idleTimeout = setTimeout(() => {
      isScrolling = false;
      startAutoScroll();
    }, IDLE_DELAY);

    // Stop when mouse leaves
    scroller.addEventListener('mouseleave', () => {
      if (idleTimeout) clearTimeout(idleTimeout);
      idleTimeout = setTimeout(() => {
        isScrolling = false;
        startAutoScroll();
      }, IDLE_DELAY);
    });
  }
  
  /* =========================
     Card Animation Initialization
  ========================== */
  
  function initCardAnimations() {
    // Add staggered animation delays to recently added cards
    const cards = document.querySelectorAll('.recent-upload-card:not([data-animated])');
    cards.forEach((card, index) => {
      card.style.animationDelay = `${index * 0.1}s`;
      card.setAttribute('data-animated', 'true');
    });
  }
  
  // Initialize animations on page load
  initCardAnimations();
});
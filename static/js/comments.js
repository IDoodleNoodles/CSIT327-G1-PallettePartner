// Close comments panel handler
function closeCommentsPanelHandler() {
    const commentsPanel = document.getElementById('commentsPanel');
    const commentsFrame = document.getElementById('commentsFrame');
    
    if (commentsPanel) commentsPanel.classList.add('hidden');
    if (commentsFrame) commentsFrame.src = '';
    
    // Remove backdrop and restore body scrolling
    const backdrop = document.getElementById('commentsBackdrop');
    if (backdrop) {
        backdrop.remove();
    }
    document.body.style.overflow = '';
}

// Comments Panel Handler
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a page with dynamic content that might reattach event listeners
    const simpleCategoryFilter = document.querySelector('.category-filter-btn');
    if (simpleCategoryFilter) {
        // We're on dashboard with dynamic filtering, event listeners will be managed by simple-category-filter.js
        console.log('Comments: Skipping event listener attachment on dashboard with dynamic filtering');
        return;
    }
    // Get DOM elements
    const openCommentsButtons = document.querySelectorAll('.open-comments');
    const commentsPanel = document.getElementById('commentsPanel');
    const commentsFrame = document.getElementById('commentsFrame');
    const closeCommentsPanel = document.getElementById('closeCommentsPanel');
    const commentsPanelHeader = document.getElementById('commentsPanelHeader');
    
    // Check if required elements exist
    if (!openCommentsButtons || !commentsPanel || !commentsFrame || !closeCommentsPanel) {
        console.log('Comments panel elements not found, skipping initialization');
        return;
    }
    
    // Add event listeners to all open comments buttons
    openCommentsButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
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
                    backdrop.addEventListener('click', closeCommentsPanelHandler);
                }
            } else {
                console.error('No comments URL found for this button');
            }
        });
    });
    
    // Add event listener to close button
    closeCommentsPanel.addEventListener('click', closeCommentsPanelHandler);
    
    // Make the comments panel draggable
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;
    
    commentsPanelHeader.addEventListener('mousedown', dragStart);
    document.addEventListener('mouseup', dragEnd);
    document.addEventListener('mousemove', drag);
    
    function dragStart(e) {
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;
        
        if (e.target === commentsPanelHeader) {
            isDragging = true;
        }
    }
    
    function dragEnd() {
        initialX = currentX;
        initialY = currentY;
        
        isDragging = false;
    }
    
    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;
            
            xOffset = currentX;
            yOffset = currentY;
            
            setTranslate(currentX, currentY, commentsPanel);
        }
    }
    
    function setTranslate(xPos, yPos, el) {
        el.style.transform = `translate3d(${xPos}px, ${yPos}px, 0)`;
    }
});
// Timeline functionality
function initializeTimeline() {
    const timelineItems = document.querySelectorAll('.timeline-item');

    timelineItems.forEach(item => {
        item.addEventListener('click', function () {
            const content = this.querySelector('.timeline-content');
            const isExpanded = content.classList.contains('expanded');

            timelineItems.forEach(tlItem => {
                tlItem.querySelector('.timeline-content').classList.remove('expanded');
            });

            if (!isExpanded) {
                content.classList.add('expanded');
            }
        });
    });
}
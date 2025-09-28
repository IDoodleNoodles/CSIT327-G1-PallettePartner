document.addEventListener('DOMContentLoaded', function () {
  // Small demo: click a swatch to copy its color to clipboard
  document.querySelectorAll('.swatch').forEach(function (el) {
    el.addEventListener('click', function () {
      const color = window.getComputedStyle(el).backgroundColor;
      navigator.clipboard?.writeText(color).then(() => {
        el.style.outline = '3px solid rgba(0,0,0,0.08)';
        setTimeout(() => (el.style.outline = ''), 600);
      }).catch(()=>{});
    });
  });
});

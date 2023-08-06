document.addEventListener('DOMContentLoaded', function() {
  const panelHeaders = document.querySelectorAll('.object > h2');
  for (let i = 0; i < panelHeaders.length; i++) {
    panelHeaders[i].addEventListener('click', function() {
      if (this.parentElement.classList.contains('wagtailuiplus__panel--collapsed')) {
        this.parentElement.classList.remove('wagtailuiplus__panel--collapsed')
      } else {
        this.parentElement.classList.add('wagtailuiplus__panel--collapsed')
      }
    });
  }
});

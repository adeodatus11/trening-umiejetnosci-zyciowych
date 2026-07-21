// Menu mobilne + wyszukiwarka/filtr modułów. Bez zależności zewnętrznych.
(function () {
  // Mobilne menu
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('main-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Filtr modułów (strona moduly.html)
  var input = document.getElementById('module-search');
  var select = document.getElementById('module-filter');
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-module-card]'));
  var count = document.getElementById('result-count');

  function apply() {
    if (!cards.length) return;
    var q = (input && input.value || '').toLowerCase().trim();
    var f = (select && select.value) || 'all';
    var visible = 0;
    cards.forEach(function (c) {
      var text = c.getAttribute('data-search') || '';
      var aud = c.getAttribute('data-audience') || '';
      var matchQ = !q || text.toLowerCase().indexOf(q) !== -1;
      var matchF = f === 'all' || aud.indexOf(f) !== -1;
      var show = matchQ && matchF;
      c.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    if (count) count.textContent = 'Widoczne moduły: ' + visible + ' z ' + cards.length;
  }
  if (input) input.addEventListener('input', apply);
  if (select) select.addEventListener('change', apply);
  apply();
})();

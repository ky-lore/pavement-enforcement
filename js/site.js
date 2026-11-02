/* Pavement Enforcement: shared behavior for every page.
   Forms are fake-submit (data-mock): nothing is sent anywhere and no generate_lead
   is pushed until the CRM is wired. See README "Before launch". */
(function () {
  'use strict';
  window.dataLayer = window.dataLayer || [];
  var dl = function (o) { window.dataLayer.push(o); };

  /* ---------- mobile menu ---------- */
  var menu = document.getElementById('mm');
  var toggle = document.querySelector('.burger');
  function setMenu(open) {
    if (!menu || !toggle) return;
    menu.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) { var c = menu.querySelector('.close'); if (c) c.focus(); } else { toggle.focus(); }
  }
  if (toggle) toggle.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
  if (menu) {
    menu.querySelector('.close').addEventListener('click', function () { setMenu(false); });
    menu.addEventListener('click', function (e) { if (e.target.tagName === 'A' && e.target.getAttribute('href').indexOf('#') > -1) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('open')) setMenu(false); });
  }

  /* ---------- click tracking ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('tel:') === 0) dl({ event: 'phone_click', link_location: a.dataset.loc || '' });
    else if (a.hasAttribute('data-quote')) dl({ event: 'quote_click', link_location: a.dataset.loc || '' });
  });

  /* ---------- attribution: latest ad-tagged landing wins, 90-day expiry ---------- */
  var AKEY = 'pe_attr', KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid', 'fbclid'];
  var store = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
                set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  var attr = null;
  try { attr = JSON.parse(store.get(AKEY) || 'null'); } catch (e) { attr = null; }
  if (attr && Date.now() - (attr.ts || 0) > 90 * 864e5) attr = null;
  var q = new URLSearchParams(location.search), tagged = KEYS.some(function (k) { return q.get(k); });
  if (tagged || !attr) {
    attr = { ts: Date.now(), landing_page: location.href, referrer: document.referrer || '' };
    KEYS.forEach(function (k) { attr[k] = q.get(k) || ''; });
    store.set(AKEY, JSON.stringify(attr));
  }

  /* ---------- forms (fake submit) ---------- */
  function e164(v) {
    var d = String(v || '').replace(/\D/g, '');
    if (d.length === 10) return '+1' + d;
    if (d.length === 11 && d[0] === '1') return '+' + d;
    return '';
  }
  function fmtPhone(v) {
    var d = String(v).replace(/\D/g, '').replace(/^1(?=\d{10})/, '').slice(0, 10);
    if (d.length < 4) return d;
    if (d.length < 7) return '(' + d.slice(0, 3) + ') ' + d.slice(3);
    return '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6);
  }
  function setErr(field, msg) {
    var id = field.id + '-err', el = document.getElementById(id);
    if (msg) {
      if (!el) { el = document.createElement('span'); el.className = 'err'; el.id = id; field.insertAdjacentElement('afterend', el); }
      el.textContent = msg;
      field.setAttribute('aria-invalid', 'true');
      field.setAttribute('aria-describedby', id);
    } else {
      if (el) el.remove();
      field.removeAttribute('aria-invalid');
      field.removeAttribute('aria-describedby');
    }
  }
  function check(field) {
    var v = field.value.trim(), n = field.name, msg = '';
    if (field.required && !v) msg = 'Please enter your ' + (field.dataset.label || n.replace('_', ' ')) + '.';
    else if (n === 'phone' && v && !e164(v)) msg = 'Please enter a 10-digit phone number.';
    else if (n === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = 'Please enter a valid email address.';
    else if (n === 'postal_code' && v && !/^\d{5}$/.test(v)) msg = 'Please enter a 5-digit ZIP code.';
    setErr(field, msg);
    return !msg;
  }

  document.querySelectorAll('form[data-mock]').forEach(function (form) {
    var started = false, t0 = Date.now();
    KEYS.concat(['landing_page', 'referrer']).forEach(function (k) {
      var h = form.querySelector('input[name="' + k + '"]');
      if (h) h.value = attr[k] || '';
    });
    form.addEventListener('focusin', function () {
      if (!started) { started = true; dl({ event: 'form_start', form_id: form.id }); }
    });
    var tel = form.querySelector('input[name="phone"]');
    if (tel) tel.addEventListener('input', function () { tel.value = fmtPhone(tel.value); });
    form.querySelectorAll('input,select,textarea').forEach(function (f) {
      if (f.name && f.name !== 'company_website') f.addEventListener('blur', function () { if (f.value || f.hasAttribute('aria-invalid')) check(f); });
    });
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var status = form.querySelector('.form-status'), ok = true, first = null;
      form.querySelectorAll('input[name],select[name],textarea[name]').forEach(function (f) {
        if (f.type === 'hidden' || f.type === 'checkbox' || f.name === 'company_website') return;
        if (!check(f)) { ok = false; first = first || f; }
      });
      if (!ok) { status.textContent = 'Please fix the highlighted fields.'; first.focus(); return; }
      status.textContent = '';
      var hp = form.querySelector('input[name="company_website"]');
      if ((hp && hp.value) || Date.now() - t0 < 2500) { location.href = '/thank-you/'; return; }  // bots: silently drop
      if (tel) tel.dataset.e164 = e164(tel.value);   // normalized for the future CRM payload
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.dataset.label = btn.innerHTML;
      btn.textContent = 'Sending…';
      var fn = form.querySelector('input[name="first_name"]');
      try { sessionStorage.setItem('pe_first', fn ? fn.value.trim() : ''); } catch (e) {}
      setTimeout(function () { location.href = '/thank-you/'; }, 900);
    });
  });

  /* ---------- thank-you greeting ---------- */
  var greet = document.getElementById('ty-name');
  if (greet) { var n = ''; try { n = sessionStorage.getItem('pe_first') || ''; } catch (e) {} if (n) greet.textContent = ', ' + n; }

  /* ---------- reviews carousel ---------- */
  var t = document.getElementById('rv-track');
  if (t) {
    var b = document.querySelectorAll('.rv-btn');
    var step = function () { var c = t.querySelector('.rv-card'); return c ? c.getBoundingClientRect().width + 22 : t.clientWidth; };
    var upd = function () { b[0].disabled = t.scrollLeft <= 2; b[1].disabled = t.scrollLeft + t.clientWidth >= t.scrollWidth - 2; };
    b.forEach(function (x) { x.addEventListener('click', function () { t.scrollBy({ left: step() * +x.dataset.dir }); }); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); t.scrollBy({ left: step() * (e.key === 'ArrowRight' ? 1 : -1) }); }
    });
    t.addEventListener('scroll', upd, { passive: true });
    window.addEventListener('resize', upd);
    upd();
  }
})();

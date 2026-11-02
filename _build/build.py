#!/usr/bin/env python3
"""Builds pavementenforcement.com into public/. Stdlib only.

    python3 _build/build.py

Every page is generated: never hand-edit anything in public/, the next build
overwrites it. Facts and copy live in content.py; layout lives here; styles and
behavior live in css/site.css and js/site.js (copied into public/ with a
content-hash cache-bust).
"""
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import date
from html import escape

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")
UPDATED = "November 3, 2026"
YEAR = date.today().year


def e(s):
    return escape(str(s), quote=True)


def asset_hash():
    h = hashlib.sha1()
    for p in ("css/site.css", "js/site.js"):
        with open(os.path.join(ROOT, p), "rb") as f:
            h.update(f.read())
    return h.hexdigest()[:10]


V = asset_hash()

# ---------------------------------------------------------------- icons
PHONE_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICONS = {
    "paving": '<path d="M3 20h18M5 20V9l7-5 7 5v11M9 20v-6h6v6"/>',
    "repair": '<circle cx="12" cy="12" r="8"/><path d="M8 12h8M12 8v8"/>',
    "seal": '<path d="M4 7c4-3 12-3 16 0M4 12c4-3 12-3 16 0M4 17c4-3 12-3 16 0"/>',
    "crack": '<path d="M4 4l6 16M20 4l-6 16M8 12h8"/>',
    "stripe": '<path d="M12 3v18M8 6h1M8 11h1M8 16h1M15 6h1M15 11h1M15 16h1"/>',
    "concrete": '<path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>',
    "ada": '<circle cx="12" cy="7" r="3"/><path d="M6 21v-3a6 6 0 0 1 12 0v3"/>',
    "maint": '<path d="M4 5h16v14H4z"/><path d="M8 3v4M16 3v4M4 10h16M8 14h3"/>',
}
G_SVG = '<svg class="rv-g" viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5a5.6 5.6 0 0 1-2.4 3.6v3h3.9c2.3-2.1 3.5-5.2 3.5-8.8z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 7.9-2.9l-3.9-3c-1.1.7-2.4 1.2-4 1.2-3.1 0-5.7-2.1-6.6-4.9h-4v3.1A12 12 0 0 0 12 24z"/><path fill="#FBBC05" d="M5.4 14.4a7.2 7.2 0 0 1 0-4.7V6.6h-4a12 12 0 0 0 0 10.9l4-3.1z"/><path fill="#EA4335" d="M12 4.8c1.7 0 3.3.6 4.6 1.8l3.4-3.4A12 12 0 0 0 1.4 6.6l4 3.1C6.3 6.9 8.9 4.8 12 4.8z"/></svg>'
SOCIAL_SVG = {
    "Instagram": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
    "TikTok": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16 3a5 5 0 0 0 5 5v3a8 8 0 0 1-5-1.7V15a6 6 0 1 1-6-6v3a3 3 0 1 0 3 3V3h3z"/></svg>',
    "Facebook": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 9V7c0-1 .5-1.5 1.5-1.5H17V2h-2.5C11.5 2 10 3.7 10 6.5V9H8v3.5h2V22h4v-9.5h2.7L17 9h-3z"/></svg>',
    "Yelp": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2c1 0 2 .5 2 1.5V11c0 1-1 1.5-2 1l-3-2c-1-.5-.5-2 .5-2.5L12 6V3.5C12 2.5 11.5 2 12 2zM6 13l3.5.5c1 .2 1.2 1.5.3 2L7 17.5c-1 .6-2-.4-1.7-1.4l.7-3zM18 13l-.7 3c-.3 1 .7 2 1.7 1.4l2.8-2c.9-.5.7-1.8-.3-2L18 13z"/></svg>',
}


SEAL = ('<svg class="seal-svg" viewBox="0 0 200 200" aria-hidden="true" focusable="false">'
        '<defs><path id="sealArc" d="M100,100 m-72,0 a72,72 0 1,1 144,0 a72,72 0 1,1 -144,0"/></defs>'
        '<circle cx="100" cy="100" r="96" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<circle cx="100" cy="100" r="88" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 4"/>'
        '<circle cx="100" cy="100" r="56" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<text font-family="JetBrains Mono,monospace" font-size="10.5" font-weight="700" fill="currentColor" textLength="440" lengthAdjust="spacing">'
        '<textPath href="#sealArc" startOffset="0">PAVEMENT ENFORCEMENT • PAVING DIVISION • SOCAL •</textPath></text>'
        '<path d="M100 62l9.4 19 21 3-15.2 14.8 3.6 20.9L100 109.8 81.2 119.7l3.6-20.9L69.6 84l21-3z" fill="currentColor"/>'
        '<text x="100" y="140" text-anchor="middle" font-family="Anton,sans-serif" font-size="13" letter-spacing="1.5" fill="currentColor">CSLB 1162987</text></svg>')


def eyebrow(text):
    return f'<span class="eyebrow-tag">{e(text)}</span>'


def icon(name, cls="div-card__ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">{ICONS[name]}</svg>'


# ---------------------------------------------------------------- shared bits
def call_btn(cls="btn-ghost", loc="", label=""):
    """Every call link shows the number exactly as displayed (call-tracking swaps match on it)."""
    text = f"{label} {C.PHONE_DISPLAY}".strip()
    return f'<a href="tel:{C.PHONE_E164}" class="{cls}" data-loc="{e(loc)}">{PHONE_SVG} {e(text)}</a>'


def quote_btn(href="#quote", loc="", text="Request a Free Site Inspection", cls="btn-primary"):
    return f'<a href="{href}" class="{cls}" data-quote data-loc="{e(loc)}">{e(text)} {ARROW}</a>'


def or_call():
    return f'<p class="or-call">Or call <a href="tel:{C.PHONE_E164}" data-loc="form">{C.PHONE_DISPLAY}</a></p>'


NAV = [("/services/", "Services"), ("/service-areas/", "Service Areas"), ("/about/", "About"),
       ("/#reviews", "Reviews"), ("/faq/", "FAQ"), ("/contact/", "Contact")]


def header(path):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href != "/#reviews" and path.startswith(href.strip("/")) and href != "/" and path else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    mobile = "".join(f'<a href="{h}">{l}</a>' for h, l in [("/", "Home")] + NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header>
  <nav class="nav" aria-label="Main">
    <a href="/" class="brand"><img src="/assets/logo-white.svg" alt="{C.NAME}" width="170" height="34"></a>
    <div class="nav__links">{"".join(links)}</div>
    <a href="tel:{C.PHONE_E164}" class="dispatch-btn" data-loc="header">{PHONE_SVG}<span><small>Dispatch</small>{C.PHONE_DISPLAY}</span></a>
    <button type="button" class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mm"><span></span><span></span><span></span></button>
  </nav>
</header>
<div class="mobile-menu" id="mm" role="dialog" aria-modal="true" aria-label="Menu">
  <button type="button" class="close" aria-label="Close menu">&times;</button>
  {mobile}
  <a class="tel" href="tel:{C.PHONE_E164}" data-loc="menu">Call {C.PHONE_DISPLAY}</a>
</div>'''


def footer():
    social = "".join(f'<a href="{u}" aria-label="{n}">{SOCIAL_SVG[n]}</a>' for n, u in C.SOCIAL)
    svc = "".join(f'<a href="/services/{s["slug"]}/">{s["name"]}</a>' for s in C.SERVICES)
    areas = "".join(f'<p>{a["name"]}</p>' for a in C.AREAS)
    hours = "".join(f"<p>{d} · {h}</p>" for d, h in C.HOURS)
    return f'''<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="/assets/logo-white.svg" alt="{C.NAME}" width="190" height="38">
        <p>Commercial asphalt paving, repair, sealcoating, striping, concrete and ADA work across Southern California.</p>
        <div class="foot-social">{social}</div>
      </div>
      <div class="foot-col"><h2 class="h5">Services</h2>{svc}</div>
      <div class="foot-col"><h2 class="h5">Service Areas</h2>{areas}<a href="/service-areas/">All service areas</a></div>
      <div class="foot-col">
        <h2 class="h5">Contact</h2>
        <a href="tel:{C.PHONE_E164}" data-loc="footer">{C.PHONE_DISPLAY}</a>
        <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>
        <p>{C.CITY}, {C.STATE}</p>
        <h2 class="h5" style="margin-top:22px">Hours</h2>{hours}
      </div>
    </div>
    <div class="foot-bar">
      <span>© {YEAR} {C.NAME} · {C.CITY}, {C.STATE} · CSLB Lic. # {C.LICENSE}</span>
      <span class="foot-legal"><a href="/privacy/">Privacy Policy</a><a href="/terms/">Terms</a><a href="/accessibility/">Accessibility</a></span>
    </div>
  </div>
  <div class="disclaimer">{C.NAME} is a private commercial paving contractor and is not affiliated with any government agency, law enforcement, or municipality.</div>
</footer>
<div class="callbar"><a class="c1" href="tel:{C.PHONE_E164}" data-loc="callbar">{PHONE_SVG} {C.PHONE_DISPLAY}</a><a class="c2" href="/contact/#quote" data-quote data-loc="callbar">Free Quote</a></div>'''


def field(fid, name, label, typ="text", req=False, ac=None, ph="", extra=""):
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ""
    a = f' autocomplete="{ac}"' if ac else ""
    r = " required" if req else ""
    p = f' placeholder="{e(ph)}"' if ph else ""
    im = ' inputmode="tel"' if typ == "tel" else (' inputmode="numeric" maxlength="5"' if name == "postal_code" else "")
    return (f'<div class="fg"><label for="{fid}-{name}">{label}{star}</label>'
            f'<input id="{fid}-{name}" name="{name}" type="{typ}" data-label="{e(label.lower())}"{a}{r}{p}{im}{extra}></div>')


def select(fid, name, label, options, selected=""):
    opts = "".join(f'<option{" selected" if o == selected else ""}>{e(o)}</option>' for o in options)
    return f'<div class="fg"><label for="{fid}-{name}">{label}</label><select id="{fid}-{name}" name="{name}">{opts}</select></div>'


def consent(fid):
    return (f'<label class="consent" for="{fid}-sms"><input type="checkbox" id="{fid}-sms" name="sms_consent" value="yes">'
            f'<span>I agree to receive text messages from {C.NAME} about my request, estimates and scheduling. '
            f'Message frequency varies. Msg &amp; data rates may apply. Reply STOP to opt out, HELP for help. '
            f'Consent is not a condition of purchase. See our <a href="/privacy/">Privacy Policy</a> and <a href="/terms/">Terms</a>.</span></label>')


HIDDEN = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "gbraid", "wbraid", "fbclid", "landing_page", "referrer"]


def hidden_fields(fid):
    hid = "".join(f'<input type="hidden" name="{k}">' for k in HIDDEN)
    hp = (f'<div class="hp" aria-hidden="true"><label for="{fid}-cw">Company website</label>'
          f'<input id="{fid}-cw" name="company_website" type="text" tabindex="-1" autocomplete="off"></div>')
    return hid + hp


SERVICE_OPTIONS = ["Not sure, need an inspection"] + [s["name"] for s in C.SERVICES]


def quote_form(fid="quote", service="", heading="Request a Free Site Inspection"):
    return f'''<form id="{fid}" class="quote" data-mock novalidate aria-labelledby="{fid}-h">
  <div class="form-head"><span class="form-code" aria-hidden="true">Form PE-100 · Inspection Request</span><h2 id="{fid}-h" class="h-inline">{heading}</h2><span class="form-free">Free · No obligation</span></div>
  <p class="req-note">Fields marked <span class="req" aria-hidden="true">*</span> are required.</p>
  <div class="fg-row">{field(fid, "first_name", "First name", req=True, ac="given-name")}{field(fid, "last_name", "Last name", req=True, ac="family-name")}</div>
  <div class="fg-row">{field(fid, "phone", "Phone", "tel", True, "tel", "(909) 555-0123")}{field(fid, "email", "Email", "email", False, "email", "you@company.com")}</div>
  <div class="fg-row">{select(fid, "property_type", "Property type", C.PROPERTY_TYPES)}{field(fid, "postal_code", "Property ZIP", ac="postal-code")}</div>
  {field(fid, "property_address", "Property address", ac="street-address", ph="Street, City")}
  {select(fid, "service", "Service needed", SERVICE_OPTIONS, service)}
  <div class="fg"><label for="{fid}-message">Describe the situation</label><textarea id="{fid}-message" name="message" rows="3" placeholder="Tell us about your lot"></textarea></div>
  {consent(fid)}
  {hidden_fields(fid)}
  <button type="submit" class="btn-primary form-submit">Submit Request {ARROW}</button>
  <p class="form-status" role="alert"></p>
  {or_call()}
</form>'''


def funnel_form(fid="estimate-form"):
    def fld(name, label, typ="text", req=False, ac=None, full=False):
        star = ' <span class="req" aria-hidden="true">*</span>' if req else ""
        r = " required" if req else ""
        im = ' inputmode="tel"' if typ == "tel" else ""
        return (f'<div class="fld{" full" if full else ""}"><label for="{fid}-{name}">{label}{star}</label>'
                f'<input id="{fid}-{name}" name="{name}" type="{typ}" data-label="{label.lower()}" autocomplete="{ac}"{r}{im}></div>')
    opts = "".join(f"<option>{e(o)}</option>" for o in C.PROPERTY_TYPES)
    return f'''<form id="{fid}" class="funnel__form" data-mock novalidate aria-label="Get your free estimate">
  <p class="req-note">Fields marked <span class="req" aria-hidden="true">*</span> are required.</p>
  {fld("first_name", "First name", req=True, ac="given-name")}{fld("last_name", "Last name", req=True, ac="family-name")}
  {fld("phone", "Phone", "tel", True, "tel")}{fld("email", "Email", "email", False, "email")}
  <div class="fld full"><label for="{fid}-property_type">Property type</label><select id="{fid}-property_type" name="property_type">{opts}</select></div>
  {consent(fid)}
  {hidden_fields(fid)}
  <button type="submit" class="btn-primary">Get My Free Estimate {ARROW}</button>
  <p class="form-status" role="alert" style="grid-column:1/-1"></p>
  {or_call()}
</form>'''


def request_section(service="", tone="request"):
    return f'''<section class="{tone} sec-pad" id="request">
  <div class="wrap">
    <div class="request__inner">
      <div>
        {eyebrow("File a Request")}
        <h2 class="display">Report Your Lot.<br>Request an Inspection.</h2>
        <p class="lead">Tell us what needs attention. We'll review the property, document the problem areas, and provide a clear scope with repair options and pricing.</p>
        <div class="contactline">{PHONE_SVG.replace('width="16" height="16"', 'width="22" height="22" class="ico"')}
          <div><a href="tel:{C.PHONE_E164}" data-loc="request"><b>{C.PHONE_DISPLAY}</b></a><span>Mon–Fri 8–6 · Sat 8–1</span></div></div>
        <div class="contactline"><svg class="ico" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 4h16v16H4z"/><path d="M22 6l-10 7L2 6"/></svg>
          <div><a href="mailto:{C.EMAIL}"><b>{C.EMAIL}</b></a><span>Email the office</span></div></div>
        <div class="contactline"><svg class="ico" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          <div><b>Serving all of SoCal</b><span>Inland Empire · Los Angeles · San Bernardino · Riverside · Orange</span></div></div>
      </div>
      {quote_form("quote", service)}
    </div>
  </div>
</section>'''


def pageband(eyebrow, h1, lead, ctas=True, loc="band"):
    cta = f'<div class="hero__cta">{quote_btn(loc=loc)}{call_btn(loc=loc)}</div>' if ctas else ""
    return f'''<section class="pageband">
  <div class="pageband__bg" aria-hidden="true"></div>
  <div class="pageband__seal">{SEAL}</div>
  <div class="wrap">
    <span class="eyebrow">{e(eyebrow)}</span>
    <h1 class="display">{h1}</h1>
    <p>{e(lead)}</p>
    {cta}
  </div>
</section>'''


def faq_list(keys):
    return '<div class="faq">' + "".join(
        f"<details><summary>{e(C.FAQ[k][0])}</summary><p>{e(C.FAQ[k][1])}</p></details>" for k in keys) + "</div>"


def reviews_block(heading_level=2):
    cards = "".join(f'''<li class="rv-card">
  <div class="rv-top"><span class="rv-stars" role="img" aria-label="5 out of 5 stars">★★★★★</span>{G_SVG}</div>
  <p>&ldquo;{e(r["text"])}&rdquo;</p>
  <div class="rv-by"><span class="av" aria-hidden="true">{"".join(w[0] for w in r["name"].split())[:2].upper()}</span><div><b>{e(r["name"])}</b><span>Google review · {r["when"]}{" · " + r["note"] if r.get("note") else ""}</span></div></div>
</li>''' for r in C.REVIEWS)
    return f'''<section class="sec-pad" id="reviews">
  <div class="wrap">
    <div class="sec-head"><div>
      {eyebrow("Public Record")}
      <h{heading_level} class="sec-title display">On The Record.</h{heading_level}>
      <div class="rev-score"><span class="stars" aria-hidden="true">★★★★★</span><b>{C.RATING}</b><em>Rated on Google<br>Business Profile</em></div>
    </div></div>
    <div class="rv" role="region" aria-roledescription="carousel" aria-label="Google reviews">
      <ul class="rv-track" id="rv-track" tabindex="0" aria-label="Reviews, use arrow keys to scroll">{cards}</ul>
      <div class="rv-nav">
        <button type="button" class="rv-btn" data-dir="-1" aria-label="Previous review" aria-controls="rv-track">&#8592;</button>
        <button type="button" class="rv-btn" data-dir="1" aria-label="Next review" aria-controls="rv-track">&#8594;</button>
      </div>
    </div>
    <a class="btn-primary rev-link" href="{C.GOOGLE_REVIEWS_URL}" target="_blank" rel="noopener">Read our reviews on Google<span class="sr-only"> (opens in new tab)</span></a>
  </div>
</section>'''


def process_section(tone=""):
    steps = "".join(f'<div class="proc"><span class="proc__no" aria-hidden="true">0{i}</span><span class="proc__k">Step 0{i}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for i, (t, d) in enumerate(C.PROCESS, 1))
    return f'''<section class="sec-pad {tone}" id="process">
  <div class="wrap">
    <div class="sec-head"><div>{eyebrow("Standard Procedure")}<h2 class="sec-title display">Inspect. Assess. Restore.</h2></div>
      <p>Every job follows the same four steps, so you always know what happens next.</p></div>
    <div class="proc-grid">{steps}</div>
  </div>
</section>'''


def service_cards(heading="h3"):
    return '<div class="div-grid four">' + "".join(f'''<a class="div-card" href="/services/{s["slug"]}/">
  <span class="div-card__no" aria-hidden="true">Division 0{i}</span>
  {icon(s["icon"])}
  <{heading}>{s["name"]}</{heading}>
  <p>{e(s["card"])}</p>
  <span class="div-card__link">View {e(s["name"])} <span aria-hidden="true">→</span></span>
</a>''' for i, s in enumerate(C.SERVICES, 1)) + "</div>"


# ---------------------------------------------------------------- schema
BIZ_ID = C.DOMAIN + "/#business"


def business():
    return {
        "@type": "GeneralContractor", "@id": BIZ_ID, "name": C.NAME, "url": C.DOMAIN + "/",
        "telephone": C.PHONE_E164, "email": C.EMAIL,
        "logo": C.DOMAIN + "/assets/logo-black.svg", "image": C.DOMAIN + "/assets/hero-lot.jpg",
        "address": {"@type": "PostalAddress", "addressLocality": C.CITY, "addressRegion": C.STATE,
                    "postalCode": C.ZIP, "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": C.GEO[0], "longitude": C.GEO[1]},
        "areaServed": [{"@type": "AdministrativeArea", "name": a["name"]} for a in C.AREAS],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"],
                                       "opens": h["opens"], "closes": h["closes"]} for h in C.HOURS_SCHEMA],
        "sameAs": [u for _, u in C.SOCIAL],
        "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
                          "name": f"California Contractors State License Board License #{C.LICENSE}"},
    }


def crumbs(*items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": C.DOMAIN + u} for i, (n, u) in enumerate((("Home", "/"),) + items, 1)]}


# ---------------------------------------------------------------- page shell
PAGES = []  # (path, noindex) for the sitemap


def gtm_head():
    if not C.GTM_ID:
        return "<script>window.dataLayer=window.dataLayer||[];</script>"
    return ("<script>window.dataLayer=window.dataLayer||[];(function(w,d,s,l,i){w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
            f"j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{C.GTM_ID}');</script>")


def gtm_body():
    if not C.GTM_ID:
        return ""
    return (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={C.GTM_ID}" height="0" width="0" '
            'style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>')


def page(path, title, desc, body, graph=(), noindex=False, out=None):
    url = C.DOMAIN + ("/" + path + "/" if path else "/")
    ld = json.dumps({"@context": "https://schema.org", "@graph": [business(), *graph]}, ensure_ascii=False)
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
{gtm_head()}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{C.NAME}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{C.DOMAIN}/assets/hero-lot.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="US-CA"><meta name="geo.placename" content="{C.CITY}">
<meta name="theme-color" content="#121116">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Anton&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css?v={V}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{gtm_body()}
{header(path)}
<main id="main">
{body}
</main>
{footer()}
<script src="/js/site.js?v={V}" defer></script>
</body>
</html>
'''
    dest = os.path.join(OUT, out) if out else os.path.join(OUT, path, "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    if not out:
        PAGES.append((path, noindex))


# ---------------------------------------------------------------- pages
TICKETS = [  # from the approved single-page site
    ("Potholes", "PE-01 · POTHOLE", True, "Water and traffic have broken through the surface. It's a liability hazard that only spreads and invites claims.", "Patch / Repair", "asphalt-repair", True),
    ("Alligator Cracking", "PE-02 · CRACKING", True, "Interconnected cracks like scales mean the base is failing underneath. Left alone, it turns into full replacement.", "Crack Seal / Overlay", "crack-sealing", True),
    ("Faded &amp; Graying", "PE-03 · OXIDATION", False, "A gray, brittle surface has lost its binder to UV and oxidation, the first sign your lot needs seal coat protection.", "Sealcoating", "sealcoating", False),
    ("Standing Water", "PE-04 · PONDING", False, "Puddles that linger after rain point to grading or drainage failure, which speeds up damage to the base.", "Regrade / Repair", "asphalt-paving", False),
    ("Worn Striping", "PE-05 · FADED LINES", False, "Faded stalls, fire lanes and arrows aren't just ugly. They're a compliance and safety liability for your tenants.", "Restriping", "parking-lot-striping", False),
    ("ADA Non-Compliance", "PE-06 · ADA", True, "Missing accessible stalls, signage or ramps put you at direct risk of complaints and claims. It's worth fixing early.", "ADA Upgrade", "ada-compliance", True),
]


def tickets():
    out = []
    for i, (t, code, hi, desc, act, slug, stamp) in enumerate(TICKETS, 1):
        sev = '<td class="sev-hi">■■■ HIGH</td>' if hi else "<td>■■□ MEDIUM</td>"
        st = '<div class="ticket__stamp" aria-hidden="true">Action Req\'d</div>' if stamp else ""
        out.append(f'''<div class="ticket">
  <div class="ticket__hd"><span>&#9888; NOTICE OF PAVEMENT ISSUE</span><span class="no">No. 909-0{i}</span></div>
  <div class="ticket__body">
    <h3 class="ticket__viol">{t}</h3>
    <table class="ticket__fields"><tr><td>Issue Code</td><td>{code}</td></tr><tr><td>Severity</td>{sev}</tr><tr><td>Location</td><td>YOUR LOT</td></tr></table>
    <p class="ticket__desc">{desc}</p>
    <div class="ticket__perf"></div>
    <div class="ticket__action"><span>REQUIRED ACTION</span><a href="/services/{slug}/"><b>{act}</b></a></div>
    <div class="ticket__foot"><div class="barcode" aria-hidden="true"></div><div class="ticket__pen"><span>PENALTY</span><b>Free Inspection</b></div></div>
  </div>{st}
</div>''')
    return "".join(out)


def build_home():
    words = ["Sealcoat", "Striping", "Crack Seal", "Overlays", "ADA", "Mill &amp; Pave", "Concrete", "Repairs"]
    band = "".join(f'<span{" class=o" if i % 2 else ""}>{w}</span>' for i, w in enumerate(words))
    body = f'''<section class="hero">
  <div class="hero__bg" aria-hidden="true"></div><div class="hero__grid" aria-hidden="true"></div>
  <div class="wrap">
    <div class="hero__unit">Inspect &bull; Enforce &bull; Restore</div>
    <h1 class="display">Commercial Parking Lots.<br><span class="y">Under</span><br>Enforcement.</h1>
    <p class="hero__sub">We enforce the standards big-name property owners expect: seal coat, striping, patch, overlays and full mill &amp; pave. Fast quotes. Clean job sites. Zero citations against your lot.</p>
    <div class="hero__cta">{quote_btn("#estimate", "hero")}{call_btn(loc="hero")}</div>
    <div class="hero__status"><span class="dot" aria-hidden="true"></span> <b>&nbsp;Free Estimates&nbsp;</b> · Licensed &amp; Insured · CSLB #{C.LICENSE}</div>
  </div>
  <div class="hero__seal">{SEAL}</div>
</section>
<div class="trust">
  <div class="wrap trust__grid">
    <div><b>CSLB #{C.LICENSE}</b><span>Licensed, bonded &amp; insured</span></div>
    <div><b>{C.RATING} ★ Google</b><span>Rated by property owners</span></div>
    <div><b>Free inspections</b><span>Written scope &amp; pricing</span></div>
    <div><b>4 counties</b><span>Inland Empire, LA, OC &amp; more</span></div>
  </div>
</div>

<section class="funnel" id="estimate">
  <div class="wrap funnel__inner">
    <div class="funnel__copy">
      <h2>Get Your Free<br>Estimate</h2>
      <p>Commercial lots are our focus. Give us the basics and we'll schedule a free on-site inspection and a fast, honest quote.</p>
      <div class="funnel__trust"><span><b>&#10003;</b> Free inspections</span><span><b>&#10003;</b> Licensed &amp; insured</span><span><b>&#10003;</b> {C.INSURANCE}</span></div>
    </div>
    {funnel_form()}
  </div>
</section>

<section class="divisions sec-pad" id="divisions">
  <div class="wrap">
    <div class="sec-head"><div>{eyebrow("Paving Division")}<h2 class="sec-title display">Every Service<br>Your Lot Will Ever Need.</h2></div>
      <p>Paving, repair, protection, striping, concrete and ADA work, all from one licensed contractor. <a class="div-card__link" href="/services/">All services <span aria-hidden="true">→</span></a></p></div>
    {service_cards()}
  </div>
</section>

<div class="band" aria-hidden="true"><div class="band__track">{band}</div></div>

<section class="viol sec-pad" id="violations">
  <div class="wrap">
    <div class="sec-head"><div>{eyebrow("Common Citations")}<h2 class="sec-title display">Know The Warning Signs.</h2></div>
      <p>If your lot has any of these, it's time for an inspection. Each one gets worse, and more expensive, the longer it sits.</p></div>
    <div class="viol-grid">{tickets()}</div>
    <div style="text-align:center;margin-top:44px">{quote_btn("#estimate", "violations")}</div>
  </div>
</section>

<div class="stats">
  <div class="stats__grid" style="max-width:var(--maxw);margin:0 auto">
    <div class="stat"><b>{C.RATING}★</b><span>Google Rated</span></div>
    <div class="stat"><b>FREE</b><span>Estimates</span></div>
    <div class="stat"><b>4</b><span>Counties Covered</span></div>
    <div class="stat"><b>100%</b><span>Commercial Focus</span></div>
  </div>
</div>

{process_section("tone-dark")}
{reviews_block()}

<section class="sec-pad tone-surface" id="faq">
  <div class="wrap">
    <div class="sec-head" style="justify-content:center;text-align:center;flex-direction:column;align-items:center;margin-bottom:40px">
      {eyebrow("Field Manual")}
      <h2 class="sec-title display">Frequently Asked Questions.</h2>
    </div>
    {faq_list(C.FAQ_FEATURED)}
    <p style="text-align:center;margin-top:30px"><a class="btn-dark" href="/faq/">See all questions {ARROW}</a></p>
  </div>
</section>

{request_section(tone="")}'''
    page("", "Commercial Paving & Parking Lot Repair | Pavement Enforcement",
         "Commercial paving, sealcoating, striping and ADA work in Pomona, the Inland Empire, LA and Orange County. Licensed CSLB #1162987. Call (909) 333-6330.",
         body, [{"@type": "WebSite", "name": C.NAME, "url": C.DOMAIN + "/"}])


def build_services():
    body = f'''{pageband("Services", "Paving &amp; Parking<br>Lot Services.", "Eight services that cover a commercial lot from the base to the stripes. Every job starts with a free site inspection and a clear, written scope.", loc="services")}
<section class="sec-pad">
  <div class="wrap">{service_cards("h2")}</div>
</section>
{process_section("tone-dark")}
{request_section(tone="")}'''
    page("services", "Commercial Paving & Parking Lot Services | Pavement Enforcement",
         "Asphalt paving, repair, sealcoating, crack sealing, striping, concrete and ADA upgrades for commercial lots in SoCal. Free inspections. Call (909) 333-6330.",
         body, [crumbs(("Services", "/services/")),
                {"@type": "OfferCatalog", "name": "Pavement services", "itemListElement": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f'{C.DOMAIN}/services/{s["slug"]}/'}} for s in C.SERVICES]}])


def spec_items(items):
    return "".join(f'<li><span aria-hidden="true">0{n}</span>{e(i)}</li>' for n, i in enumerate(items, 1))


def build_service(s):
    others = "".join(f'<a href="/services/{o["slug"]}/">{o["name"]}</a>' for o in C.SERVICES if o is not s)
    body = f'''{pageband("Service", e(s["name"]), s["lead"], loc=s["slug"])}
<section class="sec-pad">
  <div class="wrap split">
    <div class="prose">
      <h2>{e(s["name"])} for commercial properties</h2>
      {"".join(f"<p>{e(p)}</p>" for p in s["body"])}
      <div class="cta-row">{quote_btn(loc=s["slug"] + "-body")}{call_btn("btn-dark", s["slug"] + "-body")}</div>
    </div>
    <div class="box">
      <h2>What's included</h2>
      <ol class="spec">{spec_items(s["includes"])}</ol>
    </div>
  </div>
</section>
<section class="sec-pad tone-surface">
  <div class="wrap split">
    <div>
      <h2 class="sec-title display" style="font-size:clamp(30px,4vw,48px)">Signs it's time.</h2>
      <p class="lead-p" style="margin:16px 0 22px">Any of these on your property? We'll inspect it for free and tell you what it needs, and what can wait.</p>
      <ul class="checklist warn">{"".join(f"<li>{e(i)}</li>" for i in s["signs"])}</ul>
    </div>
    <div>
      <h2 class="sec-title display" style="font-size:clamp(30px,4vw,48px)">Common questions.</h2>
      <div style="margin-top:18px">{faq_list(s["faq"])}</div>
      <p style="margin-top:18px"><a class="div-card__link" href="/faq/">More answers <span aria-hidden="true">→</span></a></p>
    </div>
  </div>
</section>
<section class="sec-pad">
  <div class="wrap">
    <h2 class="sec-title display" style="font-size:clamp(28px,3.4vw,40px);margin-bottom:22px">Other services.</h2>
    <div class="chips">{others}</div>
  </div>
</section>
{request_section(s["name"], tone="request")}'''
    page(f'services/{s["slug"]}', f'{s["title"]} | Pavement Enforcement' if len(s["title"]) <= 42 else s["title"], s["desc"], body,
         [crumbs(("Services", "/services/"), (s["name"], f'/services/{s["slug"]}/')),
          {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["lead"],
           "provider": {"@id": BIZ_ID}, "areaServed": [a["name"] for a in C.AREAS], "url": f'{C.DOMAIN}/services/{s["slug"]}/'}])


def build_areas():
    lat, lng = C.GEO
    cards = "".join(f'<div class="area"><h3>{a["name"]}</h3><p>{e(a["blurb"])}</p></div>' for a in C.AREAS)
    who = "".join(f"<span>{e(c)}</span>" for c in C.CUSTOMERS)
    body = f'''{pageband("Service Areas", "Serving Southern<br>California.", "Based in Pomona and serving commercial properties across the Inland Empire, Los Angeles, San Bernardino, Riverside and Orange counties.", loc="areas")}
<section class="sec-pad">
  <div class="wrap">
    <div class="sec-head"><div>{eyebrow("Under Jurisdiction")}<h2 class="sec-title display">Where we work.</h2></div><p>Not sure if your property is in range? Call {C.PHONE_DISPLAY} and we'll tell you right away.</p></div>
    <div class="area-grid">{cards}</div>
  </div>
</section>
<section class="sec-pad tone-surface">
  <div class="wrap split">
    <div class="map-wrap"><iframe title="Map of the Pavement Enforcement service area around Pomona, California" src="https://maps.google.com/maps?ll={lat},{lng}&amp;z=9&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
    <div>
      <h2 class="sec-title display" style="font-size:clamp(30px,4vw,48px)">Who we serve.</h2>
      <p class="lead-p" style="margin:16px 0 22px">Commercial and managed properties of every size, from a single church lot to a multi-site portfolio.</p>
      <div class="chips">{who}</div>
      <div class="cta-row">{quote_btn(loc="areas-body")}{call_btn("btn-dark", "areas-body")}</div>
    </div>
  </div>
</section>
{request_section(tone="")}'''
    page("service-areas", "Service Areas: Inland Empire, LA & OC | Pavement Enforcement",
         "Pavement Enforcement serves commercial lots in the Inland Empire, Los Angeles, San Bernardino, Riverside and Orange counties from Pomona. Call (909) 333-6330.",
         body, [crumbs(("Service Areas", "/service-areas/"))])


def build_about():
    who = "".join(f"<li>{e(c)}</li>" for c in C.CUSTOMERS)
    body = f'''{pageband("About", "About Pavement<br>Enforcement.", "A Pomona-based commercial paving contractor focused on quality work, honest communication and doing things the right way.", loc="about")}
<section class="sec-pad">
  <div class="wrap split">
    <div class="prose">
      <h2>Who we are</h2>
      {"".join(f"<p>{e(p)}</p>" for p in C.ABOUT["pitch"])}
      <p>{e(C.ABOUT["honest"])}</p>
      <p>{C.NAME} is led by owner {e(C.ABOUT["owner"])} and is licensed, bonded and insured in California under CSLB License #{C.LICENSE}.</p>
      <div class="cta-row">{quote_btn(loc="about-body")}{call_btn("btn-dark", "about-body")}</div>
    </div>
    <div class="box">
      <h2>Who we work with</h2>
      <ul class="checklist">{who}</ul>
    </div>
  </div>
</section>
{process_section("tone-dark")}
{reviews_block()}
{request_section(tone="request")}'''
    page("about", "About Us | Pavement Enforcement, Pomona Paving Contractor",
         "Pavement Enforcement is a licensed Pomona paving contractor (CSLB #1162987) serving commercial properties across Southern California. Call (909) 333-6330.",
         body, [crumbs(("About", "/about/"))])


def build_faq():
    groups, entities = [], []
    for name, items in C.FAQ_GROUPS:
        groups.append(f'<h2 class="faq-group">{e(name)}</h2>' + faq_list([k for k, _, _ in items]))
        entities += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, q, a in items]
    body = f'''{pageband("FAQ", "Frequently Asked<br>Questions.", "Straight answers about commercial paving, sealcoating, striping, ADA work, costs and scheduling.", loc="faq")}
<section class="sec-pad">
  <div class="wrap">{"".join(groups)}
    <div class="cta-row" style="justify-content:center;margin-top:48px">{quote_btn("/contact/#quote", "faq")}{call_btn("btn-dark", "faq")}</div>
  </div>
</section>'''
    page("faq", "Paving & Parking Lot FAQ | Pavement Enforcement",
         "Answers on commercial paving, sealcoating, crack sealing, striping and ADA upgrades in Southern California from Pavement Enforcement. Call (909) 333-6330.",
         body, [crumbs(("FAQ", "/faq/")), {"@type": "FAQPage", "mainEntity": entities}])


def build_contact():
    lat, lng = C.GEO
    hours = "".join(f"<li>{d}: {h}</li>" for d, h in C.HOURS)
    body = f'''{pageband("Contact", "Request a Free<br>Site Inspection.", "Call, email or send the form. We'll schedule a visit, document the problem areas and send a clear scope with pricing.", ctas=False)}
<section class="sec-pad">
  <div class="wrap request__inner">
    {quote_form("quote")}
    <div>
      <div class="box" style="margin-bottom:22px">
        <h2>Call or email</h2>
        <p style="margin-bottom:14px">{call_btn("btn-primary", "contact")}</p>
        <p><a class="div-card__link" href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
      </div>
      <div class="box" style="margin-bottom:22px">
        <h2>Hours</h2>
        <ul class="checklist">{hours}</ul>
      </div>
      <div class="box">
        <h2>Service area</h2>
        <p style="color:var(--grey-2);margin-bottom:14px">Based in {C.CITY}, serving the Inland Empire, Los Angeles, San Bernardino, Riverside and Orange counties.</p>
        <div class="map-wrap"><iframe title="Map of the Pavement Enforcement service area around Pomona, California" src="https://maps.google.com/maps?ll={lat},{lng}&amp;z=9&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
      </div>
    </div>
  </div>
</section>'''
    page("contact", "Contact Us | Free Paving Inspection | Pavement Enforcement",
         "Request a free commercial paving site inspection from Pavement Enforcement in Pomona, CA. Serving the Inland Empire, LA and OC. Call (909) 333-6330.",
         body, [crumbs(("Contact", "/contact/"))])


def legal(path, eyebrow, h1, lead, html, title, desc):
    body = f'''{pageband(eyebrow, h1, lead, ctas=False)}
<section class="sec-pad"><div class="wrap prose">{html}<p><em>Last updated: {UPDATED}</em></p></div></section>'''
    page(path, title, desc, body, [crumbs((eyebrow, f"/{path}/"))])


CONTACT_BLOCK = (f"<p>{C.LEGAL_NAME}<br>{C.CITY}, {C.STATE}<br>Phone: <a href=\"tel:{C.PHONE_E164}\" data-loc=\"legal\">{C.PHONE_DISPLAY}</a>"
                 f"<br>Email: <a href=\"mailto:{C.EMAIL}\">{C.EMAIL}</a></p>")


def build_legal():
    legal("privacy", "Privacy", "Privacy Policy", "How we collect, use and protect information you share with us.", f'''
<p>This policy explains how {C.LEGAL_NAME} ("we", "us") handles information you give us through pavementenforcement.com, by phone or by text message.</p>
<h2>What we collect</h2>
<ul><li>Information you enter in our forms: your name, phone number, email address, property address or ZIP code, property type, the service you need and any message you write.</li>
<li>Information from calls and texts with us: your phone number, the time of the call or message, and what you tell us about your project.</li>
<li>How you found us: if you arrive from an ad or a link with tracking tags (such as utm or gclid parameters), the site stores those tags and the page you landed on in your browser for up to 90 days so we can tell which ads work.</li>
<li>Basic technical data your browser sends when you visit, such as your IP address, browser type and the pages you view.</li></ul>
<h2>How we use it</h2>
<p>We use your information to respond to your request, schedule site inspections, prepare estimates, do the work, send updates about your project and improve our website and service. We do not sell your personal information.</p>
<h2>Text messages (SMS)</h2>
<p>If you check the text-message box on our forms or otherwise agree to receive texts from {C.NAME}, we may text you about your inquiry, estimates, scheduling and service updates. Message frequency varies. Message and data rates may apply. Reply STOP to opt out at any time, or HELP for help. Consent to receive texts is not a condition of purchase. Mobile phone numbers and SMS consent are never shared with or sold to third parties or affiliates for their marketing purposes.</p>
<h2>Sharing</h2>
<p>We share information only with service providers who help us run our business (for example website hosting, phone and messaging services, and customer-management tools), and only as needed to provide our services, or when required by law.</p>
<h2>Cookies and analytics</h2>
<p>Our website loads fonts from Google Fonts and a map from Google Maps, which receive your IP address when those load. We may use analytics and advertising tools, such as Google Tag Manager, Google Analytics and Google Ads, that use cookies to measure how visitors use the site and how well our ads work. You can block or delete cookies in your browser settings.</p>
<h2>Your choices</h2>
<p>You can ask us to see, correct or delete the personal information we hold about you, and you can opt out of texts at any time by replying STOP. California residents may have additional rights under the California Consumer Privacy Act. To make a request, contact us using the details below.</p>
<h2>Contact us</h2>{CONTACT_BLOCK}''', "Privacy Policy | Pavement Enforcement", "Privacy policy for Pavement Enforcement.")

    legal("terms", "Terms", "Terms of Use", "The terms that apply when you use this website or our text messages.", f'''
<p>These terms apply to your use of pavementenforcement.com and to text messages from {C.LEGAL_NAME}. By using the site, you agree to them.</p>
<h2>Our services</h2>
<p>Information on this website is general and for planning purposes. It isn't a quote, warranty or professional engineering, legal or accessibility-compliance advice. Every project is priced and scoped in writing after a site inspection, and the written proposal or contract governs the work. {C.NAME} is licensed by the California Contractors State License Board, License #{C.LICENSE}.</p>
<h2>Text message program</h2>
<ul><li><strong>Program:</strong> {C.NAME} sends texts about your inquiry, estimates, scheduling and service updates to people who opt in through our forms or by texting us.</li>
<li><strong>Frequency:</strong> Message frequency varies.</li>
<li><strong>Cost:</strong> Message and data rates may apply.</li>
<li><strong>Opt out:</strong> Reply STOP at any time to stop receiving texts. You'll get one confirmation message.</li>
<li><strong>Help:</strong> Reply HELP, or call <a href="tel:{C.PHONE_E164}" data-loc="terms">{C.PHONE_DISPLAY}</a>.</li>
<li>Consent to receive texts is not a condition of purchase. Carriers are not liable for delayed or undelivered messages.</li>
<li>See our <a href="/privacy/">Privacy Policy</a> for how we handle your information.</li></ul>
<h2>Website use</h2>
<p>Don't misuse the site, interfere with how it works, or submit false information through our forms. The site's content, logo and design belong to {C.LEGAL_NAME} and can't be reused without permission.</p>
<h2>Not a government agency</h2>
<p>{C.NAME} is a private commercial paving contractor. Our name and design are our brand; we are not affiliated with any government agency, law enforcement or municipality.</p>
<h2>Limitation of liability</h2>
<p>The website is provided as is. To the extent allowed by law, {C.LEGAL_NAME} isn't liable for damages arising from your use of the website. Nothing here limits rights you have under California law or under a signed contract with us.</p>
<h2>Changes and governing law</h2>
<p>We may update these terms; the date below shows the latest version. These terms are governed by California law.</p>
<h2>Contact us</h2>{CONTACT_BLOCK}''', "Terms of Use | Pavement Enforcement", "Terms of use and SMS program terms.")

    legal("accessibility", "Accessibility", "Accessibility", "We want everyone to be able to use this website.", f'''
<p>{C.LEGAL_NAME} wants everyone to be able to use this website, including people who use screen readers, keyboard navigation, voice control, magnification or captions.</p>
<h2>Our standard</h2>
<p>This website is designed and tested to meet the <strong>Web Content Accessibility Guidelines (WCAG) 2.2, Level AA</strong>. We check it with automated tools and by hand: keyboard-only use, screen reader testing, color contrast and zoom to 200%.</p>
<h2>What we've done</h2>
<ul><li>Text alternatives for meaningful images</li><li>Full keyboard access with visible focus</li><li>Color contrast that meets WCAG AA</li>
<li>Labeled form fields with clear error messages</li><li>Pages that work when zoomed and on small screens</li></ul>
<h2>Known limitations</h2>
<p>Our service-area map is provided by Google Maps, and our reviews link goes to Google; we don't control the accessibility of those third-party pages. Apart from that, we're not aware of any barriers right now. If you find one, please tell us.</p>
<h2>Need help or found a barrier?</h2>
<p>If anything on this site is hard to use, or you'd like information in a different format, contact us and we'll help:</p>
<ul><li><strong>Phone:</strong> <a href="tel:{C.PHONE_E164}" data-loc="a11y">{C.PHONE_DISPLAY}</a></li><li><strong>Email:</strong> <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li></ul>
<p>Please tell us the page and what went wrong. We aim to respond within 2 business days. You can always call us to request a quote or service instead of using the online form.</p>''',
          "Accessibility Statement | Pavement Enforcement", "Accessibility statement.")


TY_H1 = 'Thank you<span id="ty-name"></span>.'


def build_utility():
    page("thank-you", "Thank You | Pavement Enforcement", "Thanks for contacting Pavement Enforcement.", f'''{pageband("Request received", TY_H1, "We've got your request. We'll reach out to schedule your free site inspection, usually within one business day.", ctas=False)}
<section class="sec-pad"><div class="wrap prose">
  <h2>Need us sooner?</h2>
  <p>Call the office during business hours and we'll get you on the schedule.</p>
  <div class="cta-row">{call_btn("btn-primary", "thank-you")}<a class="btn-dark" href="/services/">Browse services</a></div>
</div></section>''', noindex=True)
    page("404", "Page Not Found | Pavement Enforcement", "Page not found.", f'''{pageband("Error 404", "Page not<br>found.", "That page doesn't exist or has moved. Try one of these instead, or give us a call.", ctas=False)}
<section class="sec-pad"><div class="wrap">
  <div class="chips" style="margin-bottom:28px"><a href="/">Home</a><a href="/services/">Services</a><a href="/service-areas/">Service Areas</a><a href="/faq/">FAQ</a><a href="/contact/">Contact</a></div>
  <div class="cta-row">{call_btn("btn-primary", "404")}{quote_btn("/contact/#quote", "404", cls="btn-dark")}</div>
</div></section>''', out="404.html")


def build_files():
    urls = "".join(f"<url><loc>{C.DOMAIN}/{p + '/' if p else ''}</loc></url>" for p, noidx in PAGES if not noidx)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {C.DOMAIN}/sitemap.xml\n")
    lines = [f"# {C.NAME}", "",
             f"> Private commercial paving contractor in {C.CITY}, {C.STATE}, serving the Inland Empire, Los Angeles, San Bernardino, Riverside and Orange counties. Not affiliated with any government agency.", "",
             "## Key facts",
             f"- Phone: {C.PHONE_E164} ({C.PHONE_DISPLAY})", f"- Email: {C.EMAIL}", f"- Based in: {C.CITY}, {C.STATE}",
             f"- License: California CSLB #{C.LICENSE}; licensed, bonded and insured",
             "- Hours: " + "; ".join(f"{d} {h}" for d, h in C.HOURS),
             f"- Google rating: {C.RATING} stars", "- Estimates: free on-site inspections; every project priced after inspection", "",
             "## Services"] + [f"- [{s['name']}]({C.DOMAIN}/services/{s['slug']}/): {s['card']}" for s in C.SERVICES] + [
             "", "## Pages", f"- [Home]({C.DOMAIN}/)", f"- [Services]({C.DOMAIN}/services/)", f"- [Service areas]({C.DOMAIN}/service-areas/)",
             f"- [About]({C.DOMAIN}/about/)", f"- [FAQ]({C.DOMAIN}/faq/)", f"- [Contact]({C.DOMAIN}/contact/)", "", "## FAQ"]
    for name, items in C.FAQ_GROUPS:
        lines.append(f"### {name}")
        for _, q, a in items:
            lines += [f"**{q}**", a, ""]
    with open(os.path.join(OUT, "llms.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------- guards
def check():
    problems = []
    for d, _, files in os.walk(OUT):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(d, fn)
            html = open(p, encoding="utf-8").read()
            rel = os.path.relpath(p, OUT)
            for href, text in re.findall(r'<a href="(tel:[^"]*)"[^>]*>(.*?)</a>', html, re.S):
                if C.PHONE_DISPLAY not in re.sub(r"<[^>]+>", "", text) or href != "tel:" + C.PHONE_E164:
                    problems.append(f"{rel}: call link without the number: {href}")
            for need in ("/privacy/", "/terms/", "/accessibility/"):
                if f'href="{need}"' not in html:
                    problems.append(f"{rel}: footer missing {need}")
    if not os.path.exists(os.path.join(OUT, "privacy", "index.html")):
        problems.append("no /privacy page")
    if problems:
        sys.exit("BUILD FAILED\n  " + "\n  ".join(problems))


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for d in ("css", "js", "assets"):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d))
    for f in ("favicon.svg", "apple-touch-icon.png"):
        shutil.copy(os.path.join(ROOT, "assets", f), OUT)
    build_home()
    build_services()
    for s in C.SERVICES:
        build_service(s)
    build_areas()
    build_about()
    build_faq()
    build_contact()
    build_legal()
    build_utility()
    build_files()
    check()
    print(f"built {len(PAGES) + 1} pages into public/ (assets v={V})")


if __name__ == "__main__":
    main()

# Pavement Enforcement website

Static site for Pavement Enforcement (Pomona, CA; CSLB #1162987). Preview: https://pavement-enforcement-production.up.railway.app

## How it's built

- `_build/content.py`: every fact and piece of copy (services, FAQ, reviews, hours, areas). Edit here.
- `_build/build.py`: page templates, forms, schema, sitemap, robots, llms.txt. Run `python3 _build/build.py`.
- `css/site.css`, `js/site.js`, `assets/`: source files, copied into `public/` with a content-hash `?v=`.
- `public/`: **generated output, never hand-edit it.** It's committed because the Dockerfile serves it.
- `server.py` + `Dockerfile`: stdlib server for `public/` only (clean URLs, 404 page, POST → 405, no-cache HTML).
- `_raw/` (gitignored): onboarding doc and original brand files. Never commit it; it holds the EIN and owner's home address.

Pages: home, `/services/` + 8 service pages, `/service-areas/`, `/about/`, `/faq/`, `/contact/`, `/privacy/`, `/terms/`, `/accessibility/`, `/thank-you/` (noindex), `404.html`.

Check: `python3 ~/site-standards/tools/check_site.py public --launch --phone "(909) 333-6330"`

## Deploy

Railway project **SITE : Pavement Enforcement** (AM Production), service `pavement-enforcement`, auto-deploys from `main` of `ky-lore/pavement-enforcement`. A push is a deploy.

## Before launch (open items)

- **Forms are not connected.** They're front-end only (`data-mock`): validation, then redirect to `/thank-you/`. Nothing is sent, so real leads are lost until the CRM is wired. Field names are stable (`first_name`, `last_name`, `phone`, `email`, `postal_code`, `property_type`, `property_address`, `service`, `message`, `sms_consent` + attribution) for a drop-in hookup.
- **GTM:** no container ID. Set `GTM_ID` in `content.py` and rebuild.
- **Repo:** lives in Kyle's personal account and is public, with the onboarding doc in its history. Move to a private `advancedmarketers` repo per AM standards.
- **Confirm with client** (tagged `CONFIRM` in `content.py`): email `service@PavementEnforcement.com`; "$2M liability" insurance claim; "Got Potholes" as a former business name.
- **Client review:** all service-page copy, FAQ answers and area blurbs are written by us (tagged `PH`); Privacy, Terms and Accessibility pages.
- **Reviews:** 3 of 9 Google reviews shown (the rest need a signed-in view). No auto-updating widget yet.
- **Favicon:** `PE` monogram is a placeholder mark.
- **Photos:** only the hero photo; service pages have no job photos yet.
- **Domain:** pavementenforcement.com still points at GoDaddy. Canonicals already use the final domain. Add the website to the Google Business Profile once live.
- Fonts load from Google Fonts (checker warning, not a blocker).

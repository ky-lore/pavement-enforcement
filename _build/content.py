"""Every fact and piece of copy for pavementenforcement.com.

Sources: _raw/pavement-enforcment-onboarding.md (client onboarding, Aug 2026),
the client-approved single-page site (Sep 29, 2026 edit-doc revisions), the
Google Business Profile, and the license number the client sent on Oct 30, 2026.

Tags (source only, never rendered): CONFIRM = fact to verify with the client,
PH = copy we wrote (general trade knowledge / process wording) for client review.
"""

NAME = "Pavement Enforcement"
LEGAL_NAME = "Pavement Enforcement"            # onboarding: legal name, S corp
DOMAIN = "https://pavementenforcement.com"
PHONE_DISPLAY = "(909) 333-6330"               # onboarding business number
PHONE_E164 = "+19093336330"
EMAIL = "service@PavementEnforcement.com"      # CONFIRM: from the approved single-page site, not in onboarding
CITY, STATE, ZIP = "Pomona", "CA", "91768"     # street address withheld: client says it's a home address
GEO = (34.0551, -117.7500)                     # Pomona, for the map center and geo meta
LICENSE = "1162987"                            # CSLB license, from the client 2026-10-30
INSURANCE = "$2M liability"                    # CONFIRM: on the approved page, not in onboarding
GTM_ID = ""                                    # CONFIRM: no GTM container yet; snippet is emitted once set
GOOGLE_REVIEWS_URL = "https://www.google.com/maps/place/Pavement+Enforcement/data=!4m2!3m1!1s0xa40170a295512aa5:0xb384c7f6ec396d5a!18m1!1e1"
RATING = "5.0"                                 # Google Business Profile, 9 reviews as of 2026-10-31

HOURS = [("Mon–Fri", "8AM–6PM"), ("Sat", "8AM–1PM"), ("Sun", "Closed")]
HOURS_SCHEMA = [
    {"days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"},
    {"days": ["Saturday"], "opens": "08:00", "closes": "13:00"},
]

SOCIAL = [
    ("Instagram", "https://instagram.com/pavementenforcement"),
    ("TikTok", "https://tiktok.com/@pavementenforcement"),
    ("Facebook", "https://www.facebook.com/PavementEnforcement/"),
    ("Yelp", "https://www.yelp.com/biz/pavement-enforcement-pomona"),
]

AREAS = [
    {"name": "Inland Empire", "blurb": "Our home base. Ontario, Rancho Cucamonga, Fontana, Chino and the rest of the IE are a short drive from our Pomona yard."},
    {"name": "Los Angeles County", "blurb": "Pomona Valley, San Gabriel Valley and greater LA County retail centers, industrial parks and multifamily communities."},
    {"name": "San Bernardino County", "blurb": "Commercial, industrial and HOA properties across the valley side of San Bernardino County."},
    {"name": "Riverside County", "blurb": "Retail, warehouse and residential-community lots throughout western Riverside County."},
    {"name": "Orange County", "blurb": "Shopping centers, office parks and managed properties across Orange County."},
]  # PH: blurbs are ours; regions are from onboarding. City names are well-known places in each region, not a service-radius promise.

CUSTOMERS = ["Commercial property managers", "HOAs", "Industrial property owners", "Retail property owners",
             "Apartment complexes", "Mobile home parks", "Churches", "Private property owners and investors"]  # onboarding: ideal customer

PROPERTY_TYPES = ["Retail Center", "Office Park", "Industrial", "Multifamily / Apartments", "HOA",
                  "Mobile Home Park", "Church", "Other"]

# ---------------------------------------------------------------------------
# Services: the 8 core services from onboarding. Copy is PH (general trade knowledge).
SERVICES = [
    {
        "slug": "asphalt-paving", "name": "Asphalt Paving", "icon": "paving",
        "card": "New lots, full replacement and mill-and-overlay, built on a properly graded and compacted base to carry commercial traffic.",
        "title": "Commercial Asphalt Paving in the Inland Empire",
        "desc": "Commercial asphalt paving, replacement and mill-and-overlay across the Inland Empire, LA and Orange County. Licensed CSLB #1162987. Call (909) 333-6330.",
        "lead": "New construction, full-depth replacement and mill-and-overlay for parking lots, drive aisles and loading areas.",
        "body": [
            "When a lot is past the point of patching, paving is the fix that resets the clock. We start with what's underneath: grade, drainage and base. Asphalt laid over a failed base cracks again, so we look at why the old surface failed before we price new asphalt.",
            "Depending on the condition, that can mean milling the top layer and overlaying fresh asphalt, or removing the pavement down to the base and rebuilding it. We'll show you which areas need which approach, so you aren't paying for full replacement where an overlay will do.",
        ],
        "includes": ["Site inspection, measurements and photos", "Grading and drainage review", "Base repair and compaction",
                     "Hot-mix asphalt laydown and rolling", "Mill-and-overlay for sound bases", "Restriping once the asphalt cures"],
        "signs": ["Widespread alligator cracking", "Potholes that keep coming back after patching",
                  "Standing water from poor grading", "Surface that's crumbling or raveling across large areas"],
        "faq": ["repair-vs-replace", "work-around-tenants", "how-long-asphalt"],
    },
    {
        "slug": "asphalt-repair", "name": "Asphalt Repair", "icon": "repair",
        "card": "Pothole repair, patching and remove-and-replace sections that stop small failures before they spread across the lot.",
        "title": "Asphalt & Pothole Repair for Commercial Lots",
        "desc": "Pothole and asphalt repair for commercial lots in Pomona, the Inland Empire, LA and Orange County. Free site inspections. Call (909) 333-6330 today.",
        "lead": "Potholes, failed patches and broken sections cut out and rebuilt with clean, sealed edges.",
        "body": [
            "A pothole is a trip hazard, a tire claim and a sign that water is already in the base. The longer it sits, the larger the failure gets. Our repairs cut out the damaged area to sound pavement, fix the base where it's needed, and fill with hot asphalt compacted flush with the surrounding surface.",
            "We document every repair area during the inspection, so you can see exactly what's being fixed, how large each patch is, and which areas can wait. It's the kind of scope property managers can take straight to ownership or a board.",
        ],
        "includes": ["Pothole repair", "Saw-cut remove-and-replace patching", "Base repair under failed areas",
                     "Edge and seam sealing", "Utility cut and trench patches", "Repair maps with photos"],
        "signs": ["Potholes or depressions", "Alligator cracking in one area", "Broken edges along curbs and aprons",
                  "Old patches that have sunk or separated"],
        "faq": ["repair-vs-replace", "proposal-speed", "inspection-free"],
    },
    {
        "slug": "sealcoating", "name": "Sealcoating", "icon": "seal",
        "card": "A protective coat that shields asphalt from sun, oil and water and restores a clean, dark finish to the whole lot.",
        "title": "Parking Lot Sealcoating in Southern California",
        "desc": "Commercial parking lot sealcoating in the Inland Empire, LA, Riverside and Orange County. Protect your asphalt. Licensed & insured. Call (909) 333-6330.",
        "lead": "Sealcoat protects asphalt from UV, oxidation and fluids, and gives the whole property a clean, finished look.",
        "body": [
            "Southern California sun breaks down asphalt binder, which is why lots turn gray and brittle. Sealcoating puts a protective layer back on the surface and is one of the least expensive ways to extend pavement life when it's done on a regular schedule.",
            "Prep is what makes sealcoat last: cleaning, treating oil spots, and sealing cracks first. We phase the work so parts of the lot stay open, and we restripe afterward so your layout is crisp on the new surface.",
        ],
        "includes": ["Surface cleaning and oil-spot treatment", "Crack sealing before coating", "Commercial-grade sealer application",
                     "Phased closures to keep the property open", "Restriping after cure"],
        "signs": ["Faded, gray or chalky asphalt", "Loose stones on the surface", "Oil and fuel stains",
                  "Fine surface cracking"],
        "faq": ["sealcoat-how-often", "sealcoat-dry", "work-around-tenants"],
    },
    {
        "slug": "crack-sealing", "name": "Crack Sealing", "icon": "crack",
        "card": "Hot-applied crack sealant that keeps water out of the base, the cheapest way to prevent bigger repairs later.",
        "title": "Asphalt Crack Sealing for Commercial Properties",
        "desc": "Hot-applied asphalt crack sealing for commercial lots in Pomona, the Inland Empire, LA and Orange County. Stop water damage early. Call (909) 333-6330.",
        "lead": "Cracks cleaned out and filled with hot-applied sealant to keep water out of the base.",
        "body": [
            "Every open crack lets water reach the base under your asphalt. Over time that water softens the base, and that's how a small crack turns into a pothole or a section that has to be replaced. Crack sealing closes those paths.",
            "We clean each crack so the sealant bonds, then fill it with flexible hot-applied material that moves with the pavement as temperatures change. Crack sealing on its own, or before sealcoating, is the foundation of any maintenance plan.",
        ],
        "includes": ["Crack cleaning and blowing out debris", "Hot-applied rubberized sealant", "Routing where needed for a better bond",
                     "Prep ahead of sealcoating"],
        "signs": ["Long cracks along seams and edges", "Cracks wider than a coin", "Weeds growing through the pavement",
                  "Cracks that hold water after rain"],
        "faq": ["crack-seal-why", "sealcoat-how-often"],
    },
    {
        "slug": "parking-lot-striping", "name": "Parking Lot Striping", "icon": "stripe",
        "card": "Stalls, fire lanes, arrows, crosswalks and stenciling laid out sharp and straight, including re-layouts.",
        "title": "Parking Lot Striping & Restriping in SoCal",
        "desc": "Parking lot striping and restriping in the Inland Empire, LA, Riverside and Orange County: stalls, fire lanes and ADA stalls. Call (909) 333-6330 today.",
        "lead": "Stalls, fire lanes, directional arrows, crosswalks and stenciling, restriped or laid out new.",
        "body": [
            "Faded lines make a property look neglected and make traffic harder to manage. Clear striping keeps stalls usable, keeps fire lanes visible, and helps customers and tenants move through the lot safely.",
            "We restripe existing layouts or lay out new ones, including re-layouts after paving or sealcoating. Striping is usually scheduled after hours or in phases so the lot stays open.",
        ],
        "includes": ["Restriping existing layouts", "New layouts after paving or sealcoat", "Fire lanes and red curbs",
                     "Directional arrows and crosswalks", "Stencils and stall numbering", "Accessible stalls and access aisles"],
        "signs": ["Faded or hard-to-see stall lines", "Fire lanes that have worn away", "Confusing traffic flow",
                  "New paving or sealcoat that needs a layout"],
        "faq": ["work-around-tenants", "ada-what"],
    },
    {
        "slug": "concrete", "name": "Concrete Services", "icon": "concrete",
        "card": "Curbs, gutters, sidewalks, ramps, aprons and pads, poured and finished to tie cleanly into your asphalt.",
        "title": "Commercial Concrete: Curbs, Sidewalks & Ramps",
        "desc": "Commercial concrete curbs, gutters, sidewalks, ramps and aprons in the Inland Empire, LA and Orange County. Licensed CSLB #1162987. Call (909) 333-6330.",
        "lead": "Curbs, gutters, sidewalks, ramps, driveway aprons and pads that tie cleanly into the surrounding asphalt.",
        "body": [
            "Concrete around a parking lot takes a beating from tires, roots and drainage. Broken curbs and lifted sidewalk panels are trip hazards and a liability for the property.",
            "We remove damaged sections and pour new concrete that matches the surrounding grade, so water drains where it should and the finished work ties into the asphalt without a lip.",
        ],
        "includes": ["Curb and gutter replacement", "Sidewalk panel replacement", "Accessible ramps", "Driveway aprons and approaches",
                     "Pads and trash enclosures", "Drainage swales"],
        "signs": ["Cracked or broken curbs", "Lifted sidewalk panels", "Water pooling along gutters", "Crumbling driveway aprons"],
        "faq": ["ada-what", "inspection-free"],
    },
    {
        "slug": "ada-compliance", "name": "ADA Compliance", "icon": "ada",
        "card": "Accessible stalls, access aisles, ramps, detectable warnings and signage brought up to current requirements.",
        "title": "ADA Parking Lot Upgrades in Southern California",
        "desc": "ADA parking lot upgrades in SoCal: accessible stalls, access aisles, ramps, detectable warnings and signage. Licensed & insured. Call (909) 333-6330.",
        "lead": "Accessible stalls, access aisles, curb ramps, detectable warnings and signage for commercial properties.",
        "body": [
            "Accessible parking and paths of travel are covered by federal ADA standards and California building code, and older lots often fall short after years of resurfacing and restriping. Accessibility issues can lead to complaints and claims, and they make the property harder to use for the people who need those spaces.",
            "We review accessible stalls, access aisles, signage, ramps and detectable warning surfaces during the inspection and give you a clear list of what to update. For a formal compliance determination, a Certified Access Specialist (CASp) inspection is the standard in California; we can work from a CASp report if you have one.",
        ],
        "includes": ["Accessible stall and van-accessible layouts", "Access aisle striping", "Accessible signage",
                     "Curb ramps", "Detectable warning (truncated dome) surfaces", "Work from CASp reports"],
        "signs": ["Faded or missing accessible stall markings", "No van-accessible stall", "Missing or outdated signage",
                  "Steep or broken curb ramps"],
        "faq": ["ada-what", "ada-casp"],
    },
    {
        "slug": "pavement-maintenance", "name": "Pavement Maintenance", "icon": "maint",
        "card": "Scheduled inspections, crack sealing, sealcoating and restriping planned around your budget and your tenants.",
        "title": "Commercial Pavement Maintenance Programs",
        "desc": "Pavement maintenance programs for property managers and HOAs in the Inland Empire, LA and Orange County: crack seal, sealcoat, striping. Call (909) 333-6330.",
        "lead": "A planned schedule of inspections, crack sealing, sealcoating, repairs and restriping that keeps small problems small.",
        "body": [
            "Pavement wears out on a predictable curve. Regular maintenance (crack sealing, sealcoating and timely repairs) keeps it in the part of that curve where fixes are inexpensive, instead of waiting until the lot needs full replacement.",
            "For property managers, HOAs and owners with more than one property, we put together a plan that tells you what needs attention now, what can wait, and roughly when. That makes it easier to budget, get approvals and avoid surprise repairs.",
        ],
        "includes": ["Pavement condition inspections", "Prioritized repair recommendations", "Crack sealing and sealcoating cycles",
                     "Restriping schedules", "Multi-property and portfolio planning", "Scopes ready for board or ownership review"],
        "signs": ["No record of when the lot was last sealed", "Budget season is coming", "Repairs keep popping up unplanned",
                  "You manage several properties"],
        "faq": ["maint-plan", "proposal-speed", "sealcoat-how-often"],
    },
]

# ---------------------------------------------------------------------------
# FAQ: answers open with a self-contained sentence naming the business or place.
# PH: general trade knowledge, phrased as general. Legal items marked "not legal advice".
FAQ_GROUPS = [
    ("Working with us", [
        ("properties", "What types of properties does Pavement Enforcement service?",
         "Pavement Enforcement works on commercial and managed properties, including shopping centers, industrial properties, multifamily communities, HOAs, office properties, mobile home parks, churches and commercial portfolios. We also work with private property owners and investors."),
        ("inspection-free", "Is the site inspection really free?",
         "Yes, Pavement Enforcement's site inspections are free. We visit the property, review the pavement conditions, take measurements and photos as needed, and prepare a clear scope with recommended repair options and pricing. There's no obligation."),
        ("proposal-speed", "How quickly can I get a proposal from Pavement Enforcement?",
         "Pavement Enforcement prepares a detailed proposal as quickly as possible after the site inspection; turnaround depends on the size and complexity of the property. If you're working toward a budget, board meeting, ownership approval or other deadline, tell us and we'll plan around it."),
        ("work-around-tenants", "Can you schedule work around tenants and business operations?",
         "Yes. Pavement Enforcement phases commercial work so properties stay accessible, coordinating traffic flow, parking access, deliveries and scheduling to keep disruption to tenants, customers and employees to a minimum."),
        ("licensed", "Is Pavement Enforcement licensed and insured?",
         "Yes. Pavement Enforcement is licensed, bonded and insured in California under CSLB License #1162987."),
        ("government", "Is Pavement Enforcement a government agency?",
         "No. Pavement Enforcement is a private commercial paving contractor based in Pomona, California. The name and look are our brand; we're not affiliated with any government agency, law enforcement or municipality."),
        ("contact", "How do I request an estimate?",
         "The fastest way to reach Pavement Enforcement is to call (909) 333-6330, Monday through Friday 8AM–6PM and Saturday 8AM–1PM. You can also send a request through the form on our contact page and we'll follow up to schedule the inspection."),
    ]),
    ("Costs and planning", [
        ("cost", "How much does commercial paving or parking lot repair cost?",
         "Pavement Enforcement prices every project after a free on-site inspection, because cost depends on the size of the area, the condition of the asphalt and base, access and phasing, and the scope of work. In general, preventive work such as crack sealing and sealcoating costs far less per square foot than patching, and patching costs less than full replacement."),
        ("repair-vs-replace", "How do I know if my pavement needs repair, sealcoating or replacement?",
         "It depends on the condition of the pavement and what's causing the failure, which is why Pavement Enforcement inspects first. As a general rule, surface wear and fine cracks call for crack sealing and sealcoat; localized potholes and alligator cracking call for patching; and widespread base failure calls for mill-and-overlay or full-depth replacement."),
        ("maint-plan", "Do you offer pavement maintenance plans?",
         "Yes. Pavement Enforcement builds maintenance plans for property managers, HOAs and owners that lay out what needs attention now, what can wait, and when to schedule crack sealing, sealcoating and restriping, so pavement costs are easier to budget and approve."),
    ]),
    ("Asphalt and sealcoating", [
        ("sealcoat-how-often", "How often should a parking lot be sealcoated?",
         "Pavement Enforcement generally recommends sealcoating commercial asphalt every two to four years, depending on traffic, sun exposure and the condition of the surface. Lots in full Southern California sun and lots with heavy truck traffic usually need it on the shorter end of that range."),
        ("sealcoat-dry", "How long does sealcoat take to dry?",
         "Sealcoat typically needs several hours before foot traffic and about a day before vehicle traffic, depending on temperature, sun and humidity. Pavement Enforcement phases sealcoating so parts of the property stay open while other sections cure."),
        ("crack-seal-why", "Why does crack sealing matter?",
         "Crack sealing keeps water out of the base under the asphalt, and water in the base is the main cause of potholes and pavement failure. For that reason, Pavement Enforcement treats crack sealing as the first step of any maintenance plan and seals cracks before sealcoating."),
        ("how-long-asphalt", "How long does a new asphalt parking lot last?",
         "A well-built commercial asphalt lot in Southern California commonly lasts 15 to 25 years with regular maintenance. The base, drainage, traffic loads and how consistently the lot is crack sealed and sealcoated make the biggest difference."),
        ("potholes-why", "What causes potholes?",
         "Potholes form when water gets through cracks into the base and traffic breaks the weakened surface apart. Pavement Enforcement repairs potholes by cutting out the damaged area to sound pavement, fixing the base where needed and filling with compacted hot asphalt."),
        ("weather", "Can you pave or sealcoat in any weather?",
         "Asphalt paving and sealcoating need dry conditions and mild-to-warm temperatures to bond and cure properly. Pavement Enforcement schedules around rain and cold, which in the Inland Empire usually means a long working season."),
    ]),
    ("Striping and ADA", [
        ("restripe-how-often", "How often should a parking lot be restriped?",
         "Most commercial lots need restriping every one to three years, and always after sealcoating or new paving. Pavement Enforcement restripes existing layouts or lays out new ones, including fire lanes, arrows, crosswalks and accessible stalls."),
        ("ada-what", "What does ADA parking lot compliance involve?",
         "ADA parking compliance generally covers the number and layout of accessible stalls, van-accessible stalls, access aisles, signage, curb ramps, slopes and detectable warning surfaces along the accessible route. Pavement Enforcement reviews these during the site inspection and lists what to update. This is general information, not legal advice."),
        ("ada-casp", "Do I need a CASp inspection?",
         "In California, a Certified Access Specialist (CASp) is the professional who formally evaluates a property's accessibility compliance, and a CASp report can help property owners if a claim is filed. Pavement Enforcement can perform the parking lot work called out in a CASp report. This is general information, not legal advice."),
    ]),
    ("Service area", [
        ("areas", "What areas does Pavement Enforcement serve?",
         "Pavement Enforcement is based in Pomona and serves commercial properties throughout the Inland Empire and surrounding areas of Los Angeles, Orange, Riverside and San Bernardino counties."),
        ("travel", "Do you work outside the Inland Empire?",
         "Yes. Pavement Enforcement regularly works in Los Angeles County, Orange County, Riverside County and San Bernardino County. If your property is near the edge of that area, call (909) 333-6330 and we'll let you know."),
    ]),
]
FAQ = {key: (q, a) for _, items in FAQ_GROUPS for key, q, a in items}
FAQ_FEATURED = ["properties", "inspection-free", "proposal-speed", "repair-vs-replace", "work-around-tenants", "areas", "licensed"]

# ---------------------------------------------------------------------------
# Reviews: verbatim from Google (2026-10-31). Only 3 of 9 are visible without signing in.
REVIEWS = [
    {"name": "Johset P.", "when": "5 months ago",
     "text": "I recently hired Pavement Enforcement for an asphalt repair and patching job, and I honestly couldn’t be happier with the results. From the beginning, their team was professional, responsive, and very knowledgeable. … If you are looking for a reliable company for asphalt repair, pavement maintenance, seal coating, or patch work, I highly recommend Pavement Enforcement. Great communication, fair pricing, and high-quality work."},
    {"name": "Mauricio L.", "when": "8 months ago",
     "text": "Really happy with how the sealcoat and parking lot striping came out. Clean edges, straight lines, and the asphalt looks refreshed. Good communication and showed up when he said he would. Would use again!"},
    {"name": "Stuart M.", "when": "2 years ago", "note": "left under former name Got Potholes",  # CONFIRM: Got Potholes is the former name
     "text": "I recently hired Diego at Got Potholes for asphalt repair, and I couldn't be more pleased with the service. They offered a fair price without any hidden costs, and their team was incredibly friendly and professional throughout the entire process. The quality of their work is top-notch; the repaired area looks seamless and durable. … I highly recommend Diego for anyone in need of high-quality asphalt repair!"},
]

PROCESS = [  # from the approved single-page site
    ("Request an Inspection", "Tell us about the property and what needs attention. We'll schedule a site visit and gather the information we need."),
    ("Inspect the Property", "We walk the site, take measurements and photos, and identify the actual pavement conditions and problem areas."),
    ("Review Your Options", "You receive a clear scope with practical recommendations based on pavement condition, budget and long-term goals."),
    ("Schedule the Work", "We coordinate access, phasing and scheduling to reduce disruption to tenants, customers, employees and normal property operations."),
]

ABOUT = {  # onboarding "Your Story" (client's own words), lightly edited
    "pitch": [
        "We're Pavement Enforcement. We help property owners protect their investment by keeping their pavement in great shape. From sealcoating and striping to crack sealing and asphalt repairs, we focus on quality work, honest communication, and doing things the right way.",
        "We want every customer to know they're getting a company they can trust, not just for one job, but for years to come.",
    ],
    "honest": "Whether your pavement needs a simple repair, preventative maintenance or a full replacement, we'll recommend the solution that's right for your property, not just the one with the biggest price tag.",
    "owner": "Diego Arce",
}

# AtlasFlow Canonical Sitemap

## Purpose
- Define the real AtlasFlow public structure based on the dumped live-site information.
- Stop local build drift inside ContinueWave.
- Separate:
  - existing AtlasFlow structure
  - current ContinueWave upgrade surfaces
  - future work that should wait for live-site access

## Rule
- Treat this sitemap as the source structure for AtlasFlow upgrades inside ContinueWave.
- Do not invent parallel AtlasFlow architecture unless it maps back to this structure.

## Canonical Public Structure

### Core Navigation
1. Home
2. Services
3. About
4. Contact
5. Book a Call

### Service Pages
1. Cannabis Marketing
2. CBD Marketing
3. Shopify Development
4. Branding & Identity
5. Paid Advertising
6. SEO & Content
7. Brand Growth

### Supporting Commercial Pages
1. About
2. Contact

## AtlasFlow Operating Model
- AtlasFlow is the parent brand.
- The brand serves two real commercial lanes:
  - regulated operators
  - trust-based / practitioner operators
- The regulated lane explicitly includes:
  - cannabis
  - CBD
  - wellness
  - e-commerce
  - related compliance-sensitive operators
- The practitioner lane explicitly includes:
  - doctors
  - dentists
  - clinics
  - chiropractors
  - wellness practitioners
  - other trust-based operators

## Current ContinueWave Upgrade Surfaces

### Already Present
1. `homepage.html`
2. `regulated_growth.html`
3. `practitioner_growth.html`
4. `compliance_report.html`
5. `strategy_call.html`
6. `about.html`
7. `contact.html`

### Existing Support / Offer Pages
1. `practitioner_growth_audit.html`
2. `lead_response_engine.html`
3. `compliance_audit.html`
4. `newsletter.html`

## Mapping: Real AtlasFlow -> ContinueWave

### Direct Match
- Home -> `homepage.html`
- About -> `about.html`
- Contact -> `contact.html`

### Category / Lane Layer
- Services -> currently represented indirectly through:
  - `regulated_growth.html`
  - `practitioner_growth.html`

### Real Service Pages Not Yet Built In ContinueWave
1. Cannabis Marketing
2. CBD Marketing
3. Shopify Development
4. Branding & Identity
5. Paid Advertising
6. SEO & Content
7. Brand Growth

## Booking / Conversion Truth
- Canonical booking link:
  - `https://tidycal.com/1042lpn/15-minute-meeting`
- Use TidyCal as the real booking target in upgraded surfaces.
- Keep email fallback truthful until the live AtlasFlow stack can be edited directly.

## Upgrade Order
1. Home
2. About
3. Contact
4. Services routing surface
5. Cannabis Marketing
6. CBD Marketing
7. Shopify Development
8. Branding & Identity
9. Paid Advertising
10. SEO & Content
11. Brand Growth
12. Practitioner-specific service layering after live-site access clarifies how that lane is presented publicly

## Work To Avoid
- Do not create a second fake AtlasFlow brand system.
- Do not expand service pages beyond this map without live-site confirmation.
- Do not let ContinueWave staging structure overwrite AtlasFlow source structure.

## Current Interpretation
- ContinueWave is the upgrade and execution layer.
- AtlasFlow is the real brand and public commercial surface.
- The dumped screenshots and copied page text are reference truth for structure and direction.

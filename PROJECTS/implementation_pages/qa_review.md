Implementation Pages QA Review

Date
- 2026-03-13

Scope
- `*.html` in workspace root (live GitHub Pages set)
- `PROJECTS/implementation_pages/*.html` (Netlify/Vercel source mirror)

Checks Run
- all expected implementation pages exist (12 files including `index.html`)
- canonical links present on all pages
- runtime/config scripts present on all pages (`assets/site-runtime.js`, `assets/site-config.js`)
- typed form wiring present on all forms (`contact`, `newsletter`, `strategy_call`)
- all local `.html` links resolve in both directories
- deployed `assets/site-config.js` checked on Netlify, Vercel, and GitHub Pages
- deployed `assets/site-runtime.js` checked on Netlify, Vercel, and GitHub Pages for activation-guard marker (`provider_activation`)

Results
- PASS: page set is complete and mirrored across root + `PROJECTS/implementation_pages`
- PASS: canonical and runtime instrumentation present on 12/12 pages in both locations
- PASS: 3/3 forms are wired to runtime submission handlers
- PASS: no broken local `.html` links detected
- PASS: production form endpoint config live on all 3 hosts (`formsubmit.co/ajax/growth@atlasflow.co.za`)
- PASS: runtime guard update is live on all 3 hosts and prevents false-success on provider `success:false`

Notes
- Form submission endpoint now points to FormSubmit (`growth@atlasflow.co.za`) for contact/newsletter/strategy-call flows.
- Production-like endpoint smoke test (with `Origin` + `Referer`) is active and returning successful submissions.
- GA4 Measurement ID `G-EGX6W6THK5` is configured in `assets/site-config.js` and deployed on all three hosts; Realtime/DebugView confirmation is still pending.
- Canonical host is set to `https://implementationpages.vercel.app` with optional redirect toggle.

Next Move
- run GA Realtime/DebugView validation for page, CTA, and form success events on production pages.

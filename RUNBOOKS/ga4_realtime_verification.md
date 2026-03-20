# GA4 Realtime Verification

Date
- 2026-03-16

Purpose
- Confirm that AtlasFlow production pages send the currently achievable GA4 events into Realtime and DebugView, and do not pretend `form_submit_success` is available while live forms are in `email_fallback` mode.

GA4 Property
- Measurement ID: `G-EGX6W6THK5`

Primary Host
- Use Vercel as the canonical verification host:
  - `https://implementationpages.vercel.app`

Secondary Hosts
- Netlify:
  - `https://atlasflow-v1-static-20260312.netlify.app`
- GitHub Pages:
  - `https://francosmit94-web.github.io/ContinueWave/`

Known Runtime Facts
- `redirectToCanonical` is `false`.
- `?ga_debug=1` shows the on-page GA debug panel.
- `window.ATLASFLOW_DEBUG` is available in the browser console.
- Current production form mode is `email_fallback` on Vercel, Netlify, and GitHub Pages.
- In `email_fallback` mode, form submission attempts emit:
  - `form_submit_attempt`
  - `form_submit_blocked`
- In `email_fallback` mode, the canonical fallback conversion event is:
  - `conversion_email_intent`
- Additional direct contact-intent events available when relevant links exist on the page:
  - `conversion_phone_intent`
  - `conversion_whatsapp_intent`
- In `email_fallback` mode, production cannot emit:
  - `form_submit_success`
- Live page reachability rechecked on 2026-03-16:
  - Vercel `200`
  - Netlify `200`
  - GitHub Pages `200`
- Read-only production smoke command:
  - `python .\SERVICES\continuewave_orchestrator.py atlasflow-smoke --host all`
  - latest result on 2026-03-16: PASS across Vercel, Netlify, and GitHub Pages

Minimal Verification Pass
1. Open:
   - `https://implementationpages.vercel.app/contact.html?ga_debug=1`
2. Confirm the debug panel appears at bottom right.
3. Wait a few seconds for the automatic `page_view`.
4. Click `Send test event` in the debug panel.
   - Expected events:
     - `cw_debug_ping`
     - `cw_debug_ping_beacon` fallback beacon path may also appear
5. Click `Book a Call`.
   - Expected event:
     - `cta_click`
6. On either `contact.html`, `newsletter.html`, or `strategy_call.html`, submit one real form.
   - Expected events:
     - `form_submit_attempt`
     - `form_submit_blocked`
     - `conversion_email_intent`

Recommended Full Pass
1. `contact.html?ga_debug=1`
   - trigger `page_view`
   - click `Send test event`
   - click `Book a Call`
   - submit contact form
2. `newsletter.html?ga_debug=1`
   - submit newsletter form
3. `strategy_call.html?ga_debug=1`
   - submit strategy call form

Suggested Test Inputs
- Contact form
  - Name: `GA Test Contact`
  - Email: your real email
  - Reason: `Service fit inquiry`
  - Message: `GA4 verification test from production page on 2026-03-16.`
- Newsletter form
  - Name: `GA Test Newsletter`
  - Email: your real email
- Strategy call form
  - Name: `GA Test Strategy`
  - Email: your real email
  - Business / Project: `AtlasFlow QA`
  - Current Situation: `Checking production GA4 form tracking.`
  - Main Question or Decision: `Confirm fallback conversion_email_intent visibility.`

What To Check In GA4
- Realtime:
  - active user appears
  - events list shows `page_view`, `cta_click`, and `form_submit_attempt`
  - if a form is submitted while fallback is active, `form_submit_blocked` should appear instead of `form_submit_success`
  - `conversion_email_intent` should be marked as the fallback conversion event in GA4
  - if phone or WhatsApp links exist, `conversion_phone_intent` and `conversion_whatsapp_intent` should be marked as conversions too
- DebugView:
  - same events appear in sequence from one device/session
  - optional debug markers:
    - `cw_debug_ping`
    - `form_submit_attempt`
    - `form_submit_blocked`
    - `conversion_email_intent`

GA4 Mapping Rule
- While production remains in `email_fallback` mode, mark `conversion_email_intent` as the conversion event in GA4.
- Mark `conversion_phone_intent` and `conversion_whatsapp_intent` as conversions when those channels exist.
- Do not mark `form_submit_attempt` as a conversion.
- When a real backend returns, shift the primary conversion event to `form_submit_success` and keep `conversion_email_intent` as the fallback-path signal.

If DebugView Does Not Show Events
- Keep `?ga_debug=1` on the URL.
- Open browser console and run:
```js
ATLASFLOW_DEBUG.analyticsStatus()
```
- Confirm:
  - `measurementId` is `G-EGX6W6THK5`
  - `gtagConfigured` is `true`
- Then run:
```js
ATLASFLOW_DEBUG.track('manual_debug_event', { source: 'console' })
ATLASFLOW_DEBUG.beaconPing()
```

Completion Rule
- Do not mark BLK-005 fully cleared while the canonical production host is in `email_fallback` mode.
- Current partial verification target:
  - `page_view`
  - `cta_click`
  - `form_submit_attempt`
  - `form_submit_blocked`
  - `conversion_email_intent`
- Full BLK-005 clearance still requires a real submission path that produces `form_submit_success` on production, or a deliberate change in conversion semantics.

# BLOCKERS
# Format: ID | status | lane/payload | description | workaround | unblock condition

## Active

### BLK-001
- **Status:** ACTIVE
- **Lane/Payload:** system
- **Description:** Live provider calls are blocked (`403 / 1010`) on both Cerebras and Groq in the current environment (verified 2026-03-12).
- **Workaround:** Use `prompt-build` plus local fallback (`Ollama + qwen2.5-coder:7b`) for continuity, and avoid forcing repeated failing cloud calls.
- **Unblock Condition:** At least one direct `call-model` check succeeds cleanly for both Cerebras and Groq from this machine.

### BLK-003
- **Status:** WATCH
- **Lane/Payload:** system
- **Description:** OpenClaw local gateway/client auth intermittently fails with OAuth refresh + `device-auth.json` EPERM errors.
- **Workaround:** Restart the gateway without `--force`, re-authenticate the operator session, and avoid stale listeners on port `18789`.
- **Unblock Condition:** `openclaw gateway health` and regular agent turns run without OAuth refresh or EPERM auth-file failures.

### BLK-005
- **Status:** WATCH
- **Lane/Payload:** AtlasFlow deploy
- **Description:** GA4 Measurement ID is deployed (`G-EGX6W6THK5`), but true backend conversion is still blocked by the current production form mode. While forms run in `email_fallback`, production can emit `page_view`, `cta_click`, `form_submit_attempt`, `form_submit_blocked`, and `conversion_email_intent`, but not `form_submit_success`.
- **Workaround:** Verify `page_view`, `cta_click`, `form_submit_attempt`, `form_submit_blocked`, and `conversion_email_intent` in GA Realtime/DebugView on production. Treat `conversion_email_intent` as the fallback conversion signal until a real backend submission path returns.
- **Unblock Condition:** GA4 event traffic is observed for page/CTA activity plus either a real production `form_submit_success` path exists, or `conversion_email_intent` is deliberately accepted as the canonical fallback conversion rule.

### BLK-006
- **Status:** WATCH
- **Lane/Payload:** AtlasFlow forms
- **Description:** External form provider path is unreliable (`formsubmit.co` browser certificate warning and upstream `403` through proxy).
- **Workaround:** Use explicit email fallback from the live forms and keep form infrastructure off the critical path.
- **Unblock Condition:** Replace the provider with a dependable same-origin backend or a verified provider that works from production without certificate or upstream rejection issues.

## Cleared

- BLK-002
- BLK-004 (2026-03-13): Vercel production deploy completed successfully to `https://implementationpages.vercel.app`.
- BLK-005 activation sub-block (2026-03-13): FormSubmit now accepts live submissions from production origin.

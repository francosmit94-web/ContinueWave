# QUEUE
# Format: [STATUS] task | lane | type | next trigger

## Now
- [READY] Start sessions with the orchestrator instead of manual improvisation | system | workflow | now
- [READY] Validate GA4 Realtime/DebugView events (`page_view`, `cta_click`, `form_submit_attempt`, `form_submit_blocked`, `conversion_email_intent`) on production | AtlasFlow | analytics | now
- [READY] Mark `conversion_email_intent`, `conversion_phone_intent`, and `conversion_whatsapp_intent` as GA4 conversions where applicable | AtlasFlow | analytics | now
- [READY] Use `RUNBOOKS/atlasflow_v1_finish_line.md` as the closeout threshold and avoid reopening system work before v1 is called finished | AtlasFlow | finish | now
- [READY] Use `PROJECTS/atlasflow_canonical_sitemap.md` as the source structure for AtlasFlow upgrades | AtlasFlow | structure | now
- [READY] Keep ContinueWave as system and AtlasFlow as payload | system | discipline | always
- [READY] Return to core AtlasFlow build work instead of form-provider debugging | AtlasFlow | focus | now

## Next
- [READY] Decide whether AtlasFlow should restore a real form backend or treat fallback-email intent as the tracked conversion event | AtlasFlow | analytics/forms | after current GA verification
- [READY] Pick one AtlasFlow first-client niche and send the first 20 outreach messages | AtlasFlow | revenue | after conversion tracking deploy
- [READY] Use `PROJECTS/continuewave_subagent_roles.md` as the first controlled multi-agent template after AtlasFlow v1 closeout | system | architecture | after v1_done
- [READY] Review `PROJECTS/nemo_agent_toolkit_phase2.md` only after AtlasFlow v1 closeout and first outreach execution | system | research | after v1_done
- [READY] Decide canonical redirect policy (`redirectToCanonical`) and enable only on chosen host if needed | AtlasFlow | routing | after endpoint tests
- [READY] Refresh NOW.md, QUEUE.md, and HANDOFF.md through actual use rather than more planning | system | maintain | after deployment passes
- [READY] Review old material only when a live task actually needs it | system | synthesize | later
- [READY] Replace temporary AtlasFlow email fallback with a dependable same-origin form backend later | AtlasFlow | forms | after core build priorities

## Later
- [READY] Import selected source material only when required by real work | system | import_on_demand | later
- [READY] Add coding/project workflows only after business operating layer is stable | system | expand | later

## Done
- [DONE] OpenCode installed
- [DONE] Aider installed
- [DONE] Continue CLI installed
- [DONE] Ollama installed
- [DONE] qwen2.5-coder:7b installed
- [DONE] OpenCode configured for local Ollama models
- [DONE] OpenCodeBrain root created
- [DONE] Initial migration backed up to ARCHIVE
- [DONE] OpenCodeBrain reset to minimal working surface
- [DONE] ContinueWave orchestrator MVP built and verified
- [DONE] AtlasFlow first-pass implementation handoff set generated (11 pages)
- [DONE] Homepage first implementation artifact created from handoff bundle
- [DONE] Compliance Report implementation artifact created from handoff bundle
- [DONE] Strategy Call implementation artifact created from handoff bundle
- [DONE] Practitioner Growth Audit implementation artifact created from handoff bundle
- [DONE] Regulated Growth implementation artifact created from handoff bundle
- [DONE] Practitioner Growth implementation artifact created from handoff bundle
- [DONE] Lead Response Engine implementation artifact created from handoff bundle
- [DONE] Compliance Audit implementation artifact created from handoff bundle
- [DONE] Newsletter implementation artifact created from handoff bundle
- [DONE] About implementation artifact created from handoff bundle
- [DONE] Contact implementation artifact created from handoff bundle
- [DONE] QA review of implementation_pages for CTA/link consistency completed
- [DONE] index.html navigation page added for implementation artifacts
- [DONE] deployment handoff document created for implementation_pages
- [DONE] v1 static zip package created and publish command runbook prepared
- [DONE] Netlify production publish completed (`https://atlasflow-v1-static-20260312.netlify.app`) with HTTP 200 checks on key pages
- [DONE] Local `gh-pages` branch prepared with implementation_pages commit (`2e1d191`)
- [DONE] GitHub authenticated and repository published at `https://github.com/francosmit94-web/ContinueWave`
- [DONE] `gh-pages` branch flattened to root and pushed (latest commit `7a37b18`)
- [DONE] GitHub Pages live at `https://francosmit94-web.github.io/ContinueWave/` with HTTP 200 verification on key pages
- [DONE] Vercel production publish completed at `https://implementationpages.vercel.app` (`francosmit94-7829s-projects`)
- [DONE] Shared runtime/config assets added for canonical control, typed forms, and analytics hooks
- [DONE] All 12 pages redeployed with canonical + runtime includes on Netlify, GitHub Pages, and Vercel
- [DONE] Real production form endpoints configured in `assets/site-config.js` and deployed to all three hosts
- [DONE] Live endpoint smoke tests executed for all form types (currently awaiting FormSubmit activation)
- [DONE] Form runtime patched to prevent false-success on provider `success:false` responses and flag activation-required submissions
- [DONE] Runtime guard redeployed across Vercel + Netlify + GitHub Pages (`gh-pages` commit `1acfbd3`)
- [DONE] FormSubmit activation confirmed live (`success:true`) for `contact`, `newsletter`, and `strategy_call` from production origin
- [DONE] GA4 Measurement ID `G-EGX6W6THK5` configured and deployed across Vercel, Netlify, and GitHub Pages (`gh-pages` commit `3d8bd83`)
- [DONE] GA runtime debug mode enabled and deployed across Vercel, Netlify, and GitHub Pages (`gh-pages` commit `83efdd6`)
- [DONE] On-page GA diagnostics (`?ga_debug=1` panel + `cw_debug_ping` trigger + `ATLASFLOW_DEBUG` API) deployed across all hosts (`gh-pages` commit `55382d9`)
- [DONE] Decision-gate policy added to ContinueWave orchestrator (`PROCEED` / `ASK` / `STOP`) for uninterrupted routine local work
- [DONE] `atlasflow-smoke` command added and verified against Vercel, Netlify, and GitHub Pages production hosts

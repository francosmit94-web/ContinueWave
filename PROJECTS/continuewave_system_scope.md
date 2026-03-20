# ContinueWave System Scope

## Purpose
- Define the canonical architecture of ContinueWave as it exists in this workspace.
- Separate the system layer from the active payload layer.
- Make the operating model inspectable without relying on chat history.

## System Identity
- ContinueWave is the local operator system.
- Franco is the decision authority.
- Continue is the operator interface/runtime shell.
- The workspace root is `C:\Users\Franco\Desktop\ContinueWave`.

## Core Layers
1. Brain layer
- File-based memory and control stack
- Primary files:
  - `README.md`
  - `NOW.md`
  - `HANDOFF.md`
  - `QUEUE.md`
  - `STATE/state.json`

2. Policy layer
- Decision gates in `STATE/decision_gates.json`
- Action classes:
  - `PROCEED`
  - `ASK`
  - `STOP`

3. Control plane
- `SERVICES/continuewave_orchestrator.py`
- Reconstructs session state, classifies actions, updates memory files, and runs repeatable commands

4. Payload layer
- AtlasFlow is the current active payload
- Static site files live at repo root and are mirrored under `PROJECTS/implementation_pages/`

## Runtime Model Stack
- Primary route: `Continue + Cerebras`
- Secondary route: `Continue + Groq`
- Local fallback: `Continue + Ollama + qwen2.5-coder:7b`

Notes:
- Runtime selection lives in `STATE/state.json`
- The system logic is model-agnostic
- Cloud-first is the intended default

## Control Stack
Read in this order:
1. `README.md`
2. `NOW.md`
3. `HANDOFF.md`
4. `QUEUE.md`
5. `STATE/state.json`

## Decision Standard
Each action should do at least one of these:
- generate revenue
- unblock a critical dependency
- improve decision quality
- harden the operating system
- simplify the workflow

## Orchestrator Responsibilities
- session start reconstruction
- gate evaluation
- blocker sync
- handoff/state updates
- prompt assembly
- direct model calls
- AtlasFlow production smoke checks

Key commands:
- `start`
- `gate-policy`
- `gate-check`
- `sync-blockers`
- `handoff-update`
- `state-update`
- `session-close`
- `atlasflow-smoke`

## AtlasFlow Scope
- AtlasFlow is the first real payload running inside ContinueWave
- Canonical public host: `https://implementationpages.vercel.app`
- Secondary hosts:
  - Netlify
  - GitHub Pages

Core runtime assets:
- `assets/site-config.js`
- `assets/site-runtime.js`

Current payload reality:
- static site
- multi-host deployment
- GA4 instrumentation
- fallback email conversion path
- local runtime now supports email, phone, and WhatsApp contact-intent tracking

## Current Conversion Model
- weak signal: `form_submit_attempt`
- fallback qualified signal: `conversion_email_intent`
- optional direct-link signals:
  - `conversion_phone_intent`
  - `conversion_whatsapp_intent`
- true backend success remains `form_submit_success`, but it is not the active production path while forms stay in `email_fallback`

## Boundaries
- ContinueWave is the hidden operator system
- AtlasFlow is the public-facing payload/output
- ContinueWave should not expand unless the new layer removes repeated friction from real payload work

## Current Status
- Brain layer: usable MVP
- Decision gates: active
- Orchestrator: working MVP
- Payload deployment flow: working
- Remaining work: refinement, deployment of the newest runtime changes, GA conversion confirmation, and eventual backend restoration if desired

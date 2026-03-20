# ContinueWave

Continue is the primary orchestrator. Franco is the decision authority.
Routine local execution is delegated through explicit decision gates.
Everything in this workspace runs from:
`C:\Users\Franco\Desktop\ContinueWave`

## Identity
ContinueWave is a clean second-generation operator workspace.
It is not a clone, port, or shell around any prior system.

Its purpose is to:
- become a clean and self-contained operator system
- reduce cost and dependency on paid AI
- simplify execution and lower cognitive load
- support clear, healthy decision-making
- evolve through deliberate design rather than reactive accumulation

## Current Scope
This workspace starts from a minimal core.
It will grow only when a real task requires it.

Active surface:
- control files
- state file
- clean folder structure
- minimal AtlasFlow operating layer

Archive surface:
- reserved for deliberately imported source material only
- not part of active operating context by default

## Operator Stack
Primary daily runtime:
- `Continue + Cerebras`

Secondary cloud runtime:
- `Continue + Groq`

Local fallback:
- `Continue + Ollama + qwen2.5-coder:7b`

Use cloud first for:
- speed
- synthesis
- planning
- longer reads
- most daily operator work

Use local `7b` for:
- offline work
- private work
- fallback when cloud is unavailable
- simple drafting and utility tasks

## Control Stack
Read in this order at session start:
1. `README.md`
2. `NOW.md`
3. `HANDOFF.md`
4. `QUEUE.md`
5. `STATE/state.json`

Do not assume archived files are active or authoritative.

## Core Rules
- Read before editing.
- Keep state in files, not chat.
- Prefer the smallest safe change.
- Prefer clean new files over broad rewrites.
- Do not import old material blindly.
- No outbound without explicit `GO SEND` from Franco.
- Escalate only for legal/compliance risk, irreversible action, money decision, or ownership/equity change.

## Decision Gates
- `PROCEED`: routine local reads, edits, tests, QA, control-file updates, and safe local git work.
- `ASK`: outbound send, public publish, remote push, production config change, dependency install, secret request, or writes outside the workspace.
- `STOP`: destructive filesystem or git action, money spend, legal/compliance claim as fact, ownership/equity change, or credential rotation.
- Source of truth: `STATE/decision_gates.json`
- Operator command: `python .\SERVICES\continuewave_orchestrator.py gate-check <action_type>`

## Evolution Discipline
- This is a curated brain, not a dump.
- Old systems are source material, not structure.
- Nothing from prior tools is automatically sacred.
- If old material is stale, noisy, desperate, or tool-shaped, leave it out.
- Prefer synthesis over migration.
- Prefer original clean structure over inherited complexity.

## Execution Loop
1. Read the control stack.
2. Summarize the current state.
3. Identify the top 3 executable priorities.
4. Recommend one highest-leverage next move.
5. Inspect before editing.
6. Make the smallest safe implementation.
7. Update `HANDOFF.md` and `STATE/state.json` at the end of meaningful work.

## File Roles
- `README.md`: system identity and operating rules
- `NOW.md`: current phase and immediate operator focus
- `QUEUE.md`: prioritized executable backlog
- `HANDOFF.md`: compressed transfer note for the next session
- `STATE/state.json`: machine-readable state
- `PROJECTS/`: curated active project and strategy files
- `RUNBOOKS/`: repeatable workflows that survive migration review
- `TEMPLATES/`: reusable prompts, formats, and delivery assets
- `SERVICES/`: productized offers and sales assets
- `ARCHIVE/`: retired or deferred material

## Decision Standard
Every action should do at least one of these:
- generate revenue
- unblock a critical dependency
- improve decision quality
- harden the operating system
- simplify the workflow

If it does none of the above, it should usually wait.

## Initial Priority
The first job of ContinueWave is not expansion.
It is stability and clarity.

The immediate goals are:
- keep the active workspace minimal
- wire the cloud-first stack cleanly
- establish a calm working rhythm
- build an original operating system that can selectively learn from past work without inheriting its mess

Orchestrator Usage

Purpose
- Define how to use the first working version of the ContinueWave orchestrator.

Location
- `SERVICES/continuewave_orchestrator.py`

What It Does Now
- reads the control stack
- prints a clean session-start summary
- prints the delegated decision-gate summary
- creates a new file safely inside the workspace
- prints guidance for explicit task modes
- updates `HANDOFF.md` after a meaningful session
- loads stored prompt templates from `PROMPTS/`
- supports a minimal direct model-call path for Cerebras and Groq
- updates a small approved subset of `STATE/state.json`
- can assemble the exact final prompt bundle without making a network call
- syncs active blockers from `BLOCKERS.md` into both handoff and machine state
- assembles page-level implementation handoffs from AtlasFlow project files
- classifies proposed actions as `PROCEED`, `ASK`, or `STOP`
- runs a read-only production smoke check for live AtlasFlow hosts

Commands

Session Start

```powershell
python .\SERVICES\continuewave_orchestrator.py start
```

Safe File Creation

```powershell
python .\SERVICES\continuewave_orchestrator.py create-file PROJECTS\example.md --title "Example" --template brief
```

Example With Content Lines

```powershell
python .\SERVICES\continuewave_orchestrator.py create-file PROJECTS\note.md --title "Note" --line "Purpose" --line "- Capture the next move."
```

Task Mode Guidance

```powershell
python .\SERVICES\continuewave_orchestrator.py mode planning
```

Handoff Update

```powershell
python .\SERVICES\continuewave_orchestrator.py handoff-update --changed "Implemented the next orchestrator feature." --open "Prompt wiring still remains." --next-move "Implement prompt wiring in the orchestrator script."
```

Prompt Registry

```powershell
python .\SERVICES\continuewave_orchestrator.py prompt list
python .\SERVICES\continuewave_orchestrator.py prompt planning
```

Direct Model Call

```powershell
python .\SERVICES\continuewave_orchestrator.py call-model --provider cerebras --prompt-name planning --input "Define the problem and the next move."
```

Prompt Build

```powershell
python .\SERVICES\continuewave_orchestrator.py prompt-build --prompt-name planning --file README.md --file NOW.md --input "Define the problem and the next move."
```

Build Handoff

```powershell
python .\SERVICES\continuewave_orchestrator.py build-handoff --page homepage
```

State Update

```powershell
python .\SERVICES\continuewave_orchestrator.py state-update --mode BUILD --direct-model-calls-ready
```

Session Close

```powershell
python .\SERVICES\continuewave_orchestrator.py session-close --changed "Closed the current pass cleanly." --open "Provider verification still remains blocked." --next-move "Use prompt-build or verify provider access directly outside the restricted environment."
```

Blocker Sync

```powershell
python .\SERVICES\continuewave_orchestrator.py sync-blockers
```

Decision Gates

```powershell
python .\SERVICES\continuewave_orchestrator.py gate-policy
python .\SERVICES\continuewave_orchestrator.py gate-check edit_local --summary "Patch the orchestrator"
python .\SERVICES\continuewave_orchestrator.py gate-check publish_external --summary "Redeploy production pages"
```

AtlasFlow Smoke

```powershell
python .\SERVICES\continuewave_orchestrator.py atlasflow-smoke --host all
```

Rules
- use workspace-relative paths only
- do not use it to overwrite files unless you mean to
- keep the first version simple
- keep direct model calls tightly scoped and file-bounded
- prefer stored prompts over ad hoc prompt sprawl
- keep state updates narrow and operational, not descriptive
- use prompt-build to inspect context before blaming the model path

Next Step
- verify live provider calls after key setup is stable

Decision Gates

Purpose
- Let ContinueWave continue through routine local work without waiting on Franco for every judgment call.

Policy File
- `STATE/decision_gates.json`

Default Rule
- Continue automatically only when the action is explicitly classified as `PROCEED`.
- Pause on `ASK`.
- Escalate immediately on `STOP`.

Proceed
- local reads
- local edits
- control-file updates
- runbook updates
- state updates
- local tests and QA
- local branch and local commit work
- blocker sync and handoff assembly
- known-host reachability checks

Ask
- outbound sending
- public publishing
- remote pushes
- production config changes
- dependency installs
- secret or credential requests
- writes outside the workspace

Stop
- destructive filesystem actions
- destructive git actions
- spending money
- legal or compliance judgments stated as facts
- ownership or equity changes
- credential rotation

Commands
```powershell
python .\SERVICES\continuewave_orchestrator.py gate-policy
python .\SERVICES\continuewave_orchestrator.py gate-check edit_local --summary "Patch the orchestrator"
python .\SERVICES\continuewave_orchestrator.py gate-check publish_external --summary "Redeploy production pages"
```

Maintenance Rule
- Update the JSON policy first.
- Keep the categories stable and boring.
- Add a new action type only when a real repeated decision point appears.

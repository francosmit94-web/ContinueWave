Git Workflow

Purpose
- Keep ContinueWave versioned and recoverable without making git a burden.

Default Rhythm
- checkpoint after meaningful system-layer changes
- checkpoint after meaningful payload-layer blocks
- do not commit every tiny scratch change

When To Commit
- new runbook completed
- new orchestrator capability added
- major payload block completed
- state/routing changes that affect future sessions

Suggested Commit Shapes
- `system: add orchestrator usage and context loading`
- `payload: add AtlasFlow page copy set`
- `system: normalize state and routing docs`

What Not To Commit
- broken experiments you already know you will discard
- duplicate placeholder files
- secret keys

Recovery Rule
- if a session gets messy, commit the last known good state before trying another big change

Minimum Safe Habit
- one clean checkpoint at the end of a useful block of work

Rule
- git should support clarity and rollback, not turn into ceremony.

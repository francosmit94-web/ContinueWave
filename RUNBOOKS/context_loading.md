Context Loading

Purpose
- Define how ContinueWave should load context without overwhelming the model.
- Keep sessions grounded, selective, and repeatable.

Default Load Order
1. README.md
2. NOW.md
3. HANDOFF.md
4. QUEUE.md
5. STATE/state.json

Only Load More If Needed
- relevant runbooks
- one active project file
- one supporting file

Context Rules
- Do not load the whole workspace by default.
- Do not load archive material unless a task explicitly requires it.
- Prefer one file set per task.
- If a session starts drifting, reduce context instead of adding more.

Task Shapes
- planning task:
  - control files
  - one project file

- editing task:
  - target file
  - one adjacent support file if necessary

- synthesis task:
  - control files
  - one synthesis brief
  - one source file at a time

Refresh Rule
- Start a fresh session when:
  - the provider starts failing repeatedly
  - the model becomes generic or unstable
  - context has grown beyond the task

Default
- If unsure, load less.

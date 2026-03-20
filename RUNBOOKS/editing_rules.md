Editing Rules

Purpose
- Define how files should be changed inside ContinueWave.
- Prevent accidental low-quality edits.
- Keep the workspace clean, deliberate, and recoverable.

Core Rule
- Do not edit a file unless the purpose of the edit is clear.

When Continue Should Edit
- Use Continue for:
  - improving or creating operating documents
  - restructuring small markdown files
  - refining page briefs or service documents
  - making bounded edits where the desired outcome is already known

When Continue Should Not Edit
- Do not use Continue for:
  - broad multi-file rewrites
  - vague “improve everything” requests
  - shell-based file construction
  - any edit that has not first been explained clearly

When Aider Should Edit
- Use Aider for:
  - precise code edits
  - small scoped file changes
  - direct implementation work where exact file control matters

When To Edit Directly
- Edit directly when:
  - the file is short
  - the desired structure is already obvious
  - the model is unstable
  - continuing the session would waste time

Pre-Edit Standard
Before any meaningful edit, define:
- what file is changing
- why it is changing
- what should be different after the edit

Scope Rule
- Prefer editing one file at a time.
- Prefer the smallest useful change.
- Do not edit adjacent files unless the current task clearly requires it.

Quality Rule
- Prefer clarity over cleverness.
- Prefer structure over flourish.
- Prefer useful specificity over generic filler.
- If the model produces vague sludge, stop and tighten the prompt.

PowerShell Rule
- Windows PowerShell only.
- No bash syntax.
- No cmd chaining with `&&`.
- Prefer direct file editing over shell-built file creation.

Recovery Rule
- If a model reports an edit, verify the file on disk.
- If the file did not actually change, do not assume success.
- If the model becomes unstable, stop and either:
  - restart the session,
  - switch provider,
  - or edit directly.

Default
- If unsure, inspect first and edit later.

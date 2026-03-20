# Session Resume
# Updated: 2026-03-11

## Start Here
Launch OpenCode in:
Launch Continue in:
`C:\Users\Franco\Desktop\ContinueWave`

Use this first prompt:

```text
Read README.md, NOW.md, HANDOFF.md, QUEUE.md, STATE/state.json, then read RUNBOOKS/stack.md.

Summarize the current operating state in 8 bullets.
Identify the top 3 executable priorities.
Recommend the single best next move.
Do not edit anything yet.
```

## After Provider Setup
Use this prompt:

```text
I want to build a healthy second-generation operating brain.

Do not copy old systems blindly.
Study the evolution across OpenClaw, Claude, and OpenCodeBrain.

First determine:
1. what is structurally useful,
2. what is noise or emotional clutter,
3. what should be preserved,
4. what should be redesigned,
5. what the clean v2 architecture should be.

Start by identifying the minimum set of source files to review first.
Do not edit anything yet.
```

## If The Model Starts Wandering
Use this correction prompt:

```text
Reduce scope.
Stay grounded in the actual files.
Recommend one move only.
Do not generalize beyond the workspace.
```

## If You Want It To Keep Building Without Chat
Use:

```text
Proceed in small safe steps.
Before each edit:
1. explain the file,
2. explain the change,
3. make the smallest safe implementation,
4. update HANDOFF.md and STATE/state.json when the step is complete.
```

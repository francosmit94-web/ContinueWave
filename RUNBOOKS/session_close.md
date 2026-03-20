Session Close

Purpose
- Define how a ContinueWave session should end.
- Preserve continuity between sessions.
- Ensure useful state is written to disk instead of left in chat.

Close Sequence

1. Summarize What Changed
- Record what was actually created, clarified, or decided.
- Ignore fluff and partial thoughts that did not result in a real change.

2. Update HANDOFF.md
- Add:
  - what changed
  - what remains open
  - the next best move

- Keep it concise and practical.

3. Update NOW.md
- Update only if the active focus changed.
- Keep NOW.md about present direction, not full history.

4. Update STATE/state.json
- Update only if actual operating state changed.
- Examples:
  - model routing changed
  - active workspace status changed
  - new major file created
  - current phase changed

5. Leave The Queue Clean
- If a task became the next obvious move, make sure QUEUE.md reflects it.
- If a task no longer matters, remove or defer it.

What To Capture
- structural decisions
- file creation
- priority changes
- workflow changes
- active blockers

What Not To Capture
- raw chat noise
- vague motivation
- speculative ideas with no decision
- anything that does not improve the next session

Definition Of A Good Close
- the next session can start without confusion
- the next move is obvious
- the important state lives in files

Default Rule
- If you do not have time to close the session properly, at minimum update HANDOFF.md.

Daily Session

Purpose
- Turn ContinueWave into a repeatable operating system.
- Define how sessions should start, run, and close.
- Keep the stack calm, useful, and low-friction.

Session Start
- Open ContinueWave first, not old workspaces.
- Start in the clean workspace root.
- Read these files in order:
  - README.md
  - NOW.md
  - HANDOFF.md
  - QUEUE.md
  - STATE/state.json

Opening Prompt
- Start with a bounded read-and-decide prompt.
- Ask for:
  - current state
  - top priorities
  - single best next move
- Do not start with broad synthesis or large file sweeps.

Model Routing
- Cerebras
  - default for live workspace sessions
  - use for reading, summarizing, and structured planning

- Groq
  - use for short, fast reasoning or refinement prompts
  - do not use as the main multi-turn workspace model if rate limits are causing friction

- Ollama qwen2.5-coder:7b
  - use only for offline fallback
  - use for low-stakes local drafting or continuity when cloud models are unavailable

Tool Routing
- Continue
  - primary orchestrator
  - use for workspace reasoning, file reading, structured planning, and selective file edits

- Aider
  - secondary editor
  - use when precise file edits or coding changes are needed
  - do not use Aider as the brain or orchestrator

Working Rule
- One move at a time.
- One file or one small file set at a time.
- Prefer creating or improving one useful document over creating many placeholders.
- Keep active context narrow.

When Creating Files
- Create a file only if it improves:
  - clarity
  - execution
  - decision quality
  - offer readiness
  - operating structure

- If a file does none of the above, do not create it yet.

End Of Session
- Update NOW.md if the active focus changed.
- Update HANDOFF.md with:
  - what changed
  - what remains open
  - the next best move

- Update STATE/state.json only when the actual operating state has changed.

Anti-Drift Rules
- Do not bulk-import old material.
- Do not let the model create broad generic filler.
- Do not let one flaky provider derail the whole system.
- Do not confuse more tooling with more leverage.

Definition Of A Good Session
- one useful decision made
- one meaningful file created or clarified
- one next move made more obvious

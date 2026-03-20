Model Routing

Purpose
- Define which model should be used for which type of work.
- Reduce friction, indecision, and provider thrashing.
- Keep the system fast and stable on this machine.

Primary Session Model
- Cerebras

Use Cerebras for:
- normal ContinueWave sessions
- reading workspace files
- summarizing and structuring information
- writing or refining operating documents
- planning next moves
- medium-length multi-turn sessions

Why
- better fit than Groq for active workspace sessions when Groq rate limits become disruptive
- keeps heavy inference off the local machine

Fast Reasoning Model
- Groq

Use Groq for:
- short one-shot prompts
- fast comparisons
- tightening copy
- concise second opinions
- quick idea pressure-tests

Do not use Groq for:
- long multi-turn workspace sessions if TPM limits are causing repeated failures
- broad file-reading sessions with accumulating context

Local Fallback Model
- Ollama + qwen2.5-coder:7b

Use local fallback for:
- offline continuity
- low-stakes drafting
- simple classification or summarization
- situations where cloud models are unavailable

Do not use local fallback for:
- deep synthesis
- long planning sessions
- anything that causes heat or slowdown significant enough to break flow

Tool Pairing
- Continue + Cerebras
  - default operating session

- Continue + Groq
  - fast short-turn reasoning only

- Aider + cloud model
  - precise edit sessions

- Aider + local fallback
  - emergency local editing only

Decision Rules
- If the session is broad and exploratory, start with Cerebras.
- If the task is very short and speed matters, use Groq.
- If the cloud path breaks, drop to local only for continuity, not for heavy work.
- If the task is a precise file edit, use Aider or direct editing.

Anti-Thrashing Rule
- Do not switch models mid-task unless:
  - the active provider is failing,
  - the rate limit is blocking progress,
  - or the task clearly changed shape.

Default
- If unsure, use Continue + Cerebras first.

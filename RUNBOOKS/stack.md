# Stack
# Updated: 2026-03-11

## Endgame Stack
- Interface: `Continue`
- Primary provider: `Groq`
- Secondary provider: `Cerebras`
- Local fallback: `Ollama + qwen2.5-coder:7b`
- Workspace: `C:\Users\Franco\Desktop\ContinueWave`

## Roles
- `Groq`
  - daily driver
  - fast reads
  - summaries
  - planning
  - synthesis
  - general build work

- `Cerebras`
  - backup cloud provider
  - overflow if Groq rate-limits
  - second-pass long-context work

- `Ollama + qwen2.5-coder:7b`
  - offline fallback
  - private work
  - low-stakes drafting
  - emergency local continuity

## Use Pattern
1. Start in `Groq`
2. Fall back to `Cerebras` if needed
3. Use local `7b` only when cloud is unavailable or local/privacy matters

## Rule
Do not default to local heavy models on this machine.
Speed and low friction matter more than squeezing out a small gain in local capability.

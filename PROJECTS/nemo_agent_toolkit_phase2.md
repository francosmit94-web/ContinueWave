# NVIDIA NeMo Agent Toolkit Phase 2

## Purpose
- Capture the NVIDIA NeMo Agent Toolkit as a later orchestration candidate without interrupting AtlasFlow v1 closeout.

## Why It Matters
- NVIDIA positions NeMo Agent Toolkit as an open-source layer for building, evaluating, profiling, optimizing, and orchestrating agent workflows.
- That overlaps with the future multi-agent direction of ContinueWave.

## What It Is Relevant For
- multi-agent orchestration
- profiling and observability
- workflow evaluation
- optimization of agent/tool/model combinations
- interoperability across frameworks

## What It Is Not For Right Now
- replacing the ContinueWave brain
- replacing the file-based control stack
- interrupting AtlasFlow v1 finish work

## ContinueWave Position
- ContinueWave remains the executive brain:
  - memory
  - handoff
  - queue
  - state
  - decision gates
- NeMo Agent Toolkit is only a possible future execution/orchestration layer for specialist agents

## Phase 2 Evaluation Questions
1. Can it orchestrate the first three planned subagent roles cleanly?
2. Does it improve observability over the current lightweight ContinueWave approach?
3. Does it justify its complexity for a small operator system?
4. Can it plug into ContinueWave without replacing the file brain?

## Earliest Valid Adoption Point
- After AtlasFlow v1 is closed out
- After the first outreach loop is running
- After subagent role boundaries are proven on paper and in manual practice

## Current Rule
- Research only
- No active integration work before AtlasFlow v1 closeout

## References
- NVIDIA Technical Blog: How to Build Custom AI Agents with NVIDIA NeMo Agent Toolkit Open Source Library
- NVIDIA Technical Blog: Extending the NVIDIA NeMo Agent Toolkit to Support New Agentic Frameworks
- NVIDIA AI-Q Blueprint

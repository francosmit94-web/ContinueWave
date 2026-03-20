from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
PROMPTS_DIR = WORKSPACE / "PROMPTS"
CONTROL_FILES = [
    WORKSPACE / "README.md",
    WORKSPACE / "NOW.md",
    WORKSPACE / "HANDOFF.md",
    WORKSPACE / "QUEUE.md",
    WORKSPACE / "STATE" / "state.json",
    WORKSPACE / "STATE" / "decision_gates.json",
]
TASK_MODES = {"planning", "writing", "editing", "synthesis", "review"}
PROMPT_FILES = {
    "session-start": "session_start.md",
    "planning": "planning.md",
    "writing": "writing.md",
    "editing": "editing.md",
    "synthesis": "synthesis.md",
    "recovery": "recovery.md",
    "powershell-guardrail": "powershell_guardrail.md",
    "session-close": "session_close.md",
}
DEFAULT_PROVIDER_MODELS = {
    "cerebras": "llama3.1-8b",
    "groq": "llama-3.1-8b-instant",
}
PROVIDER_CONFIG = {
    "cerebras": {
        "env": "CEREBRAS_API_KEY",
        "base": "https://api.cerebras.ai/v1/chat/completions",
    },
    "groq": {
        "env": "GROQ_API_KEY",
        "base": "https://api.groq.com/openai/v1/chat/completions",
    },
}
SAST = timezone(timedelta(hours=2))
SMOKE_PAGES = [
    "contact.html?ga_debug=1",
    "newsletter.html?ga_debug=1",
    "strategy_call.html?ga_debug=1",
]
SMOKE_RUNTIME_MARKERS = [
    "ATLASFLOW_DEBUG",
    "cw_debug_ping",
    "form_submit_success",
    "cta_click",
    "page_view",
]
IMPLEMENTATION_GLOBAL_FILES = [
    "PROJECTS/page_dependency_map.md",
    "PROJECTS/site_component_map.md",
    "PROJECTS/site_style_guide.md",
]
IMPLEMENTATION_PAGE_SUFFIXES = [
    "_brief.md",
    "_page_brief.md",
    "_copy.md",
    "_page_copy.md",
    "_meta_copy.md",
    "_open_graph_copy.md",
    "_faq.md",
    "_build_checklist.md",
    "_form_logic.md",
    "_email_sequence.md",
    "_wireframe.md",
    "_lovable_prompt.md",
]


@dataclass
class SessionState:
    phase: str
    focus: str
    top_priorities: list[str]
    ready_queue: list[str]
    next_best_move: str
    provider: str
    primary_model: str
    payload_hint: str
    gate_summary: dict[str, list[str]]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\r?\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_numbered_items(section: str) -> list[str]:
    items: list[str] = []
    for line in section.splitlines():
        match = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if match:
            items.append(match.group(1).strip())
    return items


def extract_bullet_items(section: str) -> list[str]:
    items: list[str] = []
    for line in section.splitlines():
        match = re.match(r"^\s*-\s+(.*)$", line)
        if match:
            items.append(match.group(1).strip())
    return items


def extract_ready_queue(queue_text: str) -> list[str]:
    ready_section = extract_section(queue_text, "Now")
    items: list[str] = []
    for line in ready_section.splitlines():
        match = re.match(r"^\s*-\s+\[READY\]\s+(.*?)(?:\s+\|\s+.*)?$", line)
        if match:
            items.append(match.group(1).strip())
    return items


def detect_payload_hint(handoff_text: str, state: dict) -> str:
    payload_active = state.get("payload", {}).get("active")
    if payload_active:
        return str(payload_active)
    if "AtlasFlow is now the first major payload" in handoff_text:
        return "AtlasFlow"
    return "None"


def build_session_state() -> SessionState:
    now_text = read_text(WORKSPACE / "NOW.md")
    handoff_text = read_text(WORKSPACE / "HANDOFF.md")
    queue_text = read_text(WORKSPACE / "QUEUE.md")
    state = json.loads(read_text(WORKSPACE / "STATE" / "state.json"))

    phase = extract_section(now_text, "Current Phase").splitlines()[0].strip()
    focus_block = extract_section(now_text, "System Focus")
    focus = focus_block.splitlines()[0].strip() if focus_block else ""
    top_priorities = extract_numbered_items(extract_section(now_text, "Current Top 3"))
    ready_queue = extract_ready_queue(queue_text)

    next_best_move = ""
    handoff_next = extract_section(handoff_text, "Next Best Move")
    if handoff_next:
        next_best_move = " ".join(line.strip() for line in handoff_next.splitlines()).strip()
    elif ready_queue:
        next_best_move = ready_queue[0]

    operator = state.get("operator", {})
    gate_summary = summarize_gate_policy(load_gate_policy())
    return SessionState(
        phase=phase,
        focus=focus,
        top_priorities=top_priorities,
        ready_queue=ready_queue,
        next_best_move=next_best_move,
        provider=operator.get("provider", ""),
        primary_model=operator.get("primary_model", ""),
        payload_hint=detect_payload_hint(handoff_text, state),
        gate_summary=gate_summary,
    )


def check_workspace() -> None:
    missing = [str(path.relative_to(WORKSPACE)) for path in CONTROL_FILES if not path.exists()]
    if missing:
        raise SystemExit(f"Missing control files: {', '.join(missing)}")


def load_dotenv() -> dict[str, str]:
    env_path = WORKSPACE / ".env"
    values: dict[str, str] = {}
    if not env_path.exists():
        return values
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def load_state() -> dict:
    return json.loads(read_text(WORKSPACE / "STATE" / "state.json"))


def load_gate_policy() -> dict:
    return json.loads(read_text(WORKSPACE / "STATE" / "decision_gates.json"))


def resolve_publish_hosts(state: dict, selected_host: str) -> dict[str, str]:
    publish = state.get("status", {}).get("atlasflow_static_publish", {})
    host_map = {
        "vercel": publish.get("vercel", {}).get("url", ""),
        "netlify": publish.get("netlify", {}).get("url", ""),
        "github_pages": publish.get("github_pages", {}).get("url", ""),
    }
    if selected_host == "all":
        return {name: url for name, url in host_map.items() if url}
    url = host_map.get(selected_host, "")
    return {selected_host: url} if url else {}


def write_state(state: dict) -> None:
    state["last_updated"] = datetime.now(SAST).isoformat(timespec="seconds")
    target = WORKSPACE / "STATE" / "state.json"
    target.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def get_secret(name: str) -> str:
    if os_value := os.environ.get(name):
        return os_value
    return load_dotenv().get(name, "")


def fetch_url_text(url: str, timeout: int) -> tuple[int, str]:
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        status = getattr(response, "status", response.getcode())
        body = response.read().decode("utf-8", errors="replace")
    return status, body


def load_prompt(name: str) -> str:
    filename = PROMPT_FILES.get(name)
    if not filename:
        raise SystemExit(f"Unknown prompt: {name}")
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise SystemExit(f"Missing prompt file: {path.relative_to(WORKSPACE)}")
    return read_text(path).strip()


def replace_section(text: str, heading: str, body_lines: list[str]) -> str:
    body = "\n".join(body_lines).rstrip()
    replacement = f"## {heading}\n"
    if body:
        replacement += f"{body}\n"
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\r?\n.*?(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    if not text.endswith("\n"):
        text += "\n"
    return f"{text}\n{replacement}"


def update_handoff(
    changed: list[str], remains_open: list[str], next_move: list[str], blockers: list[str]
) -> None:
    handoff_path = WORKSPACE / "HANDOFF.md"
    text = read_text(handoff_path)
    text = replace_section(text, "What Changed This Session", [f"- {item}" for item in changed])
    text = replace_section(text, "Active Blockers", [f"- {item}" for item in blockers])
    text = replace_section(text, "Next Best Move", next_move)
    if remains_open:
        text = replace_section(text, "What Remains Open", [f"- {item}" for item in remains_open])
    handoff_path.write_text(text.rstrip() + "\n", encoding="utf-8")


def parse_active_blockers(blockers_text: str) -> list[str]:
    active_section = extract_section(blockers_text, "Active")
    if not active_section:
        return []

    entries: list[str] = []
    chunks = re.split(r"(?m)^###\s+", active_section)
    for chunk in chunks[1:]:
        lines = [line.rstrip() for line in chunk.strip().splitlines() if line.strip()]
        if not lines:
            continue
        blocker_id = lines[0].strip()
        status = ""
        description = ""
        for line in lines[1:]:
            status_match = re.match(r"^\s*-\s+\*\*Status:\*\*\s*(.+?)\s*$", line)
            if status_match:
                status = status_match.group(1).strip().upper()
                continue
            description_match = re.match(r"^\s*-\s+\*\*Description:\*\*\s*(.+?)\s*$", line)
            if description_match:
                description = description_match.group(1).strip()

        if not status or status == "CLEARED":
            continue
        summary = f"{blocker_id} ({status})"
        if description:
            summary = f"{summary}: {description}"
        entries.append(summary)
    return entries


def cmd_sync_blockers(_: argparse.Namespace) -> int:
    check_workspace()
    blockers_path = WORKSPACE / "BLOCKERS.md"
    if not blockers_path.exists():
        raise SystemExit("Missing blocker register: BLOCKERS.md")

    entries = parse_active_blockers(read_text(blockers_path))
    summary = ["See BLOCKERS.md for the live blocker register.", *entries]
    if len(summary) == 1:
        summary.append("No active blockers listed.")

    handoff_path = WORKSPACE / "HANDOFF.md"
    handoff_text = read_text(handoff_path)
    handoff_text = replace_section(handoff_text, "Active Blockers", [f"- {item}" for item in summary])
    handoff_path.write_text(handoff_text.rstrip() + "\n", encoding="utf-8")

    state = load_state()
    state["major_blockers"] = summary
    write_state(state)

    print("Synchronized blockers from BLOCKERS.md")
    print(f"- Active blockers: {max(0, len(summary) - 1)}")
    return 0


def cmd_start(_: argparse.Namespace) -> int:
    check_workspace()
    state = build_session_state()
    print("# ContinueWave Session Start\n")
    print(f"- Phase: {state.phase}")
    print(f"- Focus: {state.focus}")
    print(f"- Provider route: {state.provider}")
    print(f"- Primary model: {state.primary_model}")
    print(f"- Active payload hint: {state.payload_hint}")
    print("\n## Top Priorities")
    for item in state.top_priorities[:3]:
        print(f"- {item}")
    print("\n## Ready Queue")
    for item in state.ready_queue[:5]:
        print(f"- {item}")
    print("\n## Single Best Next Move")
    print(f"- {state.next_best_move}")
    print("\n## Decision Gates")
    print(f"- Proceed by default: {', '.join(state.gate_summary['PROCEED'][:6])}")
    print(f"- Ask first: {', '.join(state.gate_summary['ASK'][:6])}")
    print(f"- Stop: {', '.join(state.gate_summary['STOP'][:6])}")
    return 0


def normalize_rel_path(path_str: str) -> Path:
    rel = Path(path_str)
    if rel.is_absolute():
        raise SystemExit("Use a workspace-relative path, not an absolute path.")
    target = (WORKSPACE / rel).resolve()
    if WORKSPACE not in [target, *target.parents]:
        raise SystemExit("Target path must stay inside ContinueWave.")
    return target


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def iter_lines(values: Iterable[str]) -> list[str]:
    lines: list[str] = []
    for value in values:
        if value:
            lines.append(value.rstrip())
    return lines


def summarize_gate_policy(policy: dict) -> dict[str, list[str]]:
    summary: dict[str, list[str]] = {"PROCEED": [], "ASK": [], "STOP": []}
    for rule in policy.get("rules", []):
        decision = str(rule.get("decision", "")).upper()
        if decision not in summary:
            continue
        for action_type in rule.get("action_types", []):
            normalized = str(action_type).strip().lower()
            if normalized and normalized not in summary[decision]:
                summary[decision].append(normalized)
    for decision in summary:
        summary[decision].sort()
    return summary


def evaluate_gate(policy: dict, action_type: str) -> dict[str, str]:
    normalized = action_type.strip().lower()
    for rule in policy.get("rules", []):
        action_types = [str(item).strip().lower() for item in rule.get("action_types", [])]
        if normalized in action_types:
            return {
                "decision": str(rule.get("decision", policy.get("default_decision", "ASK"))).upper(),
                "rule_id": str(rule.get("id", "unnamed-rule")),
                "reason": str(rule.get("reason", "")).strip(),
            }
    return {
        "decision": str(policy.get("default_decision", "ASK")).upper(),
        "rule_id": "default-decision",
        "reason": str(policy.get("default_reason", "")).strip(),
    }


def cmd_create_file(args: argparse.Namespace) -> int:
    check_workspace()
    target = normalize_rel_path(args.path)
    if target.exists() and not args.force:
        raise SystemExit(f"File already exists: {target.relative_to(WORKSPACE)}")

    lines = []
    if args.title:
        lines.append(args.title.strip())
        lines.append("")

    lines.extend(iter_lines(args.line or []))

    if args.template == "brief":
        if lines:
            lines.append("")
        lines.extend(
            [
                "Purpose",
                "- ",
                "",
                "Role",
                "- ",
                "",
                "Next Move",
                "- ",
            ]
        )
    elif args.template == "runbook":
        if lines:
            lines.append("")
        lines.extend(
            [
                "Purpose",
                "- ",
                "",
                "Default Rule",
                "- ",
                "",
                "Workflow",
                "1. ",
            ]
        )

    ensure_parent(target)
    content = "\n".join(lines).rstrip() + "\n"
    target.write_text(content, encoding="utf-8")
    print(f"Created {target.relative_to(WORKSPACE)}")
    return 0


def cmd_handoff_update(args: argparse.Namespace) -> int:
    check_workspace()
    changed = iter_lines(args.changed or [])
    remains_open = iter_lines(args.open or [])
    next_move = iter_lines(args.next_move or [])
    blockers = iter_lines(args.blocker or [])

    if not changed:
        raise SystemExit("Provide at least one --changed item.")
    if not next_move:
        raise SystemExit("Provide at least one --next-move item.")
    if not blockers:
        blockers = ["See `BLOCKERS.md` for the live blocker register."]

    update_handoff(changed, remains_open, next_move, blockers)
    print(f"Updated {(WORKSPACE / 'HANDOFF.md').relative_to(WORKSPACE)}")
    return 0


def cmd_mode(args: argparse.Namespace) -> int:
    check_workspace()
    mode = args.name.lower()
    if mode not in TASK_MODES:
        raise SystemExit(f"Unknown mode: {args.name}")

    guidance = {
        "planning": [
            "Load only the control files first.",
            "Add one project file only if it materially affects the next move.",
            "Output summary, priorities, and one next move.",
        ],
        "writing": [
            "Load the control files and one target brief or support file.",
            "Create or extend one document only.",
            "Prefer calm, direct output over broad exploration.",
        ],
        "editing": [
            "Load the target file first.",
            "Load at most one support file if needed.",
            "Make the smallest useful change only.",
        ],
        "synthesis": [
            "Load one source file at a time.",
            "Extract only what improves clarity, execution, reusable assets, or operating structure.",
            "Do not import old wording blindly.",
        ],
        "review": [
            "Inspect the current file set without editing.",
            "Report issues, gaps, and the single best next move.",
            "Keep the review concise and factual.",
        ],
    }

    print(f"# ContinueWave Task Mode: {mode}\n")
    for line in guidance[mode]:
        print(f"- {line}")
    prompt_map = {
        "planning": "planning",
        "writing": "writing",
        "editing": "editing",
        "synthesis": "synthesis",
        "review": "recovery",
    }
    print(f"\n- Recommended prompt: {prompt_map[mode]}")
    return 0


def cmd_prompt(args: argparse.Namespace) -> int:
    check_workspace()
    if args.name == "list":
        print("# ContinueWave Prompt Registry\n")
        for name in PROMPT_FILES:
            print(f"- {name}")
        return 0

    prompt_text = load_prompt(args.name)
    print(prompt_text)
    return 0


def build_model_messages(
    prompt_name: str | None,
    prompt_text: str | None,
    user_input: str | None,
    files: list[str],
) -> list[dict[str, str]]:
    parts: list[str] = [load_prompt("powershell-guardrail")]
    if prompt_name:
        parts.append(load_prompt(prompt_name))
    if prompt_text:
        parts.append(prompt_text.strip())
    if user_input:
        parts.append(user_input.strip())

    for file_arg in files:
        target = normalize_rel_path(file_arg)
        parts.append(f"File: {file_arg}\n\n{read_text(target).strip()}")

    return [{"role": "user", "content": "\n\n".join(part for part in parts if part)}]


def cmd_prompt_build(args: argparse.Namespace) -> int:
    check_workspace()
    messages = build_model_messages(args.prompt_name, args.prompt_text, args.input, args.file or [])
    print(messages[0]["content"])
    return 0


def collect_implementation_files(page: str) -> list[Path]:
    page_slug = page.strip().lower().replace(" ", "_")
    files: list[Path] = []
    for suffix in IMPLEMENTATION_PAGE_SUFFIXES:
        candidate = WORKSPACE / "PROJECTS" / f"{page_slug}{suffix}"
        if candidate.exists():
            files.append(candidate)
    for rel in IMPLEMENTATION_GLOBAL_FILES:
        candidate = WORKSPACE / rel
        if candidate.exists():
            files.append(candidate)
    return files


def cmd_build_handoff(args: argparse.Namespace) -> int:
    check_workspace()
    page_slug = args.page.strip().lower().replace(" ", "_")
    if not page_slug:
        raise SystemExit("Provide a non-empty --page value.")

    sources = collect_implementation_files(page_slug)
    if not sources:
        raise SystemExit(
            f"No implementation source files found for page '{page_slug}' in PROJECTS/."
        )

    if args.output:
        target = normalize_rel_path(args.output)
    else:
        target = WORKSPACE / "PROJECTS" / "implementation_handoffs" / f"{page_slug}_implementation_handoff.md"

    if target.exists() and not args.force:
        raise SystemExit(
            f"File already exists: {target.relative_to(WORKSPACE)} (use --force to overwrite)."
        )

    lines: list[str] = [
        f"# {page_slug.replace('_', ' ').title()} Implementation Handoff",
        f"- Generated: {datetime.now(SAST).isoformat(timespec='seconds')}",
        f"- Page: `{page_slug}`",
        "",
        "## Source Files",
    ]
    for src in sources:
        lines.append(f"- `{src.relative_to(WORKSPACE).as_posix()}`")

    lines.extend(
        [
            "",
            "## Build Bundle",
            "- Use the sections below as the direct implementation source.",
            "- Keep structure and message intent intact unless a blocker requires adjustment.",
        ]
    )

    for src in sources:
        lines.extend(
            [
                "",
                f"### {src.relative_to(WORKSPACE).as_posix()}",
                "",
                read_text(src).rstrip(),
            ]
        )

    lines.extend(
        [
            "",
            "## Next Move",
            "- Implement the page from this handoff in one focused build pass.",
            "- Record what changed and what remains open in `HANDOFF.md`.",
        ]
    )

    ensure_parent(target)
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Created {target.relative_to(WORKSPACE)}")
    print(f"- Source files included: {len(sources)}")
    return 0


def cmd_call_model(args: argparse.Namespace) -> int:
    check_workspace()
    provider = args.provider.lower()
    provider_meta = PROVIDER_CONFIG[provider]
    api_key = get_secret(provider_meta["env"])
    if not api_key:
        raise SystemExit(f"Missing API key for {provider}. Expected {provider_meta['env']}.")

    messages = build_model_messages(args.prompt_name, args.prompt_text, args.input, args.file or [])
    payload = {
        "model": args.model or DEFAULT_PROVIDER_MODELS[provider],
        "messages": messages,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }
    req = urllib.request.Request(
        provider_meta["base"],
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"{provider} API error ({exc.code}): {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"{provider} request failed: {exc}") from exc

    content = data["choices"][0]["message"]["content"]
    print(content)
    return 0


def cmd_state_update(args: argparse.Namespace) -> int:
    check_workspace()
    state = load_state()

    if args.mode:
        state["mode"] = args.mode
    if args.primary_model:
        state.setdefault("operator", {})["primary_model"] = args.primary_model
    if args.secondary_model:
        state.setdefault("operator", {})["secondary_model"] = args.secondary_model
    if args.provider:
        state.setdefault("operator", {})["provider"] = args.provider
    if args.payload:
        state.setdefault("payload", {})["active"] = args.payload

    workflows = state.setdefault("workflows", {})
    if args.session_start_ready is not None:
        workflows["session_start_ready"] = args.session_start_ready
    if args.handoff_update_ready is not None:
        workflows["handoff_update_ready"] = args.handoff_update_ready
    if args.task_modes_ready is not None:
        workflows["task_modes_ready"] = args.task_modes_ready
    if args.prompt_library_wired is not None:
        workflows["prompt_library_wired"] = args.prompt_library_wired
    if args.direct_model_calls_ready is not None:
        workflows["direct_model_calls_ready"] = args.direct_model_calls_ready

    if args.blocker:
        state["major_blockers"] = list(args.blocker)

    write_state(state)
    print(f"Updated {(WORKSPACE / 'STATE' / 'state.json').relative_to(WORKSPACE)}")
    return 0


def cmd_session_close(args: argparse.Namespace) -> int:
    check_workspace()
    changed = iter_lines(args.changed or [])
    remains_open = iter_lines(args.open or [])
    next_move = iter_lines(args.next_move or [])
    blockers = iter_lines(args.blocker or [])

    if changed:
        if not next_move:
            raise SystemExit("Provide at least one --next-move item when using --changed.")
        if not blockers:
            blockers = ["See `BLOCKERS.md` for the live blocker register."]
        update_handoff(changed, remains_open, next_move, blockers)

    state = load_state()
    if args.mode:
        state["mode"] = args.mode
    if args.provider:
        state.setdefault("operator", {})["provider"] = args.provider
    if args.primary_model:
        state.setdefault("operator", {})["primary_model"] = args.primary_model
    if args.secondary_model:
        state.setdefault("operator", {})["secondary_model"] = args.secondary_model
    if args.payload:
        state.setdefault("payload", {})["active"] = args.payload
    if args.blocker:
        state["major_blockers"] = list(args.blocker)
    write_state(state)

    print("Session close complete")
    print(f"- HANDOFF updated: {'yes' if changed else 'no'}")
    print("- STATE updated: yes")
    return 0


def cmd_gate_policy(args: argparse.Namespace) -> int:
    check_workspace()
    policy = load_gate_policy()
    summary = summarize_gate_policy(policy)

    if args.json:
        print(json.dumps(policy, indent=2))
        return 0

    print("# ContinueWave Decision Gates\n")
    print(f"- Default decision: {str(policy.get('default_decision', 'ASK')).upper()}")
    print(f"- Default reason: {str(policy.get('default_reason', '')).strip()}")
    for decision in ("PROCEED", "ASK", "STOP"):
        print(f"\n## {decision}")
        for action_type in summary[decision]:
            print(f"- {action_type}")
    return 0


def cmd_gate_check(args: argparse.Namespace) -> int:
    check_workspace()
    policy = load_gate_policy()
    result = evaluate_gate(policy, args.action_type)

    next_move_map = {
        "PROCEED": "Continue without asking.",
        "ASK": "Pause and ask Franco before taking this action.",
        "STOP": "Do not continue. Escalate immediately.",
    }

    print("# ContinueWave Gate Check\n")
    print(f"- Action type: {args.action_type.strip().lower()}")
    if args.summary:
        print(f"- Summary: {args.summary.strip()}")
    print(f"- Decision: {result['decision']}")
    print(f"- Rule: {result['rule_id']}")
    print(f"- Reason: {result['reason']}")
    print(f"- Next move: {next_move_map.get(result['decision'], 'Pause and inspect the policy.')}")
    return 0


def cmd_atlasflow_smoke(args: argparse.Namespace) -> int:
    check_workspace()
    state = load_state()
    hosts = resolve_publish_hosts(state, args.host)
    if not hosts:
        raise SystemExit(f"No publish URL found for host selection: {args.host}")

    measurement_id = (
        state.get("status", {})
        .get("atlasflow_static_publish", {})
        .get("analytics", {})
        .get("measurement_id", "")
    )
    failures = 0

    print("# AtlasFlow Production Smoke\n")
    for host_name, base_url in hosts.items():
        base = base_url.rstrip("/") + "/"
        print(f"## {host_name}")

        for page in SMOKE_PAGES:
            page_url = urllib.parse.urljoin(base, page)
            try:
                status, body = fetch_url_text(page_url, args.timeout)
                has_config = "assets/site-config.js" in body
                has_runtime = "assets/site-runtime.js" in body
                if status == 200 and has_config and has_runtime:
                    print(f"- PASS page {page}: 200 + runtime/config markers")
                else:
                    failures += 1
                    print(f"- FAIL page {page}: status={status} config={has_config} runtime={has_runtime}")
            except (urllib.error.HTTPError, urllib.error.URLError) as exc:
                failures += 1
                print(f"- FAIL page {page}: {exc}")

        config_url = urllib.parse.urljoin(base, "assets/site-config.js")
        runtime_url = urllib.parse.urljoin(base, "assets/site-runtime.js")

        try:
            _, config_text = fetch_url_text(config_url, args.timeout)
            config_markers = [
                measurement_id,
                "contactEndpoint",
                "newsletterEndpoint",
                "strategyCallEndpoint",
            ]
            missing = [marker for marker in config_markers if marker and marker not in config_text]
            if missing:
                failures += 1
                print(f"- FAIL config asset: missing {', '.join(missing)}")
            else:
                print("- PASS config asset: measurement ID and form endpoints present")
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            failures += 1
            print(f"- FAIL config asset: {exc}")

        try:
            _, runtime_text = fetch_url_text(runtime_url, args.timeout)
            missing_runtime = [marker for marker in SMOKE_RUNTIME_MARKERS if marker not in runtime_text]
            if missing_runtime:
                failures += 1
                print(f"- FAIL runtime asset: missing {', '.join(missing_runtime)}")
            else:
                print("- PASS runtime asset: GA debug and event markers present")
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            failures += 1
            print(f"- FAIL runtime asset: {exc}")

        print("")

    if failures:
        print(f"Smoke result: FAIL ({failures} issue(s))")
        return 1

    print("Smoke result: PASS")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="continuewave_orchestrator",
        description="Minimal orchestrator for ContinueWave session starts and safe file creation.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Read control files and print a clean session start summary.")
    start_parser.set_defaults(func=cmd_start)

    create_parser = subparsers.add_parser("create-file", help="Create a new workspace file safely.")
    create_parser.add_argument("path", help="Workspace-relative path to create.")
    create_parser.add_argument("--title", help="Optional first-line title.")
    create_parser.add_argument(
        "--line",
        action="append",
        help="Add a content line. Can be passed multiple times.",
    )
    create_parser.add_argument(
        "--template",
        choices=["brief", "runbook"],
        help="Optional starter structure.",
    )
    create_parser.add_argument("--force", action="store_true", help="Allow overwriting an existing file.")
    create_parser.set_defaults(func=cmd_create_file)

    handoff_parser = subparsers.add_parser("handoff-update", help="Refresh key HANDOFF.md sections after a real session.")
    handoff_parser.add_argument(
        "--changed",
        action="append",
        help="One item for What Changed This Session. Can be passed multiple times.",
    )
    handoff_parser.add_argument(
        "--open",
        action="append",
        help="One item for What Remains Open. Can be passed multiple times.",
    )
    handoff_parser.add_argument(
        "--next-move",
        action="append",
        help="One line for Next Best Move. Can be passed multiple times.",
    )
    handoff_parser.add_argument(
        "--blocker",
        action="append",
        help="One active blocker line. Can be passed multiple times.",
    )
    handoff_parser.set_defaults(func=cmd_handoff_update)

    mode_parser = subparsers.add_parser("mode", help="Print the loading and behavior rules for a task mode.")
    mode_parser.add_argument("name", choices=sorted(TASK_MODES), help="Task mode to activate conceptually.")
    mode_parser.set_defaults(func=cmd_mode)

    prompt_parser = subparsers.add_parser("prompt", help="Print a stored prompt template from the on-disk prompt registry.")
    prompt_parser.add_argument("name", choices=["list", *PROMPT_FILES.keys()], help="Prompt name or 'list'.")
    prompt_parser.set_defaults(func=cmd_prompt)

    call_parser = subparsers.add_parser("call-model", help="Send a minimal direct prompt to Cerebras or Groq.")
    call_parser.add_argument("--provider", choices=sorted(PROVIDER_CONFIG.keys()), required=True, help="Provider to call directly.")
    call_parser.add_argument("--model", help="Optional explicit model override.")
    call_parser.add_argument("--prompt-name", choices=sorted(PROMPT_FILES.keys()), help="Stored prompt to prepend.")
    call_parser.add_argument("--prompt-text", help="Inline prompt text to prepend.")
    call_parser.add_argument("--input", help="Extra user input for the prompt.")
    call_parser.add_argument("--file", action="append", help="Workspace-relative file to include. Can be passed multiple times.")
    call_parser.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature.")
    call_parser.add_argument("--max-tokens", type=int, default=800, help="Max tokens for the response.")
    call_parser.add_argument("--timeout", type=int, default=60, help="Request timeout in seconds.")
    call_parser.set_defaults(func=cmd_call_model)

    prompt_build_parser = subparsers.add_parser("prompt-build", help="Assemble the exact prompt bundle without making a model call.")
    prompt_build_parser.add_argument("--prompt-name", choices=sorted(PROMPT_FILES.keys()), help="Stored prompt to prepend.")
    prompt_build_parser.add_argument("--prompt-text", help="Inline prompt text to prepend.")
    prompt_build_parser.add_argument("--input", help="Extra user input for the prompt.")
    prompt_build_parser.add_argument("--file", action="append", help="Workspace-relative file to include. Can be passed multiple times.")
    prompt_build_parser.set_defaults(func=cmd_prompt_build)

    build_handoff_parser = subparsers.add_parser(
        "build-handoff",
        help="Assemble a page implementation handoff from AtlasFlow project files.",
    )
    build_handoff_parser.add_argument(
        "--page",
        required=True,
        help="Page slug prefix in PROJECTS (example: homepage, compliance_report).",
    )
    build_handoff_parser.add_argument(
        "--output",
        help="Optional workspace-relative output path. Defaults to PROJECTS/implementation_handoffs/<page>_implementation_handoff.md",
    )
    build_handoff_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )
    build_handoff_parser.set_defaults(func=cmd_build_handoff)

    state_parser = subparsers.add_parser("state-update", help="Update a small approved subset of STATE/state.json.")
    state_parser.add_argument("--mode", help="Set the current operating mode.")
    state_parser.add_argument("--provider", help="Set the operator provider route.")
    state_parser.add_argument("--primary-model", help="Set the primary model.")
    state_parser.add_argument("--secondary-model", help="Set the secondary model.")
    state_parser.add_argument("--payload", help="Set the active payload.")
    state_parser.add_argument("--blocker", action="append", help="Set one major blocker. Can be passed multiple times.")
    state_parser.add_argument("--session-start-ready", dest="session_start_ready", action=argparse.BooleanOptionalAction, default=None)
    state_parser.add_argument("--handoff-update-ready", dest="handoff_update_ready", action=argparse.BooleanOptionalAction, default=None)
    state_parser.add_argument("--task-modes-ready", dest="task_modes_ready", action=argparse.BooleanOptionalAction, default=None)
    state_parser.add_argument("--prompt-library-wired", dest="prompt_library_wired", action=argparse.BooleanOptionalAction, default=None)
    state_parser.add_argument("--direct-model-calls-ready", dest="direct_model_calls_ready", action=argparse.BooleanOptionalAction, default=None)
    state_parser.set_defaults(func=cmd_state_update)

    close_parser = subparsers.add_parser("session-close", help="Update HANDOFF.md and STATE/state.json together at session end.")
    close_parser.add_argument("--changed", action="append", help="One item for What Changed This Session. Can be passed multiple times.")
    close_parser.add_argument("--open", action="append", help="One item for What Remains Open. Can be passed multiple times.")
    close_parser.add_argument("--next-move", action="append", help="One line for Next Best Move. Can be passed multiple times.")
    close_parser.add_argument("--blocker", action="append", help="One active blocker line. Can be passed multiple times.")
    close_parser.add_argument("--mode", help="Set the current operating mode.")
    close_parser.add_argument("--provider", help="Set the operator provider route.")
    close_parser.add_argument("--primary-model", help="Set the primary model.")
    close_parser.add_argument("--secondary-model", help="Set the secondary model.")
    close_parser.add_argument("--payload", help="Set the active payload.")
    close_parser.set_defaults(func=cmd_session_close)

    sync_blockers_parser = subparsers.add_parser(
        "sync-blockers",
        help="Sync active blockers from BLOCKERS.md into HANDOFF.md and STATE/state.json.",
    )
    sync_blockers_parser.set_defaults(func=cmd_sync_blockers)

    gate_policy_parser = subparsers.add_parser(
        "gate-policy",
        help="Print the current decision-gate policy.",
    )
    gate_policy_parser.add_argument("--json", action="store_true", help="Print the raw JSON policy.")
    gate_policy_parser.set_defaults(func=cmd_gate_policy)

    gate_check_parser = subparsers.add_parser(
        "gate-check",
        help="Classify an action as PROCEED, ASK, or STOP using the decision-gate policy.",
    )
    gate_check_parser.add_argument("action_type", help="Action type to evaluate.")
    gate_check_parser.add_argument("--summary", help="Optional short description of the proposed action.")
    gate_check_parser.set_defaults(func=cmd_gate_check)

    smoke_parser = subparsers.add_parser(
        "atlasflow-smoke",
        help="Fetch live AtlasFlow hosts and verify core page/runtime markers.",
    )
    smoke_parser.add_argument(
        "--host",
        choices=["all", "vercel", "netlify", "github_pages"],
        default="all",
        help="Host to verify. Defaults to all live hosts in STATE/state.json.",
    )
    smoke_parser.add_argument("--timeout", type=int, default=20, help="Request timeout in seconds.")
    smoke_parser.set_defaults(func=cmd_atlasflow_smoke)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

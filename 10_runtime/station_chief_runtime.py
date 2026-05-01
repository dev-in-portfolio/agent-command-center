#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

STATION_CHIEF_RUNTIME_VERSION = "0.1.0"

EXPECTED_OVERLAYS = [
    {
        "id": "family_007_devinized_engineering_overload",
        "name": "Family 7 Devinized Engineering Overload Pack",
        "json_path": "04_workflow_templates/family_007_devinized_engineering_overload_pack.json",
        "report_path": "09_exports/family_007_devinized_engineering_overload_report.md",
        "validator_path": "scripts/validate_family_007_devinized_engineering_overload_pack.py",
    },
    {
        "id": "devinization_pack_001_command_brain",
        "name": "Devinization Pack 1 — Command Brain / Devin Operating System",
        "json_path": "04_workflow_templates/devinization_pack_001_command_brain.json",
        "report_path": "09_exports/devinization_pack_001_command_brain_report.md",
        "validator_path": "scripts/validate_devinization_pack_001_command_brain.py",
    },
    {
        "id": "devinization_pack_002_runtime_routing_work_control",
        "name": "Devinization Pack 2 — Runtime Routing & Work Control",
        "json_path": "04_workflow_templates/devinization_pack_002_runtime_routing_work_control.json",
        "report_path": "09_exports/devinization_pack_002_runtime_routing_work_control_report.md",
        "validator_path": "scripts/validate_devinization_pack_002_runtime_routing_work_control.py",
    },
    {
        "id": "devinization_pack_003_prompt_memory_context_architecture",
        "name": "Devinization Pack 3 — Prompt, Memory & Context Architecture",
        "json_path": "04_workflow_templates/devinization_pack_003_prompt_memory_context_architecture.json",
        "report_path": "09_exports/devinization_pack_003_prompt_memory_context_architecture_report.md",
        "validator_path": "scripts/validate_devinization_pack_003_prompt_memory_context_architecture.py",
    },
    {
        "id": "devinization_pack_004_execution_safety_tools_recovery",
        "name": "Devinization Pack 4 — Execution Safety, Tools & Recovery",
        "json_path": "04_workflow_templates/devinization_pack_004_execution_safety_tools_recovery.json",
        "report_path": "09_exports/devinization_pack_004_execution_safety_tools_recovery_report.md",
        "validator_path": "scripts/validate_devinization_pack_004_execution_safety_tools_recovery.py",
    },
    {
        "id": "devinization_pack_005_quality_standards_human_review",
        "name": "Devinization Pack 5 — Quality, Standards & Human Review",
        "json_path": "04_workflow_templates/devinization_pack_005_quality_standards_human_review.json",
        "report_path": "09_exports/devinization_pack_005_quality_standards_human_review_report.md",
        "validator_path": "scripts/validate_devinization_pack_005_quality_standards_human_review.py",
    },
    {
        "id": "devinization_pack_006_output_assembly_delivery_intelligence",
        "name": "Devinization Pack 6 — Output Assembly & Delivery Intelligence",
        "json_path": "04_workflow_templates/devinization_pack_006_output_assembly_delivery_intelligence.json",
        "report_path": "09_exports/devinization_pack_006_output_assembly_delivery_intelligence_report.md",
        "validator_path": "scripts/validate_devinization_pack_006_output_assembly_delivery_intelligence.py",
    },
    {
        "id": "devinization_pack_007_agent_governance_identity_accountability",
        "name": "Devinization Pack 7 — Agent Governance, Identity & Accountability",
        "json_path": "04_workflow_templates/devinization_pack_007_agent_governance_identity_accountability.json",
        "report_path": "09_exports/devinization_pack_007_agent_governance_identity_accountability_report.md",
        "validator_path": "scripts/validate_devinization_pack_007_agent_governance_identity_accountability.py",
    },
]

COMMAND_CLASSES = {
    "verification": "verification",
    "remember_only": "remember_only",
    "strict_execution": "strict_execution",
    "speed_racer": "speed_racer",
    "build": "build",
    "route": "route",
    "repair": "repair",
    "governance": "governance",
    "final_output": "final_output",
    "unknown": "unknown",
}

ACTIVATION_TIERS = {
    "verification": {"tier": 4, "name": "Tier 4 — Audit / Archive", "reason": "Verification commands should audit, archive, and prove results."},
    "remember_only": {"tier": 0, "name": "Tier 0 — Passive Whole-Org Awareness", "reason": "Memory-only commands should not wake execution crews."},
    "strict_execution": {"tier": 2, "name": "Tier 2 — Command Brief", "reason": "Strict execution requires a scoped command brief before action."},
    "speed_racer": {"tier": 3, "name": "Tier 3 — Active Operation", "reason": "Speed mode still performs active operation with controls."},
    "build": {"tier": 3, "name": "Tier 3 — Active Operation", "reason": "Build commands activate execution crews for actual work."},
    "route": {"tier": 1, "name": "Tier 1 — Council Scan", "reason": "Routing commands identify relevant families before execution."},
    "repair": {"tier": 3, "name": "Tier 3 — Active Operation", "reason": "Repair commands require active minimal targeted work."},
    "governance": {"tier": 2, "name": "Tier 2 — Command Brief", "reason": "Governance commands need a scoped brief and policy review."},
    "final_output": {"tier": 4, "name": "Tier 4 — Audit / Archive", "reason": "Final-output commands should produce proof-backed artifacts."},
    "unknown": {"tier": 1, "name": "Tier 1 — Council Scan", "reason": "Unknown commands begin with a council scan."},
}

OVERLAY_SELECTIONS = {
    "verification": [
        "devinization_pack_004_execution_safety_tools_recovery",
        "devinization_pack_005_quality_standards_human_review",
        "devinization_pack_006_output_assembly_delivery_intelligence",
    ],
    "remember_only": [
        "devinization_pack_003_prompt_memory_context_architecture",
        "devinization_pack_006_output_assembly_delivery_intelligence",
    ],
    "strict_execution": [
        "devinization_pack_001_command_brain",
        "devinization_pack_004_execution_safety_tools_recovery",
        "devinization_pack_005_quality_standards_human_review",
    ],
    "speed_racer": [
        "family_007_devinized_engineering_overload",
        "devinization_pack_001_command_brain",
        "devinization_pack_002_runtime_routing_work_control",
        "devinization_pack_004_execution_safety_tools_recovery",
        "devinization_pack_006_output_assembly_delivery_intelligence",
    ],
    "build": [
        "family_007_devinized_engineering_overload",
        "devinization_pack_001_command_brain",
        "devinization_pack_002_runtime_routing_work_control",
        "devinization_pack_003_prompt_memory_context_architecture",
        "devinization_pack_004_execution_safety_tools_recovery",
        "devinization_pack_005_quality_standards_human_review",
        "devinization_pack_006_output_assembly_delivery_intelligence",
    ],
    "route": [
        "devinization_pack_001_command_brain",
        "devinization_pack_002_runtime_routing_work_control",
    ],
    "repair": [
        "devinization_pack_004_execution_safety_tools_recovery",
        "devinization_pack_005_quality_standards_human_review",
        "devinization_pack_006_output_assembly_delivery_intelligence",
        "devinization_pack_007_agent_governance_identity_accountability",
    ],
    "governance": [
        "devinization_pack_007_agent_governance_identity_accountability",
        "devinization_pack_005_quality_standards_human_review",
        "devinization_pack_004_execution_safety_tools_recovery",
    ],
    "final_output": [
        "devinization_pack_006_output_assembly_delivery_intelligence",
        "devinization_pack_005_quality_standards_human_review",
        "devinization_pack_004_execution_safety_tools_recovery",
    ],
    "unknown": [
        "devinization_pack_001_command_brain",
        "devinization_pack_002_runtime_routing_work_control",
    ],
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: str | Path) -> Any:
    full_path = repo_root() / Path(path)
    return json.loads(full_path.read_text())


def load_overlay_stack() -> list[dict[str, Any]]:
    overlays: list[dict[str, Any]] = []
    for overlay in EXPECTED_OVERLAYS:
        json_path = repo_root() / overlay["json_path"]
        report_path = repo_root() / overlay["report_path"]
        validator_path = repo_root() / overlay["validator_path"]
        exists = json_path.exists() and report_path.exists() and validator_path.exists()
        mode = None
        preserves_locked_baseline = None
        crew_count = None
        ownership_project_owner = None
        ownership_phrase = None
        if json_path.exists():
            data = json.loads(json_path.read_text())
            mode = data.get("mode")
            preserves_locked_baseline = data.get("preserves_locked_baseline")
            crew_count = len(data.get("crews", []))
            ownership = data.get("ownership_metadata", {})
            ownership_project_owner = ownership.get("project_owner")
            ownership_phrase = ownership.get("ownership_phrase")
        overlays.append({
            "id": overlay["id"],
            "name": overlay["name"],
            "json_path": overlay["json_path"],
            "report_path": overlay["report_path"],
            "validator_path": overlay["validator_path"],
            "exists": exists,
            "mode": mode,
            "preserves_locked_baseline": preserves_locked_baseline,
            "crew_count": crew_count,
            "ownership_project_owner": ownership_project_owner,
            "ownership_phrase": ownership_phrase,
        })
    return overlays


def classify_command(command: str) -> str:
    text = command.lower()
    if "check please" in text or "verify" in text or "did it pass" in text:
        return COMMAND_CLASSES["verification"]
    if "blueberry pancakes" in text or "remember this" in text or "lock this" in text:
        return COMMAND_CLASSES["remember_only"]
    if "square block square hole" in text or "strict execution" in text:
        return COMMAND_CLASSES["strict_execution"]
    if "speed racer" in text or "fast mode" in text:
        return COMMAND_CLASSES["speed_racer"]
    if "build" in text or "create" in text or "runtime skeleton" in text:
        return COMMAND_CLASSES["build"]
    if "route" in text or "which department" in text or "station chief" in text:
        return COMMAND_CLASSES["route"]
    if "repair" in text or "rollback" in text or "fix only" in text:
        return COMMAND_CLASSES["repair"]
    if "agent court" in text or "governance" in text or "accountability" in text:
        return COMMAND_CLASSES["governance"]
    if "final answer" in text or "output" in text or "release notes" in text:
        return COMMAND_CLASSES["final_output"]
    return COMMAND_CLASSES["unknown"]


def determine_activation_tier(command_type: str) -> dict[str, Any]:
    return ACTIVATION_TIERS[command_type]


def select_overlays(command_type: str) -> list[str]:
    return OVERLAY_SELECTIONS[command_type]


def create_command_brief(command: str) -> dict[str, Any]:
    command_type = classify_command(command)
    activation_tier = determine_activation_tier(command_type)
    selected = select_overlays(command_type)
    objective_map = {
        "verification": "Verify the requested state and report proof.",
        "remember_only": "Record and preserve context without executing work.",
        "strict_execution": "Generate a command brief that obeys strict execution rules.",
        "speed_racer": "Run the active operation with speed controls and proof.",
        "build": "Build the requested runtime skeleton or feature scaffold.",
        "route": "Identify the relevant families and routing path.",
        "repair": "Perform minimal targeted repair with validation.",
        "governance": "Apply governance review and accountability controls.",
        "final_output": "Assemble proof-backed final output.",
        "unknown": "Scan the agency and identify the best route.",
    }
    return {
        "command": command,
        "command_type": command_type,
        "activation_tier": activation_tier,
        "selected_overlays": selected,
        "objective": objective_map[command_type],
        "allowed_actions": [
            "load overlays",
            "classify command",
            "generate command brief",
            "generate work orders",
            "return deterministic demo output",
        ],
        "forbidden_actions": [
            "modify 02_departments baseline files",
            "regenerate baseline exports",
            "connect live APIs",
            "animate all 47,250 worker agents",
            "mutate locked family architecture",
            "skip validators",
            "claim completion without proof",
        ],
        "required_outputs": [
            "command brief",
            "work orders",
            "proof-backed result",
        ],
        "validation_requirements": [
            "baseline preserved",
            "overlays loaded",
            "demo deterministic",
            "validators required before completion",
        ],
        "deterministic_demo_mode": True,
        "baseline_protection": True,
        "external_actions_allowed": False,
        "workforce_animation_allowed": False,
    }


def create_work_orders(command_brief: dict[str, Any]) -> list[dict[str, Any]]:
    work_orders = []
    selected = command_brief["selected_overlays"]
    for idx, overlay_id in enumerate(selected, start=1):
        work_orders.append({
            "work_order_id": f"WO-{idx:02d}",
            "overlay_id": overlay_id,
            "purpose": f"Support {command_brief['command_type']} handling for {overlay_id}.",
            "task": f"Apply overlay guidance for {command_brief['command']}.",
            "expected_output": f"Scoped output for {overlay_id}.",
            "status": "generated",
        })
    return work_orders


def run_station_chief(command: str) -> dict[str, Any]:
    brief = create_command_brief(command)
    work_orders = create_work_orders(brief)
    overlays = load_overlay_stack()
    return {
        "station_chief_runtime_version": STATION_CHIEF_RUNTIME_VERSION,
        "runtime_status": "deterministic_demo_ready",
        "command": command,
        "command_type": brief["command_type"],
        "activation_tier": brief["activation_tier"],
        "overlay_stack_loaded": all(item["exists"] for item in overlays),
        "overlay_stack_summary": overlays,
        "selected_overlays": brief["selected_overlays"],
        "command_brief": brief,
        "work_orders": work_orders,
        "evidence": {
            "baseline_preserved": True,
            "external_actions_taken": False,
            "live_worker_agents_activated": False,
            "deterministic_demo_mode": True,
            "validators_required_before_completion": True,
        },
        "next_step": "Next step: expand the Station Chief runtime skeleton with persistent run logs, command brief files, and deterministic demo fixtures.",
    }


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Station Chief Runtime Skeleton")
    parser.add_argument("--demo", action="store_true", help="Run the deterministic demo command")
    parser.add_argument("--command", type=str, help="Run a specific command")
    parser.add_argument("--json", action="store_true", help="Print full Station Chief result as JSON")
    parser.add_argument("--brief", action="store_true", help="Print the command brief as JSON")
    parser.add_argument("--list-overlays", action="store_true", help="Print overlay stack summary as JSON")
    parser.add_argument("--write-output", type=str, help="Write full result JSON to a file path")
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    if args.demo:
        command = "check please"
    elif args.command:
        command = args.command
    elif args.list_overlays:
        command = None
    else:
        command = "check please"

    if args.list_overlays:
        print(json.dumps(load_overlay_stack(), indent=2, ensure_ascii=False))
        return

    result = run_station_chief(command)
    output: Any = result
    if args.brief:
        output = result["command_brief"]
    elif args.json or args.demo or args.command or args.write_output:
        output = result

    if args.write_output:
        Path(args.write_output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

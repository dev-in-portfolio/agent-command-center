#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from station_chief_adapters import (
    classify_path_safety,
    create_execution_plan,
    create_file_operation_plan,
    evaluate_execution_gate,
    list_adapters,
    run_noop_adapter,
    run_sandbox_file_write_adapter,
)

STATION_CHIEF_RUNTIME_VERSION = "0.4.0"

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
        overlays.append(
            {
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
            }
        )
    return overlays


def normalize_command_for_id(command: str) -> str:
    normalized = command.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    return normalized or "empty-command"


def generate_run_id(command: str, run_label: str = "station-chief-runtime") -> str:
    normalized = normalize_command_for_id(command)
    digest = hashlib.sha256(f"{STATION_CHIEF_RUNTIME_VERSION}|{run_label}|{command}".encode("utf-8")).hexdigest()
    return f"station-chief-v0-4-{normalized}-{digest[:12]}"


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
            "connect external services",
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
        work_orders.append(
            {
                "work_order_id": f"WO-{idx:02d}",
                "overlay_id": overlay_id,
                "purpose": f"Support {command_brief['command_type']} handling for {overlay_id}.",
                "task": f"Apply overlay guidance for {command_brief['command']}.",
                "expected_output": f"Scoped output for {overlay_id}.",
                "status": "generated",
            }
        )
    return work_orders


def load_registry(registry_dir: str | Path) -> dict:
    registry_path = Path(registry_dir) / "run_registry.json"
    if not registry_path.exists():
        return {
            "registry_version": "0.4.0",
            "runtime_name": "Station Chief Runtime",
            "runs": [],
        }
    return json.loads(registry_path.read_text())


def save_registry(registry_dir: str | Path, registry: dict) -> None:
    registry_path = Path(registry_dir)
    registry_path.mkdir(parents=True, exist_ok=True)
    (registry_path / "run_registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n")


def update_registry(registry_dir: str | Path, index_entry: dict) -> dict:
    registry = load_registry(registry_dir)
    runs = [run for run in registry.get("runs", []) if run.get("run_id") != index_entry.get("run_id")]
    runs.append(index_entry)
    registry["registry_version"] = "0.4.0"
    registry["runtime_name"] = "Station Chief Runtime"
    registry["runs"] = runs
    save_registry(registry_dir, registry)
    return registry


def write_runtime_index(registry_dir: str | Path, registry: dict) -> dict:
    index = {
        "index_version": "0.4.0",
        "runtime_name": "Station Chief Runtime",
        "run_count": len(registry.get("runs", [])),
        "runs": registry.get("runs", []),
    }
    registry_path = Path(registry_dir)
    registry_path.mkdir(parents=True, exist_ok=True)
    (registry_path / "runtime_index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    return index


def resume_run(registry_dir: str | Path, run_id: str) -> dict:
    registry = load_registry(registry_dir)
    for run_entry in registry.get("runs", []):
        if run_entry.get("run_id") == run_id:
            return {
                "resume_status": "FOUND",
                "run_id": run_id,
                "registry_dir": str(registry_dir),
                "run_entry": run_entry,
            }
    return {
        "resume_status": "NOT_FOUND",
        "run_id": run_id,
        "registry_dir": str(registry_dir),
        "run_entry": None,
    }


def build_runtime_index_entry(result: dict, run_id: str, artifact_dir: str | None = None) -> dict:
    return {
        "run_id": run_id,
        "runtime_version": STATION_CHIEF_RUNTIME_VERSION,
        "command": result["command"],
        "command_type": result["command_type"],
        "activation_tier": result["activation_tier"]["name"],
        "selected_overlays": result["selected_overlays"],
        "artifact_dir": artifact_dir,
        "baseline_preserved": True,
        "external_actions_taken": False,
        "live_worker_agents_activated": False,
        "deterministic_demo_mode": True,
        "runtime_status": result["runtime_status"],
    }


def run_station_chief(command: str, adapter_name: str = "noop") -> dict[str, Any]:
    brief = create_command_brief(command)
    work_orders = create_work_orders(brief)
    overlays = load_overlay_stack()
    execution_plan = create_execution_plan(brief, work_orders, adapter_name=adapter_name)
    adapter_result = run_noop_adapter(execution_plan)
    return {
        "station_chief_runtime_version": STATION_CHIEF_RUNTIME_VERSION,
        "runtime_status": "deterministic_demo_ready",
        "run_capabilities": {
            "persistent_run_logs": True,
            "command_brief_artifacts": True,
            "work_order_artifacts": True,
            "deterministic_fixture_tests": True,
            "selected_overlay_artifacts": True,
            "evidence_artifacts": True,
            "persistent_runtime_index": True,
            "resumable_run_registry": True,
            "controlled_execution_adapters": True,
            "noop_execution_adapter": True,
            "controlled_file_operation_adapter": True,
            "human_confirmed_execution_gates": True,
            "sandbox_file_write_adapter": True,
        },
        "command": command,
        "command_type": brief["command_type"],
        "activation_tier": brief["activation_tier"],
        "overlay_stack_loaded": all(item["exists"] for item in overlays),
        "overlay_stack_summary": overlays,
        "selected_overlays": brief["selected_overlays"],
        "command_brief": brief,
        "work_orders": work_orders,
        "adapter_name": adapter_name,
        "execution_plan": execution_plan,
        "adapter_result": adapter_result,
        "file_operation_plan": None,
        "execution_gate": None,
        "file_operation_result": None,
        "evidence": {
            "baseline_preserved": True,
            "external_actions_taken": False,
            "live_worker_agents_activated": False,
            "deterministic_demo_mode": True,
            "validators_required_before_completion": True,
            "controlled_file_write_requires_confirmation": True,
        },
        "next_step": "Next step: add human-approved repo patch adapters with changed-file scope enforcement.",
    }


def build_runtime_artifacts(result: dict, run_id: str) -> dict:
    adapter_name = result.get("adapter_name", "noop")
    command_brief = result["command_brief"]
    work_orders = result["work_orders"]
    execution_plan = result.get("execution_plan") or create_execution_plan(command_brief, work_orders, adapter_name=adapter_name)
    adapter_result = result.get("adapter_result") or run_noop_adapter(execution_plan)
    file_operation_plan = result.get("file_operation_plan")
    execution_gate = result.get("execution_gate")
    file_operation_result = result.get("file_operation_result")
    selected_records = [
        item
        for item in result["overlay_stack_summary"]
        if item["id"] in result["selected_overlays"]
    ]
    runtime_index_entry = build_runtime_index_entry(result, run_id, artifact_dir=None)
    return {
        "run_log": {
            "run_id": run_id,
            "runtime_version": result["station_chief_runtime_version"],
            "command": result["command"],
            "command_type": result["command_type"],
            "activation_tier": result["activation_tier"],
            "runtime_status": result["runtime_status"],
            "overlay_stack_loaded": result["overlay_stack_loaded"],
            "deterministic_demo_mode": result["evidence"]["deterministic_demo_mode"],
            "baseline_preserved": result["evidence"]["baseline_preserved"],
            "external_actions_taken": result["evidence"]["external_actions_taken"],
            "live_worker_agents_activated": result["evidence"]["live_worker_agents_activated"],
            "validators_required_before_completion": result["evidence"]["validators_required_before_completion"],
            "next_step": result["next_step"],
        },
        "command_brief": command_brief,
        "work_orders": work_orders,
        "selected_overlays": {
            "selected_overlay_ids": result["selected_overlays"],
            "selected_overlay_records": selected_records,
        },
        "evidence": result["evidence"],
        "execution_plan": execution_plan,
        "adapter_result": adapter_result,
        "file_operation_plan": file_operation_plan,
        "execution_gate": execution_gate,
        "file_operation_result": file_operation_result,
        "runtime_index_entry": runtime_index_entry,
        "manifest": {
            "run_id": run_id,
            "runtime_version": result["station_chief_runtime_version"],
            "artifact_type": "station_chief_runtime_v0_4_artifacts",
            "files_planned": [
                "run_log.json",
                "command_brief.json",
                "work_orders.json",
                "selected_overlays.json",
                "evidence.json",
                "execution_plan.json",
                "adapter_result.json",
                "file_operation_plan.json",
                "execution_gate.json",
                "file_operation_result.json",
                "runtime_index_entry.json",
                "manifest.json",
                "full_result.json",
            ],
            "baseline_preserved": True,
            "external_actions_taken": False,
            "live_worker_agents_activated": False,
            "deterministic_demo_mode": True,
            "controlled_execution_adapter": "noop",
            "controlled_file_operations_supported": True,
            "human_confirmation_required_for_file_write": True,
        },
    }


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def write_runtime_artifacts(
    result: dict,
    output_dir: str | Path,
    run_label: str = "station-chief-runtime",
    registry_dir: str | Path | None = None,
) -> dict:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    run_id = generate_run_id(result["command"], run_label=run_label)
    artifact_dir = output_path / run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)

    artifacts = build_runtime_artifacts(result, run_id)
    artifacts["runtime_index_entry"] = build_runtime_index_entry(result, run_id, artifact_dir=str(artifact_dir))

    files_written = []
    mapping = {
        "run_log.json": artifacts["run_log"],
        "command_brief.json": artifacts["command_brief"],
        "work_orders.json": artifacts["work_orders"],
        "selected_overlays.json": artifacts["selected_overlays"],
        "evidence.json": artifacts["evidence"],
        "execution_plan.json": artifacts["execution_plan"],
        "adapter_result.json": artifacts["adapter_result"],
        "file_operation_plan.json": artifacts["file_operation_plan"],
        "execution_gate.json": artifacts["execution_gate"],
        "file_operation_result.json": artifacts["file_operation_result"],
        "runtime_index_entry.json": artifacts["runtime_index_entry"],
        "manifest.json": artifacts["manifest"],
        "full_result.json": result,
    }
    for filename, payload in mapping.items():
        _write_json(artifact_dir / filename, payload)
        files_written.append(filename)

    registry_updated = False
    registry_dir_str = None
    if registry_dir is not None:
        registry_dir_path = Path(registry_dir)
        registry_dir_path.mkdir(parents=True, exist_ok=True)
        registry = update_registry(registry_dir_path, artifacts["runtime_index_entry"])
        write_runtime_index(registry_dir_path, registry)
        registry_updated = True
        registry_dir_str = str(registry_dir_path)

    return {
        "run_id": run_id,
        "artifact_dir": str(artifact_dir),
        "files_written": files_written,
        "registry_updated": registry_updated,
        "registry_dir": registry_dir_str,
    }


def run_fixture_tests() -> dict:
    cases = load_json("10_runtime/station_chief_demo_cases.json")["demo_cases"]
    results = []
    passed = 0
    failed = 0
    for case in cases:
        result = run_station_chief(case["command"])
        actual_command_type = result["command_type"]
        actual_activation_tier = result["activation_tier"]["name"]
        case_passed = (
            actual_command_type == case["expected_command_type"]
            and actual_activation_tier == case["expected_activation_tier"]
        )
        if case_passed:
            passed += 1
        else:
            failed += 1
        results.append(
            {
                "case_id": case["case_id"],
                "command": case["command"],
                "expected_command_type": case["expected_command_type"],
                "actual_command_type": actual_command_type,
                "expected_activation_tier": case["expected_activation_tier"],
                "actual_activation_tier": actual_activation_tier,
                "passed": case_passed,
            }
        )
    return {
        "fixture_test_status": "PASS" if failed == 0 else "FAIL",
        "runtime_version": STATION_CHIEF_RUNTIME_VERSION,
        "case_count": len(cases),
        "passed": passed,
        "failed": failed,
        "results": results,
    }


def attach_file_operation(
    result: dict,
    execution_dir: str | None,
    target_filename: str,
    confirmation_token: str | None,
    execute: bool,
) -> dict:
    updated = dict(result)
    file_operation_plan = create_file_operation_plan(
        result["command_brief"],
        execution_dir=execution_dir,
        target_filename=target_filename,
    )
    execution_gate = evaluate_execution_gate(file_operation_plan, confirmation_token if execute else None)
    if execute:
        file_operation_result = run_sandbox_file_write_adapter(file_operation_plan, execution_gate)
    else:
        file_operation_result = {
            "adapter_result_status": "PLANNED_ONLY",
            "operation_type": "sandbox_file_write",
            "file_written": False,
            "target_path": file_operation_plan["target_path"],
            "live_execution_performed": False,
            "external_actions_taken": False,
            "worker_agents_activated": False,
            "reason": "File operation planned but not executed.",
        }
    updated["file_operation_plan"] = file_operation_plan
    updated["execution_gate"] = execution_gate
    updated["file_operation_result"] = file_operation_result
    return updated


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Station Chief Runtime Skeleton")
    parser.add_argument("--demo", action="store_true", help="Run the deterministic demo command")
    parser.add_argument("--command", type=str, help="Run a specific command")
    parser.add_argument("--json", action="store_true", help="Print full Station Chief result as JSON")
    parser.add_argument("--brief", action="store_true", help="Print the command brief as JSON")
    parser.add_argument("--list-overlays", action="store_true", help="Print overlay stack summary as JSON")
    parser.add_argument("--list-adapters", action="store_true", help="Print adapter catalog as JSON")
    parser.add_argument("--write-output", type=str, help="Write full result JSON to a file path")
    parser.add_argument("--write-artifacts", type=str, help="Write runtime artifacts into the provided directory")
    parser.add_argument("--run-label", type=str, default="station-chief-runtime", help="Label included in artifact run IDs")
    parser.add_argument("--fixture-test", action="store_true", help="Run deterministic fixture tests")
    parser.add_argument("--adapter", type=str, default="noop", help="Choose the controlled execution adapter")
    parser.add_argument("--simulate-adapter", action="store_true", help="Simulate the selected controlled execution adapter")
    parser.add_argument("--registry-dir", type=str, help="Directory used for the persistent run registry")
    parser.add_argument("--resume-run-id", type=str, help="Resume a previously recorded run by run ID")
    parser.add_argument("--plan-file-operation", action="store_true", help="Plan a sandbox file operation without executing it")
    parser.add_argument("--execution-dir", type=str, help="Directory used for sandbox file-operation execution")
    parser.add_argument("--target-filename", type=str, default="station_chief_sandbox_output.txt", help="Target filename for sandbox file operations")
    parser.add_argument("--confirm-execution", type=str, help="Confirmation token required for sandbox file writes")
    parser.add_argument("--execute-sandbox-file-write", action="store_true", help="Execute a sandbox file write if the gate approves")
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    if args.fixture_test:
        print(json.dumps(run_fixture_tests(), indent=2, ensure_ascii=False))
        return

    if args.list_adapters:
        print(json.dumps(list_adapters(), indent=2, ensure_ascii=False))
        return

    if args.resume_run_id:
        if not args.registry_dir:
            print(json.dumps({"resume_status": "ERROR", "error": "--resume-run-id requires --registry-dir"}, indent=2, ensure_ascii=False))
            return
        print(json.dumps(resume_run(args.registry_dir, args.resume_run_id), indent=2, ensure_ascii=False))
        return

    if args.demo:
        command = "check please"
    elif args.command:
        command = args.command
    else:
        command = "check please"

    if args.list_overlays:
        print(json.dumps(load_overlay_stack(), indent=2, ensure_ascii=False))
        return

    if args.execute_sandbox_file_write and not args.execution_dir:
        print(json.dumps({"execution_status": "ERROR", "error": "--execute-sandbox-file-write requires --execution-dir"}, indent=2, ensure_ascii=False))
        return

    result = run_station_chief(command, adapter_name=args.adapter)

    if args.plan_file_operation or args.execute_sandbox_file_write:
        result = attach_file_operation(
            result,
            args.execution_dir,
            args.target_filename,
            args.confirm_execution,
            execute=args.execute_sandbox_file_write,
        )

    artifact_summary = None
    if args.write_artifacts:
        artifact_summary = write_runtime_artifacts(
            dict(result),
            args.write_artifacts,
            run_label=args.run_label,
            registry_dir=args.registry_dir,
        )
        result = dict(result)
        result["artifact_write_summary"] = artifact_summary

    if args.write_output:
        Path(args.write_output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")

    if args.brief and not (args.plan_file_operation or args.execute_sandbox_file_write):
        output: Any = result["command_brief"]
        if artifact_summary is not None:
            output = {
                "command_brief": result["command_brief"],
                "artifact_write_summary": artifact_summary,
            }
    else:
        output = result

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

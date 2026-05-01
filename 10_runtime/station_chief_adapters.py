#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any

ADAPTER_MODULE_VERSION = "0.4.0"

YES_I_APPROVE_SANDBOX_FILE_WRITE = "YES_I_APPROVE_SANDBOX_FILE_WRITE"
SAFE_SANDBOX_PATH = "SAFE_SANDBOX_PATH"
BLOCKED_FORBIDDEN_PATH = "BLOCKED_FORBIDDEN_PATH"
BLOCKED_OUTSIDE_EXECUTION_DIR = "BLOCKED_OUTSIDE_EXECUTION_DIR"

SUPPORTED_ADAPTERS = {
    "noop": {
        "name": "No-Op Controlled Execution Adapter",
        "live_execution": False,
        "external_actions": False,
        "worker_animation": False,
        "description": "Safely simulates execution boundaries without performing live work.",
    },
    "sandbox_file_write": {
        "name": "Human-Confirmed Sandbox File Write Adapter",
        "live_execution": False,
        "external_actions": False,
        "worker_animation": False,
        "requires_human_confirmation": True,
        "sandbox_only": True,
        "description": "Writes only approved sandbox files inside a provided execution directory after explicit confirmation.",
    },
}


def list_adapters() -> dict:
    return {
        "adapter_module_version": ADAPTER_MODULE_VERSION,
        "supported_adapters": SUPPORTED_ADAPTERS,
    }


def create_execution_plan(command_brief: dict, work_orders: list[dict], adapter_name: str = "noop") -> dict:
    adapter = SUPPORTED_ADAPTERS.get(adapter_name)
    adapter_available = adapter is not None
    if not adapter_available:
        return {
            "adapter_name": adapter_name,
            "adapter_available": False,
            "execution_mode": "unsupported_adapter",
            "live_execution": False,
            "external_actions": False,
            "worker_animation": False,
            "command_type": command_brief["command_type"],
            "activation_tier": command_brief["activation_tier"],
            "work_order_count": len(work_orders),
            "planned_steps": [],
        }

    planned_steps = []
    for idx, work_order in enumerate(work_orders, start=1):
        planned_steps.append(
            {
                "step_id": f"STEP-{idx:02d}",
                "work_order_id": work_order["work_order_id"],
                "overlay_id": work_order["overlay_id"],
                "action": "simulate_noop_execution_boundary",
                "status": "planned_not_executed",
            }
        )

    return {
        "adapter_name": adapter_name,
        "adapter_available": True,
        "execution_mode": "controlled_noop",
        "live_execution": False,
        "external_actions": False,
        "worker_animation": False,
        "command_type": command_brief["command_type"],
        "activation_tier": command_brief["activation_tier"],
        "work_order_count": len(work_orders),
        "planned_steps": planned_steps,
    }


def run_noop_adapter(execution_plan: dict) -> dict:
    adapter_available = execution_plan.get("adapter_available", False)
    planned_steps = execution_plan.get("planned_steps", [])
    if not adapter_available:
        return {
            "adapter_result_status": "BLOCKED",
            "adapter_name": execution_plan.get("adapter_name", "noop"),
            "execution_mode": execution_plan.get("execution_mode", "unsupported_adapter"),
            "live_execution_performed": False,
            "external_actions_taken": False,
            "worker_agents_activated": False,
            "steps_received": len(planned_steps),
            "steps_simulated": 0,
            "step_results": [],
        }

    step_results = []
    for step in planned_steps:
        step_results.append(
            {
                "step_id": step["step_id"],
                "work_order_id": step["work_order_id"],
                "overlay_id": step["overlay_id"],
                "status": "simulated_noop_complete",
            }
        )

    return {
        "adapter_result_status": "PASS",
        "adapter_name": execution_plan.get("adapter_name", "noop"),
        "execution_mode": execution_plan.get("execution_mode", "controlled_noop"),
        "live_execution_performed": False,
        "external_actions_taken": False,
        "worker_agents_activated": False,
        "steps_received": len(planned_steps),
        "steps_simulated": len(step_results),
        "step_results": step_results,
    }


def _resolve_path(path_value: str | Path) -> Path:
    return Path(path_value).expanduser().resolve(strict=False)


def _path_contains_forbidden_marker(path_value: str) -> bool:
    normalized = path_value.replace("\\", "/").lower()
    forbidden_markers = [
        "02_departments",
        "04_workflow_templates",
        "09_exports/dashboard_seed.json",
        "09_exports/org_chart_export.json",
        "09_exports/master_department_list.md",
        "devinization_pack_",
        "family_007_devinized_engineering_overload",
        "ownership_metadata",
    ]
    return any(marker in normalized for marker in forbidden_markers)


def _is_within_directory(candidate: Path, base_dir: Path) -> bool:
    try:
        candidate.relative_to(base_dir)
        return True
    except ValueError:
        return False


def classify_path_safety(target_path: str, execution_dir: str | None = None) -> dict:
    target_path_obj = Path(target_path).expanduser()
    is_absolute = target_path_obj.is_absolute()
    raw_target_text = str(target_path)

    if execution_dir is None:
        resolved_target = target_path_obj.resolve(strict=False)
        forbidden = _path_contains_forbidden_marker(raw_target_text) or _path_contains_forbidden_marker(
            resolved_target.as_posix()
        )
        return {
            "target_path": target_path,
            "execution_dir": execution_dir,
            "is_absolute": is_absolute,
            "is_inside_execution_dir": False,
            "is_forbidden_project_path": forbidden,
            "safety_status": BLOCKED_OUTSIDE_EXECUTION_DIR,
            "reason": "execution_dir is required for sandbox file writes.",
        }

    execution_dir_path = _resolve_path(execution_dir)
    if target_path_obj.is_absolute():
        resolved_target = target_path_obj.resolve(strict=False)
    else:
        resolved_target = (execution_dir_path / target_path_obj).resolve(strict=False)

    forbidden = _path_contains_forbidden_marker(raw_target_text) or _path_contains_forbidden_marker(
        resolved_target.as_posix()
    )
    inside = _is_within_directory(resolved_target, execution_dir_path)

    if not inside:
        return {
            "target_path": str(resolved_target),
            "execution_dir": str(execution_dir_path),
            "is_absolute": is_absolute,
            "is_inside_execution_dir": False,
            "is_forbidden_project_path": forbidden,
            "safety_status": BLOCKED_OUTSIDE_EXECUTION_DIR,
            "reason": "Target path must resolve inside execution_dir.",
        }

    if forbidden:
        return {
            "target_path": str(resolved_target),
            "execution_dir": str(execution_dir_path),
            "is_absolute": is_absolute,
            "is_inside_execution_dir": True,
            "is_forbidden_project_path": True,
            "safety_status": BLOCKED_FORBIDDEN_PATH,
            "reason": "Target path resolves to a forbidden project path.",
        }

    return {
        "target_path": str(resolved_target),
        "execution_dir": str(execution_dir_path),
        "is_absolute": is_absolute,
        "is_inside_execution_dir": True,
        "is_forbidden_project_path": False,
        "safety_status": SAFE_SANDBOX_PATH,
        "reason": "Target path is inside execution_dir and allowed for sandbox write.",
    }


def create_file_operation_plan(
    command_brief: dict,
    execution_dir: str | None = None,
    target_filename: str = "station_chief_sandbox_output.txt",
) -> dict:
    if execution_dir is None:
        target_path = str(Path(target_filename))
    else:
        target_path = str((_resolve_path(execution_dir) / Path(target_filename)).resolve(strict=False))

    path_safety = classify_path_safety(target_path, execution_dir=execution_dir)
    planned_content = "\n".join(
        [
            "Station Chief Runtime v0.4.0 sandbox file operation",
            f"command_type={command_brief['command_type']}",
            f"activation_tier={command_brief['activation_tier']['name']}",
            "baseline_preserved=true",
            "external_actions_taken=false",
            "live_worker_agents_activated=false",
        ]
    )
    operation_status = "PLANNED_SAFE" if path_safety["safety_status"] == SAFE_SANDBOX_PATH else "BLOCKED"
    return {
        "operation_type": "sandbox_file_write",
        "execution_dir": execution_dir,
        "target_filename": target_filename,
        "target_path": target_path,
        "requires_human_confirmation": True,
        "confirmation_token_required": YES_I_APPROVE_SANDBOX_FILE_WRITE,
        "path_safety": path_safety,
        "planned_content": planned_content,
        "operation_status": operation_status,
    }


def evaluate_execution_gate(file_operation_plan: dict, confirmation_token: str | None = None) -> dict:
    token_received = confirmation_token == YES_I_APPROVE_SANDBOX_FILE_WRITE
    path_status = file_operation_plan["path_safety"]["safety_status"]
    approved = token_received and path_status == SAFE_SANDBOX_PATH
    if approved:
        reason = "Sandbox file write approved."
    elif path_status != SAFE_SANDBOX_PATH:
        reason = file_operation_plan["path_safety"]["reason"]
    else:
        reason = "Sandbox file write blocked: confirmation token missing or incorrect."
    return {
        "gate_status": "APPROVED" if approved else "BLOCKED",
        "requires_human_confirmation": True,
        "confirmation_token_required": YES_I_APPROVE_SANDBOX_FILE_WRITE,
        "confirmation_token_received": token_received,
        "path_safety_status": path_status,
        "approved_for_sandbox_write": approved,
        "reason": reason,
    }


def run_sandbox_file_write_adapter(file_operation_plan: dict, execution_gate: dict) -> dict:
    if execution_gate.get("gate_status") != "APPROVED":
        return {
            "adapter_result_status": "BLOCKED",
            "operation_type": "sandbox_file_write",
            "file_written": False,
            "target_path": file_operation_plan["target_path"],
            "live_execution_performed": False,
            "external_actions_taken": False,
            "worker_agents_activated": False,
            "reason": execution_gate.get("reason", "Sandbox file write blocked."),
        }

    target_path = Path(file_operation_plan["target_path"])
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(file_operation_plan["planned_content"] + "\n", encoding="utf-8")
    return {
        "adapter_result_status": "PASS",
        "operation_type": "sandbox_file_write",
        "file_written": True,
        "target_path": str(target_path),
        "live_execution_performed": False,
        "external_actions_taken": False,
        "worker_agents_activated": False,
        "reason": "Sandbox-only file write completed after explicit human confirmation.",
    }

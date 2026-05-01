#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

ADAPTER_MODULE_VERSION = "0.3.0"

SUPPORTED_ADAPTERS = {
    "noop": {
        "name": "No-Op Controlled Execution Adapter",
        "live_execution": False,
        "external_actions": False,
        "worker_animation": False,
        "description": "Safely simulates execution boundaries without performing live work.",
    }
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

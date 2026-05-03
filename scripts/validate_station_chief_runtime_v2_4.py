#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read_text(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


def run_command(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def parse_json(output: str, label: str, errors: list[str]):
    try:
        return json.loads(output)
    except Exception as exc:
        errors.append(f"{label}: invalid JSON ({exc})\n{output}")
        return None


def assert_keys(errors: list[str], mapping: dict, required: list[str], label: str) -> None:
    for key in required:
        require(errors, key in mapping, f"{label} missing key: {key}")


def validate_files(errors: list[str]) -> None:
    required = [
        "10_runtime/station_chief_runtime.py",
        "10_runtime/station_chief_demo_cases.json",
        "10_runtime/station_chief_runtime_readme.md",
        "10_runtime/station_chief_fixture_tests.py",
        "10_runtime/station_chief_adapters.py",
        "10_runtime/station_chief_execution_profiles.py",
        "10_runtime/station_chief_approval_handoff.py",
        "10_runtime/station_chief_approval_records.py",
        "10_runtime/station_chief_approval_ledger.py",
        "10_runtime/station_chief_release_lock.py",
        "10_runtime/station_chief_controlled_execution.py",
        "10_runtime/station_chief_work_order_executor.py",
        "10_runtime/station_chief_worker_hiring_registry.py",
        "10_runtime/station_chief_department_routing.py",
        "10_runtime/station_chief_multi_agent_orchestration.py",
        "10_runtime/station_chief_operator_console.py",
        "10_runtime/station_chief_github_patch_hardening.py",
        "10_runtime/station_chief_deployment_packaging.py",
        "10_runtime/station_chief_controlled_worker_execution.py",
        "10_runtime/station_chief_tool_permission_binding.py",
        "10_runtime/station_chief_live_execution_telemetry_abort.py",
        "10_runtime/station_chief_post_run_audit_expansion.py",
        "10_runtime/station_chief_multi_worker_sandbox_coordination.py",
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v2_4_report.md",
        "scripts/validate_station_chief_runtime_v2_4.py",
    ]
    for rel in required:
        require(errors, (ROOT / rel).exists(), f"Missing file: {rel}")


def validate_source_strings(errors: list[str]) -> None:
    runtime = read_text("10_runtime/station_chief_runtime.py")
    adapters = read_text("10_runtime/station_chief_adapters.py")
    post_run = read_text("10_runtime/station_chief_post_run_audit_expansion.py")
    multi_worker = read_text("10_runtime/station_chief_multi_worker_sandbox_coordination.py")

    for needle in [
        'STATION_CHIEF_RUNTIME_VERSION = "2.4.0"',
        "attach_post_run_audit_expansion",
        "write_post_run_audit_expansion",
        "attach_multi_worker_sandbox_coordination",
        "write_multi_worker_sandbox_coordination",
        "--multi-worker-coordination-schema",
        "--multi-worker-sandbox-coordination",
        "--write-multi-worker-sandbox-coordination",
        "--multi-worker-roster-label",
        "--multi-worker-confirm-token",
        "--multi-worker-count",
        "--multi-worker-role",
        "--multi-worker-shared-resource",
        "--multi-worker-abort-reason",
        "--multi-worker-failure-reason",
        "post_run_audit_expansion_bundle",
        "post_run_audit_expansion_schema",
        "expanded_audit_evidence_schema",
        "post_run_audit_approval_gate",
        "before_after_run_comparison_proof",
        "validator_backed_audit_artifact_index",
        "audit_replay_record",
        "failure_class_taxonomy",
        "human_review_packet",
        "audit_integrity_score",
        "audit_evidence_ledger",
        "audit_expansion_readiness_summary",
        "multi_worker_sandbox_coordination_readiness_bridge",
        "multi_worker_sandbox_coordination_bundle",
        "multi_worker_sandbox_coordination_schema",
        "multi_worker_coordination_approval_gate",
        "sandbox_worker_roster",
        "worker_coordination_graph",
        "inter_worker_handoff_contract",
        "multi_worker_dry_run_ledger",
        "coordination_conflict_detector",
        "coordination_abort_contract",
        "coordination_quarantine_contract",
        "coordination_audit_proof",
        "coordination_readiness_summary",
        "controlled_external_tool_adapter_preview_readiness_bridge",
        "single_worker_post_run_audit_expansion_only",
        "multi_worker_sandbox_coordination_preview_only",
        "multi_worker_sandbox_coordination_requires_token",
        "multi_worker_sandbox_coordination_does_not_hire_real_workers",
        "multi_worker_sandbox_coordination_does_not_start_worker_processes",
        "multi_worker_sandbox_coordination_does_not_perform_live_routing",
        "multi_worker_sandbox_coordination_does_not_perform_live_orchestration",
        "multi_worker_sandbox_coordination_does_not_modify_repo_files",
        'runtime_status": "multi_worker_sandbox_coordination"',
        'station-chief-v2-4-',
        'artifact_type": "station_chief_runtime_v2_4_artifacts"',
        'Next step: build controlled external tool adapter preview.',
    ]:
        require(errors, needle in runtime, f"runtime missing string: {needle}")

    for needle in [
        'ADAPTER_MODULE_VERSION = "2.4.0"',
        'supports_post_run_audit_expansion',
        'post_run_audit_expansion_requires_specific_token',
        'actual_replay_execution_allowed',
        'external_artifact_fetch_allowed',
        'audit_background_monitoring_allowed',
        'supports_multi_worker_sandbox_coordination',
        'multi_worker_sandbox_coordination_requires_specific_token',
        'real_worker_hiring_allowed',
        'worker_process_start_allowed',
        'live_worker_routing_allowed',
        'live_orchestration_allowed',
        'multi_worker_sandbox_coordination_requires_separate_gate',
        'YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION',
        'YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION',
    ]:
        require(errors, needle in adapters, f"adapter module missing string: {needle}")

    for needle in [
        'POST_RUN_AUDIT_EXPANSION_MODULE_VERSION = "2.4.0"',
        'POST_RUN_AUDIT_EXPANSION_STATUS',
        'POST_RUN_AUDIT_EXPANSION_PHASE',
        'POST_RUN_AUDIT_EXPANSION_APPROVAL_TOKEN',
        'canonical_json',
        'sha256_digest',
        'normalize_audit_label',
        'generate_post_run_audit_expansion_id',
        'create_post_run_audit_expansion_schema',
        'create_expanded_audit_evidence_schema',
        'create_post_run_audit_approval_gate',
        'create_before_after_run_comparison_proof',
        'create_validator_backed_audit_artifact_index',
        'create_audit_replay_record',
        'create_failure_class_taxonomy',
        'create_human_review_packet',
        'create_audit_integrity_score',
        'create_audit_evidence_ledger',
        'create_audit_expansion_readiness_summary',
        'create_multi_worker_sandbox_coordination_readiness_bridge',
        'create_post_run_audit_expansion_bundle',
    ]:
        require(errors, needle in post_run, f"post-run module missing string: {needle}")

    for needle in [
        'MULTI_WORKER_SANDBOX_COORDINATION_MODULE_VERSION = "2.4.0"',
        'MULTI_WORKER_SANDBOX_COORDINATION_STATUS',
        'MULTI_WORKER_SANDBOX_COORDINATION_PHASE',
        'MULTI_WORKER_SANDBOX_COORDINATION_APPROVAL_TOKEN',
        'canonical_json',
        'sha256_digest',
        'normalize_coordination_label',
        'generate_multi_worker_coordination_id',
        'create_multi_worker_sandbox_coordination_schema',
        'create_multi_worker_coordination_approval_gate',
        'create_sandbox_worker_roster',
        'create_worker_coordination_graph',
        'create_inter_worker_handoff_contract',
        'create_multi_worker_dry_run_ledger',
        'create_coordination_conflict_detector',
        'create_coordination_abort_contract',
        'create_coordination_quarantine_contract',
        'create_coordination_audit_proof',
        'create_coordination_readiness_summary',
        'create_controlled_external_tool_adapter_preview_readiness_bridge',
        'create_multi_worker_sandbox_coordination_bundle',
    ]:
        require(errors, needle in multi_worker, f"multi-worker module missing string: {needle}")

    forbidden_common = ["requests", "urllib.request", "os.system", "pip install", "npm install", "live API", "API key", "import subprocess"]
    for rel in [
        "10_runtime/station_chief_runtime.py",
        "10_runtime/station_chief_adapters.py",
        "10_runtime/station_chief_execution_profiles.py",
        "10_runtime/station_chief_approval_handoff.py",
        "10_runtime/station_chief_approval_records.py",
        "10_runtime/station_chief_approval_ledger.py",
        "10_runtime/station_chief_release_lock.py",
        "10_runtime/station_chief_controlled_execution.py",
        "10_runtime/station_chief_work_order_executor.py",
        "10_runtime/station_chief_worker_hiring_registry.py",
        "10_runtime/station_chief_department_routing.py",
        "10_runtime/station_chief_multi_agent_orchestration.py",
        "10_runtime/station_chief_operator_console.py",
        "10_runtime/station_chief_github_patch_hardening.py",
        "10_runtime/station_chief_deployment_packaging.py",
        "10_runtime/station_chief_controlled_worker_execution.py",
        "10_runtime/station_chief_tool_permission_binding.py",
        "10_runtime/station_chief_live_execution_telemetry_abort.py",
        "10_runtime/station_chief_post_run_audit_expansion.py",
        "10_runtime/station_chief_multi_worker_sandbox_coordination.py",
    ]:
        text = read_text(rel)
        for needle in forbidden_common:
            require(errors, needle not in text, f"forbidden string '{needle}' found in {rel}")

    for needle in ["eval(", "exec(", "compile(", "open(", "socket", "http.server", "socketserver", "uvicorn", "streamlit", "netlify", "vercel", "cloudflare", "firebase", "railway", "render", "gh api", "git push", "create_deployment", "create_commit", "update_ref", "__import__", "threading", "multiprocessing", "kill(", "terminate("]:
        require(errors, needle not in multi_worker, f"forbidden string '{needle}' found in multi-worker module")


def validate_demo_and_fixture(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "2.4.0", "demo runtime version mismatch")
        require(errors, demo.get("runtime_status") == "multi_worker_sandbox_coordination", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type mismatch")
        evidence = demo.get("evidence", {})
        true_keys = [
            "baseline_preserved",
            "post_run_audit_expansion_available",
            "single_worker_post_run_audit_expansion_only",
            "post_run_audit_expansion_requires_token",
            "post_run_audit_expansion_does_not_perform_actual_replay",
            "post_run_audit_expansion_does_not_fetch_external_artifacts",
            "post_run_audit_expansion_does_not_run_shell_commands",
            "post_run_audit_expansion_does_not_modify_repo_files",
            "multi_worker_sandbox_coordination_not_yet_active",
            "multi_worker_sandbox_coordination_available",
            "multi_worker_sandbox_coordination_preview_only",
            "multi_worker_sandbox_coordination_requires_token",
            "multi_worker_sandbox_coordination_does_not_hire_real_workers",
            "multi_worker_sandbox_coordination_does_not_start_worker_processes",
            "multi_worker_sandbox_coordination_does_not_perform_live_routing",
            "multi_worker_sandbox_coordination_does_not_perform_live_orchestration",
            "multi_worker_sandbox_coordination_does_not_modify_repo_files",
            "controlled_external_tool_adapter_preview_not_yet_active",
        ]
        false_keys = [
            "external_actions_taken",
            "live_worker_agents_activated",
        ]
        for key in true_keys:
            require(errors, evidence.get(key) is True, f"demo evidence {key} mismatch")
        for key in false_keys:
            require(errors, evidence.get(key) is False, f"demo evidence {key} mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture status mismatch")
        require(errors, fixture.get("runtime_version") == "2.4.0", "fixture runtime version mismatch")
        require(errors, fixture.get("case_count") == 5, "fixture case_count mismatch")
        require(errors, fixture.get("failed") == 0, "fixture failed mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: {err}")
    fixture_runner = parse_json(out, "fixture runner", errors)
    if fixture_runner:
        require(errors, fixture_runner.get("fixture_test_status") == "PASS", "fixture runner status mismatch")
        require(errors, fixture_runner.get("runtime_version") == "2.4.0", "fixture runner version mismatch")
        require(errors, fixture_runner.get("case_count") == 5, "fixture runner case_count mismatch")
        require(errors, fixture_runner.get("failed") == 0, "fixture runner failed mismatch")


def validate_overlay_and_adapter_views(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-overlays"])
    require(errors, code == 0, f"--list-overlays failed: {err}")
    overlays = parse_json(out, "--list-overlays", errors)
    if overlays is not None:
        require(errors, len(overlays) == 8, "overlay count mismatch")
        for overlay in overlays:
            require(errors, overlay.get("exists") is True, f"overlay missing: {overlay.get('id')}")
            require(errors, overlay.get("preserves_locked_baseline") is True, f"overlay baseline mismatch: {overlay.get('id')}")
            owner = overlay.get("ownership_project_owner", "") or ""
            require(errors, "Devin O’Rourke" in owner, f"overlay owner mismatch: {overlay.get('id')}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: {err}")
    adapters = parse_json(out, "--list-adapters", errors)
    if adapters is not None:
        require(errors, adapters.get("adapter_module_version") == "2.4.0", "adapter module version mismatch")
        require(errors, adapters.get("supports_post_run_audit_expansion") is True, "adapter post-run support mismatch")
        require(errors, adapters.get("post_run_audit_expansion_requires_specific_token") is True, "adapter post-run token mismatch")
        require(errors, adapters.get("actual_replay_execution_allowed") is False, "adapter replay flag mismatch")
        require(errors, adapters.get("external_artifact_fetch_allowed") is False, "adapter artifact fetch flag mismatch")
        require(errors, adapters.get("audit_background_monitoring_allowed") is False, "adapter monitoring flag mismatch")
        require(errors, adapters.get("supports_multi_worker_sandbox_coordination") is True, "adapter multi-worker support mismatch")
        require(errors, adapters.get("multi_worker_sandbox_coordination_requires_specific_token") is True, "adapter multi-worker token mismatch")
        require(errors, adapters.get("real_worker_hiring_allowed") is False, "adapter hiring flag mismatch")
        require(errors, adapters.get("worker_process_start_allowed") is False, "adapter worker process flag mismatch")
        require(errors, adapters.get("live_worker_routing_allowed") is False, "adapter live routing flag mismatch")
        require(errors, adapters.get("live_orchestration_allowed") is False, "adapter live orchestration flag mismatch")
        noop = adapters.get("supported_adapters", {}).get("noop", {})
        scoped = adapters.get("supported_adapters", {}).get("scoped_repo_patch", {})
        require(errors, noop.get("supports_post_run_audit_expansion") is True, "noop post-run support mismatch")
        require(errors, noop.get("supports_multi_worker_sandbox_coordination") is True, "noop multi-worker support mismatch")
        require(errors, scoped.get("supports_post_run_audit_expansion") is False, "scoped patch post-run support mismatch")
        require(errors, scoped.get("post_run_audit_expansion_requires_separate_gate") is True, "scoped patch post-run gate mismatch")
        require(errors, scoped.get("supports_multi_worker_sandbox_coordination") is False, "scoped patch multi-worker support mismatch")
        require(errors, scoped.get("multi_worker_sandbox_coordination_requires_separate_gate") is True, "scoped patch multi-worker gate mismatch")


def validate_schema_views(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--post-run-audit-schema"])
    require(errors, code == 0, f"--post-run-audit-schema failed: {err}")
    post_run_schema = parse_json(out, "--post-run-audit-schema", errors)
    if post_run_schema:
        require(errors, post_run_schema.get("post_run_audit_expansion_schema_version") == "2.4.0", "post-run schema version mismatch")
        require(errors, post_run_schema.get("schema_status") == "SINGLE_WORKER_POST_RUN_AUDIT_EXPANSION_ONLY", "post-run schema status mismatch")
        for key in [
            "expanded_audit_evidence_schema",
            "post_run_audit_approval_gate",
            "before_after_run_comparison_proof",
            "validator_backed_audit_artifact_index",
            "audit_replay_record",
            "failure_class_taxonomy",
            "human_review_packet",
            "audit_integrity_score",
            "audit_evidence_ledger",
            "audit_expansion_readiness_summary",
            "multi_worker_sandbox_coordination_readiness_bridge",
        ]:
            require(errors, key in post_run_schema.get("required_sections", []), f"post-run required_sections missing {key}")
        require(errors, "local_audit_preview" in post_run_schema.get("allowed_audit_modes", []), "post-run allowed_audit_modes missing local_audit_preview")
        require(errors, "approved_single_worker_audit_expansion_records" in post_run_schema.get("allowed_audit_modes", []), "post-run allowed_audit_modes missing approved_single_worker_audit_expansion_records")
        for key in ["actual_replay_execution", "external_artifact_fetch", "shell_command_replay", "background_audit_monitoring"]:
            require(errors, key in post_run_schema.get("blocked_audit_modes", []), f"post-run blocked_audit_modes missing {key}")
        require(errors, "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION" in post_run_schema.get("required_confirmation_tokens", []), "post-run token missing")
        require(errors, post_run_schema.get("baseline_preserved") is True, "post-run schema baseline mismatch")
        require(errors, post_run_schema.get("external_actions_taken") is False, "post-run schema external_actions mismatch")
        require(errors, post_run_schema.get("actual_replay_performed") is False, "post-run schema replay mismatch")
        require(errors, post_run_schema.get("repo_files_modified") is False, "post-run schema repo modification mismatch")
        require(errors, post_run_schema.get("external_artifact_fetch_performed") is False, "post-run schema artifact fetch mismatch")
        require(errors, post_run_schema.get("broad_worker_activation_performed") is False, "post-run schema broad worker mismatch")
        require(errors, post_run_schema.get("execution_authorized") is False, "post-run schema execution mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--multi-worker-coordination-schema"])
    require(errors, code == 0, f"--multi-worker-coordination-schema failed: {err}")
    multi_schema = parse_json(out, "--multi-worker-coordination-schema", errors)
    if multi_schema:
        require(errors, multi_schema.get("multi_worker_sandbox_coordination_schema_version") == "2.4.0", "multi-worker schema version mismatch")
        require(errors, multi_schema.get("schema_status") == "MULTI_WORKER_SANDBOX_COORDINATION_PREVIEW_ONLY", "multi-worker schema status mismatch")
        for key in [
            "multi_worker_coordination_approval_gate",
            "sandbox_worker_roster",
            "worker_coordination_graph",
            "inter_worker_handoff_contract",
            "multi_worker_dry_run_ledger",
            "coordination_conflict_detector",
            "coordination_abort_contract",
            "coordination_quarantine_contract",
            "coordination_audit_proof",
            "coordination_readiness_summary",
            "controlled_external_tool_adapter_preview_readiness_bridge",
        ]:
            require(errors, key in multi_schema.get("required_sections", []), f"multi-worker required_sections missing {key}")
        for key in ["schema_only", "local_coordination_preview", "approved_multi_worker_sandbox_coordination_records", "handoff_contract_preview", "conflict_detection_preview", "dry_run_ledger_preview"]:
            require(errors, key in multi_schema.get("allowed_coordination_modes", []), f"multi-worker allowed_coordination_modes missing {key}")
        for key in ["full_workforce_animation", "real_worker_hiring", "live_worker_routing", "live_orchestration", "background_worker_processes"]:
            require(errors, key in multi_schema.get("blocked_coordination_modes", []), f"multi-worker blocked_coordination_modes missing {key}")
        require(errors, "YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION" in multi_schema.get("required_confirmation_tokens", []), "multi-worker token missing")
        require(errors, multi_schema.get("baseline_preserved") is True, "multi-worker schema baseline mismatch")
        require(errors, multi_schema.get("external_actions_taken") is False, "multi-worker schema external_actions mismatch")
        require(errors, multi_schema.get("real_workers_hired") is False, "multi-worker schema real_workers mismatch")
        require(errors, multi_schema.get("worker_processes_started") is False, "multi-worker schema worker processes mismatch")
        require(errors, multi_schema.get("live_worker_routing_performed") is False, "multi-worker schema routing mismatch")
        require(errors, multi_schema.get("live_orchestration_performed") is False, "multi-worker schema orchestration mismatch")
        require(errors, multi_schema.get("repo_files_modified") is False, "multi-worker schema repo mismatch")
        require(errors, multi_schema.get("broad_worker_activation_performed") is False, "multi-worker schema broad worker mismatch")
        require(errors, multi_schema.get("execution_authorized") is False, "multi-worker schema execution mismatch")


def validate_post_run_flow(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--post-run-audit-expansion"])
    require(errors, code == 0, f"post-run default failed: {err}")
    result = parse_json(out, "post-run default", errors)
    if result:
        for key in [
            "post_run_audit_expansion_bundle",
            "post_run_audit_expansion_schema",
            "expanded_audit_evidence_schema",
            "post_run_audit_approval_gate",
            "before_after_run_comparison_proof",
            "validator_backed_audit_artifact_index",
            "audit_replay_record",
            "failure_class_taxonomy",
            "human_review_packet",
            "audit_integrity_score",
            "audit_evidence_ledger",
            "audit_expansion_readiness_summary",
            "multi_worker_sandbox_coordination_readiness_bridge",
        ]:
            require(errors, key in result, f"post-run default missing {key}")
        require(errors, result["post_run_audit_expansion_bundle"]["post_run_audit_expansion_bundle_version"] == "2.4.0", "post-run bundle version mismatch")
        require(errors, result["post_run_audit_approval_gate"]["gate_status"] == "BLOCKED_PENDING_POST_RUN_AUDIT_EXPANSION_APPROVAL", "post-run gate status mismatch")
        require(errors, result["post_run_audit_approval_gate"]["confirmation_token_valid"] is False, "post-run token-valid mismatch")
        require(errors, result["before_after_run_comparison_proof"]["comparison_status"] == "BLOCKED", "post-run comparison status mismatch")
        require(errors, result["audit_replay_record"]["replay_status"] == "BLOCKED", "post-run replay status mismatch")
        require(errors, result["human_review_packet"]["packet_status"] == "BLOCKED", "post-run packet status mismatch")
        require(errors, result["audit_integrity_score"]["integrity_status"] == "BLOCKED", "post-run integrity status mismatch")
        require(errors, result["audit_expansion_readiness_summary"]["readiness_status"] == "BLOCKED", "post-run readiness status mismatch")
        require(errors, result.get("external_actions_taken") is False, "post-run external actions mismatch")
        require(errors, result.get("actual_replay_performed") is False, "post-run replay mismatch")
        require(errors, result.get("external_artifact_fetch_performed") is False, "post-run artifact fetch mismatch")
        require(errors, result.get("repo_files_modified") is False, "post-run repo mismatch")
        require(errors, result.get("execution_authorized") is False, "post-run execution mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--post-run-audit-expansion", "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION"])
    require(errors, code == 0, f"post-run approved failed: {err}")
    result = parse_json(out, "post-run approved", errors)
    if result:
        require(errors, result["post_run_audit_approval_gate"]["gate_status"] == "APPROVED_FOR_SINGLE_WORKER_POST_RUN_AUDIT_EXPANSION_RECORDS", "approved post-run gate mismatch")
        require(errors, result["post_run_audit_approval_gate"]["confirmation_token_valid"] is True, "approved post-run token-valid mismatch")
        require(errors, result["before_after_run_comparison_proof"]["comparison_status"] == "CREATED", "approved post-run comparison mismatch")
        require(errors, result["validator_backed_audit_artifact_index"]["index_status"] == "INDEX_CREATED", "approved post-run index mismatch")
        require(errors, result["audit_replay_record"]["replay_status"] == "REPLAY_RECORD_CREATED", "approved post-run replay mismatch")
        require(errors, result["failure_class_taxonomy"]["taxonomy_status"] == "TAXONOMY_CREATED", "approved post-run taxonomy mismatch")
        require(errors, result["human_review_packet"]["packet_status"] == "READY_FOR_HUMAN_REVIEW", "approved post-run packet mismatch")
        require(errors, result["audit_integrity_score"]["integrity_status"] == "PASS", "approved post-run integrity mismatch")
        require(errors, result["audit_evidence_ledger"]["ledger_status"] == "SINGLE_WORKER_POST_RUN_AUDIT_LEDGER", "approved post-run ledger mismatch")
        require(errors, result["audit_expansion_readiness_summary"]["ready_for_multi_worker_sandbox_coordination"] is True, "approved post-run readiness boolean mismatch")
        require(errors, result["multi_worker_sandbox_coordination_readiness_bridge"]["next_layer"] == "Multi-Worker Sandbox Coordination", "approved post-run bridge next layer mismatch")
        require(errors, result["multi_worker_sandbox_coordination_readiness_bridge"]["ready_for_multi_worker_sandbox_coordination"] is True, "approved post-run bridge readiness mismatch")
        require(errors, result.get("external_actions_taken") is False, "approved post-run external actions mismatch")
        require(errors, result.get("actual_replay_performed") is False, "approved post-run replay mismatch")
        require(errors, result.get("external_artifact_fetch_performed") is False, "approved post-run artifact fetch mismatch")
        require(errors, result.get("repo_files_modified") is False, "approved post-run repo mismatch")
        require(errors, result.get("execution_authorized") is False, "approved post-run execution mismatch")

    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--post-run-audit-expansion", "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION", "--post-run-audit-observed-failure", "digest_mismatch"
    ])
    require(errors, code == 0, f"post-run observed failure failed: {err}")
    result = parse_json(out, "post-run observed failure", errors)
    if result:
        require(errors, result["failure_class_taxonomy"]["failure_count"] == 1, "observed failure count mismatch")
        require(errors, "digest_mismatch" in result["failure_class_taxonomy"]["classified_failures"], "observed failure classification mismatch")
        require(errors, result["audit_integrity_score"]["integrity_score"] < 100, "observed failure integrity score mismatch")
        require(errors, result.get("external_actions_taken") is False, "observed failure external actions mismatch")
        require(errors, result.get("actual_replay_performed") is False, "observed failure replay mismatch")
        require(errors, result.get("repo_files_modified") is False, "observed failure repo mismatch")

    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--post-run-audit-expansion", "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION", "--post-run-audit-before-json", '{"a":1}', "--post-run-audit-after-json", '{"a":1,"b":2}'
    ])
    require(errors, code == 0, f"post-run before/after failed: {err}")
    result = parse_json(out, "post-run before/after", errors)
    if result:
        proof = result["before_after_run_comparison_proof"]
        require(errors, proof["comparison_status"] == "CREATED", "comparison status mismatch")
        require(errors, "b" in proof["added_top_level_keys"], "added key mismatch")
        require(errors, proof["git_diff_performed"] is False, "git diff mismatch")
        require(errors, proof["filesystem_read"] is False, "filesystem read mismatch")
        require(errors, result.get("external_actions_taken") is False, "before/after external actions mismatch")


def validate_multi_worker_flow(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--multi-worker-sandbox-coordination"])
    require(errors, code == 0, f"multi-worker default failed: {err}")
    result = parse_json(out, "multi-worker default", errors)
    if result:
        for key in [
            "multi_worker_sandbox_coordination_bundle",
            "multi_worker_sandbox_coordination_schema",
            "multi_worker_coordination_approval_gate",
            "sandbox_worker_roster",
            "worker_coordination_graph",
            "inter_worker_handoff_contract",
            "multi_worker_dry_run_ledger",
            "coordination_conflict_detector",
            "coordination_abort_contract",
            "coordination_quarantine_contract",
            "coordination_audit_proof",
            "coordination_readiness_summary",
            "controlled_external_tool_adapter_preview_readiness_bridge",
        ]:
            require(errors, key in result, f"multi-worker default missing {key}")
        require(errors, result["multi_worker_sandbox_coordination_bundle"]["multi_worker_sandbox_coordination_bundle_version"] == "2.4.0", "multi-worker bundle version mismatch")
        require(errors, result["multi_worker_coordination_approval_gate"]["gate_status"] == "BLOCKED_PENDING_MULTI_WORKER_SANDBOX_COORDINATION_APPROVAL", "multi-worker gate status mismatch")
        require(errors, result["multi_worker_coordination_approval_gate"]["confirmation_token_valid"] is False, "multi-worker token-valid mismatch")
        require(errors, result["sandbox_worker_roster"]["roster_status"] == "BLOCKED", "multi-worker roster status mismatch")
        require(errors, result["worker_coordination_graph"]["graph_status"] == "BLOCKED", "multi-worker graph status mismatch")
        require(errors, result["inter_worker_handoff_contract"]["contract_status"] == "BLOCKED", "multi-worker handoff status mismatch")
        require(errors, result["multi_worker_dry_run_ledger"]["ledger_status"] == "BLOCKED", "multi-worker ledger status mismatch")
        require(errors, result["coordination_audit_proof"]["audit_status"] == "BLOCKED", "multi-worker audit status mismatch")
        require(errors, result["coordination_readiness_summary"]["readiness_status"] == "BLOCKED", "multi-worker readiness status mismatch")
        require(errors, result.get("external_actions_taken") is False, "multi-worker external actions mismatch")
        require(errors, result.get("real_workers_hired") is False, "multi-worker real workers mismatch")
        require(errors, result.get("worker_processes_started") is False, "multi-worker worker process mismatch")
        require(errors, result.get("live_worker_routing_performed") is False, "multi-worker routing mismatch")
        require(errors, result.get("live_orchestration_performed") is False, "multi-worker orchestration mismatch")
        require(errors, result.get("repo_files_modified") is False, "multi-worker repo mismatch")
        require(errors, result.get("execution_authorized") is False, "multi-worker execution mismatch")

    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--multi-worker-sandbox-coordination", "--multi-worker-confirm-token", "YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION"
    ])
    require(errors, code == 0, f"multi-worker approved failed: {err}")
    result = parse_json(out, "multi-worker approved", errors)
    if result:
        require(errors, result["multi_worker_coordination_approval_gate"]["gate_status"] == "APPROVED_FOR_MULTI_WORKER_SANDBOX_COORDINATION_RECORDS", "approved multi-worker gate mismatch")
        require(errors, result["multi_worker_coordination_approval_gate"]["confirmation_token_valid"] is True, "approved multi-worker token-valid mismatch")
        require(errors, result["sandbox_worker_roster"]["roster_status"] == "ROSTER_CREATED", "approved multi-worker roster status mismatch")
        require(errors, result["sandbox_worker_roster"]["actual_worker_count"] == 3, "approved multi-worker worker count mismatch")
        require(errors, result["worker_coordination_graph"]["graph_status"] == "GRAPH_CREATED", "approved multi-worker graph status mismatch")
        require(errors, result["inter_worker_handoff_contract"]["contract_status"] == "CONTRACT_CREATED", "approved multi-worker contract status mismatch")
        require(errors, result["multi_worker_dry_run_ledger"]["ledger_status"] == "MULTI_WORKER_SANDBOX_DRY_RUN_LEDGER", "approved multi-worker ledger status mismatch")
        require(errors, result["coordination_conflict_detector"]["conflict_status"] == "CLEAR", "approved multi-worker conflict status mismatch")
        require(errors, result["coordination_abort_contract"]["contract_status"] == "READY", "approved multi-worker abort status mismatch")
        require(errors, result["coordination_quarantine_contract"]["quarantine_status"] == "QUARANTINE_RECORD_READY", "approved multi-worker quarantine mismatch")
        require(errors, result["coordination_audit_proof"]["audit_status"] == "PASS", "approved multi-worker audit status mismatch")
        require(errors, result["coordination_readiness_summary"]["ready_for_controlled_external_tool_adapter_preview"] is True, "approved multi-worker readiness bool mismatch")
        require(errors, result["controlled_external_tool_adapter_preview_readiness_bridge"]["next_layer"] == "Controlled External Tool Adapter Preview", "approved multi-worker next layer mismatch")
        require(errors, result["controlled_external_tool_adapter_preview_readiness_bridge"]["ready_for_controlled_external_tool_adapter_preview"] is True, "approved multi-worker bridge readiness mismatch")
        require(errors, result.get("external_actions_taken") is False, "approved multi-worker external actions mismatch")
        require(errors, result.get("real_workers_hired") is False, "approved multi-worker real workers mismatch")
        require(errors, result.get("worker_processes_started") is False, "approved multi-worker worker process mismatch")
        require(errors, result.get("handoffs_executed") is False, "approved multi-worker handoffs mismatch")
        require(errors, result.get("live_worker_routing_performed") is False, "approved multi-worker routing mismatch")
        require(errors, result.get("live_orchestration_performed") is False, "approved multi-worker orchestration mismatch")
        require(errors, result.get("repo_files_modified") is False, "approved multi-worker repo mismatch")
        require(errors, result.get("execution_authorized") is False, "approved multi-worker execution mismatch")

    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--multi-worker-sandbox-coordination", "--multi-worker-confirm-token", "YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION", "--multi-worker-count", "2", "--multi-worker-role", "planner", "--multi-worker-role", "verifier"
    ])
    require(errors, code == 0, f"multi-worker custom failed: {err}")
    result = parse_json(out, "multi-worker custom", errors)
    if result:
        require(errors, result["sandbox_worker_roster"]["roster_status"] == "ROSTER_CREATED", "custom roster status mismatch")
        require(errors, result["sandbox_worker_roster"]["actual_worker_count"] == 2, "custom worker count mismatch")
        require(errors, result["worker_coordination_graph"]["node_count"] == 2, "custom node count mismatch")
        require(errors, result["worker_coordination_graph"]["edge_count"] == 1, "custom edge count mismatch")
        require(errors, result["inter_worker_handoff_contract"]["handoff_count"] == 1, "custom handoff count mismatch")
        require(errors, result["coordination_audit_proof"]["audit_status"] == "PASS", "custom audit status mismatch")
        require(errors, result.get("real_workers_hired") is False, "custom real workers mismatch")
        require(errors, result.get("worker_processes_started") is False, "custom worker process mismatch")

    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--multi-worker-sandbox-coordination", "--multi-worker-confirm-token", "YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION", "--multi-worker-shared-resource", "same-box", "--multi-worker-shared-resource", "same-box"
    ])
    require(errors, code == 0, f"multi-worker conflict failed: {err}")
    result = parse_json(out, "multi-worker conflict", errors)
    if result:
        require(errors, result["coordination_conflict_detector"]["conflict_status"] == "CONFLICTS_FOUND", "conflict status mismatch")
        require(errors, result["coordination_conflict_detector"]["conflict_count"] >= 1, "conflict count mismatch")
        require(errors, result["coordination_abort_contract"]["abort_recommended"] is True, "conflict abort recommendation mismatch")
        require(errors, result["coordination_quarantine_contract"]["quarantine_recommended"] is True, "conflict quarantine recommendation mismatch")
        require(errors, result["coordination_audit_proof"]["audit_status"] == "REVIEW_REQUIRED", "conflict audit status mismatch")
        require(errors, result["coordination_readiness_summary"]["readiness_status"] == "REVIEW_REQUIRED", "conflict readiness status mismatch")
        require(errors, result.get("external_actions_taken") is False, "conflict external actions mismatch")
        require(errors, result.get("repo_files_modified") is False, "conflict repo mismatch")
        require(errors, result.get("worker_processes_started") is False, "conflict worker process mismatch")

    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py", "--command", "build controlled external tool adapter preview", "--multi-worker-sandbox-coordination", "--multi-worker-confirm-token", "YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION"
    ])
    require(errors, code == 0, f"multi-worker next layer failed: {err}")
    result = parse_json(out, "multi-worker next layer", errors)
    if result:
        require(errors, result["controlled_external_tool_adapter_preview_readiness_bridge"]["next_layer"] == "Controlled External Tool Adapter Preview", "next layer bridge mismatch")
        require(errors, result["controlled_external_tool_adapter_preview_readiness_bridge"]["ready_for_controlled_external_tool_adapter_preview"] is True, "next layer bridge readiness mismatch")
        require(errors, result["coordination_readiness_summary"]["next_layer"] == "Controlled External Tool Adapter Preview", "next layer summary mismatch")
        require(errors, result["coordination_readiness_summary"]["readiness_status"] == "READY_FOR_NEXT_LAYER", "next layer readiness status mismatch")
        require(errors, result["coordination_audit_proof"]["audit_status"] == "PASS", "next layer audit status mismatch")
        require(errors, result.get("external_actions_taken") is False, "next layer external actions mismatch")
        require(errors, result.get("worker_processes_started") is False, "next layer worker process mismatch")
        require(errors, result.get("live_worker_routing_performed") is False, "next layer routing mismatch")
        require(errors, result.get("live_orchestration_performed") is False, "next layer orchestration mismatch")
        require(errors, result.get("repo_files_modified") is False, "next layer repo mismatch")


def validate_write_flows(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--write-post-run-audit-expansion", tmpdir, "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION"
        ])
        require(errors, code == 0, f"write post-run failed: {err}")
        result = parse_json(out, "write post-run", errors)
        if result:
            require(errors, "post_run_audit_expansion_write_summary" in result, "write post-run summary missing")
            summary = result["post_run_audit_expansion_write_summary"]
            written = summary.get("files_written", [])
            for name in [
                "post_run_audit_expansion_bundle.json",
                "post_run_audit_expansion_schema.json",
                "expanded_audit_evidence_schema.json",
                "post_run_audit_approval_gate.json",
                "before_after_run_comparison_proof.json",
                "validator_backed_audit_artifact_index.json",
                "audit_replay_record.json",
                "failure_class_taxonomy.json",
                "human_review_packet.json",
                "audit_integrity_score.json",
                "audit_evidence_ledger.json",
                "audit_expansion_readiness_summary.json",
                "multi_worker_sandbox_coordination_readiness_bridge.json",
                "post_run_audit_expansion_manifest.json",
            ]:
                require(errors, name in written, f"write post-run missing file {name}")
            manifest = json.loads((Path(summary["post_run_audit_expansion_dir"]) / "post_run_audit_expansion_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "2.4.0", "post-run manifest runtime_version mismatch")
            require(errors, manifest.get("status") == "SINGLE_WORKER_POST_RUN_AUDIT_EXPANSION_ONLY", "post-run manifest status mismatch")
            require(errors, manifest.get("external_actions_taken") is False, "post-run manifest external_actions mismatch")
            require(errors, manifest.get("actual_replay_performed") is False, "post-run manifest replay mismatch")
            require(errors, manifest.get("external_artifact_fetch_performed") is False, "post-run manifest artifact fetch mismatch")
            require(errors, manifest.get("repo_files_modified") is False, "post-run manifest repo mismatch")
            require(errors, manifest.get("execution_authorized") is False, "post-run manifest execution mismatch")

    with tempfile.TemporaryDirectory() as tmpdir:
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--write-multi-worker-sandbox-coordination", tmpdir, "--multi-worker-confirm-token", "YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION"
        ])
        require(errors, code == 0, f"write multi-worker failed: {err}")
        result = parse_json(out, "write multi-worker", errors)
        if result:
            require(errors, "multi_worker_sandbox_coordination_write_summary" in result, "write multi-worker summary missing")
            summary = result["multi_worker_sandbox_coordination_write_summary"]
            written = summary.get("files_written", [])
            for name in [
                "multi_worker_sandbox_coordination_bundle.json",
                "multi_worker_sandbox_coordination_schema.json",
                "multi_worker_coordination_approval_gate.json",
                "sandbox_worker_roster.json",
                "worker_coordination_graph.json",
                "inter_worker_handoff_contract.json",
                "multi_worker_dry_run_ledger.json",
                "coordination_conflict_detector.json",
                "coordination_abort_contract.json",
                "coordination_quarantine_contract.json",
                "coordination_audit_proof.json",
                "coordination_readiness_summary.json",
                "controlled_external_tool_adapter_preview_readiness_bridge.json",
                "multi_worker_sandbox_coordination_manifest.json",
            ]:
                require(errors, name in written, f"write multi-worker missing file {name}")
            manifest = json.loads((Path(summary["multi_worker_sandbox_coordination_dir"]) / "multi_worker_sandbox_coordination_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "2.4.0", "multi-worker manifest runtime_version mismatch")
            require(errors, manifest.get("status") == "MULTI_WORKER_SANDBOX_COORDINATION_PREVIEW_ONLY", "multi-worker manifest status mismatch")
            require(errors, manifest.get("external_actions_taken") is False, "multi-worker manifest external_actions mismatch")
            require(errors, manifest.get("real_workers_hired") is False, "multi-worker manifest real_workers mismatch")
            require(errors, manifest.get("worker_processes_started") is False, "multi-worker manifest worker processes mismatch")
            require(errors, manifest.get("live_worker_routing_performed") is False, "multi-worker manifest routing mismatch")
            require(errors, manifest.get("live_orchestration_performed") is False, "multi-worker manifest orchestration mismatch")
            require(errors, manifest.get("repo_files_modified") is False, "multi-worker manifest repo mismatch")
            require(errors, manifest.get("execution_authorized") is False, "multi-worker manifest execution mismatch")

    with tempfile.TemporaryDirectory() as run_dir, tempfile.TemporaryDirectory() as registry_dir:
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--write-artifacts", run_dir, "--registry-dir", registry_dir, "--multi-worker-sandbox-coordination", "--multi-worker-confirm-token", "YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION"
        ])
        require(errors, code == 0, f"write artifacts failed: {err}")
        result = parse_json(out, "write artifacts", errors)
        if result:
            summary = result.get("artifact_write_summary", {})
            require(errors, summary.get("run_id", "").startswith("station-chief-v2-4-check-please-"), "artifact run_id prefix mismatch")
            artifact_dir = Path(summary.get("artifact_dir", ""))
            require(errors, artifact_dir.exists(), "artifact dir missing")
            require(errors, summary.get("registry_updated") is True, "registry updated mismatch")
            for name in [
                "multi_worker_sandbox_coordination_bundle.json",
                "multi_worker_sandbox_coordination_schema.json",
                "multi_worker_coordination_approval_gate.json",
                "sandbox_worker_roster.json",
                "worker_coordination_graph.json",
                "inter_worker_handoff_contract.json",
                "multi_worker_dry_run_ledger.json",
                "coordination_conflict_detector.json",
                "coordination_abort_contract.json",
                "coordination_quarantine_contract.json",
                "coordination_audit_proof.json",
                "coordination_readiness_summary.json",
                "controlled_external_tool_adapter_preview_readiness_bridge.json",
                "manifest.json",
                "full_result.json",
            ]:
                require(errors, (artifact_dir / name).exists(), f"artifact missing {name}")
            manifest = json.loads((artifact_dir / "manifest.json").read_text())
            require(errors, manifest.get("artifact_type") == "station_chief_runtime_v2_4_artifacts", "artifact manifest type mismatch")
            require(errors, manifest.get("runtime_version") == "2.4.0", "artifact manifest runtime_version mismatch")
            for key in [
                "multi_worker_sandbox_coordination_schema",
                "multi_worker_coordination_approval_gate",
                "sandbox_worker_roster",
                "worker_coordination_graph",
                "inter_worker_handoff_contract",
                "multi_worker_dry_run_ledger",
                "coordination_conflict_detector",
                "coordination_abort_contract",
                "coordination_quarantine_contract",
                "coordination_audit_proof",
                "coordination_readiness_summary",
                "controlled_external_tool_adapter_preview_readiness_bridge",
                "multi_worker_sandbox_coordination_preview_only",
                "multi_worker_sandbox_coordination_requires_token",
                "multi_worker_sandbox_coordination_does_not_hire_real_workers",
                "multi_worker_sandbox_coordination_does_not_start_worker_processes",
                "multi_worker_sandbox_coordination_does_not_perform_live_routing",
                "multi_worker_sandbox_coordination_does_not_perform_live_orchestration",
                "multi_worker_sandbox_coordination_does_not_modify_repo_files",
            ]:
                require(errors, manifest.get(key) is True, f"artifact manifest flag mismatch: {key}")
            registry = json.loads((Path(registry_dir) / "run_registry.json").read_text())
            index = json.loads((Path(registry_dir) / "runtime_index.json").read_text())
            require(errors, registry.get("registry_version") == "2.4.0", "registry version mismatch")
            require(errors, len(registry.get("runs", [])) >= 1, "registry runs mismatch")
            require(errors, index.get("index_version") == "2.4.0", "runtime index version mismatch")
            require(errors, index.get("run_count", 0) >= 1, "runtime index run count mismatch")


def validate_regressions(errors: list[str]) -> None:
    commands = [
        (["python3", "10_runtime/station_chief_runtime.py", "--stable-release-manifest"], lambda data: require(errors, data.get("runtime_version") == "2.4.0", "stable manifest runtime version mismatch")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--release-lock"], lambda data: require(errors, "release_lock_bundle" in data, "release lock bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--controlled-execution"], lambda data: require(errors, "controlled_execution_bundle" in data, "controlled execution bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--work-order-executor"], lambda data: require(errors, "work_order_executor_bundle" in data, "work order bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--worker-hiring-registry"], lambda data: require(errors, "worker_hiring_registry_bundle" in data, "worker hiring bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--department-routing"], lambda data: require(errors, "department_routing_bundle" in data, "department routing bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--multi-agent-orchestration"], lambda data: require(errors, "multi_agent_orchestration_bundle" in data, "orchestration bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--operator-console"], lambda data: require(errors, "operator_console_bundle" in data, "operator console bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--github-patch-hardening"], lambda data: require(errors, "github_patch_hardening_bundle" in data, "patch hardening bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--deployment-packaging"], lambda data: require(errors, "deployment_packaging_bundle" in data, "deployment packaging bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--controlled-worker-execution"], lambda data: require(errors, "controlled_worker_execution_bundle" in data, "controlled worker bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--tool-permission-binding"], lambda data: require(errors, "tool_permission_binding_bundle" in data, "tool permission bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--live-telemetry-abort"], lambda data: require(errors, "live_execution_telemetry_abort_bundle" in data, "telemetry abort bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--post-run-audit-expansion", "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION"], lambda data: require(errors, "post_run_audit_expansion_bundle" in data, "post-run audit bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--approval-handoff"], lambda data: require(errors, "approval_handoff_packet" in data, "approval handoff packet missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--plan-repo-patch", "--patch-root", "TEMP_PATCH_ROOT", "--allowed-patch-file", "runtime_patch_preview/station_chief_patch_output.txt", "--dry-run-bundle"], lambda data: require(errors, "dry_run_bundle" in data, "dry-run bundle missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--plan-file-operation", "--execution-dir", "TEMP_EXEC_DIR"], lambda data: require(errors, "file_operation_plan" in data, "file operation plan missing")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--json"], lambda data: require(errors, data.get("station_chief_runtime_version") == "2.4.0", "json runtime version mismatch")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "build controlled external tool adapter preview", "--brief"], lambda data: require(errors, isinstance(data, dict), "brief output invalid")),
        (["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--simulate-adapter"], lambda data: require(errors, isinstance(data, dict), "simulate adapter output invalid")),
    ]
    for args, check in commands:
        code, out, err = run_command(args)
        require(errors, code == 0, f"command failed {' '.join(args)}: {err}")
        data = parse_json(out, ' '.join(args), errors)
        if data is not None:
            check(data)


def validate_documents(errors: list[str]) -> None:
    readme = read_text("10_runtime/station_chief_runtime_readme.md")
    skeleton = read_text("09_exports/station_chief_runtime_skeleton_report.md")
    report = read_text("09_exports/station_chief_runtime_v2_4_report.md")
    for text, label in [
        (readme, "README"),
        (skeleton, "skeleton report"),
        (report, "v2.4 report"),
    ]:
        for banned in ["Explain that", "Include:", "List:", "Write:"]:
            require(errors, banned not in text, f"{label} contains scaffold wording: {banned}")
    readme_needles = [
        "Station Chief Runtime upgraded to v2.4.0.",
        "Multi-worker sandbox coordination added.",
        "post-run audit proof expansion",
        "multi-worker sandbox coordination schema",
        "controlled external tool adapter preview readiness bridge",
        "no broad workforce animation",
        "no external API calls",
        "no external artifact fetching",
        "no actual replay execution",
        "no process termination",
        "no shell command execution",
        "no arbitrary code execution",
        "no repo mutation",
        "no deployment",
        "Station Chief Runtime v2.4.0 adds Multi-Worker Sandbox Coordination without full workforce animation, real worker hiring, worker process creation, live routing, live orchestration, external API calls, or broad execution",
        "Next recommended step: build controlled external tool adapter preview.",
    ]
    skeleton_needles = [
        "Station Chief Runtime upgraded to v2.4.0.",
        "Multi-worker sandbox coordination added.",
        "multi-worker sandbox coordination schema",
        "multi-worker coordination approval gate",
        "sandbox worker roster",
        "worker coordination graph",
        "inter-worker handoff contract",
        "multi-worker dry-run ledger",
        "coordination conflict detector",
        "coordination abort contract",
        "coordination quarantine contract",
        "coordination audit proof",
        "coordination readiness summary",
        "controlled external tool adapter preview readiness bridge",
        "no broad workforce animation",
        "no real worker hiring",
        "no worker process starts",
        "no external API calls",
        "no live worker routing",
        "no live orchestration",
        "no shell command execution",
        "no arbitrary code execution",
        "no repo mutation",
        "no deployment",
        "python3 scripts/validate_station_chief_runtime_v2_4.py",
        "Next recommended build step: build controlled external tool adapter preview.",
    ]
    report_needles = [
        "# Station Chief Runtime v2.4.0 Report",
        "Station Chief Runtime upgraded to v2.4.0. Locked 175-family baseline preserved. Multi-worker sandbox coordination added.",
        "multi-worker sandbox coordination schema",
        "multi-worker coordination approval gate",
        "sandbox worker roster",
        "worker coordination graph",
        "inter-worker handoff contract",
        "multi-worker dry-run ledger",
        "coordination conflict detector",
        "coordination abort contract",
        "coordination quarantine contract",
        "coordination audit proof",
        "coordination readiness summary",
        "controlled external tool adapter preview readiness bridge",
        "no baseline mutation",
        "no Devinization overlay mutation",
        "no live API calls",
        "no worker process starts",
        "no real worker hiring",
        "no live worker routing",
        "no live orchestration",
        "no shell command execution",
        "no arbitrary code execution",
        "no full workforce animation",
        "no repo mutation",
        "Station Chief Runtime v2.4.0 adds Multi-Worker Sandbox Coordination without full workforce animation, real worker hiring, worker process creation, live routing, live orchestration, external API calls, or broad execution",
        "Next recommended build step",
    ]
    for needle in report_needles:
        require(errors, needle in report, f"v2.4 report missing string: {needle}")
    for needle in readme_needles:
        require(errors, needle in readme, f"README missing string: {needle}")
    for needle in skeleton_needles:
        require(errors, needle in skeleton, f"skeleton report missing string: {needle}")


def main() -> None:
    errors: list[str] = []
    validate_files(errors)
    validate_source_strings(errors)
    validate_demo_and_fixture(errors)
    validate_overlay_and_adapter_views(errors)
    validate_schema_views(errors)
    validate_post_run_flow(errors)
    validate_multi_worker_flow(errors)
    validate_write_flows(errors)
    validate_regressions(errors)
    validate_documents(errors)

    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v2.4 runtime files.")
    if errors:
        for error in errors:
            print(error)
        print("FAIL")
        raise SystemExit(1)

    print("PASS: Station Chief Runtime v2.4 valid.")


if __name__ == "__main__":
    main()

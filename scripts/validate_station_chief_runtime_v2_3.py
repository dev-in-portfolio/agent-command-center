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


def run_command(args: list[str]):
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def json_output(output: str, label: str, errors: list[str]):
    try:
        return json.loads(output)
    except Exception as exc:
        errors.append(f"{label}: invalid JSON ({exc})\n{output}")
        return None


def validate_files_exist(errors: list[str]) -> None:
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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v2_3_report.md",
        "scripts/validate_station_chief_runtime_v2_3.py",
    ]
    for rel in required:
        require(errors, (ROOT / rel).exists(), f"Missing file: {rel}")


def validate_source_strings(errors: list[str]) -> None:
    runtime = read_text("10_runtime/station_chief_runtime.py")
    module = read_text("10_runtime/station_chief_post_run_audit_expansion.py")
    adapters = read_text("10_runtime/station_chief_adapters.py")

    for needle in [
        'STATION_CHIEF_RUNTIME_VERSION = "2.3.0"',
        "attach_post_run_audit_expansion",
        "write_post_run_audit_expansion",
        "--post-run-audit-schema",
        "--post-run-audit-expansion",
        "--write-post-run-audit-expansion",
        "--post-run-audit-worker-id",
        "--post-run-audit-confirm-token",
        "--post-run-audit-before-json",
        "--post-run-audit-after-json",
        "--post-run-audit-artifact-name",
        "--post-run-audit-validator-name",
        "--post-run-audit-observed-failure",
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
        "single_worker_post_run_audit_expansion_only",
        "post_run_audit_expansion_requires_token",
        "post_run_audit_expansion_does_not_perform_actual_replay",
        "post_run_audit_expansion_does_not_fetch_external_artifacts",
        "post_run_audit_expansion_does_not_run_shell_commands",
        "post_run_audit_expansion_does_not_modify_repo_files",
        'runtime_status": "post_run_audit_proof_expansion"',
        'station-chief-v2-3-',
        'artifact_type": "station_chief_runtime_v2_3_artifacts"',
        'Next step: build multi-worker sandbox coordination.',
        'post_run_audit_expansion_available',
    ]:
        require(errors, needle in runtime, f"runtime missing string: {needle}")

    for needle in [
        'POST_RUN_AUDIT_EXPANSION_MODULE_VERSION = "2.3.0"',
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
        require(errors, needle in module, f"post-run module missing string: {needle}")

    for needle in [
        'ADAPTER_MODULE_VERSION = "2.3.0"',
        'supports_post_run_audit_expansion',
        'post_run_audit_expansion_requires_specific_token',
        'actual_replay_execution_allowed',
        'external_artifact_fetch_allowed',
        'audit_background_monitoring_allowed',
        'post_run_audit_expansion_requires_separate_gate',
        'YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION',
    ]:
        require(errors, needle in adapters, f"adapter module missing string: {needle}")

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
    ]:
        text = read_text(rel)
        for needle in forbidden_common:
            require(errors, needle not in text, f"forbidden string '{needle}' found in {rel}")

    post_run = read_text("10_runtime/station_chief_post_run_audit_expansion.py")
    for needle in ["eval(", "exec(", "compile(", "open(", "socket", "http.server", "socketserver", "uvicorn", "streamlit", "netlify", "vercel", "cloudflare", "firebase", "railway", "render", "gh api", "git push", "create_deployment", "create_commit", "update_ref", "__import__", "threading", "multiprocessing", "kill(", "terminate("]:
        require(errors, needle not in post_run, f"forbidden string '{needle}' found in post-run module")


def validate_demo_and_fixture(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "2.3.0", "demo runtime version mismatch")
        require(errors, demo.get("runtime_status") == "post_run_audit_proof_expansion", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "demo baseline_preserved mismatch")
        require(errors, evidence.get("external_actions_taken") is False, "demo external_actions_taken mismatch")
        require(errors, evidence.get("live_worker_agents_activated") is False, "demo live_worker_agents_activated mismatch")
        for key in [
            "post_run_audit_expansion_available",
            "single_worker_post_run_audit_expansion_only",
            "post_run_audit_expansion_requires_token",
            "post_run_audit_expansion_does_not_perform_actual_replay",
            "post_run_audit_expansion_does_not_fetch_external_artifacts",
            "post_run_audit_expansion_does_not_run_shell_commands",
            "post_run_audit_expansion_does_not_modify_repo_files",
            "multi_worker_sandbox_coordination_not_yet_active",
        ]:
            require(errors, evidence.get(key) is True, f"demo evidence {key} mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture status mismatch")
        require(errors, fixture.get("runtime_version") == "2.3.0", "fixture runtime version mismatch")
        require(errors, fixture.get("case_count") == 5, "fixture case_count mismatch")
        require(errors, fixture.get("failed") == 0, "fixture failed mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: {err}")
    fixture_runner = json_output(out, "fixture runner", errors)
    if fixture_runner:
        require(errors, fixture_runner.get("fixture_test_status") == "PASS", "fixture runner status mismatch")
        require(errors, fixture_runner.get("runtime_version") == "2.3.0", "fixture runner version mismatch")
        require(errors, fixture_runner.get("case_count") == 5, "fixture runner case_count mismatch")
        require(errors, fixture_runner.get("failed") == 0, "fixture runner failed mismatch")


def validate_overlays_and_adapters(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-overlays"])
    require(errors, code == 0, f"--list-overlays failed: {err}")
    overlays = json_output(out, "--list-overlays", errors)
    if overlays is not None:
        require(errors, len(overlays) == 8, f"overlay count mismatch: {len(overlays)}")
        for overlay in overlays:
            require(errors, overlay.get("exists") is True, f"overlay {overlay.get('id')} missing")
            require(errors, overlay.get("preserves_locked_baseline") is True, f"overlay {overlay.get('id')} baseline flag mismatch")
            require(errors, "Devin O’Rourke" in (overlay.get("ownership_project_owner") or ""), f"overlay {overlay.get('id')} owner mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: {err}")
    adapters = json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "2.3.0", "adapter module version mismatch")
        supported = adapters.get("supported_adapters", {})
        noop = supported.get("noop", {})
        scoped = supported.get("scoped_repo_patch", {})
        require(errors, noop.get("supports_post_run_audit_expansion") is True, "noop post-run support mismatch")
        require(errors, scoped.get("supports_post_run_audit_expansion") is False, "scoped post-run support mismatch")
        require(errors, scoped.get("post_run_audit_expansion_requires_separate_gate") is True, "scoped separate gate mismatch")
        require(errors, noop.get("actual_replay_execution_allowed") is False, "noop actual replay mismatch")
        require(errors, noop.get("external_artifact_fetch_allowed") is False, "noop external artifact fetch mismatch")
        require(errors, noop.get("audit_background_monitoring_allowed") is False, "noop background monitoring mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-execution-profiles"])
    require(errors, code == 0, f"--list-execution-profiles failed: {err}")
    profiles = json_output(out, "--list-execution-profiles", errors)
    if profiles:
        require(errors, profiles.get("execution_profile_module_version") == "2.3.0", "execution profile version mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-controlled-execution-profiles"])
    require(errors, code == 0, f"--list-controlled-execution-profiles failed: {err}")
    cprofiles = json_output(out, "--list-controlled-execution-profiles", errors)
    if cprofiles:
        require(errors, cprofiles.get("controlled_execution_profile_catalog_version") == "2.3.0", "controlled execution profile version mismatch")


def validate_post_run_schema_and_behaviour(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--post-run-audit-schema"])
    require(errors, code == 0, f"--post-run-audit-schema failed: {err}")
    schema = json_output(out, "--post-run-audit-schema", errors)
    if schema:
        require(errors, schema.get("post_run_audit_expansion_schema_version") == "2.3.0", "post-run schema version mismatch")
        require(errors, schema.get("schema_status") == "SINGLE_WORKER_POST_RUN_AUDIT_EXPANSION_ONLY", "post-run schema status mismatch")
        req_sections = set(schema.get("required_sections", []))
        for section in ["expanded_audit_evidence_schema", "post_run_audit_approval_gate", "before_after_run_comparison_proof", "validator_backed_audit_artifact_index", "audit_replay_record", "failure_class_taxonomy", "human_review_packet", "audit_integrity_score", "audit_evidence_ledger", "audit_expansion_readiness_summary", "multi_worker_sandbox_coordination_readiness_bridge"]:
            require(errors, section in req_sections, f"post-run schema missing {section}")
        allowed = set(schema.get("allowed_audit_modes", []))
        blocked = set(schema.get("blocked_audit_modes", []))
        require(errors, "local_audit_preview" in allowed, "allowed audit mode missing local_audit_preview")
        require(errors, "approved_single_worker_audit_expansion_records" in allowed, "allowed audit mode missing approved_single_worker_audit_expansion_records")
        for item in ["actual_replay_execution", "external_artifact_fetch", "shell_command_replay", "background_audit_monitoring"]:
            require(errors, item in blocked, f"blocked audit mode missing {item}")
        require(errors, "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION" in set(schema.get("required_confirmation_tokens", [])), "required token missing")
        require(errors, schema.get("baseline_preserved") is True, "schema baseline mismatch")
        require(errors, schema.get("external_actions_taken") is False, "schema external actions mismatch")
        require(errors, schema.get("actual_replay_performed") is False, "schema replay mismatch")
        require(errors, schema.get("repo_files_modified") is False, "schema repo mutation mismatch")
        require(errors, schema.get("external_artifact_fetch_performed") is False, "schema artifact fetch mismatch")
        require(errors, schema.get("broad_worker_activation_performed") is False, "schema broad worker mismatch")
        require(errors, schema.get("execution_authorized") is False, "schema execution authorized mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--post-run-audit-expansion"])
    require(errors, code == 0, f"post-run default failed: {err}")
    default = json_output(out, "post-run default", errors)
    if default:
        for key in ["post_run_audit_expansion_bundle", "post_run_audit_expansion_schema", "expanded_audit_evidence_schema", "post_run_audit_approval_gate", "before_after_run_comparison_proof", "validator_backed_audit_artifact_index", "audit_replay_record", "failure_class_taxonomy", "human_review_packet", "audit_integrity_score", "audit_evidence_ledger", "audit_expansion_readiness_summary", "multi_worker_sandbox_coordination_readiness_bridge"]:
            require(errors, key in default, f"default post-run missing {key}")
        require(errors, default["post_run_audit_expansion_bundle"]["post_run_audit_expansion_bundle_version"] == "2.3.0", "default bundle version mismatch")
        require(errors, default["post_run_audit_approval_gate"]["gate_status"] == "BLOCKED_PENDING_POST_RUN_AUDIT_EXPANSION_APPROVAL", "default gate mismatch")
        require(errors, default["post_run_audit_approval_gate"]["confirmation_token_valid"] is False, "default token validity mismatch")
        require(errors, default["before_after_run_comparison_proof"]["comparison_status"] == "BLOCKED", "default comparison mismatch")
        require(errors, default["audit_replay_record"]["replay_status"] == "BLOCKED", "default replay mismatch")
        require(errors, default["human_review_packet"]["packet_status"] == "BLOCKED", "default packet mismatch")
        require(errors, default["audit_integrity_score"]["integrity_status"] == "BLOCKED", "default integrity mismatch")
        require(errors, default["audit_expansion_readiness_summary"]["readiness_status"] == "BLOCKED", "default readiness mismatch")
        require(errors, default["post_run_audit_expansion_bundle"]["external_actions_taken"] is False, "default external actions")
        require(errors, default["post_run_audit_expansion_bundle"]["actual_replay_performed"] is False, "default replay performed")
        require(errors, default["post_run_audit_expansion_bundle"]["external_artifact_fetch_performed"] is False, "default external fetch")
        require(errors, default["post_run_audit_expansion_bundle"]["repo_files_modified"] is False, "default repo mutation")
        require(errors, default["post_run_audit_expansion_bundle"]["execution_authorized"] is False, "default execution authorization")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--post-run-audit-expansion", "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION"])
    require(errors, code == 0, f"post-run valid failed: {err}")
    valid = json_output(out, "post-run valid", errors)
    if valid:
        require(errors, valid["post_run_audit_approval_gate"]["gate_status"] == "APPROVED_FOR_SINGLE_WORKER_POST_RUN_AUDIT_EXPANSION_RECORDS", "valid gate mismatch")
        require(errors, valid["post_run_audit_approval_gate"]["confirmation_token_valid"] is True, "valid token mismatch")
        require(errors, valid["before_after_run_comparison_proof"]["comparison_status"] == "CREATED", "valid comparison mismatch")
        require(errors, valid["validator_backed_audit_artifact_index"]["index_status"] == "INDEX_CREATED", "valid index mismatch")
        require(errors, valid["audit_replay_record"]["replay_status"] == "REPLAY_RECORD_CREATED", "valid replay mismatch")
        require(errors, valid["failure_class_taxonomy"]["taxonomy_status"] == "TAXONOMY_CREATED", "valid taxonomy mismatch")
        require(errors, valid["human_review_packet"]["packet_status"] == "READY_FOR_HUMAN_REVIEW", "valid packet mismatch")
        require(errors, valid["audit_integrity_score"]["integrity_status"] == "PASS", "valid integrity mismatch")
        require(errors, valid["audit_evidence_ledger"]["ledger_status"] == "SINGLE_WORKER_POST_RUN_AUDIT_LEDGER", "valid ledger mismatch")
        require(errors, valid["audit_expansion_readiness_summary"]["ready_for_multi_worker_sandbox_coordination"] is True, "valid readiness mismatch")
        require(errors, valid["multi_worker_sandbox_coordination_readiness_bridge"]["next_layer"] == "Multi-Worker Sandbox Coordination", "valid next layer mismatch")
        require(errors, valid["multi_worker_sandbox_coordination_readiness_bridge"]["ready_for_multi_worker_sandbox_coordination"] is True, "valid bridge readiness mismatch")
        require(errors, valid["post_run_audit_expansion_bundle"]["external_actions_taken"] is False, "valid external actions")
        require(errors, valid["post_run_audit_expansion_bundle"]["actual_replay_performed"] is False, "valid replay performed")
        require(errors, valid["post_run_audit_expansion_bundle"]["external_artifact_fetch_performed"] is False, "valid external fetch")
        require(errors, valid["post_run_audit_expansion_bundle"]["repo_files_modified"] is False, "valid repo mutation")
        require(errors, valid["post_run_audit_expansion_bundle"]["execution_authorized"] is False, "valid execution authorization")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--post-run-audit-expansion", "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION", "--post-run-audit-observed-failure", "digest_mismatch"])
    require(errors, code == 0, f"post-run failure failed: {err}")
    failure_case = json_output(out, "post-run failure", errors)
    if failure_case:
        require(errors, failure_case["failure_class_taxonomy"]["failure_count"] == 1, "failure count mismatch")
        require(errors, "digest_mismatch" in failure_case["failure_class_taxonomy"]["classified_failures"], "digest mismatch not classified")
        require(errors, failure_case["audit_integrity_score"]["integrity_score"] < 100, "integrity not lowered")
        require(errors, failure_case["post_run_audit_expansion_bundle"]["external_actions_taken"] is False, "failure external actions")
        require(errors, failure_case["post_run_audit_expansion_bundle"]["actual_replay_performed"] is False, "failure replay")
        require(errors, failure_case["post_run_audit_expansion_bundle"]["repo_files_modified"] is False, "failure repo mutation")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--post-run-audit-expansion", "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION", "--post-run-audit-before-json", '{"a":1}', "--post-run-audit-after-json", '{"a":1,"b":2}'])
    require(errors, code == 0, f"post-run comparison failed: {err}")
    comparison_case = json_output(out, "post-run comparison", errors)
    if comparison_case:
        proof = comparison_case["before_after_run_comparison_proof"]
        require(errors, proof["comparison_status"] == "CREATED", "comparison status mismatch")
        require(errors, "b" in proof["added_top_level_keys"], "comparison added key b missing")
        require(errors, proof["git_diff_performed"] is False, "comparison git diff mismatch")
        require(errors, proof["filesystem_read"] is False, "comparison filesystem read mismatch")
        require(errors, comparison_case["post_run_audit_expansion_bundle"]["external_actions_taken"] is False, "comparison external actions")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build multi-worker sandbox coordination", "--post-run-audit-expansion", "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION"])
    require(errors, code == 0, f"post-run next layer failed: {err}")
    next_layer = json_output(out, "post-run next layer", errors)
    if next_layer:
        require(errors, next_layer["multi_worker_sandbox_coordination_readiness_bridge"]["next_layer"] == "Multi-Worker Sandbox Coordination", "next layer bridge mismatch")
        require(errors, next_layer["multi_worker_sandbox_coordination_readiness_bridge"]["ready_for_multi_worker_sandbox_coordination"] is True, "next layer bridge readiness mismatch")
        require(errors, next_layer["audit_expansion_readiness_summary"]["next_layer"] == "Multi-Worker Sandbox Coordination", "next layer summary mismatch")
        require(errors, next_layer["audit_expansion_readiness_summary"]["readiness_status"] == "READY_FOR_NEXT_LAYER", "next layer readiness status mismatch")
        require(errors, next_layer["audit_integrity_score"]["integrity_status"] == "PASS", "next layer integrity mismatch")


def validate_write_paths(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        post_dir = tmp_path / "post_run"
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-post-run-audit-expansion", str(post_dir),
            "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION",
        ])
        require(errors, code == 0, f"write-post-run failed: {err}")
        written = json_output(out, "write-post-run", errors)
        if written:
            require(errors, "post_run_audit_expansion_write_summary" in written, "write summary missing")
            summary = written["post_run_audit_expansion_write_summary"]
            artifact_dir = Path(summary["post_run_audit_expansion_dir"])
            require(errors, artifact_dir.exists(), "post-run artifact dir missing")
            expected = [
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
            ]
            require(errors, summary["files_written"] == expected, "write-post-run files mismatch")
            manifest = json.loads((artifact_dir / "post_run_audit_expansion_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "2.3.0", "post-run manifest runtime version mismatch")
            require(errors, manifest.get("status") == "SINGLE_WORKER_POST_RUN_AUDIT_EXPANSION_ONLY", "post-run manifest status mismatch")
            require(errors, manifest.get("external_actions_taken") is False, "post-run manifest external actions")
            require(errors, manifest.get("actual_replay_performed") is False, "post-run manifest replay")
            require(errors, manifest.get("external_artifact_fetch_performed") is False, "post-run manifest artifact fetch")
            require(errors, manifest.get("repo_files_modified") is False, "post-run manifest repo mutation")
            require(errors, manifest.get("execution_authorized") is False, "post-run manifest execution")

        run_dir = tmp_path / "runs"
        registry_dir = tmp_path / "registry"
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(run_dir),
            "--registry-dir", str(registry_dir),
            "--post-run-audit-expansion",
            "--post-run-audit-confirm-token", "YES_I_APPROVE_POST_RUN_AUDIT_PROOF_EXPANSION",
        ])
        require(errors, code == 0, f"write-artifacts failed: {err}")
        result = json_output(out, "write-artifacts", errors)
        if result:
            require(errors, "artifact_write_summary" in result, "artifact_write_summary missing")
            summary = result["artifact_write_summary"]
            require(errors, summary["run_id"].startswith("station-chief-v2-3-check-please-"), "run id prefix mismatch")
            artifact_dir = Path(summary["artifact_dir"])
            require(errors, artifact_dir.exists(), "artifact dir missing")
            for filename in [
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
                "manifest.json",
                "full_result.json",
            ]:
                require(errors, (artifact_dir / filename).exists(), f"missing artifact file {filename}")
            manifest = json.loads((artifact_dir / "manifest.json").read_text())
            require(errors, manifest.get("artifact_type") == "station_chief_runtime_v2_3_artifacts", "artifact manifest type mismatch")
            require(errors, manifest.get("runtime_version") == "2.3.0", "artifact manifest version mismatch")
            for key in [
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
                "single_worker_post_run_audit_expansion_only",
                "post_run_audit_expansion_requires_token",
                "post_run_audit_expansion_does_not_perform_actual_replay",
                "post_run_audit_expansion_does_not_fetch_external_artifacts",
                "post_run_audit_expansion_does_not_run_shell_commands",
                "post_run_audit_expansion_does_not_modify_repo_files",
            ]:
                require(errors, manifest.get(key) is True, f"artifact manifest missing {key}")
            registry = json.loads((registry_dir / "run_registry.json").read_text())
            index = json.loads((registry_dir / "runtime_index.json").read_text())
            require(errors, registry.get("registry_version") == "2.3.0", "registry version mismatch")
            require(errors, len(registry.get("runs", [])) >= 1, "registry runs missing")
            require(errors, index.get("index_version") == "2.3.0", "runtime index version mismatch")
            require(errors, index.get("run_count", 0) >= 1, "runtime index count missing")


def validate_regression_commands(errors: list[str]) -> None:
    commands = [
        ["python3", "10_runtime/station_chief_runtime.py", "--stable-release-manifest"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--release-lock"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--controlled-execution"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--work-order-executor"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--worker-hiring-registry"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--department-routing"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--multi-agent-orchestration"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--operator-console"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--github-patch-hardening"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--deployment-packaging"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--controlled-worker-execution"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--tool-permission-binding"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--live-telemetry-abort"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--approval-handoff"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--plan-repo-patch", "--patch-root", str(ROOT / "tmp_patch_root_should_not_exist"), "--allowed-patch-file", "runtime_patch_preview/station_chief_patch_output.txt", "--dry-run-bundle"],
        ["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--plan-file-operation", "--execution-dir", str(ROOT / "tmp_exec_dir_should_not_exist")],
    ]
    for cmd in commands:
        code, out, err = run_command(cmd)
        require(errors, code == 0, f"command failed: {' '.join(cmd)} :: {err}")
        parsed = json_output(out, "regression command", errors)
        if parsed is None:
            continue
        joined = " ".join(cmd)
        if "--stable-release-manifest" in joined:
            require(errors, parsed.get("runtime_version") == "2.3.0", "stable release manifest version mismatch")
        elif "--release-lock" in joined:
            require(errors, "release_lock_bundle" in parsed, "release lock bundle missing")
        elif "--controlled-execution" in joined:
            require(errors, "controlled_execution_bundle" in parsed, "controlled execution bundle missing")
        elif "--work-order-executor" in joined:
            require(errors, "work_order_executor_bundle" in parsed, "work order executor bundle missing")
        elif "--worker-hiring-registry" in joined:
            require(errors, "worker_hiring_registry_bundle" in parsed, "worker hiring registry bundle missing")
        elif "--department-routing" in joined:
            require(errors, "department_routing_bundle" in parsed, "department routing bundle missing")
        elif "--multi-agent-orchestration" in joined:
            require(errors, "multi_agent_orchestration_bundle" in parsed, "multi-agent orchestration bundle missing")
        elif "--operator-console" in joined:
            require(errors, "operator_console_bundle" in parsed, "operator console bundle missing")
        elif "--github-patch-hardening" in joined:
            require(errors, "github_patch_hardening_bundle" in parsed, "github patch hardening bundle missing")
        elif "--deployment-packaging" in joined:
            require(errors, "deployment_packaging_bundle" in parsed, "deployment packaging bundle missing")
        elif "--controlled-worker-execution" in joined:
            require(errors, "controlled_worker_execution_bundle" in parsed, "controlled worker bundle missing")
        elif "--tool-permission-binding" in joined:
            require(errors, "tool_permission_binding_bundle" in parsed, "tool permission bundle missing")
        elif "--live-telemetry-abort" in joined:
            require(errors, "live_execution_telemetry_abort_bundle" in parsed, "telemetry bundle missing")
        elif "--approval-handoff" in joined:
            require(errors, "approval_handoff_packet" in parsed, "approval handoff packet missing")


def validate_docs(errors: list[str]) -> None:
    readme = read_text("10_runtime/station_chief_runtime_readme.md")
    for phrase in [
        "Station Chief Runtime upgraded to v2.3.0.",
        "Post-run audit proof expansion added.",
        "post-run audit expansion schema",
        "expanded audit evidence schema",
        "post-run audit approval gate",
        "before/after run comparison proof",
        "validator-backed audit artifact index",
        "audit replay record",
        "failure-class taxonomy",
        "human review packet",
        "audit integrity score",
        "audit evidence ledger",
        "audit expansion readiness summary",
        "multi-worker sandbox coordination readiness bridge",
        "no broad workforce animation",
        "no external API calls",
        "no external artifact fetching",
        "no actual replay execution",
        "no process termination",
        "no shell command execution",
        "no arbitrary code execution",
        "no repo mutation",
        "no deployment",
    ]:
        require(errors, phrase in readme, f"readme missing phrase: {phrase}")
    for forbidden in ["Explain that", "Include:", "List:", "Write:"]:
        require(errors, forbidden not in readme, f"readme contains scaffold text: {forbidden}")
    require(errors, "Station Chief Runtime v2.3.0 adds Post-Run Audit Proof Expansion without actual replay execution, external artifact fetching, background monitoring, or broad execution" in readme, "readme doctrine missing")

    skeleton = read_text("09_exports/station_chief_runtime_skeleton_report.md")
    for phrase in [
        "Station Chief Runtime upgraded to v2.3.0.",
        "Post-run audit proof expansion added.",
        "post-run audit expansion schema",
        "expanded audit evidence schema",
        "post-run audit approval gate",
        "before/after run comparison proof",
        "validator-backed audit artifact index",
        "audit replay record",
        "failure-class taxonomy",
        "human review packet",
        "audit integrity score",
        "audit evidence ledger",
        "audit expansion readiness summary",
        "multi-worker sandbox coordination readiness bridge",
        "no broad workforce animation",
        "no external API calls",
        "no external artifact fetching",
        "no actual replay execution",
        "no process termination",
        "no shell command execution",
        "no arbitrary code execution",
        "no repo mutation",
        "no deployment",
    ]:
        require(errors, phrase in skeleton, f"skeleton missing phrase: {phrase}")
    for forbidden in ["Explain that", "Include:", "List:", "Write:"]:
        require(errors, forbidden not in skeleton, f"skeleton contains scaffold text: {forbidden}")
    require(errors, "python3 scripts/validate_station_chief_runtime_v2_3.py" in skeleton, "skeleton missing v2.3 validator")
    require(errors, "Next recommended build step: build multi-worker sandbox coordination." in skeleton, "skeleton missing next step")

    report = read_text("09_exports/station_chief_runtime_v2_3_report.md")
    for phrase in [
        "Station Chief Runtime v2.3.0 Report",
        "Station Chief Runtime upgraded to v2.3.0. Locked 175-family baseline preserved. Post-run audit proof expansion added.",
        "post-run audit expansion schema",
        "expanded audit evidence schema",
        "post-run audit approval gate",
        "before/after run comparison proof",
        "validator-backed audit artifact index",
        "audit replay record",
        "failure-class taxonomy",
        "human review packet",
        "audit integrity score",
        "audit evidence ledger",
        "audit expansion readiness summary",
        "multi-worker sandbox coordination readiness bridge",
        "no baseline mutation",
        "no Devinization overlay mutation",
        "no live API calls",
        "no external artifact fetching",
        "no actual replay execution",
        "no process termination",
        "no shell command execution",
        "no arbitrary code execution",
        "no full workforce animation",
        "no real worker hiring",
        "no repo mutation",
        "Station Chief Runtime v2.3.0 adds Post-Run Audit Proof Expansion without actual replay execution, external artifact fetching, background monitoring, or broad execution",
        "Next recommended build step",
    ]:
        require(errors, phrase in report, f"v2.3 report missing phrase: {phrase}")


def main() -> None:
    errors: list[str] = []
    validate_files_exist(errors)
    if not errors:
        validate_source_strings(errors)
    if not errors:
        validate_demo_and_fixture(errors)
    if not errors:
        validate_overlays_and_adapters(errors)
    if not errors:
        validate_post_run_schema_and_behaviour(errors)
    if not errors:
        validate_write_paths(errors)
    if not errors:
        validate_regression_commands(errors)
    if not errors:
        validate_docs(errors)

    if errors:
        for error in errors:
            print(error)
        print("FAIL")
        sys.exit(1)

    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v2.3 runtime files.")
    print("PASS: Station Chief Runtime v2.3 valid.")


if __name__ == "__main__":
    main()

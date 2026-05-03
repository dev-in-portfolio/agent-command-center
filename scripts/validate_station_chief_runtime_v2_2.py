#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    result = subprocess.run(cmd, cwd=cwd or REPO_ROOT, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

def parse_json_output(output: str, context: str, errors: list[str]) -> dict | list | None:
    try:
        start_idx = output.find('{')
        start_idx_list = output.find('[')
        if start_idx == -1 and start_idx_list == -1:
            errors.append(f"No JSON found in output from {context}")
            return None
        if start_idx != -1 and start_idx_list != -1:
            start_idx = min(start_idx, start_idx_list)
        elif start_idx == -1:
            start_idx = start_idx_list
        json_str = output[start_idx:]
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        errors.append(f"Failed to parse JSON output from {context}: {e}")
        return None

def check_contains(errors: list[str], file_path: Path, expected_strings: list[str], exclude: list[str] | None = None) -> None:
    if not file_path.exists():
        errors.append(f"Missing file: {file_path}")
        return
    content = file_path.read_text(encoding="utf-8")
    for s in expected_strings:
        if s not in content:
            errors.append(f"{file_path.name} missing expected string: '{s}'")
    if exclude:
        for s in exclude:
            if s == "deploy":
                if re.search(r"\bdeploy\b", content):
                    errors.append(f"{file_path.name} contains forbidden word: '{s}'")
            elif s in content:
                errors.append(f"{file_path.name} contains forbidden string: '{s}'")

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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v2_2_report.md",
        "scripts/validate_station_chief_runtime_v2_2.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    telemetry_path = REPO_ROOT / "10_runtime/station_chief_live_execution_telemetry_abort.py"
    
    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "2.2.0"',
            "attach_live_execution_telemetry_abort",
            "write_live_execution_telemetry_abort",
            "--telemetry-abort-schema",
            "--live-telemetry-abort",
            "--write-live-telemetry-abort",
            "--telemetry-worker-id",
            "--telemetry-confirm-token",
            "--telemetry-abort-reason",
            "--telemetry-failure-reason",
            "--telemetry-timeout-limit-steps",
            "--telemetry-observed-steps",
            "--telemetry-partial-payload-json",
            "live_execution_telemetry_abort_bundle",
            "live_execution_telemetry_abort_schema",
            "telemetry_event_schema",
            "execution_state_model",
            "telemetry_approval_gate",
            "heartbeat_stub",
            "abort_signal_contract",
            "timeout_contract",
            "partial_result_capture",
            "failed_run_quarantine_contract",
            "post_abort_audit_proof",
            "telemetry_ledger",
            "telemetry_readiness_summary",
            "post_run_audit_expansion_readiness_bridge",
            "single_worker_telemetry_abort_controls_only",
            "telemetry_abort_controls_require_token",
            "telemetry_abort_does_not_send_external_telemetry",
            "telemetry_abort_does_not_terminate_processes",
            "telemetry_abort_does_not_run_shell_commands",
            "telemetry_abort_does_not_modify_repo_files"
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess", "netlify", "vercel", "cloudflare", "firebase", "railway", "render"]
    )

    check_contains(
        errors,
        telemetry_path,
        [
            'LIVE_EXECUTION_TELEMETRY_ABORT_MODULE_VERSION = "2.2.0"',
            "LIVE_EXECUTION_TELEMETRY_ABORT_STATUS",
            "LIVE_EXECUTION_TELEMETRY_ABORT_PHASE",
            "LIVE_EXECUTION_TELEMETRY_ABORT_APPROVAL_TOKEN",
            "canonical_json",
            "sha256_digest",
            "normalize_telemetry_label",
            "generate_telemetry_abort_id",
            "create_live_execution_telemetry_abort_schema",
            "create_telemetry_event_schema",
            "create_execution_state_model",
            "create_telemetry_approval_gate",
            "create_heartbeat_stub",
            "create_abort_signal_contract",
            "create_timeout_contract",
            "create_partial_result_capture",
            "create_failed_run_quarantine_contract",
            "create_post_abort_audit_proof",
            "create_telemetry_ledger",
            "create_telemetry_readiness_summary",
            "create_post_run_audit_expansion_readiness_bridge",
            "create_live_execution_telemetry_abort_bundle"
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess", "eval(", "exec(", "compile(", "socket", "http.server", "socketserver", "uvicorn", "streamlit", "netlify", "vercel", "cloudflare", "firebase", "railway", "render", "__import__", "threading", "multiprocessing", "kill(", "terminate("]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "2.2.0", "demo runtime version != 2.2.0")
        require(errors, demo.get("runtime_status") == "live_execution_telemetry_abort_controls", "demo runtime_status mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("live_execution_telemetry_abort_available") is True, "evidence available True")
        require(errors, evidence.get("single_worker_telemetry_abort_controls_only") is True, "evidence single_worker True")
        require(errors, evidence.get("telemetry_abort_controls_require_token") is True, "evidence require_token True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "2.2.0", "fixture runtime_version != 2.2.0")

    # Telemetry/abort default without token
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--live-telemetry-abort"
    ])
    require(errors, code == 0, f"default telemetry-abort failed: {err}")
    res = parse_json_output(out, "default telemetry-abort", errors)
    if res:
        require(errors, "live_execution_telemetry_abort_bundle" in res, "bundle missing")
        require(errors, res.get("telemetry_approval_gate", {}).get("confirmation_token_valid") is False, "token valid mismatch")
        require(errors, res.get("post_abort_audit_proof", {}).get("audit_status") == "BLOCKED", "audit status mismatch")

    # Telemetry/abort with valid token
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--live-telemetry-abort",
        "--telemetry-confirm-token", "YES_I_APPROVE_SINGLE_WORKER_TELEMETRY_ABORT_CONTROLS"
    ])
    require(errors, code == 0, f"approved telemetry-abort failed: {err}")
    res = parse_json_output(out, "approved telemetry-abort", errors)
    if res:
        require(errors, res.get("telemetry_approval_gate", {}).get("confirmation_token_valid") is True, "token valid mismatch")
        require(errors, res.get("post_abort_audit_proof", {}).get("audit_status") == "PASS", "audit status mismatch")
        require(errors, res.get("telemetry_readiness_summary", {}).get("ready_for_post_run_audit_proof_expansion") is True, "ready mismatch")

    # Timeout record
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--live-telemetry-abort",
        "--telemetry-confirm-token", "YES_I_APPROVE_SINGLE_WORKER_TELEMETRY_ABORT_CONTROLS",
        "--telemetry-timeout-limit-steps", "2",
        "--telemetry-observed-steps", "5"
    ])
    require(errors, code == 0, f"timeout record failed: {err}")
    res = parse_json_output(out, "timeout record", errors)
    if res:
        require(errors, res.get("timeout_contract", {}).get("timeout_triggered") is True, "timeout triggered mismatch")

    # Artifact writing
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--live-telemetry-abort",
            "--telemetry-confirm-token", "YES_I_APPROVE_SINGLE_WORKER_TELEMETRY_ABORT_CONTROLS"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v2-2-check-please-"), f"run_id {run_id} format mismatch")
            
            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v2_2_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "2.2.0", "man version mismatch")
                require(errors, man.get("post_abort_audit_proof") is True, "man audit_proof True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "2.2.0", "rr version mismatch")

def main():
    print("Running validate_station_chief_runtime_v2_2.py...")
    errors = []
    
    validate_files_exist(errors)
    if not errors:
        validate_source_files(errors)
    if not errors:
        validate_commands_and_behavior(errors)

    if errors:
        print("FAIL")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
        
    print("PASS: Station Chief Runtime v2.2 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v2.2 runtime files.")

if __name__ == "__main__":
    main()

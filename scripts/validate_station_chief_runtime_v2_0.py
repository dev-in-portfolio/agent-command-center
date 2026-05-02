#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
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
            if s in content:
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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v2_0_report.md",
        "scripts/validate_station_chief_runtime_v2_0.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    worker_exec_path = REPO_ROOT / "10_runtime/station_chief_controlled_worker_execution.py"
    
    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "2.0.0"',
            "attach_controlled_worker_execution",
            "write_controlled_worker_execution",
            "--controlled-worker-schema",
            "--controlled-worker-execution",
            "--write-controlled-worker-execution",
            "--controlled-worker-id",
            "--controlled-worker-task",
            "--controlled-worker-payload-json",
            "--controlled-worker-tool-permission",
            "--confirm-controlled-worker-execution",
            "controlled_worker_execution_bundle",
            "controlled_worker_execution_schema",
            "worker_execution_gate",
            "tool_permission_binding",
            "sandbox_worker_task",
            "worker_abort_contract",
            "worker_rollback_contract",
            "worker_execution_telemetry_stub",
            "controlled_worker_execution_result",
            "post_run_audit_proof",
            "worker_execution_ledger",
            "single_worker_tool_permission_binding_readiness_bridge",
            "single_worker_sandbox_execution_only",
            "controlled_worker_execution_requires_token",
            "controlled_worker_execution_does_not_call_external_apis",
            "controlled_worker_execution_does_not_run_shell_commands",
            "controlled_worker_execution_does_not_modify_repo_files",
            "controlled_worker_execution_does_not_animate_broad_workforce"
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess", "netlify", "vercel", "cloudflare", "firebase", "railway", "render"]
    )

    check_contains(
        errors,
        worker_exec_path,
        [
            'CONTROLLED_WORKER_EXECUTION_MODULE_VERSION = "2.0.0"',
            "CONTROLLED_WORKER_EXECUTION_STATUS",
            "CONTROLLED_WORKER_EXECUTION_PHASE",
            "FIRST_CONTROLLED_WORKER_EXECUTION_TOKEN",
            "canonical_json",
            "sha256_digest",
            "normalize_worker_execution_label",
            "generate_worker_execution_run_id",
            "create_controlled_worker_execution_schema",
            "create_worker_execution_gate",
            "create_tool_permission_binding",
            "create_sandbox_worker_task",
            "create_worker_abort_contract",
            "create_worker_rollback_contract",
            "create_worker_execution_telemetry_stub",
            "run_single_worker_sandbox_task",
            "create_post_run_audit_proof",
            "create_worker_execution_ledger",
            "create_single_worker_tool_permission_binding_readiness_bridge",
            "create_controlled_worker_execution_bundle"
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess", "eval(", "exec(", "compile(", "socket", "http.server", "socketserver", "uvicorn", "streamlit", "netlify", "vercel", "cloudflare", "firebase", "railway", "render"]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "2.0.0", "demo runtime version != 2.0.0")
        require(errors, demo.get("runtime_status") == "first_controlled_worker_execution", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("controlled_worker_execution_available") is True, "evidence available True")
        require(errors, evidence.get("single_worker_sandbox_execution_only") is True, "evidence single_worker True")
        require(errors, evidence.get("controlled_worker_execution_requires_token") is True, "evidence requires_token True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "2.0.0", "fixture runtime_version != 2.0.0")

    # Controlled worker execution default without token
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--controlled-worker-execution"])
    require(errors, code == 0, f"default controlled-worker failed: {err}")
    res = parse_json_output(out, "default controlled-worker", errors)
    if res:
        require(errors, "controlled_worker_execution_bundle" in res, "bundle missing")
        bundle = res["controlled_worker_execution_bundle"]
        require(errors, bundle.get("controlled_worker_execution_bundle_version") == "2.0.0", "bundle version mismatch")
        require(errors, res.get("worker_execution_gate", {}).get("gate_status") == "BLOCKED_PENDING_FIRST_WORKER_APPROVAL", "gate status mismatch")
        require(errors, res.get("controlled_worker_execution_result", {}).get("result_status") == "BLOCKED_NOT_EXECUTED", "result status mismatch")

    # Controlled worker execution with approval token
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--controlled-worker-execution",
        "--controlled-worker-task", "echo_command_summary",
        "--confirm-controlled-worker-execution", "YES_I_APPROVE_FIRST_CONTROLLED_WORKER_EXECUTION"
    ])
    require(errors, code == 0, f"approved controlled-worker failed: {err}")
    res = parse_json_output(out, "approved controlled-worker", errors)
    if res:
        require(errors, res.get("worker_execution_gate", {}).get("gate_status") == "APPROVED_FOR_SINGLE_WORKER_SANDBOX_EXECUTION", "gate status mismatch")
        require(errors, res.get("controlled_worker_execution_result", {}).get("result_status") == "SANDBOX_EXECUTED", "result status mismatch")
        require(errors, res.get("controlled_worker_execution_result", {}).get("single_worker_sandbox_execution_performed") is True, "execution_performed mismatch")
        require(errors, res.get("post_run_audit_proof", {}).get("audit_status") == "PASS", "audit status mismatch")
        require(errors, res.get("single_worker_tool_permission_binding_readiness_bridge", {}).get("ready_for_single_worker_tool_permission_binding") is True, "bridge ready mismatch")

    # Controlled worker execution blocks forbidden tool permission
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--controlled-worker-execution",
        "--controlled-worker-task", "noop",
        "--controlled-worker-tool-permission", "network_access",
        "--confirm-controlled-worker-execution", "YES_I_APPROVE_FIRST_CONTROLLED_WORKER_EXECUTION"
    ])
    require(errors, code == 0, f"forbidden permission failed: {err}")
    res = parse_json_output(out, "forbidden permission", errors)
    if res:
        require(errors, res.get("tool_permission_binding", {}).get("binding_status") == "BLOCKED", "binding status mismatch")
        require(errors, "network_access" in res.get("tool_permission_binding", {}).get("blocked_tool_permissions", []), "network_access not blocked")
        require(errors, res.get("controlled_worker_execution_result", {}).get("result_status") == "BLOCKED_NOT_EXECUTED", "result status mismatch")

    # Artifact writing with registry and controlled worker execution
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--controlled-worker-execution",
            "--confirm-controlled-worker-execution", "YES_I_APPROVE_FIRST_CONTROLLED_WORKER_EXECUTION"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v2-0-check-please-"), f"run_id {run_id} format mismatch")
            
            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v2_0_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "2.0.0", "man version mismatch")
                require(errors, man.get("controlled_worker_execution_result") is True, "man result True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "2.0.0", "rr version mismatch")

def main():
    print("Running validate_station_chief_runtime_v2_0.py...")
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
        
    print("PASS: Station Chief Runtime v2.0 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v2.0 runtime files.")

if __name__ == "__main__":
    main()

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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v2_1_report.md",
        "scripts/validate_station_chief_runtime_v2_1.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    tool_binding_path = REPO_ROOT / "10_runtime/station_chief_tool_permission_binding.py"
    
    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "2.1.0"',
            "attach_tool_permission_binding",
            "write_tool_permission_binding",
            "--tool-permission-schema",
            "--tool-permission-binding",
            "--write-tool-permission-binding",
            "--tool-permission-worker-id",
            "--tool-permission-request",
            "--tool-permission-token",
            "--tool-permission-output-json",
            "--tool-permission-sandbox-task",
            "tool_permission_binding_bundle",
            "tool_permission_binding_schema",
            "per_tool_permission_registry",
            "tool_permission_request_validation",
            "tool_specific_approval_binding",
            "tool_invocation_dry_run_contract",
            "tool_output_validation_schema",
            "tool_output_validation_result",
            "tool_failure_handling_contract",
            "tool_revocation_contract",
            "per_run_permission_audit_proof",
            "tool_permission_ledger",
            "tool_permission_readiness_summary",
            "live_execution_telemetry_abort_readiness_bridge",
            "single_worker_tool_permission_binding_only",
            "tool_permission_binding_requires_specific_tokens",
            "tool_permission_binding_does_not_invoke_external_tools",
            "tool_permission_binding_does_not_call_external_apis",
            "tool_permission_binding_does_not_run_shell_commands",
            "tool_permission_binding_does_not_modify_repo_files"
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess", "netlify", "vercel", "cloudflare", "firebase", "railway", "render"]
    )

    check_contains(
        errors,
        tool_binding_path,
        [
            'TOOL_PERMISSION_BINDING_MODULE_VERSION = "2.1.0"',
            "TOOL_PERMISSION_BINDING_STATUS",
            "TOOL_PERMISSION_BINDING_PHASE",
            "TOOL_PERMISSION_APPROVAL_TOKENS",
            "canonical_json",
            "sha256_digest",
            "normalize_tool_permission_label",
            "generate_tool_permission_binding_id",
            "create_tool_permission_binding_schema",
            "create_per_tool_permission_registry",
            "create_tool_permission_request_validation",
            "create_tool_specific_approval_binding",
            "create_tool_invocation_dry_run_contract",
            "create_tool_output_validation_schema",
            "create_tool_output_validation_result",
            "create_tool_failure_handling_contract",
            "create_tool_revocation_contract",
            "create_per_run_permission_audit_proof",
            "create_tool_permission_ledger",
            "create_tool_permission_readiness_summary",
            "create_live_execution_telemetry_abort_readiness_bridge",
            "create_tool_permission_binding_bundle"
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess", "eval(", "exec(", "compile(", "socket", "http.server", "socketserver", "uvicorn", "streamlit", "netlify", "vercel", "cloudflare", "firebase", "railway", "render", "__import__"]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "2.1.0", "demo runtime version != 2.1.0")
        require(errors, demo.get("runtime_status") == "single_worker_tool_permission_binding", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("tool_permission_binding_available") is True, "evidence available True")
        require(errors, evidence.get("single_worker_tool_permission_binding_only") is True, "evidence single_worker True")
        require(errors, evidence.get("tool_permission_binding_requires_specific_tokens") is True, "evidence requires_specific_tokens True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "2.1.0", "fixture runtime_version != 2.1.0")

    # Tool permission binding default without tokens
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--tool-permission-binding",
        "--tool-permission-request", "deterministic_summary"
    ])
    require(errors, code == 0, f"default tool-binding failed: {err}")
    res = parse_json_output(out, "default tool-binding", errors)
    if res:
        require(errors, "tool_permission_binding_bundle" in res, "bundle missing")
        require(errors, res.get("tool_permission_request_validation", {}).get("validation_status") == "BLOCKED", "validation_status mismatch")
        require(errors, res.get("per_run_permission_audit_proof", {}).get("audit_status") == "BLOCKED", "audit_status mismatch")

    # Tool permission binding with valid token
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--tool-permission-binding",
        "--tool-permission-request", "deterministic_summary",
        "--tool-permission-token", "deterministic_summary=YES_I_APPROVE_TOOL_DETERMINISTIC_SUMMARY"
    ])
    require(errors, code == 0, f"approved tool-binding failed: {err}")
    res = parse_json_output(out, "approved tool-binding", errors)
    if res:
        require(errors, res.get("tool_permission_request_validation", {}).get("validation_status") == "PASS", "validation_status mismatch")
        require(errors, res.get("tool_specific_approval_binding", {}).get("binding_status") == "BOUND", "binding_status mismatch")
        require(errors, res.get("per_run_permission_audit_proof", {}).get("audit_status") == "PASS", "audit_status mismatch")
        require(errors, res.get("tool_permission_readiness_summary", {}).get("ready_for_live_execution_telemetry_abort_controls") is True, "ready mismatch")

    # Tool permission binding blocks forbidden permission
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--tool-permission-binding",
        "--tool-permission-request", "network_access",
        "--tool-permission-token", "network_access=NOPE"
    ])
    require(errors, code == 0, f"forbidden tool-binding failed: {err}")
    res = parse_json_output(out, "forbidden tool-binding", errors)
    if res:
        require(errors, res.get("tool_permission_request_validation", {}).get("validation_status") == "BLOCKED", "validation_status mismatch")
        require(errors, "network_access" in res.get("tool_permission_request_validation", {}).get("blocked_tool_permissions", []), "network_access not blocked")

    # Unsafe output validation
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--tool-permission-binding",
        "--tool-permission-request", "deterministic_summary",
        "--tool-permission-token", "deterministic_summary=YES_I_APPROVE_TOOL_DETERMINISTIC_SUMMARY",
        "--tool-permission-output-json", '{"permission_id":"deterministic_summary","output_status":"PASS","output_payload":{"bad":"api_key=123"},"output_digest":"bad","external_actions_taken":false,"repo_files_modified":false,"execution_authorized":false}'
    ])
    require(errors, code == 0, f"unsafe output failed: {err}")
    res = parse_json_output(out, "unsafe output", errors)
    if res:
        require(errors, res.get("tool_output_validation_result", {}).get("validation_status") == "BLOCKED", "output validation_status mismatch")
        require(errors, res.get("per_run_permission_audit_proof", {}).get("audit_status") == "BLOCKED", "audit_status mismatch")

    # Artifact writing
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--tool-permission-binding",
            "--tool-permission-request", "deterministic_summary",
            "--tool-permission-token", "deterministic_summary=YES_I_APPROVE_TOOL_DETERMINISTIC_SUMMARY"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v2-1-check-please-"), f"run_id {run_id} format mismatch")
            
            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v2_1_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "2.1.0", "man version mismatch")
                require(errors, man.get("per_run_permission_audit_proof") is True, "man audit_proof True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "2.1.0", "rr version mismatch")

def main():
    print("Running validate_station_chief_runtime_v2_1.py...")
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
        
    print("PASS: Station Chief Runtime v2.1 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v2.1 runtime files.")

if __name__ == "__main__":
    main()

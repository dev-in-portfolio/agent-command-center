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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v1_1_report.md",
        "scripts/validate_station_chief_runtime_v1_1.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    controlled_exec_path = REPO_ROOT / "10_runtime/station_chief_controlled_execution.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    report_skeleton_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    report_v11_path = REPO_ROOT / "09_exports/station_chief_runtime_v1_1_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "1.1.0"',
            "attach_controlled_execution",
            "write_controlled_execution",
            "--list-controlled-execution-profiles",
            "--controlled-execution",
            "--controlled-execution-profile",
            "--attempted-action",
            "--write-controlled-execution",
            "controlled_execution_profile_catalog",
            "controlled_execution_selection",
            "execution_permission_matrix",
            "execution_mode_contract",
            "blocked_action_ledger",
            "controlled_execution_preflight_contract",
            "controlled_execution_readiness_summary",
            "work_order_executor_readiness_bridge",
            "controlled_execution_does_not_execute_live_actions",
            "controlled_execution_does_not_hire_workers",
            "controlled_execution_does_not_animate_workforce",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        controlled_exec_path,
        [
            'CONTROLLED_EXECUTION_MODULE_VERSION = "1.1.0"',
            "CONTROLLED_EXECUTION_PHASE",
            "CONTROLLED_EXECUTION_STATUS",
            "create_controlled_execution_profile_catalog",
            "select_controlled_execution_profile",
            "create_execution_permission_matrix",
            "create_execution_mode_contract",
            "create_blocked_action_ledger",
            "create_controlled_execution_preflight_contract",
            "create_controlled_execution_readiness_summary",
            "create_work_order_executor_readiness_bridge",
            "create_controlled_execution_bundle",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        adapter_path,
        ['ADAPTER_MODULE_VERSION = "1.1.0"', 'supports_controlled_execution_profiles'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v1.1.0.",
            "Controlled execution profile expansion added.",
            "controlled execution profile catalog",
            "execution permission matrix",
            "execution mode contract",
            "blocked-action ledger",
            "controlled execution preflight contract",
            "controlled execution readiness summary",
            "work order executor readiness bridge",
            "no real worker hiring",
            "no worker animation",
            "Station Chief Runtime v1.1.0 begins the controlled execution engine and worker hiring phase without performing live execution",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_skeleton_path,
        [
            "Station Chief Runtime upgraded to v1.1.0.",
            "Controlled execution profile expansion added.",
            "controlled execution profile catalog",
            "execution permission matrix",
            "execution mode contract",
            "blocked-action ledger",
            "controlled execution preflight contract",
            "controlled execution readiness summary",
            "work order executor readiness bridge",
            "no real worker hiring",
            "no worker animation",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_v11_path,
        [
            "Station Chief Runtime v1.1.0 Report",
            "Station Chief Runtime upgraded to v1.1.0. Locked 175-family baseline preserved. Controlled execution profile expansion added.",
            "controlled execution profile expansion",
            "execution permission matrices",
            "execution mode contracts",
            "blocked-action ledgers",
            "controlled execution preflight contracts",
            "readiness summaries",
            "work-order-executor readiness bridge",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "no real worker hiring",
            "Station Chief Runtime v1.1.0 begins the controlled execution engine and worker hiring phase without performing live execution",
            "Next recommended build step",
        ]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "1.1.0", "demo runtime version != 1.1.0")
        require(errors, demo.get("runtime_status") == "controlled_execution_profile_expansion", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "evidence baseline_preserved must be True")
        require(errors, evidence.get("external_actions_taken") is False, "evidence external_actions_taken must be False")
        require(errors, evidence.get("live_worker_agents_activated") is False, "evidence live_worker_agents_activated must be False")
        require(errors, evidence.get("controlled_execution_profile_expansion_available") is True, "evidence expansion_available True")
        require(errors, evidence.get("controlled_execution_does_not_execute_live_actions") is True, "evidence no_live_actions True")
        require(errors, evidence.get("controlled_execution_does_not_hire_workers") is True, "evidence no_hiring True")
        require(errors, evidence.get("controlled_execution_does_not_animate_workforce") is True, "evidence no_animation True")
        require(errors, evidence.get("work_order_executor_not_yet_active") is True, "evidence executor_not_active True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "1.1.0", "fixture runtime_version != 1.1.0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: {err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-controlled-execution-profiles"])
    require(errors, code == 0, f"--list-controlled-execution-profiles failed: {err}")
    catalog = parse_json_output(out, "--list-controlled-execution-profiles", errors)
    if catalog:
        require(errors, catalog.get("controlled_execution_profile_catalog_version") == "1.1.0", "catalog version mismatch")
        profiles = catalog.get("profiles", {})
        expected = ["audit_only", "dry_run_patch", "sandbox_write", "scoped_repo_patch", "work_order_preview", "worker_hiring_preview", "department_routing_preview", "orchestration_sandbox_preview"]
        for p in expected:
            require(errors, p in profiles, f"profile {p} missing from catalog")
        require(errors, catalog.get("real_worker_hiring_performed") is False, "hiring performed must be False")
        require(errors, catalog.get("live_worker_agents_activated") is False, "animation must be False")

    # Controlled execution default
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--controlled-execution"])
    require(errors, code == 0, f"default controlled execution failed: {err}")
    res = parse_json_output(out, "default controlled-execution", errors)
    if res:
        require(errors, "controlled_execution_bundle" in res, "controlled_execution_bundle missing")
        sel = res.get("controlled_execution_selection", {})
        require(errors, sel.get("selected_profile_id") == "audit_only", "default profile mismatch")
        require(errors, "execution_permission_matrix" in res, "permission matrix missing")
        require(errors, res.get("execution_mode_contract", {}).get("mode_status") == "CONTRACT_ONLY", "mode status mismatch")
        require(errors, res.get("blocked_action_ledger", {}).get("blocked_action_status") == "CLEAR", "blocked status mismatch")
        require(errors, res.get("controlled_execution_preflight_contract", {}).get("preflight_status") == "PASS", "preflight status mismatch")
        require(errors, res.get("controlled_execution_readiness_summary", {}).get("readiness_status") == "READY_FOR_NEXT_LAYER", "readiness status mismatch")
        require(errors, res.get("work_order_executor_readiness_bridge", {}).get("ready_for_work_order_executor_skeleton") is True, "bridge ready mismatch")

    # Controlled execution requested profile
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build work order executor skeleton", "--controlled-execution", "--controlled-execution-profile", "work_order_preview"])
    require(errors, code == 0, f"requested profile failed: {err}")
    res = parse_json_output(out, "requested profile", errors)
    if res:
        require(errors, res.get("controlled_execution_selection", {}).get("selected_profile_id") == "work_order_preview", "selected profile mismatch")
        require(errors, "Requested controlled execution profile accepted." in res.get("controlled_execution_selection", {}).get("selection_reason", ""), "reason mismatch")

    # Invalid requested profile
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--controlled-execution", "--controlled-execution-profile", "does_not_exist"])
    require(errors, code == 0, f"invalid profile failed: {err}")
    res = parse_json_output(out, "invalid profile", errors)
    if res:
        require(errors, res.get("controlled_execution_selection", {}).get("selected_profile_id") == "audit_only", "invalid default mismatch")
        require(errors, "defaulted to audit_only" in res.get("controlled_execution_selection", {}).get("selection_reason", ""), "invalid reason mismatch")

    # Blocked attempted action
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--controlled-execution", "--attempted-action", "live_external_api_action"])
    require(errors, code == 0, f"attempted action failed: {err}")
    res = parse_json_output(out, "attempted action", errors)
    if res:
        require(errors, res.get("blocked_action_ledger", {}).get("blocked_action_status") == "BLOCKED_ACTIONS_PRESENT", "blocked ledger status mismatch")
        require(errors, res.get("controlled_execution_readiness_summary", {}).get("readiness_status") == "BLOCKED", "readiness status blocked mismatch")

    # Write controlled execution
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-controlled-execution", str(td_path / "ce")
        ])
        require(errors, code == 0, f"write ce failed: {err}")
        write_res = parse_json_output(out, "write ce", errors)
        if write_res:
            require(errors, "controlled_execution_write_summary" in write_res, "write summary missing")
            summ = write_res["controlled_execution_write_summary"]
            cedir = Path(summ.get("controlled_execution_dir", ""))
            require(errors, cedir.exists(), "ce dir missing")
            
            fw = summ.get("files_written", [])
            expected = [
                "controlled_execution_bundle.json", "controlled_execution_profile_catalog.json",
                "controlled_execution_selection.json", "execution_permission_matrix.json",
                "execution_mode_contract.json", "blocked_action_ledger.json",
                "controlled_execution_preflight_contract.json", "controlled_execution_readiness_summary.json",
                "work_order_executor_readiness_bridge.json", "controlled_execution_manifest.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in files_written")
            
            manifest = json.loads((cedir / "controlled_execution_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "1.1.0", "manifest version mismatch")
            require(errors, manifest.get("status") == "PROFILE_EXPANSION_ONLY", "manifest status mismatch")

    # Artifact writing with registry and controlled execution
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--controlled-execution"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v1-1-check-please-"), "run_id format mismatch")
            
            fw = art_sum.get("files_written", [])
            expected_v11 = [
                "controlled_execution_bundle.json", "controlled_execution_profile_catalog.json",
                "controlled_execution_selection.json", "execution_permission_matrix.json",
                "execution_mode_contract.json", "blocked_action_ledger.json",
                "controlled_execution_preflight_contract.json", "controlled_execution_readiness_summary.json",
                "work_order_executor_readiness_bridge.json"
            ]
            for f in expected_v11:
                require(errors, f in fw, f"file {f} not in artifact files_written")

            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v1_1_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "1.1.0", "man version mismatch")
                require(errors, man.get("controlled_execution_readiness_summary") is True, "man readiness True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "1.1.0", "rr version mismatch")

def main():
    print("Running validate_station_chief_runtime_v1_1.py...")
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
        
    print("PASS: Station Chief Runtime v1.1 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v1.1 runtime files.")

if __name__ == "__main__":
    main()

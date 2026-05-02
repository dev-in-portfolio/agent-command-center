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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v1_2_report.md",
        "scripts/validate_station_chief_runtime_v1_2.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    executor_path = REPO_ROOT / "10_runtime/station_chief_work_order_executor.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    report_skeleton_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    report_v12_path = REPO_ROOT / "09_exports/station_chief_runtime_v1_2_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "1.2.0"',
            "attach_work_order_executor",
            "write_work_order_executor",
            "--work-order-schema",
            "--work-order-executor",
            "--write-work-order-executor",
            "executable_work_order_schema",
            "work_order_status_lifecycle",
            "work_order_dependency_map",
            "work_order_dry_run_results",
            "work_order_execution_ledger",
            "work_order_completion_proofs",
            "work_order_executor_summary",
            "work_order_executor_dry_run_only",
            "work_order_executor_does_not_execute_live_actions",
            "work_order_executor_does_not_hire_workers",
            "work_order_executor_does_not_animate_workforce",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        executor_path,
        [
            'WORK_ORDER_EXECUTOR_MODULE_VERSION = "1.2.0"',
            "WORK_ORDER_EXECUTOR_STATUS",
            "WORK_ORDER_EXECUTOR_PHASE",
            "canonical_json",
            "sha256_digest",
            "normalize_work_order_label",
            "generate_work_order_id",
            "create_executable_work_order_schema",
            "create_work_order",
            "create_work_orders_from_runtime_result",
            "create_work_order_status_lifecycle",
            "create_work_order_dependency_map",
            "dry_run_execute_work_order",
            "dry_run_execute_work_orders",
            "create_work_order_execution_ledger",
            "create_work_order_completion_proof",
            "create_work_order_completion_proofs",
            "create_work_order_executor_summary",
            "create_work_order_executor_bundle",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        adapter_path,
        ['ADAPTER_MODULE_VERSION = "1.2.0"', 'supports_work_order_executor_skeleton'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v1.2.0.",
            "Work order executor skeleton added.",
            "executable work order schema",
            "deterministic work order ID generation",
            "work order status lifecycle",
            "work order dependency mapping",
            "dry-run work order executor",
            "work order execution ledger",
            "work order completion proof",
            "work order executor summary",
            "no live work order execution",
            "no real worker hiring",
            "no worker animation",
            "Station Chief Runtime v1.2.0 adds the Work Order Executor Skeleton without performing live execution",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_skeleton_path,
        [
            "Station Chief Runtime upgraded to v1.2.0.",
            "Work order executor skeleton added.",
            "executable work order schema",
            "deterministic work order ID generation",
            "work order status lifecycle",
            "work order dependency mapping",
            "dry-run work order executor",
            "work order execution ledger",
            "work order completion proof",
            "work order executor summary",
            "no live work order execution",
            "no real worker hiring",
            "no worker animation",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_v12_path,
        [
            "Station Chief Runtime v1.2.0 Report",
            "Station Chief Runtime upgraded to v1.2.0. Locked 175-family baseline preserved. Work order executor skeleton added.",
            "executable work order schema",
            "work order status lifecycle",
            "dependency mapping",
            "dry-run work order execution",
            "work order execution ledgers",
            "completion proofs",
            "work order executor summary",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "no real worker hiring",
            "Station Chief Runtime v1.2.0 adds the Work Order Executor Skeleton without performing live execution",
            "Next recommended build step",
        ]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "1.2.0", "demo runtime version != 1.2.0")
        require(errors, demo.get("runtime_status") == "work_order_executor_skeleton", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "evidence baseline_preserved must be True")
        require(errors, evidence.get("external_actions_taken") is False, "evidence external_actions_taken must be False")
        require(errors, evidence.get("live_worker_agents_activated") is False, "evidence live_worker_agents_activated must be False")
        require(errors, evidence.get("work_order_executor_skeleton_available") is True, "evidence skeleton_available True")
        require(errors, evidence.get("work_order_executor_dry_run_only") is True, "evidence dry_run_only True")
        require(errors, evidence.get("work_order_executor_does_not_execute_live_actions") is True, "evidence no_live_actions True")
        require(errors, evidence.get("work_order_executor_does_not_hire_workers") is True, "evidence no_hiring True")
        require(errors, evidence.get("work_order_executor_does_not_animate_workforce") is True, "evidence no_animation True")
        require(errors, evidence.get("worker_hiring_registry_not_yet_active") is True, "evidence hiring_not_active True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "1.2.0", "fixture runtime_version != 1.2.0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: {err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: {err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "1.2.0", "adapter_module_version != 1.2.0")
        srp = adapters.get("supported_adapters", {}).get("scoped_repo_patch", {})
        require(errors, srp.get("supports_work_order_executor_skeleton") is True, "scoped_repo_patch supports_work_order_executor_skeleton must be True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--work-order-schema"])
    require(errors, code == 0, f"--work-order-schema failed: {err}")
    schema = parse_json_output(out, "--work-order-schema", errors)
    if schema:
        require(errors, schema.get("executable_work_order_schema_version") == "1.2.0", "schema version mismatch")
        require(errors, schema.get("schema_status") == "SKELETON_DRY_RUN_ONLY", "schema status mismatch")
        req = schema.get("required_fields", [])
        require(errors, "work_order_id" in req, "work_order_id missing from required fields")
        require(errors, "status" in req, "status missing from required fields")
        require(errors, "dependencies" in req, "dependencies missing from required fields")
        stat = schema.get("allowed_statuses", [])
        require(errors, "CREATED" in stat, "CREATED status missing")
        require(errors, "DRY_RUN_COMPLETE" in stat, "DRY_RUN_COMPLETE status missing")
        modes = schema.get("allowed_execution_modes", [])
        require(errors, "dry_run_only" in modes, "dry_run_only mode missing")
        require(errors, schema.get("baseline_preserved") is True, "baseline preserved mismatch")
        require(errors, schema.get("external_actions_taken") is False, "external actions taken mismatch")
        require(errors, schema.get("live_worker_agents_activated") is False, "worker animation mismatch")
        require(errors, schema.get("real_worker_hiring_performed") is False, "hiring mismatch")
        require(errors, schema.get("execution_authorized") is False, "execution authorized mismatch")

    # Work order executor default
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--work-order-executor"])
    require(errors, code == 0, f"default work-order-executor failed: {err}")
    res = parse_json_output(out, "default work-order-executor", errors)
    if res:
        require(errors, "work_order_executor_bundle" in res, "work_order_executor_bundle missing")
        require(errors, "executable_work_order_schema" in res, "executable_work_order_schema missing")
        require(errors, "work_orders_executable" in res, "work_orders exists missing")
        require(errors, "work_order_status_lifecycle" in res, "work_order_status_lifecycle missing")
        require(errors, "work_order_dependency_map" in res, "work_order_dependency_map missing")
        require(errors, "work_order_dry_run_results" in res, "work_order_dry_run_results missing")
        require(errors, "work_order_execution_ledger" in res, "work_order_execution_ledger missing")
        require(errors, "work_order_completion_proofs" in res, "work_order_completion_proofs missing")
        require(errors, "work_order_executor_summary" in res, "work_order_executor_summary missing")
        
        bundle = res.get("work_order_executor_bundle", {})
        require(errors, bundle.get("work_order_executor_bundle_version") == "1.2.0", "bundle version mismatch")
        require(errors, bundle.get("executor_status") == "SKELETON_DRY_RUN_ONLY", "executor status mismatch")
        
        summ = res.get("work_order_executor_summary", {})
        require(errors, summ.get("executor_status") == "DRY_RUN_ONLY", "summary executor_status mismatch")
        require(errors, summ.get("work_order_count", 0) >= 1, "work_order_count < 1")
        require(errors, summ.get("dry_run_pass_count", 0) >= 1, "dry_run_pass_count < 1")
        require(errors, summ.get("ready_for_worker_hiring_registry") is True, "ready_for_worker_hiring_registry mismatch")
        require(errors, res.get("evidence", {}).get("external_actions_taken") is False, "external actions taken True")
        require(errors, res.get("evidence", {}).get("live_worker_agents_activated") is False, "worker agents activated True")
        require(errors, res.get("evidence", {}).get("real_worker_hiring_performed", False) is False, "real hiring performed True")

    # Work order executor command for next layer
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build worker hiring registry", "--work-order-executor"])
    require(errors, code == 0, f"next layer command failed: {err}")
    res = parse_json_output(out, "next layer command", errors)
    if res:
        summ = res.get("work_order_executor_summary", {})
        require(errors, summ.get("next_layer") == "Worker Hiring Registry", "next_layer mismatch")
        proofs = res.get("work_order_completion_proofs", [])
        require(errors, len(proofs) >= 1, "proofs empty")
        for p in proofs:
            require(errors, p.get("safety_constraints_met") is True, "safety_constraints_met mismatch")
        results = res.get("work_order_dry_run_results", [])
        for r in results:
            require(errors, r.get("external_actions_taken") is False, "dry run external actions mismatch")
            require(errors, r.get("repo_files_modified") is False, "dry run repo files modified mismatch")

    # Write work order executor
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-work-order-executor", str(td_path / "woe")
        ])
        require(errors, code == 0, f"write woe failed: {err}")
        write_res = parse_json_output(out, "write woe", errors)
        if write_res:
            require(errors, "work_order_executor_write_summary" in write_res, "summary missing")
            summ = write_res["work_order_executor_write_summary"]
            woedir = Path(summ.get("work_order_executor_dir", ""))
            require(errors, woedir.exists(), "woe dir missing")
            
            fw = summ.get("files_written", [])
            expected = [
                "work_order_executor_bundle.json", "executable_work_order_schema.json",
                "work_orders.json", "work_order_status_lifecycle.json",
                "work_order_dependency_map.json", "work_order_dry_run_results.json",
                "work_order_execution_ledger.json", "work_order_completion_proofs.json",
                "work_order_executor_summary.json", "work_order_executor_manifest.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in files_written")
                
            manifest = json.loads((woedir / "work_order_executor_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "1.2.0", "manifest version mismatch")
            require(errors, manifest.get("status") == "SKELETON_DRY_RUN_ONLY", "manifest status mismatch")

    # Artifact writing with registry and work order executor
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--work-order-executor"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v1-2-check-please-"), "run_id format mismatch")
            
            fw = art_sum.get("files_written", [])
            expected_v12 = [
                "work_order_executor_bundle.json", "executable_work_order_schema.json",
                "work_orders_executable.json", "work_order_status_lifecycle.json",
                "work_order_dependency_map.json", "work_order_dry_run_results.json",
                "work_order_execution_ledger.json", "work_order_completion_proofs.json",
                "work_order_executor_summary.json"
            ]
            for f in expected_v12:
                require(errors, f in fw, f"file {f} not in artifact files_written")

            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v1_2_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "1.2.0", "man version mismatch")
                require(errors, man.get("work_order_executor_summary") is True, "man summary True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "1.2.0", "rr version mismatch")

    # Regression behavior
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--stable-release-manifest"])
    require(errors, code == 0, f"stable manifest failed: {err}")
    res = parse_json_output(out, "stable manifest", errors)
    if res:
        require(errors, res.get("runtime_version") == "1.2.0", "manifest version mismatch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--release-lock"])
    require(errors, code == 0, f"release lock failed: {err}")
    res = parse_json_output(out, "release lock", errors)
    if res:
        require(errors, "release_lock_bundle" in res, "release_lock_bundle missing")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--controlled-execution"])
    require(errors, code == 0, f"controlled execution failed: {err}")
    res = parse_json_output(out, "controlled execution", errors)
    if res:
        require(errors, "controlled_execution_bundle" in res, "controlled_execution_bundle missing")

def main():
    print("Running validate_station_chief_runtime_v1_2.py...")
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
        
    print("PASS: Station Chief Runtime v1.2 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v1.2 runtime files.")

if __name__ == "__main__":
    main()

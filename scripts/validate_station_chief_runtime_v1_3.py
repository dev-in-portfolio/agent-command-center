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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v1_3_report.md",
        "scripts/validate_station_chief_runtime_v1_3.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    registry_path = REPO_ROOT / "10_runtime/station_chief_worker_hiring_registry.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    report_skeleton_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    report_v13_path = REPO_ROOT / "09_exports/station_chief_runtime_v1_3_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "1.3.0"',
            "attach_worker_hiring_registry",
            "write_worker_hiring_registry",
            "--worker-role-schema",
            "--worker-hiring-registry",
            "--write-worker-hiring-registry",
            "worker_role_schema",
            "worker_candidates",
            "worker_registry_status_lifecycle",
            "worker_assignment_plan",
            "worker_registry_ledger",
            "worker_hiring_preview_records",
            "worker_hiring_readiness_summary",
            "department_routing_readiness_bridge",
            "worker_hiring_registry_preview_only",
            "worker_hiring_registry_does_not_hire_workers",
            "worker_hiring_registry_does_not_animate_workforce",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        registry_path,
        [
            'WORKER_HIRING_REGISTRY_MODULE_VERSION = "1.3.0"',
            "WORKER_HIRING_REGISTRY_STATUS",
            "WORKER_HIRING_REGISTRY_PHASE",
            "canonical_json",
            "sha256_digest",
            "normalize_worker_label",
            "generate_worker_id",
            "create_worker_role_schema",
            "create_worker_candidate",
            "create_worker_candidates_from_work_orders",
            "create_worker_registry_status_lifecycle",
            "create_worker_assignment_plan",
            "create_worker_registry_ledger",
            "create_worker_hiring_preview_record",
            "create_worker_hiring_preview_records",
            "create_worker_hiring_readiness_summary",
            "create_department_routing_readiness_bridge",
            "create_worker_hiring_registry_bundle",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        adapter_path,
        ['ADAPTER_MODULE_VERSION = "1.3.0"', 'supports_worker_hiring_registry_preview'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v1.3.0.",
            "Worker hiring registry preview added.",
            "worker role schema",
            "deterministic worker ID generation",
            "worker candidate generation from work orders",
            "worker registry status lifecycle",
            "worker assignment planning",
            "worker registry ledger",
            "worker hiring preview records",
            "worker hiring readiness summary",
            "department routing readiness bridge",
            "no real worker hiring",
            "no worker animation",
            "no live worker assignment",
            "Station Chief Runtime v1.3.0 adds the Worker Hiring Registry preview without performing real hiring or worker animation",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_skeleton_path,
        [
            "Station Chief Runtime upgraded to v1.3.0.",
            "Worker hiring registry preview added.",
            "worker role schema",
            "deterministic worker ID generation",
            "worker candidate generation from work orders",
            "worker registry status lifecycle",
            "worker assignment planning",
            "worker registry ledger",
            "worker hiring preview records",
            "worker hiring readiness summary",
            "department routing readiness bridge",
            "no real worker hiring",
            "no worker animation",
            "no live worker assignment",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_v13_path,
        [
            "Station Chief Runtime v1.3.0 Report",
            "Station Chief Runtime upgraded to v1.3.0. Locked 175-family baseline preserved. Worker hiring registry preview added.",
            "worker role schema",
            "deterministic worker ID generation",
            "worker candidate generation from work orders",
            "worker registry status lifecycle",
            "worker assignment planning",
            "worker registry ledger",
            "worker hiring preview records",
            "hiring readiness summary",
            "department routing readiness bridge",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "no real worker hiring",
            "Station Chief Runtime v1.3.0 adds the Worker Hiring Registry preview without performing real hiring or worker animation",
            "Next recommended build step",
        ]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "1.3.0", "demo runtime version != 1.3.0")
        require(errors, demo.get("runtime_status") == "worker_hiring_registry_preview", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "evidence baseline_preserved must be True")
        require(errors, evidence.get("external_actions_taken") is False, "evidence external_actions_taken must be False")
        require(errors, evidence.get("live_worker_agents_activated") is False, "evidence live_worker_agents_activated must be False")
        require(errors, evidence.get("worker_hiring_registry_available") is True, "evidence registry_available True")
        require(errors, evidence.get("worker_hiring_registry_preview_only") is True, "evidence preview_only True")
        require(errors, evidence.get("worker_hiring_registry_does_not_hire_workers") is True, "evidence no_hiring True")
        require(errors, evidence.get("worker_hiring_registry_does_not_animate_workforce") is True, "evidence no_animation True")
        require(errors, evidence.get("department_routing_runtime_not_yet_active") is True, "evidence routing_not_active True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "1.3.0", "fixture runtime_version != 1.3.0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: {err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: {err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "1.3.0", "adapter_module_version != 1.3.0")
        srp = adapters.get("supported_adapters", {}).get("scoped_repo_patch", {})
        require(errors, srp.get("supports_worker_hiring_registry_preview") is True, "scoped_repo_patch supports_worker_hiring_registry_preview must be True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--worker-role-schema"])
    require(errors, code == 0, f"--worker-role-schema failed: {err}")
    schema = parse_json_output(out, "--worker-role-schema", errors)
    if schema:
        require(errors, schema.get("worker_role_schema_version") == "1.3.0", "schema version mismatch")
        require(errors, schema.get("schema_status") == "REGISTRY_PREVIEW_ONLY", "schema status mismatch")
        req = schema.get("required_fields", [])
        require(errors, "worker_id" in req, "worker_id missing from required fields")
        require(errors, "worker_role_title" in req, "worker_role_title missing from required fields")
        require(errors, "source_work_order_id" in req, "source_work_order_id missing from required fields")
        stat = schema.get("allowed_worker_statuses", [])
        require(errors, "CANDIDATE_CREATED" in stat, "CANDIDATE_CREATED status missing")
        require(errors, "REGISTRY_RECORDED" in stat, "REGISTRY_RECORDED status missing")
        modes = schema.get("allowed_worker_modes", [])
        require(errors, "registry_preview_only" in modes, "registry_preview_only mode missing")
        require(errors, schema.get("baseline_preserved") is True, "baseline preserved mismatch")
        require(errors, schema.get("external_actions_taken") is False, "external actions taken mismatch")
        require(errors, schema.get("live_worker_agents_activated") is False, "worker animation mismatch")
        require(errors, schema.get("real_worker_hiring_performed") is False, "hiring mismatch")
        require(errors, schema.get("execution_authorized") is False, "execution authorized mismatch")

    # Worker hiring registry default
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--worker-hiring-registry"])
    require(errors, code == 0, f"default worker-hiring-registry failed: {err}")
    res = parse_json_output(out, "default worker-hiring-registry", errors)
    if res:
        require(errors, "worker_hiring_registry_bundle" in res, "worker_hiring_registry_bundle missing")
        require(errors, "worker_role_schema" in res, "worker_role_schema missing")
        require(errors, "worker_candidates" in res, "worker_candidates exists missing")
        require(errors, "worker_registry_status_lifecycle" in res, "worker_registry_status_lifecycle missing")
        require(errors, "worker_assignment_plan" in res, "worker_assignment_plan missing")
        require(errors, "worker_registry_ledger" in res, "worker_registry_ledger missing")
        require(errors, "worker_hiring_preview_records" in res, "worker_hiring_preview_records missing")
        require(errors, "worker_hiring_readiness_summary" in res, "worker_hiring_readiness_summary missing")
        require(errors, "department_routing_readiness_bridge" in res, "department_routing_readiness_bridge missing")
        
        bundle = res.get("worker_hiring_registry_bundle", {})
        require(errors, bundle.get("worker_hiring_registry_bundle_version") == "1.3.0", "bundle version mismatch")
        require(errors, bundle.get("registry_status") == "REGISTRY_PREVIEW_ONLY", "registry status mismatch")
        
        summ = res.get("worker_hiring_readiness_summary", {})
        require(errors, summ.get("registry_status") == "REGISTRY_PREVIEW_ONLY", "summary registry_status mismatch")
        require(errors, summ.get("worker_count", 0) >= 1, "worker_count < 1")
        require(errors, summ.get("ready_for_department_routing_runtime") is True, "ready_for_department_routing_runtime mismatch")
        
        plan = res.get("worker_assignment_plan", {})
        require(errors, plan.get("assignment_status") == "PLANNED_PREVIEW_ONLY", "assignment status mismatch")
        
        require(errors, res.get("evidence", {}).get("external_actions_taken") is False, "external actions taken True")
        require(errors, res.get("evidence", {}).get("live_worker_agents_activated") is False, "worker agents activated True")
        require(errors, res.get("evidence", {}).get("real_worker_hiring_performed", False) is False, "real hiring performed True")

    # Worker hiring registry command for next layer
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build department routing runtime", "--worker-hiring-registry"])
    require(errors, code == 0, f"next layer command failed: {err}")
    res = parse_json_output(out, "next layer command", errors)
    if res:
        summ = res.get("worker_hiring_readiness_summary", {})
        require(errors, summ.get("next_layer") == "Department Routing Runtime", "next_layer mismatch")
        bridge = res.get("department_routing_readiness_bridge", {})
        require(errors, bridge.get("next_layer") == "Department Routing Runtime", "bridge next_layer mismatch")
        require(errors, bridge.get("ready_for_department_routing_runtime") is True, "bridge ready mismatch")
        
        previews = res.get("worker_hiring_preview_records", [])
        require(errors, len(previews) >= 1, "previews empty")
        for p in previews:
            require(errors, p.get("real_worker_hiring_performed") is False, "real_worker_hiring_performed mismatch")
            require(errors, p.get("live_worker_agents_activated") is False, "live_worker_agents_activated mismatch")

    # Write worker hiring registry
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-worker-hiring-registry", str(td_path / "whr")
        ])
        require(errors, code == 0, f"write whr failed: {err}")
        write_res = parse_json_output(out, "write whr", errors)
        if write_res:
            require(errors, "worker_hiring_registry_write_summary" in write_res, "summary missing")
            summ = write_res["worker_hiring_registry_write_summary"]
            whrdir = Path(summ.get("worker_hiring_registry_dir", ""))
            require(errors, whrdir.exists(), "whr dir missing")
            
            fw = summ.get("files_written", [])
            expected = [
                "worker_hiring_registry_bundle.json", "worker_role_schema.json",
                "worker_candidates.json", "worker_registry_status_lifecycle.json",
                "worker_assignment_plan.json", "worker_registry_ledger.json",
                "worker_hiring_preview_records.json", "worker_hiring_readiness_summary.json",
                "department_routing_readiness_bridge.json", "worker_hiring_registry_manifest.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in files_written")
                
            manifest = json.loads((whrdir / "worker_hiring_registry_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "1.3.0", "manifest version mismatch")
            require(errors, manifest.get("status") == "REGISTRY_PREVIEW_ONLY", "manifest status mismatch")

    # Artifact writing with registry and worker hiring registry
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--worker-hiring-registry"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v1-3-check-please-"), "run_id format mismatch")
            
            fw = art_sum.get("files_written", [])
            expected_v13 = [
                "worker_hiring_registry_bundle.json", "worker_role_schema.json",
                "worker_candidates.json", "worker_registry_status_lifecycle.json",
                "worker_assignment_plan.json", "worker_registry_ledger.json",
                "worker_hiring_preview_records.json", "worker_hiring_readiness_summary.json",
                "department_routing_readiness_bridge.json"
            ]
            for f in expected_v13:
                require(errors, f in fw, f"file {f} not in artifact files_written")

            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v1_3_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "1.3.0", "man version mismatch")
                require(errors, man.get("worker_hiring_readiness_summary") is True, "man summary True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "1.3.0", "rr version mismatch")

    # Regression behavior
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--stable-release-manifest"])
    require(errors, code == 0, f"stable manifest failed: {err}")
    res = parse_json_output(out, "stable manifest", errors)
    if res:
        require(errors, res.get("runtime_version") == "1.3.0", "manifest version mismatch")

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

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--work-order-executor"])
    require(errors, code == 0, f"work order executor failed: {err}")
    res = parse_json_output(out, "work order executor", errors)
    if res:
        require(errors, "work_order_executor_bundle" in res, "work_order_executor_bundle missing")

def main():
    print("Running validate_station_chief_runtime_v1_3.py...")
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
        
    print("PASS: Station Chief Runtime v1.3 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v1.3 runtime files.")

if __name__ == "__main__":
    main()

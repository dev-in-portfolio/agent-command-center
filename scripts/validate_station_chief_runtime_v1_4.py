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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v1_4_report.md",
        "scripts/validate_station_chief_runtime_v1_4.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    routing_path = REPO_ROOT / "10_runtime/station_chief_department_routing.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    report_skeleton_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    report_v14_path = REPO_ROOT / "09_exports/station_chief_runtime_v1_4_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "1.4.0"',
            "attach_department_routing",
            "write_department_routing",
            "--department-routing-schema",
            "--department-routing",
            "--write-department-routing",
            "department_routing_schema",
            "department_route_candidates",
            "family_to_department_routing_map",
            "worker_to_department_assignment_map",
            "department_routing_conflict_detector",
            "department_routing_dry_run_results",
            "department_routing_ledger",
            "department_routing_completion_proofs",
            "department_routing_readiness_summary",
            "multi_agent_orchestration_readiness_bridge",
            "department_routing_preview_only",
            "department_routing_does_not_route_live_workers",
            "department_routing_does_not_hire_workers",
            "department_routing_does_not_animate_workforce",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        routing_path,
        [
            'DEPARTMENT_ROUTING_MODULE_VERSION = "1.4.0"',
            "DEPARTMENT_ROUTING_STATUS",
            "DEPARTMENT_ROUTING_PHASE",
            "canonical_json",
            "sha256_digest",
            "normalize_route_label",
            "generate_route_id",
            "create_department_routing_schema",
            "infer_target_department",
            "create_department_route_candidate",
            "create_department_route_candidates_from_worker_registry",
            "create_family_to_department_routing_map",
            "create_worker_to_department_assignment_map",
            "detect_department_routing_conflicts",
            "dry_run_department_routing",
            "create_department_routing_ledger",
            "create_department_routing_completion_proof",
            "create_department_routing_completion_proofs",
            "create_department_routing_readiness_summary",
            "create_multi_agent_orchestration_readiness_bridge",
            "create_department_routing_bundle",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        adapter_path,
        ['ADAPTER_MODULE_VERSION = "1.4.0"', 'supports_department_routing_preview'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v1.4.0.",
            "Department routing runtime preview added.",
            "department routing schema",
            "deterministic route ID generation",
            "department route candidate generation",
            "family-to-department routing map",
            "worker-to-department assignment map",
            "department routing conflict detector",
            "department routing dry-run engine",
            "department routing ledger",
            "department routing completion proofs",
            "department routing readiness summary",
            "multi_agent_orchestration_readiness_bridge",
            "no live worker routing",
            "no real worker hiring",
            "no worker animation",
            "Station Chief Runtime v1.4.0 adds the Department Routing Runtime preview without performing live routing or worker animation",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_skeleton_path,
        [
            "Station Chief Runtime upgraded to v1.4.0.",
            "Department routing runtime preview added.",
            "department routing schema",
            "deterministic route ID generation",
            "department route candidate generation",
            "family-to-department routing map",
            "worker-to-department assignment map",
            "department routing conflict detector",
            "department routing dry-run engine",
            "department routing ledger",
            "department routing completion proof",
            "department routing readiness summary",
            "multi_agent_orchestration_readiness_bridge",
            "no live worker routing",
            "no real worker hiring",
            "no worker animation",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_v14_path,
        [
            "Station Chief Runtime v1.4.0 Report",
            "Station Chief Runtime upgraded to v1.4.0. Locked 175-family baseline preserved. Department routing runtime preview added.",
            "department routing schema",
            "deterministic route ID generation",
            "family-to-department routing map",
            "worker-to-department assignment map",
            "routing dry-run engine",
            "routing conflict detector",
            "routing completion proof",
            "department routing ledger",
            "department routing readiness summary",
            "multi-agent orchestration readiness bridge",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "no real worker hiring",
            "no live worker routing",
            "Station Chief Runtime v1.4.0 adds the Department Routing Runtime preview without performing live routing or worker animation",
            "Next recommended build step",
        ]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "1.4.0", "demo runtime version != 1.4.0")
        require(errors, demo.get("runtime_status") == "department_routing_preview", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "evidence baseline_preserved must be True")
        require(errors, evidence.get("external_actions_taken") is False, "evidence external_actions_taken must be False")
        require(errors, evidence.get("live_worker_agents_activated") is False, "evidence live_worker_agents_activated must be False")
        require(errors, evidence.get("department_routing_available") is True, "evidence routing_available True")
        require(errors, evidence.get("department_routing_preview_only") is True, "evidence preview_only True")
        require(errors, evidence.get("department_routing_does_not_route_live_workers") is True, "evidence no_live_routing True")
        require(errors, evidence.get("department_routing_does_not_hire_workers") is True, "evidence no_hiring True")
        require(errors, evidence.get("department_routing_does_not_animate_workforce") is True, "evidence no_animation True")
        require(errors, evidence.get("multi_agent_orchestration_sandbox_not_yet_active") is True, "evidence orchestration_not_active True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "1.4.0", "fixture runtime_version != 1.4.0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: {err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: {err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "1.4.0", "adapter_module_version != 1.4.0")
        srp = adapters.get("supported_adapters", {}).get("scoped_repo_patch", {})
        require(errors, srp.get("supports_department_routing_preview") is True, "scoped_repo_patch supports_department_routing_preview must be True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--department-routing-schema"])
    require(errors, code == 0, f"--department-routing-schema failed: {err}")
    schema = parse_json_output(out, "--department-routing-schema", errors)
    if schema:
        require(errors, schema.get("department_routing_schema_version") == "1.4.0", "schema version mismatch")
        require(errors, schema.get("schema_status") == "ROUTING_PREVIEW_ONLY", "schema status mismatch")
        req = schema.get("required_fields", [])
        require(errors, "route_id" in req, "route_id missing from required fields")
        require(errors, "source_worker_id" in req, "source_worker_id missing from required fields")
        require(errors, "target_department" in req, "target_department missing from required fields")
        stat = schema.get("allowed_route_statuses", [])
        require(errors, "ROUTE_CANDIDATE_CREATED" in stat, "ROUTE_CANDIDATE_CREATED status missing")
        require(errors, "ROUTE_RECORDED" in stat, "ROUTE_RECORDED status missing")
        modes = schema.get("allowed_route_modes", [])
        require(errors, "routing_preview_only" in modes, "routing_preview_only mode missing")
        require(errors, schema.get("baseline_preserved") is True, "baseline preserved mismatch")
        require(errors, schema.get("external_actions_taken") is False, "external actions taken mismatch")
        require(errors, schema.get("live_worker_agents_activated") is False, "worker animation mismatch")
        require(errors, schema.get("real_worker_hiring_performed") is False, "hiring mismatch")
        require(errors, schema.get("live_worker_routing_performed") is False, "routing mismatch")
        require(errors, schema.get("execution_authorized") is False, "execution authorized mismatch")

    # Department routing default
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--department-routing"])
    require(errors, code == 0, f"default department-routing failed: {err}")
    res = parse_json_output(out, "default department-routing", errors)
    if res:
        require(errors, "department_routing_bundle" in res, "department_routing_bundle missing")
        require(errors, "department_routing_schema" in res, "department_routing_schema missing")
        require(errors, "department_route_candidates" in res, "department_route_candidates missing")
        require(errors, "family_to_department_routing_map" in res, "family_to_department_routing_map missing")
        require(errors, "worker_to_department_assignment_map" in res, "worker_to_department_assignment_map missing")
        require(errors, "department_routing_conflict_detector" in res, "department_routing_conflict_detector missing")
        require(errors, "department_routing_dry_run_results" in res, "department_routing_dry_run_results missing")
        require(errors, "department_routing_ledger" in res, "department_routing_ledger missing")
        require(errors, "department_routing_completion_proofs" in res, "department_routing_completion_proofs missing")
        require(errors, "department_routing_readiness_summary" in res, "department_routing_readiness_summary missing")
        require(errors, "multi_agent_orchestration_readiness_bridge" in res, "multi_agent_orchestration_readiness_bridge missing")
        
        bundle = res.get("department_routing_bundle", {})
        require(errors, bundle.get("department_routing_bundle_version") == "1.4.0", "bundle version mismatch")
        require(errors, bundle.get("routing_status") == "ROUTING_PREVIEW_ONLY", "routing status mismatch")
        
        summ = res.get("department_routing_readiness_summary", {})
        require(errors, summ.get("routing_status") == "ROUTING_PREVIEW_ONLY", "summary routing_status mismatch")
        require(errors, summ.get("route_count", 0) >= 1, "route_count < 1")
        require(errors, summ.get("ready_for_multi_agent_orchestration_sandbox") is True, "ready_for_multi_agent_orchestration_sandbox mismatch")
        
        conflicts = res.get("department_routing_conflict_detector", {})
        require(errors, conflicts.get("conflict_status") == "CLEAR", "conflict status mismatch")
        
        require(errors, res.get("evidence", {}).get("external_actions_taken") is False, "external actions taken True")
        require(errors, res.get("evidence", {}).get("live_worker_agents_activated") is False, "worker agents activated True")
        require(errors, res.get("evidence", {}).get("live_worker_routing_performed", False) is False, "live routing performed True")

    # Department routing command for next layer
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build multi-agent orchestration sandbox", "--department-routing"])
    require(errors, code == 0, f"next layer command failed: {err}")
    res = parse_json_output(out, "next layer command", errors)
    if res:
        summ = res.get("department_routing_readiness_summary", {})
        require(errors, summ.get("next_layer") == "Multi-Agent Orchestration Sandbox", "next_layer mismatch")
        bridge = res.get("multi_agent_orchestration_readiness_bridge", {})
        require(errors, bridge.get("next_layer") == "Multi-Agent Orchestration Sandbox", "bridge next_layer mismatch")
        require(errors, bridge.get("ready_for_multi_agent_orchestration_sandbox") is True, "bridge ready mismatch")
        
        proofs = res.get("department_routing_completion_proofs", [])
        require(errors, len(proofs) >= 1, "proofs empty")
        for p in proofs:
            require(errors, p.get("live_worker_routing_performed") is False, "live_worker_routing_performed mismatch")
        results = res.get("department_routing_dry_run_results", [])
        for r in results:
            require(errors, r.get("live_worker_routing_performed") is False, "dry run live routing mismatch")

    # Write department routing
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-department-routing", str(td_path / "dr")
        ])
        require(errors, code == 0, f"write dr failed: {err}")
        write_res = parse_json_output(out, "write dr", errors)
        if write_res:
            require(errors, "department_routing_write_summary" in write_res, "summary missing")
            summ = write_res["department_routing_write_summary"]
            drdir = Path(summ.get("department_routing_dir", ""))
            require(errors, drdir.exists(), "dr dir missing")
            
            fw = summ.get("files_written", [])
            expected = [
                "department_routing_bundle.json", "department_routing_schema.json",
                "department_route_candidates.json", "family_to_department_routing_map.json",
                "worker_to_department_assignment_map.json", "department_routing_conflict_detector.json",
                "department_routing_dry_run_results.json", "department_routing_ledger.json",
                "department_routing_completion_proofs.json", "department_routing_readiness_summary.json",
                "multi_agent_orchestration_readiness_bridge.json", "department_routing_manifest.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in files_written")
                
            manifest = json.loads((drdir / "department_routing_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "1.4.0", "manifest version mismatch")
            require(errors, manifest.get("status") == "ROUTING_PREVIEW_ONLY", "manifest status mismatch")

    # Artifact writing with registry and department routing
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--department-routing"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v1-4-check-please-"), "run_id format mismatch")
            
            fw = art_sum.get("files_written", [])
            expected_v14 = [
                "department_routing_bundle.json", "department_routing_schema.json",
                "department_route_candidates.json", "family_to_department_routing_map.json",
                "worker_to_department_assignment_map.json", "department_routing_conflict_detector.json",
                "department_routing_dry_run_results.json", "department_routing_ledger.json",
                "department_routing_completion_proofs.json", "department_routing_readiness_summary.json",
                "multi_agent_orchestration_readiness_bridge.json"
            ]
            for f in expected_v14:
                require(errors, f in fw, f"file {f} not in artifact files_written")

            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v1_4_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "1.4.0", "man version mismatch")
                require(errors, man.get("department_routing_readiness_summary") is True, "man summary True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "1.4.0", "rr version mismatch")

    # Regression behavior
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--stable-release-manifest"])
    require(errors, code == 0, f"stable manifest failed: {err}")
    res = parse_json_output(out, "stable manifest", errors)
    if res:
        require(errors, res.get("runtime_version") == "1.4.0", "manifest version mismatch")

def main():
    print("Running validate_station_chief_runtime_v1_4.py...")
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
        
    print("PASS: Station Chief Runtime v1.4 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v1.4 runtime files.")

if __name__ == "__main__":
    main()

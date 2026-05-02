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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v1_5_report.md",
        "scripts/validate_station_chief_runtime_v1_5.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    orchestration_path = REPO_ROOT / "10_runtime/station_chief_multi_agent_orchestration.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    report_skeleton_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    report_v15_path = REPO_ROOT / "09_exports/station_chief_runtime_v1_5_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "1.5.0"',
            "attach_multi_agent_orchestration",
            "write_multi_agent_orchestration",
            "--orchestration-schema",
            "--multi-agent-orchestration",
            "--write-multi-agent-orchestration",
            "orchestration_topology_schema",
            "orchestration_nodes",
            "multi_worker_coordination_map",
            "task_handoff_simulation",
            "inter_worker_dependency_graph",
            "orchestration_conflict_detector",
            "orchestration_dry_run_results",
            "orchestration_ledger",
            "orchestration_completion_proofs",
            "orchestration_readiness_summary",
            "ui_operator_console_readiness_bridge",
            "multi_agent_orchestration_sandbox_only",
            "multi_agent_orchestration_does_not_animate_workers",
            "multi_agent_orchestration_does_not_hire_workers",
            "multi_agent_orchestration_does_not_route_live_workers",
            "multi_agent_orchestration_does_not_perform_live_orchestration",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        orchestration_path,
        [
            'MULTI_AGENT_ORCHESTRATION_MODULE_VERSION = "1.5.0"',
            "MULTI_AGENT_ORCHESTRATION_STATUS",
            "MULTI_AGENT_ORCHESTRATION_PHASE",
            "canonical_json",
            "sha256_digest",
            "normalize_orchestration_label",
            "generate_orchestration_id",
            "create_orchestration_topology_schema",
            "create_orchestration_node",
            "create_orchestration_nodes_from_department_routing",
            "create_multi_worker_coordination_map",
            "create_task_handoff_simulation",
            "create_inter_worker_dependency_graph",
            "detect_orchestration_conflicts",
            "dry_run_multi_agent_orchestration",
            "create_orchestration_ledger",
            "create_orchestration_completion_proof",
            "create_orchestration_completion_proofs",
            "create_orchestration_readiness_summary",
            "create_ui_operator_console_readiness_bridge",
            "create_multi_agent_orchestration_bundle",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        adapter_path,
        ['ADAPTER_MODULE_VERSION = "1.5.0"', 'supports_multi_agent_orchestration_sandbox'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v1.5.0.",
            "Multi-agent orchestration sandbox added.",
            "orchestration topology schema",
            "deterministic orchestration ID generation",
            "orchestration node generation",
            "multi-worker dry-run coordination map",
            "task handoff simulation",
            "inter-worker dependency graph",
            "orchestration conflict detector",
            "orchestration dry-run engine",
            "orchestration ledger",
            "orchestration completion proofs",
            "orchestration readiness summary",
            "UI/operator-console readiness bridge",
            "no live orchestration",
            "no live worker routing",
            "no real worker hiring",
            "no worker animation",
            "Station Chief Runtime v1.5.0 adds the Multi-Agent Orchestration Sandbox without performing live orchestration or worker animation",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_skeleton_path,
        [
            "Station Chief Runtime upgraded to v1.5.0.",
            "Multi-agent orchestration sandbox added.",
            "orchestration topology schema",
            "deterministic orchestration ID generation",
            "orchestration node generation",
            "multi-worker dry-run coordination map",
            "task handoff simulation",
            "inter-worker dependency graph",
            "orchestration conflict detector",
            "orchestration dry-run engine",
            "orchestration ledger",
            "orchestration completion proof",
            "orchestration readiness summary",
            "UI/operator-console readiness bridge",
            "no live orchestration",
            "no live worker routing",
            "no real worker hiring",
            "no worker animation",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_v15_path,
        [
            "Station Chief Runtime v1.5.0 Report",
            "Station Chief Runtime upgraded to v1.5.0. Locked 175-family baseline preserved. Multi-agent orchestration sandbox added.",
            "orchestration topology schema",
            "deterministic orchestration ID generation",
            "multi-worker dry-run coordination map",
            "task handoff simulation",
            "inter-worker dependency graph",
            "orchestration conflict detector",
            "orchestration dry-run engine",
            "orchestration ledger",
            "orchestration completion proof",
            "orchestration readiness summary",
            "UI/operator-console readiness bridge",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "no real worker hiring",
            "no live worker routing",
            "no live orchestration",
            "Station Chief Runtime v1.5.0 adds the Multi-Agent Orchestration Sandbox without performing live orchestration or worker animation",
            "Next recommended build step",
        ]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "1.5.0", "demo runtime version != 1.5.0")
        require(errors, demo.get("runtime_status") == "multi_agent_orchestration_sandbox", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "evidence baseline_preserved must be True")
        require(errors, evidence.get("external_actions_taken") is False, "evidence external_actions_taken must be False")
        require(errors, evidence.get("live_worker_agents_activated") is False, "evidence live_worker_agents_activated must be False")
        require(errors, evidence.get("multi_agent_orchestration_available") is True, "evidence orchestration_available True")
        require(errors, evidence.get("multi_agent_orchestration_sandbox_only") is True, "evidence sandbox_only True")
        require(errors, evidence.get("multi_agent_orchestration_does_not_animate_workers") is True, "evidence no_animation True")
        require(errors, evidence.get("multi_agent_orchestration_does_not_hire_workers") is True, "evidence no_hiring True")
        require(errors, evidence.get("multi_agent_orchestration_does_not_route_live_workers") is True, "evidence no_live_routing True")
        require(errors, evidence.get("multi_agent_orchestration_does_not_perform_live_orchestration") is True, "evidence no_live_orchestration True")
        require(errors, evidence.get("ui_operator_console_schema_not_yet_active") is True, "evidence ui_not_active True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "1.5.0", "fixture runtime_version != 1.5.0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: {err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: {err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "1.5.0", "adapter_module_version != 1.5.0")
        srp = adapters.get("supported_adapters", {}).get("scoped_repo_patch", {})
        require(errors, srp.get("supports_multi_agent_orchestration_sandbox") is True, "scoped_repo_patch supports_multi_agent_orchestration_sandbox must be True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--orchestration-schema"])
    require(errors, code == 0, f"--orchestration-schema failed: {err}")
    schema = parse_json_output(out, "--orchestration-schema", errors)
    if schema:
        require(errors, schema.get("orchestration_topology_schema_version") == "1.5.0", "schema version mismatch")
        require(errors, schema.get("schema_status") == "ORCHESTRATION_SANDBOX_ONLY", "schema status mismatch")
        req = schema.get("required_fields", [])
        require(errors, "orchestration_id" in req, "orchestration_id missing from required fields")
        require(errors, "source_route_id" in req, "source_route_id missing from required fields")
        require(errors, "source_worker_id" in req, "source_worker_id missing from required fields")
        stat = schema.get("allowed_node_statuses", [])
        require(errors, "NODE_CANDIDATE_CREATED" in stat, "NODE_CANDIDATE_CREATED status missing")
        require(errors, "NODE_RECORDED" in stat, "NODE_RECORDED status missing")
        modes = schema.get("allowed_orchestration_modes", [])
        require(errors, "orchestration_sandbox_only" in modes, "orchestration_sandbox_only mode missing")
        require(errors, schema.get("baseline_preserved") is True, "baseline preserved mismatch")
        require(errors, schema.get("external_actions_taken") is False, "external actions taken mismatch")
        require(errors, schema.get("live_worker_agents_activated") is False, "worker animation mismatch")
        require(errors, schema.get("real_worker_hiring_performed") is False, "hiring mismatch")
        require(errors, schema.get("live_worker_routing_performed") is False, "routing mismatch")
        require(errors, schema.get("live_orchestration_performed") is False, "orchestration mismatch")
        require(errors, schema.get("execution_authorized") is False, "execution authorized mismatch")

    # Multi-agent orchestration default
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--multi-agent-orchestration"])
    require(errors, code == 0, f"default multi-agent-orchestration failed: {err}")
    res = parse_json_output(out, "default multi-agent-orchestration", errors)
    if res:
        require(errors, "multi_agent_orchestration_bundle" in res, "multi_agent_orchestration_bundle missing")
        require(errors, "orchestration_topology_schema" in res, "orchestration_topology_schema missing")
        require(errors, "orchestration_nodes" in res, "orchestration_nodes missing")
        require(errors, "multi_worker_coordination_map" in res, "multi_worker_coordination_map missing")
        require(errors, "task_handoff_simulation" in res, "task_handoff_simulation missing")
        require(errors, "inter_worker_dependency_graph" in res, "inter_worker_dependency_graph missing")
        require(errors, "orchestration_conflict_detector" in res, "orchestration_conflict_detector missing")
        require(errors, "orchestration_dry_run_results" in res, "orchestration_dry_run_results missing")
        require(errors, "orchestration_ledger" in res, "orchestration_ledger missing")
        require(errors, "orchestration_completion_proofs" in res, "orchestration_completion_proofs missing")
        require(errors, "orchestration_readiness_summary" in res, "orchestration_readiness_summary missing")
        require(errors, "ui_operator_console_readiness_bridge" in res, "ui_operator_console_readiness_bridge missing")
        
        bundle = res.get("multi_agent_orchestration_bundle", {})
        require(errors, bundle.get("multi_agent_orchestration_bundle_version") == "1.5.0", "bundle version mismatch")
        require(errors, bundle.get("orchestration_status") == "ORCHESTRATION_SANDBOX_ONLY", "orchestration status mismatch")
        
        summ = res.get("orchestration_readiness_summary", {})
        require(errors, summ.get("orchestration_status") == "ORCHESTRATION_SANDBOX_ONLY", "summary orchestration_status mismatch")
        require(errors, summ.get("node_count", 0) >= 1, "node_count < 1")
        require(errors, summ.get("ready_for_ui_operator_console_schema") is True, "ready_for_ui_operator_console_schema mismatch")
        
        conflicts = res.get("orchestration_conflict_detector", {})
        require(errors, conflicts.get("conflict_status") == "CLEAR", "conflict status mismatch")
        
        require(errors, res.get("evidence", {}).get("external_actions_taken") is False, "external actions taken True")
        require(errors, res.get("evidence", {}).get("live_worker_agents_activated") is False, "worker agents activated True")
        require(errors, res.get("evidence", {}).get("live_orchestration_performed", False) is False, "live orchestration performed True")

    # Multi-agent orchestration command for next layer
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build UI operator console schema", "--multi-agent-orchestration"])
    require(errors, code == 0, f"next layer command failed: {err}")
    res = parse_json_output(out, "next layer command", errors)
    if res:
        summ = res.get("orchestration_readiness_summary", {})
        require(errors, summ.get("next_layer") == "UI / Operator Console Schema", "next_layer mismatch")
        bridge = res.get("ui_operator_console_readiness_bridge", {})
        require(errors, bridge.get("next_layer") == "UI / Operator Console Schema", "bridge next_layer mismatch")
        require(errors, bridge.get("ready_for_ui_operator_console_schema") is True, "bridge ready mismatch")
        
        proofs = res.get("orchestration_completion_proofs", [])
        require(errors, len(proofs) >= 1, "proofs empty")
        for p in proofs:
            require(errors, p.get("live_orchestration_performed") is False, "live_orchestration_performed mismatch")
        results = res.get("orchestration_dry_run_results", [])
        for r in results:
            require(errors, r.get("live_orchestration_performed") is False, "dry run live orchestration mismatch")

    # Write multi-agent orchestration
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-multi-agent-orchestration", str(td_path / "mo")
        ])
        require(errors, code == 0, f"write mo failed: {err}")
        write_res = parse_json_output(out, "write mo", errors)
        if write_res:
            require(errors, "multi_agent_orchestration_write_summary" in write_res, "summary missing")
            summ = write_res["multi_agent_orchestration_write_summary"]
            modir = Path(summ.get("multi_agent_orchestration_dir", ""))
            require(errors, modir.exists(), "mo dir missing")
            
            fw = summ.get("files_written", [])
            expected = [
                "multi_agent_orchestration_bundle.json", "orchestration_topology_schema.json",
                "orchestration_nodes.json", "multi_worker_coordination_map.json",
                "task_handoff_simulation.json", "inter_worker_dependency_graph.json",
                "orchestration_conflict_detector.json", "orchestration_dry_run_results.json",
                "orchestration_ledger.json", "orchestration_completion_proofs.json",
                "orchestration_readiness_summary.json", "ui_operator_console_readiness_bridge.json",
                "multi_agent_orchestration_manifest.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in files_written")
                
            manifest = json.loads((modir / "multi_agent_orchestration_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "1.5.0", "manifest version mismatch")
            require(errors, manifest.get("status") == "ORCHESTRATION_SANDBOX_ONLY", "manifest status mismatch")

    # Artifact writing with registry and multi-agent orchestration
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--multi-agent-orchestration"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v1-5-check-please-"), "run_id format mismatch")
            
            fw = art_sum.get("files_written", [])
            expected_v15 = [
                "multi_agent_orchestration_bundle.json", "orchestration_topology_schema.json",
                "orchestration_nodes.json", "multi_worker_coordination_map.json",
                "task_handoff_simulation.json", "inter_worker_dependency_graph.json",
                "orchestration_conflict_detector.json", "orchestration_dry_run_results.json",
                "orchestration_ledger.json", "orchestration_completion_proofs.json",
                "orchestration_readiness_summary.json", "ui_operator_console_readiness_bridge.json"
            ]
            for f in expected_v15:
                require(errors, f in fw, f"file {f} not in artifact files_written")

            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v1_5_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "1.5.0", "man version mismatch")
                require(errors, man.get("orchestration_readiness_summary") is True, "man summary True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "1.5.0", "rr version mismatch")

    # Regression behavior
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--stable-release-manifest"])
    require(errors, code == 0, f"stable manifest failed: {err}")
    res = parse_json_output(out, "stable manifest", errors)
    if res:
        require(errors, res.get("runtime_version") == "1.5.0", "manifest version mismatch")

def main():
    print("Running validate_station_chief_runtime_v1_5.py...")
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
        
    print("PASS: Station Chief Runtime v1.5 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v1.5 runtime files.")

if __name__ == "__main__":
    main()

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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v1_6_report.md",
        "scripts/validate_station_chief_runtime_v1_6.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    console_path = REPO_ROOT / "10_runtime/station_chief_operator_console.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    report_skeleton_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    report_v16_path = REPO_ROOT / "09_exports/station_chief_runtime_v1_6_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "1.6.0"',
            "attach_operator_console",
            "write_operator_console",
            "--operator-console-schema",
            "--operator-console",
            "--write-operator-console",
            "operator_console_bundle",
            "operator_console_review_bundle",
            "operator_console_screen_schema",
            "runtime_status_panel_schema",
            "approval_queue_panel_schema",
            "work_order_panel_schema",
            "worker_registry_panel_schema",
            "department_routing_panel_schema",
            "orchestration_sandbox_panel_schema",
            "release_lock_panel_schema",
            "human_control_surface_schema",
            "operator_action_registry",
            "disabled_action_state_map",
            "operator_console_safety_summary",
            "operator_console_readiness_summary",
            "github_patch_hardening_readiness_bridge",
            "operator_console_schema_only",
            "operator_console_does_not_render_live_ui",
            "operator_console_does_not_authorize_execution",
            "operator_console_does_not_connect_live_apis",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        console_path,
        [
            'OPERATOR_CONSOLE_MODULE_VERSION = "1.6.0"',
            "OPERATOR_CONSOLE_STATUS",
            "OPERATOR_CONSOLE_PHASE",
            "canonical_json",
            "sha256_digest",
            "normalize_console_label",
            "generate_console_id",
            "create_operator_console_screen_schema",
            "create_runtime_status_panel_schema",
            "create_approval_queue_panel_schema",
            "create_work_order_panel_schema",
            "create_worker_registry_panel_schema",
            "create_department_routing_panel_schema",
            "create_orchestration_sandbox_panel_schema",
            "create_release_lock_panel_schema",
            "create_human_control_surface_schema",
            "create_operator_action_registry",
            "create_disabled_action_state_map",
            "create_operator_console_review_bundle",
            "create_operator_console_safety_summary",
            "create_operator_console_readiness_summary",
            "create_github_patch_hardening_readiness_bridge",
            "create_operator_console_bundle",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess", "Flask", "FastAPI", "Django", "React", "http.server", "socketserver", "uvicorn", "streamlit"]
    )

    check_contains(
        errors,
        adapter_path,
        ['ADAPTER_MODULE_VERSION = "1.6.0"', 'supports_operator_console_schema'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v1.6.0.",
            "UI/operator console schema added.",
            "operator console screen schema",
            "runtime status panel schema",
            "approval queue panel schema",
            "work order panel schema",
            "worker registry panel schema",
            "department routing panel schema",
            "orchestration sandbox panel schema",
            "release lock panel schema",
            "human control surface schema",
            "operator action registry",
            "disabled action state map",
            "read_only operator console review bundle",
            "operator console safety summary",
            "operator console readiness summary",
            "GitHub patch hardening readiness bridge",
            "no live UI rendering",
            "no live orchestration",
            "no live worker routing",
            "no real worker hiring",
            "no worker animation",
            "Station Chief Runtime v1.6.0 adds the UI / Operator Console Schema without rendering a live UI or authorizing execution",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_skeleton_path,
        [
            "Station Chief Runtime upgraded to v1.6.0.",
            "UI/operator console schema added.",
            "operator console screen schema",
            "runtime status panel schema",
            "approval queue panel schema",
            "work order panel schema",
            "worker registry panel schema",
            "department routing panel schema",
            "orchestration sandbox panel schema",
            "release lock panel schema",
            "human control surface schema",
            "operator action registry",
            "disabled action state map",
            "operator console review bundle",
            "operator console safety summary",
            "operator console readiness summary",
            "GitHub patch hardening readiness bridge",
            "no live UI rendering",
            "no live orchestration",
            "no live worker routing",
            "no real worker hiring",
            "no worker animation",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_v16_path,
        [
            "Station Chief Runtime v1.6.0 Report",
            "Station Chief Runtime upgraded to v1.6.0. Locked 175-family baseline preserved. UI/operator console schema added.",
            "operator console screen schema",
            "runtime status panel schema",
            "approval queue panel schema",
            "work order panel schema",
            "worker registry panel schema",
            "department routing panel schema",
            "orchestration sandbox panel schema",
            "release lock panel schema",
            "human control surface schema",
            "operator action registry",
            "disabled action state map",
            "read-only operator console review bundle",
            "operator console safety summary",
            "operator console readiness summary",
            "GitHub patch hardening readiness bridge",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "no real worker hiring",
            "no live worker assignment",
            "no live worker routing",
            "no live orchestration",
            "no live UI rendering",
            "Station Chief Runtime v1.6.0 adds the UI / Operator Console Schema without rendering a live UI or authorizing execution",
            "Next recommended build step",
        ]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "1.6.0", "demo runtime version != 1.6.0")
        require(errors, demo.get("runtime_status") == "operator_console_schema", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "evidence baseline_preserved must be True")
        require(errors, evidence.get("external_actions_taken") is False, "evidence external_actions_taken must be False")
        require(errors, evidence.get("live_worker_agents_activated") is False, "evidence live_worker_agents_activated must be False")
        require(errors, evidence.get("operator_console_schema_available") is True, "evidence console_available True")
        require(errors, evidence.get("operator_console_schema_only") is True, "evidence schema_only True")
        require(errors, evidence.get("operator_console_does_not_render_live_ui") is True, "evidence no_live_ui True")
        require(errors, evidence.get("operator_console_does_not_authorize_execution") is True, "evidence no_auth True")
        require(errors, evidence.get("operator_console_does_not_connect_live_apis") is True, "evidence no_live_apis True")
        require(errors, evidence.get("github_patch_hardening_not_yet_active") is True, "evidence patch_hardening_not_active True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "1.6.0", "fixture runtime_version != 1.6.0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: {err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: {err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "1.6.0", "adapter_module_version != 1.6.0")
        srp = adapters.get("supported_adapters", {}).get("scoped_repo_patch", {})
        require(errors, srp.get("supports_operator_console_schema") is True, "scoped_repo_patch supports_operator_console_schema must be True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--operator-console-schema"])
    require(errors, code == 0, f"--operator-console-schema failed: {err}")
    schema = parse_json_output(out, "--operator-console-schema", errors)
    if schema:
        require(errors, schema.get("operator_console_screen_schema_version") == "1.6.0", "schema version mismatch")
        require(errors, schema.get("schema_status") == "SCHEMA_ONLY", "schema status mismatch")
        require(errors, schema.get("console_title") == "Station Chief Operator Console", "console_title mismatch")
        req = schema.get("primary_sections", [])
        require(errors, "runtime_status_panel" in req, "runtime_status_panel missing from primary sections")
        require(errors, "approval_queue_panel" in req, "approval_queue_panel missing from primary sections")
        require(errors, "orchestration_sandbox_panel" in req, "orchestration_sandbox_panel missing from primary sections")
        require(errors, "human_control_surface_panel" in req, "human_control_surface_panel missing from primary sections")
        aim = schema.get("allowed_interaction_modes", [])
        require(errors, "read_only_review" in aim, "read_only_review interaction mode missing")
        bim = schema.get("blocked_interaction_modes", [])
        require(errors, "live_execution" in bim, "live_execution interaction mode missing")
        require(errors, "live_worker_animation" in bim, "live_worker_animation interaction mode missing")
        require(errors, "real_worker_hiring" in bim, "real_worker_hiring interaction mode missing")
        require(errors, "live_orchestration" in bim, "live_orchestration interaction mode missing")
        require(errors, schema.get("baseline_preserved") is True, "baseline preserved mismatch")
        require(errors, schema.get("external_actions_taken") is False, "external actions taken mismatch")
        require(errors, schema.get("live_worker_agents_activated") is False, "worker animation mismatch")
        require(errors, schema.get("real_worker_hiring_performed") is False, "hiring mismatch")
        require(errors, schema.get("live_worker_routing_performed") is False, "routing mismatch")
        require(errors, schema.get("live_orchestration_performed") is False, "orchestration mismatch")
        require(errors, schema.get("live_ui_rendered") is False, "live UI mismatch")
        require(errors, schema.get("execution_authorized") is False, "execution authorized mismatch")

    # Operator console default
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--operator-console"])
    require(errors, code == 0, f"default operator-console failed: {err}")
    res = parse_json_output(out, "default operator-console", errors)
    if res:
        require(errors, "operator_console_bundle" in res, "operator_console_bundle missing")
        require(errors, "operator_console_review_bundle" in res, "operator_console_review_bundle missing")
        require(errors, "operator_console_screen_schema" in res, "operator_console_screen_schema missing")
        require(errors, "runtime_status_panel_schema" in res, "runtime_status_panel_schema missing")
        require(errors, "approval_queue_panel_schema" in res, "approval_queue_panel_schema missing")
        require(errors, "work_order_panel_schema" in res, "work_order_panel_schema missing")
        require(errors, "worker_registry_panel_schema" in res, "worker_registry_panel_schema missing")
        require(errors, "department_routing_panel_schema" in res, "department_routing_panel_schema missing")
        require(errors, "orchestration_sandbox_panel_schema" in res, "orchestration_sandbox_panel_schema missing")
        require(errors, "release_lock_panel_schema" in res, "release_lock_panel_schema missing")
        require(errors, "human_control_surface_schema" in res, "human_control_surface_schema missing")
        require(errors, "operator_action_registry" in res, "operator_action_registry missing")
        require(errors, "disabled_action_state_map" in res, "disabled_action_state_map missing")
        require(errors, "operator_console_safety_summary" in res, "operator_console_safety_summary missing")
        require(errors, "operator_console_readiness_summary" in res, "operator_console_readiness_summary missing")
        require(errors, "github_patch_hardening_readiness_bridge" in res, "github_patch_hardening_readiness_bridge missing")
        
        bundle = res.get("operator_console_bundle", {})
        require(errors, bundle.get("operator_console_bundle_version") == "1.6.0", "bundle version mismatch")
        require(errors, bundle.get("console_status") == "SCHEMA_ONLY", "console status mismatch")
        
        safety = res.get("operator_console_safety_summary", {})
        require(errors, safety.get("safety_status") == "SAFE_SCHEMA_ONLY", "safety status mismatch")
        
        summ = res.get("operator_console_readiness_summary", {})
        require(errors, summ.get("console_status") == "SCHEMA_ONLY", "summary console_status mismatch")
        require(errors, summ.get("ready_for_github_patch_hardening") is True, "ready_for_github_patch_hardening mismatch")
        
        bridge = res.get("github_patch_hardening_readiness_bridge", {})
        require(errors, bridge.get("ready_for_github_patch_hardening") is True, "bridge ready mismatch")
        
        require(errors, res.get("evidence", {}).get("external_actions_taken") is False, "external actions taken True")
        require(errors, res.get("evidence", {}).get("live_worker_agents_activated") is False, "worker agents activated True")
        require(errors, res.get("evidence", {}).get("live_ui_rendered", False) is False, "live UI rendered True")

    # Operator console command for next layer
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build GitHub patch application hardening", "--operator-console"])
    require(errors, code == 0, f"next layer command failed: {err}")
    res = parse_json_output(out, "next layer command", errors)
    if res:
        summ = res.get("operator_console_readiness_summary", {})
        require(errors, summ.get("next_layer") == "GitHub Patch Application Hardening", "next_layer mismatch")
        bridge = res.get("github_patch_hardening_readiness_bridge", {})
        require(errors, bridge.get("next_layer") == "GitHub Patch Application Hardening", "bridge next_layer mismatch")
        require(errors, bridge.get("ready_for_github_patch_hardening") is True, "bridge ready mismatch")
        
        registry = res.get("operator_action_registry", {})
        blocked = registry.get("blocked_actions", [])
        require(errors, "execute_live_action" in blocked, "execute_live_action not blocked")
        require(errors, "animate_worker" in blocked, "animate_worker not blocked")
        require(errors, "hire_real_worker" in blocked, "hire_real_worker not blocked")
        require(errors, "perform_live_orchestration" in blocked, "perform_live_orchestration not blocked")
        
        disabled = res.get("disabled_action_state_map", {})
        require(errors, disabled.get("disabled_action_count", 0) >= 1, "disabled_action_count < 1")

    # Write operator console
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-operator-console", str(td_path / "oc")
        ])
        require(errors, code == 0, f"write oc failed: {err}")
        write_res = parse_json_output(out, "write oc", errors)
        if write_res:
            require(errors, "operator_console_write_summary" in write_res, "summary missing")
            summ = write_res["operator_console_write_summary"]
            ocdir = Path(summ.get("operator_console_dir", ""))
            require(errors, ocdir.exists(), "oc dir missing")
            
            fw = summ.get("files_written", [])
            expected = [
                "operator_console_bundle.json", "operator_console_review_bundle.json",
                "operator_console_screen_schema.json", "runtime_status_panel_schema.json",
                "approval_queue_panel_schema.json", "work_order_panel_schema.json",
                "worker_registry_panel_schema.json", "department_routing_panel_schema.json",
                "orchestration_sandbox_panel_schema.json", "release_lock_panel_schema.json",
                "human_control_surface_schema.json", "operator_action_registry.json",
                "disabled_action_state_map.json", "operator_console_safety_summary.json",
                "operator_console_readiness_summary.json", "github_patch_hardening_readiness_bridge.json",
                "operator_console_manifest.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in files_written")
                
            manifest = json.loads((ocdir / "operator_console_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "1.6.0", "manifest version mismatch")
            require(errors, manifest.get("status") == "SCHEMA_ONLY", "manifest status mismatch")

    # Artifact writing with registry and operator console
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--operator-console"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v1-6-check-please-"), "run_id format mismatch")
            
            fw = art_sum.get("files_written", [])
            expected_v16 = [
                "operator_console_bundle.json", "operator_console_review_bundle.json",
                "operator_console_screen_schema.json", "runtime_status_panel_schema.json",
                "approval_queue_panel_schema.json", "work_order_panel_schema.json",
                "worker_registry_panel_schema.json", "department_routing_panel_schema.json",
                "orchestration_sandbox_panel_schema.json", "release_lock_panel_schema.json",
                "human_control_surface_schema.json", "operator_action_registry.json",
                "disabled_action_state_map.json", "operator_console_safety_summary.json",
                "operator_console_readiness_summary.json", "github_patch_hardening_readiness_bridge.json"
            ]
            for f in expected_v16:
                require(errors, f in fw, f"file {f} not in artifact files_written")

            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v1_6_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "1.6.0", "man version mismatch")
                require(errors, man.get("operator_console_readiness_summary") is True, "man summary True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "1.6.0", "rr version mismatch")

    # Regression behavior
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--stable-release-manifest"])
    require(errors, code == 0, f"stable manifest failed: {err}")
    res = parse_json_output(out, "stable manifest", errors)
    if res:
        require(errors, res.get("runtime_version") == "1.6.0", "manifest version mismatch")

def main():
    print("Running validate_station_chief_runtime_v1_6.py...")
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
        
    print("PASS: Station Chief Runtime v1.6 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v1.6 runtime files.")

if __name__ == "__main__":
    main()

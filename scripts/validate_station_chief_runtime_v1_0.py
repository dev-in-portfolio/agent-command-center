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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v1_0_report.md",
        "scripts/validate_station_chief_runtime_v1_0.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    profiles_path = REPO_ROOT / "10_runtime/station_chief_execution_profiles.py"
    handoff_path = REPO_ROOT / "10_runtime/station_chief_approval_handoff.py"
    records_path = REPO_ROOT / "10_runtime/station_chief_approval_records.py"
    ledger_path = REPO_ROOT / "10_runtime/station_chief_approval_ledger.py"
    release_lock_path = REPO_ROOT / "10_runtime/station_chief_release_lock.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    report_skeleton_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    report_v10_path = REPO_ROOT / "09_exports/station_chief_runtime_v1_0_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "1.0.0"',
            "attach_release_lock",
            "write_release_lock",
            "--release-lock",
            "--stable-release-manifest",
            "--write-release-lock",
            "--verify-release-manifest",
            "stable_runtime_contract",
            "stable_release_manifest",
            "stable_capability_inventory",
            "stable_artifact_contract",
            "stable_adapter_boundary_contract",
            "stable_safety_doctrine_lock",
            "stable_approval_flow_lock",
            "stable_known_limitations_record",
            "stable_next_phase_handoff",
            "stable_release_readiness_summary",
            "stable_release_locked",
            "release_lock_does_not_execute_patch",
            "v1_0_stable_foundation_complete",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        release_lock_path,
        [
            'RELEASE_LOCK_MODULE_VERSION = "1.0.0"',
            'STABLE_RUNTIME_VERSION = "1.0.0"',
            "create_stable_capability_inventory",
            "create_stable_runtime_contract",
            "create_stable_artifact_contract",
            "create_stable_adapter_boundary_contract",
            "create_stable_safety_doctrine_lock",
            "create_stable_approval_flow_lock",
            "create_known_limitations_record",
            "create_next_phase_handoff_record",
            "create_release_readiness_summary",
            "create_stable_release_manifest",
            "verify_stable_release_manifest",
            "create_release_lock_bundle",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        adapter_path,
        ['ADAPTER_MODULE_VERSION = "1.0.0"', 'stable_release_locked'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        profiles_path,
        ['EXECUTION_PROFILE_MODULE_VERSION = "1.0.0"', 'dry_run_bundle_version', '1.0.0'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        handoff_path,
        ['APPROVAL_HANDOFF_MODULE_VERSION = "1.0.0"', 'approval_handoff_version', '1.0.0'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        records_path,
        ['APPROVAL_RECORD_MODULE_VERSION = "1.0.0"', 'approval_record_version', '1.0.0', 'approval_review_ui_schema_version', 'approval_record_audit_manifest_version'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        ledger_path,
        ['APPROVAL_LEDGER_MODULE_VERSION = "1.0.0"', 'approval_ledger_version', '1.0.0', 'approval_record_comparison_version', 'ledger_verification_version'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v1.0.0.",
            "Stable runtime foundation locked.",
            "stable runtime contract",
            "stable release manifest",
            "stable capability inventory",
            "stable artifact contract",
            "stable adapter boundary contract",
            "stable safety doctrine lock",
            "stable approval flow lock",
            "stable known limitations record",
            "stable next-phase handoff",
            "release_lock_bundle.json",
            "stable_release_manifest.json",
            "stable_release_verification.json",
            "stable_runtime_contract.json",
            "stable_capability_inventory.json",
            "stable_artifact_contract.json",
            "stable_adapter_boundary_contract.json",
            "stable_safety_doctrine_lock.json",
            "stable_approval_flow_lock.json",
            "known_limitations.json",
            "next_phase_handoff.json",
            "release_readiness_summary.json",
            "The Station Chief runtime keeps the full 175-family command civilization intact",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_skeleton_path,
        [
            "Station Chief Runtime upgraded to v1.0.0.",
            "Stable runtime foundation locked.",
            "stable runtime contract",
            "stable release manifest",
            "stable capability inventory",
            "stable artifact contract",
            "stable adapter boundary contract",
            "stable safety doctrine lock",
            "stable approval flow lock",
            "no live API calls",
            "no full workforce animation",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_v10_path,
        [
            "Station Chief Runtime v1.0.0 Report",
            "Station Chief Runtime upgraded to v1.0.0. Locked 175-family baseline preserved. Stable runtime foundation locked.",
            "stable release lock",
            "stable runtime contract",
            "stable artifact contract",
            "stable adapter boundary contract",
            "stable safety doctrine lock",
            "stable approval flow lock",
            "known limitations record",
            "release readiness summary",
            "next-phase handoff",
            "v1.0 release lock does not execute repo patches by itself",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "Station Chief Runtime v1.0.0 keeps execution deterministic",
            "Next recommended build step",
        ]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: rc={code}, stderr={err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "1.0.0", "demo runtime version != 1.0.0")
        require(errors, demo.get("runtime_status") == "stable_release_locked", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type != verification")
        require(errors, demo.get("activation_tier", {}).get("name") == "Tier 4 — Audit / Archive", "demo tier != Tier 4")
        caps = demo.get("run_capabilities", {})
        require(errors, caps.get("stable_runtime_contract") is True, "capability stable_runtime_contract missing")
        require(errors, caps.get("stable_release_manifest") is True, "capability stable_release_manifest missing")
        require(errors, caps.get("stable_capability_inventory") is True, "capability stable_capability_inventory missing")
        require(errors, caps.get("stable_artifact_contract") is True, "capability stable_artifact_contract missing")
        require(errors, caps.get("stable_adapter_boundary_contract") is True, "capability stable_adapter_boundary_contract missing")
        require(errors, caps.get("stable_safety_doctrine_lock") is True, "capability stable_safety_doctrine_lock missing")
        require(errors, caps.get("stable_approval_flow_lock") is True, "capability stable_approval_flow_lock missing")
        require(errors, caps.get("stable_known_limitations_record") is True, "capability stable_known_limitations_record missing")
        require(errors, caps.get("stable_next_phase_handoff") is True, "capability stable_next_phase_handoff missing")
        require(errors, caps.get("stable_release_readiness_summary") is True, "capability stable_release_readiness_summary missing")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "evidence baseline_preserved must be True")
        require(errors, evidence.get("external_actions_taken") is False, "evidence external_actions_taken must be False")
        require(errors, evidence.get("live_worker_agents_activated") is False, "evidence live_worker_agents_activated must be False")
        require(errors, evidence.get("deterministic_demo_mode") is True, "evidence deterministic_demo_mode must be True")
        require(errors, evidence.get("stable_release_locked") is True, "evidence stable_release_locked must be True")
        require(errors, evidence.get("release_manifest_available") is True, "evidence release_manifest_available must be True")
        require(errors, evidence.get("release_lock_does_not_execute_patch") is True, "evidence release_lock_does_not_execute_patch must be True")
        require(errors, evidence.get("v1_0_stable_foundation_complete") is True, "evidence v1_0_stable_foundation_complete must be True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: rc={code}, stderr={err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "1.0.0", "fixture runtime_version != 1.0.0")
        require(errors, fixture.get("case_count") == 5, "fixture case_count != 5")
        require(errors, fixture.get("failed") == 0, "fixture failed != 0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: rc={code}, stderr={err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: rc={code}, stderr={err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "1.0.0", "adapter_module_version != 1.0.0")
        srp = adapters.get("supported_adapters", {}).get("scoped_repo_patch", {})
        require(errors, srp.get("stable_release_locked") is True, "scoped_repo_patch stable_release_locked must be True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--stable-release-manifest"])
    require(errors, code == 0, f"--stable-release-manifest failed: rc={code}, stderr={err}")
    manifest = parse_json_output(out, "--stable-release-manifest", errors)
    if manifest:
        require(errors, manifest.get("stable_release_manifest_version") == "1.0.0", "stable_release_manifest_version != 1.0.0")
        require(errors, manifest.get("release_status") == "STABLE_LOCKED", "release_status != STABLE_LOCKED")
        require(errors, manifest.get("runtime_version") == "1.0.0", "runtime_version != 1.0.0")
        require(errors, "release_digest" in manifest, "release_digest missing")
        require(errors, manifest.get("release_readiness_summary", {}).get("release_readiness_status") == "READY_FOR_V1_0_LOCK", "release_readiness_status mismatch")

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        
        # A. Release lock output
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--release-lock"
        ])
        require(errors, code == 0, f"release lock failed: {err}")
        res = parse_json_output(out, "release-lock", errors)
        if res:
            require(errors, "release_lock_bundle" in res, "release_lock_bundle missing")
            require(errors, "stable_release_manifest" in res, "stable_release_manifest missing")
            require(errors, "stable_release_verification" in res, "stable_release_verification missing")
            require(errors, res.get("release_lock_bundle", {}).get("release_lock_bundle_version") == "1.0.0", "bundle version mismatch")
            require(errors, res.get("stable_release_verification", {}).get("verification_status") == "PASS", "verification failed")

        # B. Write release lock
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-release-lock", str(td_path / "locks")
        ])
        require(errors, code == 0, f"write release lock failed: {err}")
        write_res = parse_json_output(out, "write release lock", errors)
        if write_res:
            require(errors, "release_lock_write_summary" in write_res, "summary missing")
            summ = write_res["release_lock_write_summary"]
            ldir = Path(summ.get("release_lock_dir", ""))
            require(errors, ldir.exists(), "release_lock_dir does not exist")
            
            fw = summ.get("files_written", [])
            expected = [
                "release_lock_bundle.json", "stable_release_manifest.json",
                "stable_release_verification.json", "stable_runtime_contract.json",
                "stable_capability_inventory.json", "stable_artifact_contract.json",
                "stable_adapter_boundary_contract.json", "stable_safety_doctrine_lock.json",
                "stable_approval_flow_lock.json", "known_limitations.json",
                "next_phase_handoff.json", "release_readiness_summary.json",
                "release_lock_manifest.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in files_written")
            
            # C. Verify release manifest
            code, out, err = run_command([
                "python3", "10_runtime/station_chief_runtime.py",
                "--verify-release-manifest", str(ldir / "stable_release_manifest.json")
            ])
            require(errors, code == 0, f"verify manifest failed: {err}")
            ver_res = parse_json_output(out, "verify manifest", errors)
            if ver_res:
                require(errors, ver_res.get("stable_release_verification_version") == "1.0.0", "ver version mismatch")
                require(errors, ver_res.get("verification_status") == "PASS", "ver status != PASS")
                require(errors, ver_res.get("release_digest_matches") is True, "digest matches mismatch")

            # D. Tampered release manifest verification fails
            tampered = json.loads((ldir / "stable_release_manifest.json").read_text())
            tampered["release_status"] = "UNSTABLE"
            (td_path / "tampered_manifest.json").write_text(json.dumps(tampered))
            
            code, out, err = run_command([
                "python3", "10_runtime/station_chief_runtime.py",
                "--verify-release-manifest", str(td_path / "tampered_manifest.json")
            ])
            require(errors, code == 0, f"verify tampered manifest failed: {err}")
            t_res = parse_json_output(out, "verify tampered manifest", errors)
            if t_res:
                require(errors, t_res.get("verification_status") == "FAIL", "tampered manifest must FAIL")
                require(errors, t_res.get("release_digest_matches") is False, "tampered digest matches must be False")

    # Regression and artifact writing with registry and release lock
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--release-lock"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v1-0-check-please-"), "run_id format mismatch")
            
            fw = art_sum.get("files_written", [])
            expected_v10 = [
                "release_lock_bundle.json", "stable_release_manifest.json",
                "stable_release_verification.json", "stable_runtime_contract.json",
                "stable_capability_inventory.json", "stable_artifact_contract.json",
                "stable_adapter_boundary_contract.json", "stable_safety_doctrine_lock.json",
                "stable_approval_flow_lock.json", "known_limitations.json",
                "next_phase_handoff.json", "release_readiness_summary.json"
            ]
            for f in expected_v10:
                require(errors, f in fw, f"file {f} not in artifact files_written")

            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v1_0_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "1.0.0", "man version mismatch")
                require(errors, man.get("stable_release_locked") is True, "man stable_release_locked True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "1.0.0", "rr version mismatch")
            require(errors, any(r.get("run_id") == run_id for r in rr.get("runs", [])), "rr run_id missing")

def main():
    print("Running validate_station_chief_runtime_v1_0.py...")
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
        
    print("PASS: Station Chief Runtime v1.0 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v1.0 runtime files.")

if __name__ == "__main__":
    main()

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
            
        # Find the earliest occurrence of { or [
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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v0_9_report.md",
        "scripts/validate_station_chief_runtime_v0_9.py",
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
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    report_skeleton_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    report_v09_path = REPO_ROOT / "09_exports/station_chief_runtime_v0_9_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "0.9.0"',
            "attach_approval_ledger",
            "write_approval_ledger",
            "--compare-approval-records",
            "--approval-record-file",
            "--approval-ledger-index",
            "--approval-ledger-label",
            "--write-approval-ledger",
            "--verify-approval-ledger",
            "--lookup-approval-digest",
            "approval_ledger_indexing",
            "signed_approval_comparison",
            "approval_history_lookup",
            "approval_duplicate_detection",
            "approval_ledger_bundle",
            "approval_ledger_index",
            "approval_ledger_verification",
            "approval_status_summary",
            "duplicate_approval_signals",
            "approval_record_comparison",
            "approval_ledger_does_not_execute_patch",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        ledger_path,
        [
            'APPROVAL_LEDGER_MODULE_VERSION = "0.9.0"',
            "canonical_json",
            "sha256_digest",
            "load_json_file",
            "extract_approval_record_summary",
            "compare_signed_approval_records",
            "collect_approval_records_from_paths",
            "create_approval_status_summary",
            "find_duplicate_approval_signals",
            "create_approval_ledger_index",
            "verify_approval_ledger_index",
            "lookup_approval_records_by_digest",
            "create_approval_ledger_bundle",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        adapter_path,
        ['ADAPTER_MODULE_VERSION = "0.9.0"', '"supports_approval_ledger"'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        profiles_path,
        ['EXECUTION_PROFILE_MODULE_VERSION = "0.9.0"', 'dry_run_bundle_version', '0.9.0'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        handoff_path,
        ['APPROVAL_HANDOFF_MODULE_VERSION = "0.9.0"', 'approval_handoff_version', '0.9.0'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        records_path,
        ['APPROVAL_RECORD_MODULE_VERSION = "0.9.0"', 'approval_record_version', '0.9.0', 'approval_review_ui_schema_version', 'approval_record_audit_manifest_version'],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v0.9.0.",
            "approval ledger indexing",
            "signed approval comparison",
            "approval history lookup",
            "duplicate approval detection",
            "approval_ledger_bundle.json",
            "approval_ledger_index.json",
            "approval_ledger_verification.json",
            "approval_status_summary.json",
            "duplicate_approval_signals.json",
            "approval_ledger_lookup.json",
            "approval_record_comparison.json",
            "approval ledgers do not execute repo patches by themselves",
            "The Station Chief runtime keeps the full 175-family command civilization intact",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_skeleton_path,
        [
            "Station Chief Runtime upgraded to v0.9.0.",
            "approval ledger indexing",
            "signed approval comparison",
            "approval history lookup",
            "duplicate approval detection",
            "no live API calls",
            "no full workforce animation",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_v09_path,
        [
            "Station Chief Runtime v0.9.0 Report",
            "Station Chief Runtime upgraded to v0.9.0. Locked 175-family baseline preserved.",
            "approval ledger indexing",
            "signed approval record comparison",
            "approval chain validation",
            "duplicate approval detection",
            "tamper-signal detection",
            "approval status summaries",
            "approval ledger bundle artifacts",
            "approval history lookup",
            "approval ledgers do not execute repo patches by themselves",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "Station Chief Runtime v0.9.0 keeps execution deterministic",
            "Next recommended build step",
        ]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    # Basic Checks
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: rc={code}, stderr={err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "0.9.0", "demo runtime version != 0.9.0")
        require(errors, demo.get("command_type") == "verification", "demo command_type != verification")
        require(errors, demo.get("activation_tier", {}).get("name") == "Tier 4 — Audit / Archive", "demo tier != Tier 4")
        caps = demo.get("run_capabilities", {})
        require(errors, caps.get("approval_ledger_indexing") is True, "capability approval_ledger_indexing missing")
        require(errors, caps.get("signed_approval_comparison") is True, "capability signed_approval_comparison missing")
        require(errors, caps.get("approval_history_lookup") is True, "capability approval_history_lookup missing")
        require(errors, caps.get("approval_duplicate_detection") is True, "capability approval_duplicate_detection missing")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "evidence baseline_preserved must be True")
        require(errors, evidence.get("external_actions_taken") is False, "evidence external_actions_taken must be False")
        require(errors, evidence.get("live_worker_agents_activated") is False, "evidence live_worker_agents_activated must be False")
        require(errors, evidence.get("deterministic_demo_mode") is True, "evidence deterministic_demo_mode must be True")
        require(errors, evidence.get("approval_ledger_does_not_execute_patch") is True, "evidence approval_ledger_does_not_execute_patch must be True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: rc={code}, stderr={err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "0.9.0", "fixture runtime_version != 0.9.0")
        require(errors, fixture.get("case_count") == 5, "fixture case_count != 5")
        require(errors, fixture.get("failed") == 0, "fixture failed != 0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: rc={code}, stderr={err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--json"])
    require(errors, code == 0, f"--json failed: rc={code}, stderr={err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build Station Chief runtime skeleton", "--brief"])
    require(errors, code == 0, f"--brief failed: rc={code}, stderr={err}")
    brief = parse_json_output(out, "--brief", errors)
    if brief:
        require(errors, brief.get("command_type") == "build", "brief command_type != build")
        require(errors, brief.get("activation_tier", {}).get("name") == "Tier 3 — Active Operation", "brief tier != Tier 3")
        require(errors, brief.get("deterministic_demo_mode") is True, "brief deterministic_demo_mode must be True")
        require(errors, brief.get("baseline_protection") is True, "brief baseline_protection must be True")
        require(errors, brief.get("external_actions_allowed") is False, "brief external_actions_allowed must be False")
        require(errors, brief.get("workforce_animation_allowed") is False, "brief workforce_animation_allowed must be False")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-overlays"])
    require(errors, code == 0, f"--list-overlays failed: rc={code}, stderr={err}")
    overlays = parse_json_output(out, "--list-overlays", errors)
    if overlays:
        require(errors, len(overlays) == 8, "exactly 8 overlays expected")
        require(errors, all(o.get("exists") for o in overlays), "every overlay exists must be True")
        require(errors, all(o.get("preserves_locked_baseline") for o in overlays), "every overlay preserves_locked_baseline must be True")
        require(errors, all("Devin O’Rourke" in (o.get("ownership_project_owner") or "") for o in overlays), "ownership must contain Devin O’Rourke")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: rc={code}, stderr={err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "0.9.0", "adapter_module_version != 0.9.0")
        supported = adapters.get("supported_adapters", {})
        require(errors, "noop" in supported, "noop adapter missing")
        require(errors, "sandbox_file_write" in supported, "sandbox_file_write missing")
        require(errors, "scoped_repo_patch" in supported, "scoped_repo_patch missing")
        srp = supported.get("scoped_repo_patch", {})
        require(errors, srp.get("supports_dry_run_bundle") is True, "scoped_repo_patch supports_dry_run_bundle must be True")
        require(errors, srp.get("supports_approval_handoff") is True, "scoped_repo_patch supports_approval_handoff must be True")
        require(errors, srp.get("supports_signed_approval_records") is True, "scoped_repo_patch supports_signed_approval_records must be True")
        require(errors, srp.get("supports_approval_ledger") is True, "scoped_repo_patch supports_approval_ledger must be True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-execution-profiles"])
    require(errors, code == 0, f"--list-execution-profiles failed: rc={code}, stderr={err}")
    profiles = parse_json_output(out, "--list-execution-profiles", errors)
    if profiles:
        require(errors, profiles.get("execution_profile_module_version") == "0.9.0", "execution_profile_module_version != 0.9.0")
        ep = profiles.get("execution_profiles", {})
        require(errors, "audit_only" in ep, "audit_only missing")
        require(errors, "dry_run_patch" in ep, "dry_run_patch missing")
        require(errors, "sandbox_write" in ep, "sandbox_write missing")
        require(errors, "scoped_repo_patch" in ep, "scoped_repo_patch missing")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--approval-review-ui-schema"])
    require(errors, code == 0, f"--approval-review-ui-schema failed: rc={code}, stderr={err}")
    schema = parse_json_output(out, "--approval-review-ui-schema", errors)
    if schema:
        require(errors, schema.get("approval_review_ui_schema_version") == "0.9.0", "approval_review_ui_schema_version != 0.9.0")
        fields = [f.get("field_id") for f in schema.get("fields", [])]
        require(errors, "reviewer_name" in fields, "reviewer_name field missing")
        require(errors, "approval_decision" in fields, "approval_decision field missing")
        require(errors, "confirmation_token" in fields, "confirmation_token field missing")
        decisions = schema.get("approval_decisions", {})
        require(errors, "approve" in decisions, "approve decision missing")
        require(errors, "reject" in decisions, "reject decision missing")
        require(errors, "needs_changes" in decisions, "needs_changes decision missing")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--simulate-adapter"])
    require(errors, code == 0, f"--simulate-adapter failed: rc={code}, stderr={err}")
    sim = parse_json_output(out, "--simulate-adapter", errors)
    if sim:
        require(errors, "execution_plan" in sim, "execution_plan missing")
        require(errors, "adapter_result" in sim, "adapter_result missing")
        ar = sim.get("adapter_result", {})
        require(errors, ar.get("adapter_result_status") == "PASS", "adapter_result_status != PASS")
        require(errors, ar.get("live_execution_performed") is False, "live_execution_performed must be False")
        require(errors, ar.get("external_actions_taken") is False, "external_actions_taken must be False")
        require(errors, ar.get("worker_agents_activated") is False, "worker_agents_activated must be False")

    # Ledger specific tests
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        record_a = {}
        record_b = {}
        
        # A. Create two approval record files
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--plan-repo-patch",
            "--patch-root", str(td_path),
            "--allowed-patch-file", "test.txt",
            "--sign-approval-record",
            "--approval-reviewer", "Devin O’Rourke",
            "--approval-decision", "approve",
            "--approval-record-token", "YES_I_APPROVE_APPROVAL_HANDOFF_RECORD",
            "--patch-preview-reviewed",
            "--changed-file-scope-reviewed",
            "--baseline-protection-reviewed",
            "--risk-summary-reviewed",
        ])
        require(errors, code == 0, f"sign record A failed: {err}")
        res_a = parse_json_output(out, "record A", errors)
        if res_a:
            record_a = res_a.get("signed_approval_record")
            (td_path / "record_a.json").write_text(json.dumps(record_a))
            
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--plan-repo-patch",
            "--patch-root", str(td_path),
            "--allowed-patch-file", "test.txt",
            "--sign-approval-record",
            "--approval-reviewer", "Devin O’Rourke",
            "--approval-decision", "needs_changes",
            "--approval-record-token", "YES_I_APPROVE_APPROVAL_HANDOFF_RECORD",
            "--patch-preview-reviewed",
            "--changed-file-scope-reviewed",
            "--baseline-protection-reviewed",
            "--risk-summary-reviewed",
        ])
        require(errors, code == 0, f"sign record B failed: {err}")
        res_b = parse_json_output(out, "record B", errors)
        if res_b:
            record_b = res_b.get("signed_approval_record")
            (td_path / "record_b.json").write_text(json.dumps(record_b))
            
        # B. Compare approval records
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--compare-approval-records",
            str(td_path / "record_a.json"),
            str(td_path / "record_b.json")
        ])
        require(errors, code == 0, f"compare records failed: {err}")
        comp = parse_json_output(out, "compare records", errors)
        if comp:
            require(errors, comp.get("approval_record_comparison_version") == "0.9.0", "approval_record_comparison_version != 0.9.0")
            require(errors, comp.get("comparison_status") == "CHANGED", "comparison_status != CHANGED")
            require(errors, comp.get("approval_decision_changed") is True, "approval_decision_changed must be True")
            require(errors, comp.get("baseline_preserved") is True, "baseline_preserved must be True")
            require(errors, comp.get("external_actions_taken") is False, "external_actions_taken must be False")
            require(errors, comp.get("live_worker_agents_activated") is False, "live_worker_agents_activated must be False")

        # C. Approval ledger index
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--approval-ledger-index",
            "--approval-record-file", str(td_path / "record_a.json"),
            "--approval-record-file", str(td_path / "record_b.json")
        ])
        require(errors, code == 0, f"ledger index failed: {err}")
        idx_res = parse_json_output(out, "ledger index", errors)
        if idx_res:
            require(errors, "approval_ledger_bundle" in idx_res, "approval_ledger_bundle missing")
            require(errors, "approval_ledger_index" in idx_res, "approval_ledger_index missing")
            require(errors, "approval_ledger_verification" in idx_res, "approval_ledger_verification missing")
            require(errors, "approval_status_summary" in idx_res, "approval_status_summary missing")
            require(errors, "duplicate_approval_signals" in idx_res, "duplicate_approval_signals missing")
            
            idx = idx_res.get("approval_ledger_index", {})
            require(errors, idx.get("approval_ledger_version") == "0.9.0", "ledger version != 0.9.0")
            require(errors, idx.get("record_count") == 2, "record_count != 2")
            require(errors, idx.get("execution_authorized") is False, "execution_authorized must be False")
            
            ver = idx_res.get("approval_ledger_verification", {})
            require(errors, ver.get("verification_status") == "PASS", "verification_status != PASS")
            
            summ = idx_res.get("approval_status_summary", {})
            require(errors, summ.get("total_records") == 2, "total_records != 2")
            require(errors, summ.get("signed_records") == 2, "signed_records != 2")
            require(errors, summ.get("approve_records", 0) >= 1, "approve_records < 1")
            require(errors, summ.get("needs_changes_records", 0) >= 1, "needs_changes_records < 1")

        # D. Duplicate detection
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--approval-ledger-index",
            "--approval-record-file", str(td_path / "record_a.json"),
            "--approval-record-file", str(td_path / "record_a.json")
        ])
        require(errors, code == 0, f"duplicate detection failed: {err}")
        dup_res = parse_json_output(out, "duplicate detection", errors)
        if dup_res:
            sigs = dup_res.get("duplicate_approval_signals", {})
            require(errors, sigs.get("duplicate_signal_status") == "DUPLICATES_FOUND", "status != DUPLICATES_FOUND")
            require(errors, len(sigs.get("duplicate_approval_signatures", [])) >= 1, "signatures length < 1")
            
            summ = dup_res.get("approval_status_summary", {})
            require(errors, summ.get("duplicate_signature_count", 0) >= 1, "count < 1")

        # E. Lookup approval digest
        digest = record_a.get("approval_packet_digest", "")
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--approval-ledger-index",
            "--approval-record-file", str(td_path / "record_a.json"),
            "--approval-record-file", str(td_path / "record_b.json"),
            "--lookup-approval-digest", digest
        ])
        require(errors, code == 0, f"lookup failed: {err}")
        look_res = parse_json_output(out, "lookup", errors)
        if look_res:
            lookup = look_res.get("approval_ledger_lookup", {})
            require(errors, lookup.get("lookup_version") == "0.9.0", "lookup_version != 0.9.0")
            require(errors, lookup.get("match_count", 0) >= 1, "match_count < 1")
            require(errors, lookup.get("approval_packet_digest") == digest, "digest mismatch")

        # F. Write approval ledger
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-approval-ledger", str(td_path / "ledgers"),
            "--approval-record-file", str(td_path / "record_a.json"),
            "--approval-record-file", str(td_path / "record_b.json")
        ])
        require(errors, code == 0, f"write ledger failed: {err}")
        write_res = parse_json_output(out, "write ledger", errors)
        if write_res:
            require(errors, "approval_ledger_write_summary" in write_res, "summary missing")
            summ = write_res["approval_ledger_write_summary"]
            ldir = Path(summ.get("approval_ledger_dir", ""))
            require(errors, ldir.exists(), "approval_ledger_dir does not exist")
            
            fw = summ.get("files_written", [])
            expected = [
                "approval_ledger_bundle.json", "approval_ledger_index.json",
                "approval_ledger_verification.json", "approval_status_summary.json",
                "duplicate_approval_signals.json", "approval_ledger_lookup.json",
                "approval_ledger_manifest.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in files_written")
                
            manifest = json.loads((ldir / "approval_ledger_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "0.9.0", "manifest version mismatch")
            require(errors, manifest.get("baseline_preserved") is True, "manifest baseline_preserved True")
            require(errors, manifest.get("external_actions_taken") is False, "manifest external_actions_taken False")
            require(errors, manifest.get("live_worker_agents_activated") is False, "manifest live_worker_agents_activated False")
            require(errors, manifest.get("execution_authorized") is False, "manifest execution_authorized False")

            # G. Verify approval ledger
            code, out, err = run_command([
                "python3", "10_runtime/station_chief_runtime.py",
                "--verify-approval-ledger", str(ldir / "approval_ledger_index.json")
            ])
            require(errors, code == 0, f"verify ledger failed: {err}")
            ver_res = parse_json_output(out, "verify ledger", errors)
            if ver_res:
                require(errors, ver_res.get("ledger_verification_version") == "0.9.0", "ver version != 0.9.0")
                require(errors, ver_res.get("verification_status") == "PASS", "ver status != PASS")
                require(errors, ver_res.get("ledger_digest_matches") is True, "digest matches must be True")
                require(errors, ver_res.get("execution_authorized") is False, "execution_authorized must be False")

            # H. Tampered ledger
            tampered = json.loads((ldir / "approval_ledger_index.json").read_text())
            tampered["record_count"] = 999
            (td_path / "tampered.json").write_text(json.dumps(tampered))
            
            code, out, err = run_command([
                "python3", "10_runtime/station_chief_runtime.py",
                "--verify-approval-ledger", str(td_path / "tampered.json")
            ])
            require(errors, code == 0, f"verify tampered failed: {err}")
            t_res = parse_json_output(out, "verify tampered", errors)
            if t_res:
                require(errors, t_res.get("verification_status") == "FAIL", "tampered verification must FAIL")
                require(errors, t_res.get("ledger_digest_matches") is False, "tampered digest matches must be False")

        # 19. Artifact writing with registry and ledger
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--approval-ledger-index",
            "--approval-record-file", str(td_path / "record_a.json"),
            "--approval-record-file", str(td_path / "record_b.json")
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            require(errors, "artifact_write_summary" in art_res, "artifact_write_summary missing")
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v0-9-check-please-"), "run_id format mismatch")
            require(errors, Path(art_sum.get("artifact_dir", "")).exists(), "artifact dir missing")
            require(errors, art_sum.get("registry_updated") is True, "registry_updated must be True")
            
            fw = art_sum.get("files_written", [])
            expected = [
                "run_log.json", "command_brief.json", "work_orders.json", "selected_overlays.json",
                "evidence.json", "execution_plan.json", "adapter_result.json", "file_operation_plan.json",
                "execution_gate.json", "file_operation_result.json", "repo_patch_plan.json", "repo_patch_gate.json",
                "repo_patch_result.json", "changed_file_scope_proof.json", "execution_profile.json", "preflight_gate_record.json",
                "patch_approval_checklist.json", "execution_readiness_score.json", "dry_run_bundle.json", "dry_run_bundle_comparison.json",
                "approval_handoff_packet.json", "approval_review_ui_schema.json", "signed_approval_record.json", "approval_record_verification.json",
                "approval_record_audit_manifest.json", "approval_record_sources.json", "approval_ledger_bundle.json", "approval_ledger_index.json",
                "approval_ledger_verification.json", "approval_status_summary.json", "duplicate_approval_signals.json", "approval_ledger_lookup.json",
                "approval_record_comparison.json", "runtime_index_entry.json", "manifest.json", "full_result.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in artifact files_written")

            reg_dir = td_path / "registry"
            require(errors, (reg_dir / "run_registry.json").exists(), "run_registry.json missing")
            require(errors, (reg_dir / "runtime_index.json").exists(), "runtime_index.json missing")

            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v0_9_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "0.9.0", "man version mismatch")
                require(errors, man.get("baseline_preserved") is True, "man baseline_preserved True")
                require(errors, man.get("external_actions_taken") is False, "man external_actions_taken False")
                require(errors, man.get("live_worker_agents_activated") is False, "man live_worker_agents_activated False")
                require(errors, man.get("deterministic_demo_mode") is True, "man deterministic_demo_mode True")
                require(errors, man.get("approval_ledger_indexing") is True, "man approval_ledger_indexing True")
                require(errors, man.get("signed_approval_comparison") is True, "man signed_approval_comparison True")
                require(errors, man.get("approval_history_lookup") is True, "man approval_history_lookup True")
                require(errors, man.get("approval_duplicate_detection") is True, "man approval_duplicate_detection True")
                require(errors, man.get("approval_ledger_does_not_execute_patch") is True, "man approval_ledger_does_not_execute_patch True")

            rr = json.loads((reg_dir / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "0.9.0", "rr version mismatch")
            require(errors, len(rr.get("runs", [])) >= 1, "rr runs empty")
            require(errors, any(r.get("run_id") == run_id for r in rr.get("runs", [])), "rr run_id missing")

            ri = json.loads((reg_dir / "runtime_index.json").read_text())
            require(errors, ri.get("index_version") == "0.9.0", "ri version mismatch")
            require(errors, ri.get("run_count", 0) >= 1, "ri run_count < 1")
            require(errors, any(r.get("run_id") == run_id for r in ri.get("runs", [])), "ri run_id missing")

            code, out, err = run_command([
                "python3", "10_runtime/station_chief_runtime.py",
                "--resume-run-id", run_id,
                "--registry-dir", str(reg_dir)
            ])
            require(errors, code == 0, f"resume failed: {err}")
            res = parse_json_output(out, "resume", errors)
            if res:
                require(errors, res.get("resume_status") == "FOUND", "resume status != FOUND")
                require(errors, res.get("run_id") == run_id, "resume run_id mismatch")
                require(errors, res.get("run_entry", {}).get("run_id") == run_id, "resume entry run_id mismatch")


def main():
    print("Running validate_station_chief_runtime_v0_9.py...")
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
        
    print("PASS: Station Chief Runtime v0.9 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v0.9 runtime files.")

if __name__ == "__main__":
    main()

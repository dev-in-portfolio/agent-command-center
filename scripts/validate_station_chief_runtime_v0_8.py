#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TARGET_REL = "runtime_patch_preview/station_chief_patch_output.txt"


def run_command(args: list[str], cwd: Path = REPO_ROOT) -> tuple[int, str, str]:
    proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def parse_json_output(output: str, label: str, errors: list[str]):
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: invalid JSON output ({exc})")
        if output:
            errors.append(f"{label}: output was {output[:500]}")
        return None


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def check_contains(errors: list[str], path: Path, snippets: list[str], label: str) -> None:
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        require(errors, snippet in text, f"{label}: missing snippet {snippet!r}")


def check_not_contains(errors: list[str], path: Path, snippets: list[str], label: str) -> None:
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        require(errors, snippet not in text, f"{label}: forbidden snippet present {snippet!r}")


def validate_required_files(errors: list[str]) -> None:
    required_files = [
        "10_runtime/station_chief_runtime.py",
        "10_runtime/station_chief_demo_cases.json",
        "10_runtime/station_chief_runtime_readme.md",
        "10_runtime/station_chief_fixture_tests.py",
        "10_runtime/station_chief_adapters.py",
        "10_runtime/station_chief_execution_profiles.py",
        "10_runtime/station_chief_approval_handoff.py",
        "10_runtime/station_chief_approval_records.py",
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v0_8_report.md",
        "scripts/validate_station_chief_runtime_v0_8.py",
    ]
    for rel in required_files:
        require(errors, (REPO_ROOT / rel).exists(), f"Missing required file: {rel}")


def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    profiles_path = REPO_ROOT / "10_runtime/station_chief_execution_profiles.py"
    approval_path = REPO_ROOT / "10_runtime/station_chief_approval_handoff.py"
    records_path = REPO_ROOT / "10_runtime/station_chief_approval_records.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    skeleton_report_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    v08_report_path = REPO_ROOT / "09_exports/station_chief_runtime_v0_8_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "0.8.0"',
            "attach_signed_approval_record",
            "write_approval_record",
            "--approval-review-ui-schema",
            "--sign-approval-record",
            "--approval-reviewer",
            "--approval-decision",
            "--approval-note",
            "--approval-record-token",
            "--patch-preview-reviewed",
            "--changed-file-scope-reviewed",
            "--baseline-protection-reviewed",
            "--risk-summary-reviewed",
            "--write-approval-record",
            "--verify-approval-record",
            "approval_review_ui_schema",
            "signed_approval_record",
            "approval_record_verification",
            "approval_record_audit_manifest",
            "signed_approval_record_available",
            "signed_approval_record_does_not_execute_patch",
        ],
        "runtime.py",
    )
    check_not_contains(
        errors,
        runtime_path,
        [
            "requests",
            "urllib.request",
            "os.system",
            "pip install",
            "npm install",
            "live API",
            "API key",
            "import subprocess",
        ],
        "runtime.py",
    )

    check_contains(
        errors,
        records_path,
        [
            'APPROVAL_RECORD_MODULE_VERSION = "0.8.0"',
            "APPROVAL_RECORD_CONFIRMATION_TOKEN",
            "YES_I_APPROVE_APPROVAL_HANDOFF_RECORD",
            "APPROVAL_DECISIONS",
            "canonical_json",
            "sha256_digest",
            "create_approval_review_ui_schema",
            "validate_approval_inputs",
            "create_signed_approval_record",
            "verify_signed_approval_record",
            "create_approval_record_audit_manifest",
        ],
        "station_chief_approval_records.py",
    )
    check_not_contains(
        errors,
        records_path,
        [
            "requests",
            "urllib.request",
            "os.system",
            "pip install",
            "npm install",
            "live API",
            "API key",
            "import subprocess",
        ],
        "station_chief_approval_records.py",
    )

    check_contains(
        errors,
        adapter_path,
        [
            'ADAPTER_MODULE_VERSION = "0.8.0"',
            "supports_dry_run_bundle",
            "supports_approval_handoff",
            "supports_signed_approval_records",
        ],
        "station_chief_adapters.py",
    )
    check_not_contains(
        errors,
        adapter_path,
        [
            "requests",
            "urllib.request",
            "os.system",
            "pip install",
            "npm install",
            "live API",
            "API key",
            "import subprocess",
        ],
        "station_chief_adapters.py",
    )

    check_contains(
        errors,
        profiles_path,
        [
            'EXECUTION_PROFILE_MODULE_VERSION = "0.8.0"',
            "dry_run_bundle_version",
            "0.8.0",
            "EXECUTION_PROFILES",
            "audit_only",
            "dry_run_patch",
            "sandbox_write",
            "scoped_repo_patch",
            "list_execution_profiles",
            "select_execution_profile",
            "create_preflight_gate_record",
            "create_patch_approval_checklist",
            "create_execution_readiness_score",
            "create_dry_run_bundle",
        ],
        "station_chief_execution_profiles.py",
    )
    check_not_contains(
        errors,
        profiles_path,
        [
            "requests",
            "urllib.request",
            "os.system",
            "pip install",
            "npm install",
            "live API",
            "API key",
            "import subprocess",
        ],
        "station_chief_execution_profiles.py",
    )

    check_contains(
        errors,
        approval_path,
        [
            'APPROVAL_HANDOFF_MODULE_VERSION = "0.8.0"',
            "comparison_version",
            "risk_summary_version",
            "approval_summary_version",
            "recommendation_version",
            "approval_handoff_version",
            "safe_get",
            "extract_bundle_summary",
            "compare_text_blocks",
            "compare_dry_run_bundles",
            "create_risk_summary",
            "create_human_approval_summary",
            "create_next_action_recommendation",
            "create_approval_handoff_packet",
        ],
        "station_chief_approval_handoff.py",
    )
    check_not_contains(
        errors,
        approval_path,
        [
            "requests",
            "urllib.request",
            "os.system",
            "pip install",
            "npm install",
            "live API",
            "API key",
            "import subprocess",
        ],
        "station_chief_approval_handoff.py",
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v0.8.0.",
            "approval review UI schema",
            "deterministic signed approval records",
            "approval record verification",
            "approval audit manifests",
            "signed approval records that document human review without executing patches",
            "approval_review_ui_schema.json",
            "signed_approval_record.json",
            "approval_record_verification.json",
            "approval_record_audit_manifest.json",
            "approval_record_manifest.json",
            "YES_I_APPROVE_APPROVAL_HANDOFF_RECORD",
            "The Station Chief runtime keeps the full 175-family command civilization intact",
        ],
        "station_chief_runtime_readme.md",
    )
    check_not_contains(errors, readme_path, ["Explain that", "Include:", "List:", "Write:"], "station_chief_runtime_readme.md")

    check_contains(
        errors,
        skeleton_report_path,
        [
            "Station Chief Runtime upgraded to v0.8.0.",
            "approval handoff review UI schema",
            "deterministic signed approval records",
            "approval record verification",
            "approval audit manifests",
            "no live API calls",
            "no full workforce animation",
        ],
        "station_chief_runtime_skeleton_report.md",
    )
    check_not_contains(errors, skeleton_report_path, ["Explain that", "Include:", "List:", "Write:"], "station_chief_runtime_skeleton_report.md")

    check_contains(
        errors,
        v08_report_path,
        [
            "Station Chief Runtime v0.8.0 Report",
            "Station Chief Runtime upgraded to v0.8.0. Locked 175-family baseline preserved.",
            "approval handoff review UI schema",
            "deterministic signed approval records",
            "approval record verification",
            "approval decision artifacts",
            "approval audit manifest artifacts",
            "review-to-approval handoff validation",
            "signed approval records do not execute repo patches by themselves",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "Station Chief Runtime v0.8.0 keeps execution deterministic",
            "Next recommended build step",
        ],
        "station_chief_runtime_v0_8_report.md",
    )


def validate_demo_and_basic_runtime(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: rc={code}, stderr={err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "0.8.0", "--demo runtime version must be 0.8.0")
        require(errors, demo.get("command_type") == "verification", "--demo command_type must be verification")
        require(errors, demo.get("activation_tier", {}).get("name") == "Tier 4 — Audit / Archive", "--demo activation tier mismatch")
        rc = demo.get("run_capabilities", {})
        require(errors, rc.get("approval_review_ui_schema") is True, "--demo approval_review_ui_schema must be true")
        require(errors, rc.get("signed_approval_records") is True, "--demo signed_approval_records must be true")
        require(errors, rc.get("approval_record_verification") is True, "--demo approval_record_verification must be true")
        require(errors, rc.get("approval_audit_manifests") is True, "--demo approval_audit_manifests must be true")
        ev = demo.get("evidence", {})
        require(errors, ev.get("baseline_preserved") is True, "--demo evidence.baseline_preserved must be true")
        require(errors, ev.get("external_actions_taken") is False, "--demo evidence.external_actions_taken must be false")
        require(errors, ev.get("live_worker_agents_activated") is False, "--demo evidence.live_worker_agents_activated must be false")
        require(errors, ev.get("deterministic_demo_mode") is True, "--demo evidence.deterministic_demo_mode must be true")
        require(errors, ev.get("signed_approval_record_available") is True, "--demo evidence.signed_approval_record_available must be true")
        require(errors, ev.get("signed_approval_record_does_not_execute_patch") is True, "--demo evidence.signed_approval_record_does_not_execute_patch must be true")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: rc={code}, stderr={err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "--fixture-test status must be PASS")
        require(errors, fixture.get("runtime_version") == "0.8.0", "--fixture-test runtime_version must be 0.8.0")
        require(errors, fixture.get("case_count") == 5, "--fixture-test case_count must be 5")
        require(errors, fixture.get("failed") == 0, "--fixture-test failed must be 0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: rc={code}, stderr={err}")
    fixture_runner = parse_json_output(out, "fixture runner", errors)
    if fixture_runner:
        require(errors, fixture_runner.get("fixture_test_status") == "PASS", "fixture runner status must be PASS")
        require(errors, fixture_runner.get("runtime_version") == "0.8.0", "fixture runner runtime_version must be 0.8.0")
        require(errors, fixture_runner.get("case_count") == 5, "fixture runner case_count must be 5")
        require(errors, fixture_runner.get("failed") == 0, "fixture runner failed must be 0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--json"])
    require(errors, code == 0, f"--json command failed: rc={code}, stderr={err}")
    command_json = parse_json_output(out, "--json command", errors)
    if command_json:
        require(errors, command_json.get("station_chief_runtime_version") == "0.8.0", "--json runtime version must be 0.8.0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build Station Chief runtime skeleton", "--brief"])
    require(errors, code == 0, f"--brief command failed: rc={code}, stderr={err}")
    brief = parse_json_output(out, "--brief command", errors)
    if brief:
        require(errors, brief.get("command_type") == "build", "--brief command_type must be build")
        require(errors, brief.get("activation_tier", {}).get("name") == "Tier 3 — Active Operation", "--brief activation tier mismatch")
        require(errors, brief.get("deterministic_demo_mode") is True, "--brief deterministic_demo_mode must be true")
        require(errors, brief.get("baseline_protection") is True, "--brief baseline_protection must be true")
        require(errors, brief.get("external_actions_allowed") is False, "--brief external_actions_allowed must be false")
        require(errors, brief.get("workforce_animation_allowed") is False, "--brief workforce_animation_allowed must be false")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-overlays"])
    require(errors, code == 0, f"--list-overlays failed: rc={code}, stderr={err}")
    overlays = parse_json_output(out, "--list-overlays", errors)
    if overlays is not None:
        require(errors, isinstance(overlays, list), "--list-overlays output must be a list")
        require(errors, len(overlays) == 8, "--list-overlays must return exactly 8 overlays")
        for overlay in overlays:
            require(errors, overlay.get("exists") is True, f"overlay {overlay.get('id')} must exist")
            require(errors, overlay.get("preserves_locked_baseline") is True, f"overlay {overlay.get('id')} must preserve locked baseline")
            require(errors, "Devin O’Rourke" in overlay.get("ownership_project_owner", ""), f"overlay {overlay.get('id')} must credit Devin O’Rourke")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: rc={code}, stderr={err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "0.8.0", "--list-adapters adapter_module_version must be 0.8.0")
        supported = adapters.get("supported_adapters", {})
        require(errors, "noop" in supported, "--list-adapters must contain noop adapter")
        require(errors, "sandbox_file_write" in supported, "--list-adapters must contain sandbox_file_write adapter")
        require(errors, "scoped_repo_patch" in supported, "--list-adapters must contain scoped_repo_patch adapter")
        scoped = supported.get("scoped_repo_patch", {})
        require(errors, scoped.get("supports_dry_run_bundle") is True, "scoped_repo_patch.supports_dry_run_bundle must be true")
        require(errors, scoped.get("supports_approval_handoff") is True, "scoped_repo_patch.supports_approval_handoff must be true")
        require(errors, scoped.get("supports_signed_approval_records") is True, "scoped_repo_patch.supports_signed_approval_records must be true")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-execution-profiles"])
    require(errors, code == 0, f"--list-execution-profiles failed: rc={code}, stderr={err}")
    profiles = parse_json_output(out, "--list-execution-profiles", errors)
    if profiles:
        require(errors, profiles.get("execution_profile_module_version") == "0.8.0", "--list-execution-profiles version must be 0.8.0")
        profs = profiles.get("execution_profiles", {})
        require(errors, "audit_only" in profs, "execution profiles must contain audit_only")
        require(errors, "dry_run_patch" in profs, "execution profiles must contain dry_run_patch")
        require(errors, "sandbox_write" in profs, "execution profiles must contain sandbox_write")
        require(errors, "scoped_repo_patch" in profs, "execution profiles must contain scoped_repo_patch")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--approval-review-ui-schema"])
    require(errors, code == 0, f"--approval-review-ui-schema failed: rc={code}, stderr={err}")
    schema = parse_json_output(out, "--approval-review-ui-schema", errors)
    if schema:
        require(errors, schema.get("approval_review_ui_schema_version") == "0.8.0", "approval review schema version must be 0.8.0")
        field_ids = {field.get("field_id") for field in schema.get("fields", [])}
        for field_id in [
            "reviewer_name",
            "approval_decision",
            "approval_note",
            "confirmation_token",
            "patch_preview_reviewed",
            "changed_file_scope_reviewed",
            "baseline_protection_reviewed",
            "risk_summary_reviewed",
        ]:
            require(errors, field_id in field_ids, f"approval review schema must contain {field_id}")
        decisions = schema.get("approval_decisions", {})
        require(errors, all(key in decisions for key in ["approve", "reject", "needs_changes"]), "approval review schema decisions incomplete")
        require(errors, schema.get("baseline_preserved") is True, "approval review schema baseline_preserved must be true")
        require(errors, schema.get("external_actions_taken") is False, "approval review schema external_actions_taken must be false")
        require(errors, schema.get("live_worker_agents_activated") is False, "approval review schema live_worker_agents_activated must be false")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--simulate-adapter"])
    require(errors, code == 0, f"--simulate-adapter failed: rc={code}, stderr={err}")
    simulated = parse_json_output(out, "--simulate-adapter", errors)
    if simulated:
        require(errors, "execution_plan" in simulated, "--simulate-adapter must include execution_plan")
        require(errors, "adapter_result" in simulated, "--simulate-adapter must include adapter_result")
        adapter_result = simulated.get("adapter_result", {})
        require(errors, adapter_result.get("adapter_result_status") == "PASS", "--simulate-adapter adapter_result_status must be PASS")
        require(errors, adapter_result.get("live_execution_performed") is False, "--simulate-adapter live_execution_performed must be false")
        require(errors, adapter_result.get("external_actions_taken") is False, "--simulate-adapter external_actions_taken must be false")
        require(errors, adapter_result.get("worker_agents_activated") is False, "--simulate-adapter worker_agents_activated must be false")


def write_bundle_json(path: Path, bundle: dict) -> None:
    path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_approval_record_flow(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory() as patch_dir, tempfile.TemporaryDirectory() as compare_dir, tempfile.TemporaryDirectory() as approval_dir:
        patch_root = Path(patch_dir)
        compare_root = Path(compare_dir)
        approval_root = Path(approval_dir)
        target_file = patch_root / TARGET_REL
        before_bundle_path = compare_root / "before.json"
        after_bundle_path = compare_root / "after.json"

        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--approval-handoff"])
        require(errors, code == 0, f"approval handoff without repo patch failed: rc={code}, stderr={err}")
        approval_only = parse_json_output(out, "approval handoff without repo patch", errors)
        if approval_only:
            packet = approval_only.get("approval_handoff_packet")
            require(errors, "dry_run_bundle" in approval_only, "approval handoff must include dry_run_bundle")
            require(errors, packet is not None, "approval handoff must include approval_handoff_packet")
            require(errors, packet.get("approval_handoff_version") == "0.8.0", "approval handoff version must be 0.8.0")
            require(errors, packet.get("baseline_preserved") is True, "approval handoff packet baseline_preserved must be true")
            require(errors, packet.get("human_approval_summary", {}).get("approval_required") is False, "audit-only approval should not be required")
            require(errors, packet.get("next_action_recommendation", {}).get("recommended_next_action") == "Archive audit-only dry-run bundle.", "audit-only next action mismatch")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            TARGET_REL,
            "--sign-approval-record",
            "--approval-reviewer",
            "Devin O’Rourke",
            "--approval-decision",
            "approve",
            "--approval-record-token",
            "YES_I_APPROVE_APPROVAL_HANDOFF_RECORD",
            "--patch-preview-reviewed",
            "--changed-file-scope-reviewed",
            "--baseline-protection-reviewed",
            "--risk-summary-reviewed",
        ])
        require(errors, code == 0, f"approved signed approval record run failed: rc={code}, stderr={err}")
        approved = parse_json_output(out, "approved signed approval record run", errors)
        if approved:
            require(errors, approved.get("approval_handoff_packet") is not None, "approved flow must include approval_handoff_packet")
            require(errors, approved.get("approval_review_ui_schema") is not None, "approved flow must include approval_review_ui_schema")
            signed = approved.get("signed_approval_record")
            verification = approved.get("approval_record_verification")
            audit_manifest = approved.get("approval_record_audit_manifest")
            require(errors, signed is not None, "approved flow must include signed_approval_record")
            require(errors, verification is not None, "approved flow must include approval_record_verification")
            require(errors, audit_manifest is not None, "approved flow must include approval_record_audit_manifest")
            require(errors, signed.get("record_status") == "SIGNED", "approved record must be SIGNED")
            require(errors, signed.get("approval_decision") == "approve", "approved record decision must be approve")
            require(errors, signed.get("approval_signature"), "approved record must include approval_signature")
            require(errors, verification.get("verification_status") == "PASS", "approved record verification must PASS")
            require(errors, audit_manifest.get("execution_authorized") is False, "approval audit manifest must not authorize execution")
            require(errors, not target_file.exists(), "approved sign flow must not write patch file")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            TARGET_REL,
            "--sign-approval-record",
            "--approval-reviewer",
            "Devin O’Rourke",
            "--approval-decision",
            "approve",
            "--patch-preview-reviewed",
            "--changed-file-scope-reviewed",
            "--baseline-protection-reviewed",
            "--risk-summary-reviewed",
        ])
        require(errors, code == 0, f"blocked approval flow run failed: rc={code}, stderr={err}")
        blocked = parse_json_output(out, "blocked approval flow run", errors)
        if blocked:
            signed = blocked.get("signed_approval_record")
            verification = blocked.get("approval_record_verification")
            require(errors, signed is not None, "blocked flow must include signed_approval_record")
            require(errors, signed.get("record_status") == "BLOCKED", "missing-token approve must block record")
            require(errors, signed.get("input_validation", {}).get("input_validation_status") == "BLOCKED", "blocked record validation must be BLOCKED")
            require(errors, verification.get("verification_status") == "FAIL", "blocked record verification must FAIL")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            TARGET_REL,
            "--sign-approval-record",
            "--approval-reviewer",
            "Devin O’Rourke",
            "--approval-decision",
            "needs_changes",
            "--approval-note",
            "Revise before approval.",
        ])
        require(errors, code == 0, f"needs_changes flow failed: rc={code}, stderr={err}")
        needs_changes = parse_json_output(out, "needs_changes flow", errors)
        if needs_changes:
            signed = needs_changes.get("signed_approval_record")
            verification = needs_changes.get("approval_record_verification")
            require(errors, signed.get("record_status") == "SIGNED", "needs_changes record must be SIGNED")
            require(errors, signed.get("approval_decision") == "needs_changes", "needs_changes decision mismatch")
            require(errors, verification.get("verification_status") == "PASS", "needs_changes verification must PASS")
            require(errors, needs_changes.get("approval_record_audit_manifest", {}).get("execution_authorized") is False, "needs_changes audit manifest must not authorize execution")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--approval-handoff",
            "--sign-approval-record",
            "--approval-reviewer",
            "Devin O’Rourke",
            "--approval-decision",
            "reject",
            "--approval-note",
            "Rejected.",
        ])
        require(errors, code == 0, f"reject flow failed: rc={code}, stderr={err}")
        rejected = parse_json_output(out, "reject flow", errors)
        if rejected:
            signed = rejected.get("signed_approval_record")
            verification = rejected.get("approval_record_verification")
            require(errors, signed.get("record_status") == "SIGNED", "reject record must be SIGNED")
            require(errors, signed.get("approval_decision") == "reject", "reject decision mismatch")
            require(errors, verification.get("verification_status") == "PASS", "reject verification must PASS")
            require(errors, rejected.get("approval_record_audit_manifest", {}).get("execution_authorized") is False, "reject audit manifest must not authorize execution")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            TARGET_REL,
            "--write-approval-record",
            str(approval_root),
            "--approval-reviewer",
            "Devin O’Rourke",
            "--approval-decision",
            "approve",
            "--approval-record-token",
            "YES_I_APPROVE_APPROVAL_HANDOFF_RECORD",
            "--patch-preview-reviewed",
            "--changed-file-scope-reviewed",
            "--baseline-protection-reviewed",
            "--risk-summary-reviewed",
        ])
        require(errors, code == 0, f"write-approval-record failed: rc={code}, stderr={err}")
        written = parse_json_output(out, "write-approval-record", errors)
        if written:
            summary = written.get("approval_record_write_summary")
            require(errors, isinstance(summary, dict), "write-approval-record output must contain approval_record_write_summary")
            if isinstance(summary, dict):
                record_dir = Path(summary.get("approval_record_dir", ""))
                require(errors, record_dir.exists(), "approval record directory must exist")
                written_files = set(summary.get("files_written", []))
                required_files = {
                    "approval_review_ui_schema.json",
                    "approval_handoff_packet.json",
                    "signed_approval_record.json",
                    "approval_record_verification.json",
                    "approval_record_audit_manifest.json",
                    "approval_record_manifest.json",
                }
                require(errors, required_files.issubset(written_files), "approval record must include all required files")
                manifest = json.loads((record_dir / "approval_record_manifest.json").read_text(encoding="utf-8"))
                require(errors, manifest.get("approval_record_manifest_version") == "0.8.0", "approval_record_manifest version must be 0.8.0")
                require(errors, manifest.get("runtime_version") == "0.8.0", "approval_record_manifest runtime_version must be 0.8.0")
                require(errors, manifest.get("baseline_preserved") is True, "approval_record_manifest baseline_preserved must be true")
                require(errors, manifest.get("external_actions_taken") is False, "approval_record_manifest external_actions_taken must be false")
                require(errors, manifest.get("live_worker_agents_activated") is False, "approval_record_manifest live_worker_agents_activated must be false")
                require(errors, manifest.get("execution_authorized") is False, "approval_record_manifest execution_authorized must be false")

                handoff_path = record_dir / "approval_handoff_packet.json"
                record_path = record_dir / "signed_approval_record.json"
                code, out, err = run_command([
                    "python3",
                    "10_runtime/station_chief_runtime.py",
                    "--verify-approval-record",
                    str(handoff_path),
                    str(record_path),
                ])
                require(errors, code == 0, f"approval record verification CLI failed: rc={code}, stderr={err}")
                verification_cli = parse_json_output(out, "approval record verification CLI", errors)
                if verification_cli:
                    require(errors, verification_cli.get("verification_status") == "PASS", "verification CLI must PASS")
                    require(errors, verification_cli.get("approval_packet_digest_matches") is True, "approval packet digest must match")
                    require(errors, verification_cli.get("approval_signature_matches") is True, "approval signature must match")
                    require(errors, verification_cli.get("record_status") == "SIGNED", "verified record_status must be SIGNED")

                tampered_path = record_dir / "tampered_signed_approval_record.json"
                tampered_record = json.loads(record_path.read_text(encoding="utf-8"))
                tampered_record["approval_note"] = "tampered"
                tampered_path.write_text(json.dumps(tampered_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                code, out, err = run_command([
                    "python3",
                    "10_runtime/station_chief_runtime.py",
                    "--verify-approval-record",
                    str(handoff_path),
                    str(tampered_path),
                ])
                require(errors, code == 0, f"tampered approval record verification CLI failed: rc={code}, stderr={err}")
                tampered_verification = parse_json_output(out, "tampered approval record verification", errors)
                if tampered_verification:
                    require(errors, tampered_verification.get("verification_status") == "FAIL", "tampered verification must FAIL")
                    require(errors, tampered_verification.get("approval_signature_matches") is False, "tampered signature match must be false")

        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--dry-run-bundle"])
        require(errors, code == 0, f"before bundle generation failed: rc={code}, stderr={err}")
        before_payload = parse_json_output(out, "before bundle generation", errors)
        if before_payload and before_payload.get("dry_run_bundle") is not None:
            write_bundle_json(before_bundle_path, before_payload["dry_run_bundle"])

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            TARGET_REL,
            "--dry-run-bundle",
        ])
        require(errors, code == 0, f"after bundle generation failed: rc={code}, stderr={err}")
        after_payload = parse_json_output(out, "after bundle generation", errors)
        if after_payload and after_payload.get("dry_run_bundle") is not None:
            write_bundle_json(after_bundle_path, after_payload["dry_run_bundle"])

        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--compare-dry-run-bundles", str(before_bundle_path), str(after_bundle_path)])
        require(errors, code == 0, f"--compare-dry-run-bundles failed: rc={code}, stderr={err}")
        comparison = parse_json_output(out, "--compare-dry-run-bundles", errors)
        if comparison:
            require(errors, comparison.get("comparison_version") == "0.8.0", "comparison version must be 0.8.0")
            require(errors, comparison.get("comparison_status") == "CHANGED", "comparison status must be CHANGED")
            require(errors, comparison.get("before_summary") is not None, "comparison must include before_summary")
            require(errors, comparison.get("after_summary") is not None, "comparison must include after_summary")
            require(errors, comparison.get("patch_preview_comparison") is not None, "comparison must include patch_preview_comparison")
            require(errors, comparison.get("baseline_preserved") is True, "comparison baseline_preserved must be true")
            require(errors, comparison.get("external_actions_taken") is False, "comparison external_actions_taken must be false")
            require(errors, comparison.get("live_worker_agents_activated") is False, "comparison live_worker_agents_activated must be false")

        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--compare-against-dry-run-bundle", str(before_bundle_path), "--approval-handoff"])
        require(errors, code == 0, f"--compare-against-dry-run-bundle failed: rc={code}, stderr={err}")
        compare_against = parse_json_output(out, "--compare-against-dry-run-bundle", errors)
        if compare_against:
            require(errors, "dry_run_bundle_comparison" in compare_against, "compare-against output must include dry_run_bundle_comparison")
            require(errors, "approval_handoff_packet" in compare_against, "compare-against output must include approval_handoff_packet")
            require(errors, compare_against["approval_handoff_packet"].get("comparison") is not None, "approval handoff packet must include comparison")


def validate_artifacts_and_registry(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory() as run_dir, tempfile.TemporaryDirectory() as registry_dir, tempfile.TemporaryDirectory() as patch_dir:
        run_root = Path(run_dir)
        registry_root = Path(registry_dir)
        patch_root = Path(patch_dir)

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--write-artifacts",
            str(run_root),
            "--registry-dir",
            str(registry_root),
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            TARGET_REL,
            "--sign-approval-record",
            "--approval-reviewer",
            "Devin O’Rourke",
            "--approval-decision",
            "approve",
            "--approval-record-token",
            "YES_I_APPROVE_APPROVAL_HANDOFF_RECORD",
            "--patch-preview-reviewed",
            "--changed-file-scope-reviewed",
            "--baseline-protection-reviewed",
            "--risk-summary-reviewed",
        ])
        require(errors, code == 0, f"artifact write run failed: rc={code}, stderr={err}")
        payload = parse_json_output(out, "artifact write run", errors)
        if not payload:
            return

        summary = payload.get("artifact_write_summary")
        require(errors, isinstance(summary, dict), "artifact write output must contain artifact_write_summary")
        if not isinstance(summary, dict):
            return

        run_id = summary.get("run_id")
        require(errors, isinstance(run_id, str) and run_id.startswith("station-chief-v0-8-check-please-"), "artifact run_id must start with station-chief-v0-8-check-please-")
        artifact_dir = Path(summary.get("artifact_dir", ""))
        require(errors, artifact_dir.exists(), "artifact directory must exist")
        require(errors, summary.get("registry_updated") is True, "registry_updated must be true")
        files_written = set(summary.get("files_written", []))
        required_files = {
            "run_log.json",
            "command_brief.json",
            "work_orders.json",
            "selected_overlays.json",
            "evidence.json",
            "execution_plan.json",
            "adapter_result.json",
            "file_operation_plan.json",
            "execution_gate.json",
            "file_operation_result.json",
            "repo_patch_plan.json",
            "repo_patch_gate.json",
            "repo_patch_result.json",
            "changed_file_scope_proof.json",
            "execution_profile.json",
            "preflight_gate_record.json",
            "patch_approval_checklist.json",
            "execution_readiness_score.json",
            "dry_run_bundle.json",
            "dry_run_bundle_comparison.json",
            "approval_handoff_packet.json",
            "approval_review_ui_schema.json",
            "signed_approval_record.json",
            "approval_record_verification.json",
            "approval_record_audit_manifest.json",
            "runtime_index_entry.json",
            "manifest.json",
            "full_result.json",
        }
        require(errors, required_files.issubset(files_written), "artifact write must include all required files")

        manifest = json.loads((artifact_dir / "manifest.json").read_text(encoding="utf-8"))
        require(errors, manifest.get("artifact_type") == "station_chief_runtime_v0_8_artifacts", "manifest artifact_type must be station_chief_runtime_v0_8_artifacts")
        require(errors, manifest.get("runtime_version") == "0.8.0", "manifest runtime_version must be 0.8.0")
        require(errors, manifest.get("baseline_preserved") is True, "manifest baseline_preserved must be true")
        require(errors, manifest.get("external_actions_taken") is False, "manifest external_actions_taken must be false")
        require(errors, manifest.get("live_worker_agents_activated") is False, "manifest live_worker_agents_activated must be false")
        require(errors, manifest.get("deterministic_demo_mode") is True, "manifest deterministic_demo_mode must be true")
        require(errors, manifest.get("approval_review_ui_schema") is True, "manifest approval_review_ui_schema must be true")
        require(errors, manifest.get("signed_approval_records") is True, "manifest signed_approval_records must be true")
        require(errors, manifest.get("approval_record_verification") is True, "manifest approval_record_verification must be true")
        require(errors, manifest.get("approval_audit_manifests") is True, "manifest approval_audit_manifests must be true")
        require(errors, manifest.get("signed_approval_record_does_not_execute_patch") is True, "manifest signed_approval_record_does_not_execute_patch must be true")

        registry = json.loads((registry_root / "run_registry.json").read_text(encoding="utf-8"))
        require(errors, registry.get("registry_version") == "0.8.0", "registry_version must be 0.8.0")
        require(errors, len(registry.get("runs", [])) >= 1, "registry must contain runs")
        require(errors, any(run.get("run_id") == run_id for run in registry.get("runs", [])), "registry must contain the run_id")

        runtime_index = json.loads((registry_root / "runtime_index.json").read_text(encoding="utf-8"))
        require(errors, runtime_index.get("index_version") == "0.8.0", "runtime_index index_version must be 0.8.0")
        require(errors, runtime_index.get("run_count", 0) >= 1, "runtime_index must contain runs")
        require(errors, any(run.get("run_id") == run_id for run in runtime_index.get("runs", [])), "runtime_index must contain the run_id")

        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--resume-run-id", run_id, "--registry-dir", str(registry_root)])
        require(errors, code == 0, f"resume run failed: rc={code}, stderr={err}")
        resume = parse_json_output(out, "resume run", errors)
        if resume:
            require(errors, resume.get("resume_status") == "FOUND", "resume status must be FOUND")
            require(errors, resume.get("run_id") == run_id, "resume run_id must match")
            require(errors, resume.get("run_entry", {}).get("run_id") == run_id, "resume run_entry.run_id must match")


def validate_scope(errors: list[str]) -> None:
    for cache_dir in REPO_ROOT.rglob("__pycache__"):
        if cache_dir.is_dir():
            shutil.rmtree(cache_dir, ignore_errors=True)
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v0.8 runtime files.")
    status = run_command(["git", "status", "--short"])[1]
    diff_names = run_command(["git", "diff", "--name-only"])[1]
    allowed = {
        "10_runtime/station_chief_runtime.py",
        "10_runtime/station_chief_runtime_readme.md",
        "10_runtime/station_chief_adapters.py",
        "10_runtime/station_chief_execution_profiles.py",
        "10_runtime/station_chief_approval_handoff.py",
        "10_runtime/station_chief_approval_records.py",
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v0_8_report.md",
        "scripts/validate_station_chief_runtime_skeleton.py",
        "scripts/validate_station_chief_runtime_v0_2.py",
        "scripts/validate_station_chief_runtime_v0_3.py",
        "scripts/validate_station_chief_runtime_v0_4.py",
        "scripts/validate_station_chief_runtime_v0_5.py",
        "scripts/validate_station_chief_runtime_v0_6.py",
        "scripts/validate_station_chief_runtime_v0_7.py",
        "scripts/validate_station_chief_runtime_v0_8.py",
    }
    for line in (status.splitlines() + diff_names.splitlines()):
        if not line.strip():
            continue
        path = line.split()[-1]
        require(errors, path in allowed, f"Unexpected changed file: {path}")


def main() -> None:
    errors: list[str] = []
    validate_required_files(errors)
    validate_source_files(errors)
    validate_demo_and_basic_runtime(errors)
    validate_approval_record_flow(errors)
    validate_artifacts_and_registry(errors)
    validate_scope(errors)
    if errors:
        for error in errors:
            print(error)
        print("FAIL")
        raise SystemExit(1)
    print("PASS: Station Chief Runtime v0.8 valid.")


if __name__ == "__main__":
    main()

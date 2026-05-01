#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import shutil
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


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
    text = path.read_text()
    for snippet in snippets:
        require(errors, snippet in text, f"{label}: missing snippet {snippet!r}")


def check_not_contains(errors: list[str], path: Path, snippets: list[str], label: str) -> None:
    text = path.read_text()
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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v0_7_report.md",
        "scripts/validate_station_chief_runtime_v0_7.py",
    ]
    for rel in required_files:
        require(errors, (REPO_ROOT / rel).exists(), f"Missing required file: {rel}")


def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    profiles_path = REPO_ROOT / "10_runtime/station_chief_execution_profiles.py"
    approval_path = REPO_ROOT / "10_runtime/station_chief_approval_handoff.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    skeleton_report_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    v07_report_path = REPO_ROOT / "09_exports/station_chief_runtime_v0_7_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "0.7.0"',
            "attach_approval_handoff",
            "write_approval_handoff",
            "--compare-dry-run-bundles",
            "--approval-handoff",
            "--compare-against-dry-run-bundle",
            "--write-approval-handoff",
            "dry_run_bundle_comparison",
            "approval_handoff_packet",
            "approval_ux_handoff",
            "risk_summary_artifacts",
            "next_action_recommendations",
            "approval_handoff_available",
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
        adapter_path,
        [
            'ADAPTER_MODULE_VERSION = "0.7.0"',
            "supports_dry_run_bundle",
            "supports_approval_handoff",
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
            'EXECUTION_PROFILE_MODULE_VERSION = "0.7.0"',
            "dry_run_bundle_version",
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
            'APPROVAL_HANDOFF_MODULE_VERSION = "0.7.0"',
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
            "Station Chief Runtime upgraded to v0.7.0.",
            "dry-run bundle comparison",
            "approval UX handoff packets",
            "human approval summaries",
            "risk summary artifacts",
            "next-action recommendations",
            "approval_handoff_packet.json",
            "human_approval_summary.json",
            "risk_summary.json",
            "next_action_recommendation.json",
            "approval_handoff_manifest.json",
            "The Station Chief runtime keeps the full 175-family command civilization intact",
        ],
        "station_chief_runtime_readme.md",
    )
    check_not_contains(errors, readme_path, ["Explain that", "Include:", "List:", "Write:"], "station_chief_runtime_readme.md")

    check_contains(
        errors,
        skeleton_report_path,
        [
            "Station Chief Runtime upgraded to v0.7.0.",
            "dry-run bundle comparison",
            "approval UX handoff packets",
            "human approval summaries",
            "risk summary artifacts",
            "next-action recommendations",
            "no live API calls",
            "no full workforce animation",
        ],
        "station_chief_runtime_skeleton_report.md",
    )
    check_not_contains(errors, skeleton_report_path, ["Explain that", "Include:", "List:", "Write:"], "station_chief_runtime_skeleton_report.md")

    check_contains(
        errors,
        v07_report_path,
        [
            "Station Chief Runtime v0.7.0 Report",
            "Station Chief Runtime upgraded to v0.7.0. Locked 175-family baseline preserved.",
            "dry-run bundle comparison",
            "approval UX handoff packets",
            "before/after review packets",
            "human approval checklist summaries",
            "diff comparison artifacts",
            "risk summaries",
            "next-action recommendations",
            "approval_handoff_manifest.json",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "Station Chief Runtime v0.7.0 keeps execution deterministic",
            "Next recommended build step",
        ],
        "station_chief_runtime_v0_7_report.md",
    )


def validate_demo_and_basic_runtime(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: rc={code}, stderr={err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "0.7.0", "--demo runtime version must be 0.7.0")
        require(errors, demo.get("command_type") == "verification", "--demo command_type must be verification")
        require(errors, demo.get("activation_tier", {}).get("name") == "Tier 4 — Audit / Archive", "--demo activation tier mismatch")
        rc = demo.get("run_capabilities", {})
        require(errors, rc.get("dry_run_bundle_comparison") is True, "--demo dry_run_bundle_comparison must be true")
        require(errors, rc.get("approval_ux_handoff") is True, "--demo approval_ux_handoff must be true")
        require(errors, rc.get("risk_summary_artifacts") is True, "--demo risk_summary_artifacts must be true")
        require(errors, rc.get("next_action_recommendations") is True, "--demo next_action_recommendations must be true")
        ev = demo.get("evidence", {})
        require(errors, ev.get("baseline_preserved") is True, "--demo evidence.baseline_preserved must be true")
        require(errors, ev.get("external_actions_taken") is False, "--demo evidence.external_actions_taken must be false")
        require(errors, ev.get("live_worker_agents_activated") is False, "--demo evidence.live_worker_agents_activated must be false")
        require(errors, ev.get("deterministic_demo_mode") is True, "--demo evidence.deterministic_demo_mode must be true")
        require(errors, ev.get("approval_handoff_available") is True, "--demo evidence.approval_handoff_available must be true")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: rc={code}, stderr={err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "--fixture-test status must be PASS")
        require(errors, fixture.get("runtime_version") == "0.7.0", "--fixture-test runtime_version must be 0.7.0")
        require(errors, fixture.get("case_count") == 5, "--fixture-test case_count must be 5")
        require(errors, fixture.get("failed") == 0, "--fixture-test failed must be 0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: rc={code}, stderr={err}")
    fixture_runner = parse_json_output(out, "fixture runner", errors)
    if fixture_runner:
        require(errors, fixture_runner.get("fixture_test_status") == "PASS", "fixture runner status must be PASS")
        require(errors, fixture_runner.get("runtime_version") == "0.7.0", "fixture runner runtime_version must be 0.7.0")
        require(errors, fixture_runner.get("case_count") == 5, "fixture runner case_count must be 5")
        require(errors, fixture_runner.get("failed") == 0, "fixture runner failed must be 0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--json"])
    require(errors, code == 0, f"--json command failed: rc={code}, stderr={err}")
    command_json = parse_json_output(out, "--json command", errors)
    if command_json:
        require(errors, command_json.get("station_chief_runtime_version") == "0.7.0", "--json runtime version must be 0.7.0")

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
        require(errors, adapters.get("adapter_module_version") == "0.7.0", "--list-adapters adapter_module_version must be 0.7.0")
        supported = adapters.get("supported_adapters", {})
        require(errors, "noop" in supported, "--list-adapters must contain noop adapter")
        require(errors, "sandbox_file_write" in supported, "--list-adapters must contain sandbox_file_write adapter")
        require(errors, "scoped_repo_patch" in supported, "--list-adapters must contain scoped_repo_patch adapter")
        scoped = supported.get("scoped_repo_patch", {})
        require(errors, scoped.get("supports_dry_run_bundle") is True, "scoped_repo_patch.supports_dry_run_bundle must be true")
        require(errors, scoped.get("supports_approval_handoff") is True, "scoped_repo_patch.supports_approval_handoff must be true")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-execution-profiles"])
    require(errors, code == 0, f"--list-execution-profiles failed: rc={code}, stderr={err}")
    profiles = parse_json_output(out, "--list-execution-profiles", errors)
    if profiles:
        require(errors, profiles.get("execution_profile_module_version") == "0.7.0", "--list-execution-profiles version must be 0.7.0")
        profs = profiles.get("execution_profiles", {})
        require(errors, "audit_only" in profs, "execution profiles must contain audit_only")
        require(errors, "dry_run_patch" in profs, "execution profiles must contain dry_run_patch")
        require(errors, "sandbox_write" in profs, "execution profiles must contain sandbox_write")
        require(errors, "scoped_repo_patch" in profs, "execution profiles must contain scoped_repo_patch")
        require(errors, profs.get("audit_only", {}).get("allows_repo_patch") is False, "audit_only.allows_repo_patch must be false")
        require(errors, profs.get("dry_run_patch", {}).get("allows_repo_patch") is False, "dry_run_patch.allows_repo_patch must be false")
        require(errors, profs.get("sandbox_write", {}).get("allows_sandbox_write") is True, "sandbox_write.allows_sandbox_write must be true")
        require(errors, profs.get("scoped_repo_patch", {}).get("allows_repo_patch") is True, "scoped_repo_patch.allows_repo_patch must be true")
        require(errors, profs.get("scoped_repo_patch", {}).get("requires_confirmation") is True, "scoped_repo_patch.requires_confirmation must be true")

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


def validate_dry_run_bundle_flow(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory() as patch_dir, tempfile.TemporaryDirectory() as compare_dir:
        patch_root = Path(patch_dir)
        compare_root = Path(compare_dir)
        target_rel = "runtime_patch_preview/station_chief_patch_output.txt"
        target_file = patch_root / target_rel

        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--dry-run-bundle"])
        require(errors, code == 0, f"dry-run bundle without repo patch failed: rc={code}, stderr={err}")
        dry_only = parse_json_output(out, "dry-run bundle without repo patch", errors)
        if dry_only:
            require(errors, "execution_profile" in dry_only, "dry-run bundle must include execution_profile")
            require(errors, "preflight_gate_record" in dry_only, "dry-run bundle must include preflight_gate_record")
            require(errors, "patch_approval_checklist" in dry_only, "dry-run bundle must include patch_approval_checklist")
            require(errors, "execution_readiness_score" in dry_only, "dry-run bundle must include execution_readiness_score")
            require(errors, "dry_run_bundle" in dry_only, "dry-run bundle must include dry_run_bundle")
            require(errors, dry_only["execution_profile"].get("selected_profile_id") == "audit_only", "default profile should be audit_only")
            require(errors, dry_only["preflight_gate_record"].get("preflight_status") == "PASS", "preflight status must PASS")
            require(errors, dry_only["patch_approval_checklist"].get("checklist_status") == "NOT_APPLICABLE", "checklist must be NOT_APPLICABLE")
            require(errors, dry_only["execution_readiness_score"].get("readiness_status") == "READY_AUDIT_ONLY", "readiness must be READY_AUDIT_ONLY")
            require(errors, dry_only["dry_run_bundle"].get("dry_run_bundle_version") == "0.7.0", "dry_run_bundle_version must be 0.7.0")
            require(errors, dry_only["dry_run_bundle"].get("baseline_preserved") is True, "dry_run_bundle baseline_preserved must be true")
            require(errors, dry_only["dry_run_bundle"].get("repo_patch_preview") is None, "audit-only bundle should not include repo patch preview")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            target_rel,
            "--dry-run-bundle",
        ])
        require(errors, code == 0, f"dry-run bundle with repo patch plan failed: rc={code}, stderr={err}")
        dry_patch = parse_json_output(out, "dry-run bundle with repo patch plan", errors)
        if dry_patch:
            require(errors, "repo_patch_plan" in dry_patch, "dry-run bundle with repo patch must include repo_patch_plan")
            require(errors, "dry_run_bundle" in dry_patch, "dry-run bundle with repo patch must include dry_run_bundle")
            require(errors, "execution_profile" in dry_patch, "dry-run bundle with repo patch must include execution_profile")
            require(errors, dry_patch["preflight_gate_record"].get("preflight_status") == "PASS", "repo patch dry-run preflight must PASS")
            require(errors, dry_patch["patch_approval_checklist"].get("checklist_status") == "READY", "repo patch dry-run checklist must be READY")
            require(errors, dry_patch["execution_readiness_score"].get("readiness_status") == "READY_FOR_APPROVAL", "repo patch dry-run readiness must be READY_FOR_APPROVAL")
            require(errors, dry_patch["dry_run_bundle"].get("repo_patch_plan") is not None, "dry_run_bundle must include repo_patch_plan")
            preview = dry_patch["dry_run_bundle"].get("repo_patch_preview") or ""
            require(errors, "Station Chief Runtime" in preview, "dry_run_bundle preview must mention Station Chief Runtime")
            require(errors, not target_file.exists(), "dry-run bundle plan must not write patch file")

        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--execution-profile", "dry_run_patch", "--dry-run-bundle"])
        require(errors, code == 0, f"requested execution profile failed: rc={code}, stderr={err}")
        requested = parse_json_output(out, "requested execution profile", errors)
        if requested:
            require(errors, requested["execution_profile"].get("selected_profile_id") == "dry_run_patch", "requested execution profile must be dry_run_patch")
            require(errors, requested["execution_profile"].get("selection_reason") == "Requested profile accepted.", "requested profile reason mismatch")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--execution-profile",
            "does_not_exist",
            "--dry-run-bundle",
        ])
        require(errors, code == 0, f"invalid requested execution profile failed: rc={code}, stderr={err}")
        invalid_profile = parse_json_output(out, "invalid requested execution profile", errors)
        if invalid_profile:
            require(errors, invalid_profile["execution_profile"].get("selected_profile_id") == "audit_only", "invalid profile should default to audit_only")
            require(errors, "defaulted to audit_only" in invalid_profile["execution_profile"].get("selection_reason", ""), "invalid profile reason should mention defaulted to audit_only")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            target_rel,
            "--write-dry-run-bundle",
            str(patch_root / "dry_run_output"),
        ])
        require(errors, code == 0, f"write-dry-run-bundle failed: rc={code}, stderr={err}")
        written = parse_json_output(out, "write-dry-run-bundle", errors)
        if written:
            summary = written.get("dry_run_bundle_write_summary")
            require(errors, isinstance(summary, dict), "write-dry-run-bundle output must contain dry_run_bundle_write_summary")
            if isinstance(summary, dict):
                bundle_dir = Path(summary.get("dry_run_bundle_dir", ""))
                require(errors, bundle_dir.exists(), "dry-run bundle directory must exist")
                written_files = set(summary.get("files_written", []))
                required_files = {
                    "dry_run_bundle.json",
                    "execution_profile.json",
                    "preflight_gate_record.json",
                    "patch_approval_checklist.json",
                    "execution_readiness_score.json",
                    "repo_patch_preview.diff",
                    "dry_run_manifest.json",
                }
                require(errors, required_files.issubset(written_files), "dry-run bundle must include all required files")
                manifest = json.loads((bundle_dir / "dry_run_manifest.json").read_text())
                require(errors, manifest.get("runtime_version") == "0.7.0", "dry_run_manifest runtime_version must be 0.7.0")
                require(errors, manifest.get("baseline_preserved") is True, "dry_run_manifest baseline_preserved must be true")
                require(errors, manifest.get("external_actions_taken") is False, "dry_run_manifest external_actions_taken must be false")
                require(errors, manifest.get("live_worker_agents_activated") is False, "dry_run_manifest live_worker_agents_activated must be false")
                preview_text = (bundle_dir / "repo_patch_preview.diff").read_text()
                require(errors, "Station Chief Runtime" in preview_text, "repo_patch_preview.diff must contain Station Chief Runtime")

        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--approval-handoff"])
        require(errors, code == 0, f"approval handoff without repo patch failed: rc={code}, stderr={err}")
        approval_only = parse_json_output(out, "approval handoff without repo patch", errors)
        if approval_only:
            require(errors, "dry_run_bundle" in approval_only, "approval handoff must include dry_run_bundle")
            require(errors, "approval_handoff_packet" in approval_only, "approval handoff must include approval_handoff_packet")
            packet = approval_only["approval_handoff_packet"]
            require(errors, packet.get("approval_handoff_version") == "0.7.0", "approval handoff version must be 0.7.0")
            require(errors, packet.get("risk_summary") is not None, "approval handoff packet must include risk_summary")
            require(errors, packet.get("human_approval_summary") is not None, "approval handoff packet must include human_approval_summary")
            require(errors, packet.get("next_action_recommendation") is not None, "approval handoff packet must include next_action_recommendation")
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
            target_rel,
            "--approval-handoff",
        ])
        require(errors, code == 0, f"approval handoff with repo patch plan failed: rc={code}, stderr={err}")
        approval_patch = parse_json_output(out, "approval handoff with repo patch plan", errors)
        if approval_patch:
            require(errors, "dry_run_bundle" in approval_patch, "approval handoff with repo patch must include dry_run_bundle")
            require(errors, "repo_patch_plan" in approval_patch, "approval handoff with repo patch must include repo_patch_plan")
            require(errors, "approval_handoff_packet" in approval_patch, "approval handoff with repo patch must include approval_handoff_packet")
            packet = approval_patch["approval_handoff_packet"]
            require(errors, packet.get("risk_summary", {}).get("risk_level") in {"low", "medium", "high", "blocked"}, "approval risk level should be present")
            require(errors, packet.get("human_approval_summary", {}).get("approval_required") is True, "repo patch approval should be required")
            require(errors, packet.get("human_approval_summary", {}).get("approval_token") == "YES_I_APPROVE_SCOPED_REPO_PATCH", "repo patch approval token mismatch")
            allowed_actions = packet.get("next_action_recommendation", {}).get("allowed_next_actions", [])
            require(errors, "review patch preview" in allowed_actions, "approval recommendation should allow patch preview review")
            require(errors, not target_file.exists(), "approval handoff plan must not write patch file")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            target_rel,
            "--write-approval-handoff",
            str(patch_root / "handoffs"),
        ])
        require(errors, code == 0, f"write-approval-handoff failed: rc={code}, stderr={err}")
        handoff_written = parse_json_output(out, "write-approval-handoff", errors)
        if handoff_written:
            summary = handoff_written.get("approval_handoff_write_summary")
            require(errors, isinstance(summary, dict), "write-approval-handoff output must contain approval_handoff_write_summary")
            if isinstance(summary, dict):
                handoff_dir = Path(summary.get("approval_handoff_dir", ""))
                require(errors, handoff_dir.exists(), "approval handoff directory must exist")
                written_files = set(summary.get("files_written", []))
                required_files = {
                    "approval_handoff_packet.json",
                    "human_approval_summary.json",
                    "risk_summary.json",
                    "next_action_recommendation.json",
                    "dry_run_bundle_comparison.json",
                    "patch_preview.diff",
                    "approval_handoff_manifest.json",
                }
                require(errors, required_files.issubset(written_files), "approval handoff must include all required files")
                manifest = json.loads((handoff_dir / "approval_handoff_manifest.json").read_text())
                require(errors, manifest.get("runtime_version") == "0.7.0", "approval_handoff_manifest runtime_version must be 0.7.0")
                require(errors, manifest.get("baseline_preserved") is True, "approval_handoff_manifest baseline_preserved must be true")
                require(errors, manifest.get("external_actions_taken") is False, "approval_handoff_manifest external_actions_taken must be false")
                require(errors, manifest.get("live_worker_agents_activated") is False, "approval_handoff_manifest live_worker_agents_activated must be false")
                patch_preview_text = (handoff_dir / "patch_preview.diff").read_text()
                require(errors, "Station Chief Runtime" in patch_preview_text, "patch_preview.diff must contain Station Chief Runtime")

        audit_bundle_path = compare_root / "before.json"
        patch_bundle_path = compare_root / "after.json"
        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--dry-run-bundle"])
        require(errors, code == 0, f"comparison audit bundle generation failed: rc={code}, stderr={err}")
        audit_payload = parse_json_output(out, "comparison audit bundle generation", errors)
        if audit_payload:
            audit_bundle = audit_payload.get("dry_run_bundle")
            if audit_bundle is not None:
                audit_bundle_path.write_text(json.dumps(audit_bundle, indent=2, ensure_ascii=False) + "\n")
        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            target_rel,
            "--dry-run-bundle",
        ])
        require(errors, code == 0, f"comparison patch bundle generation failed: rc={code}, stderr={err}")
        patch_payload = parse_json_output(out, "comparison patch bundle generation", errors)
        if patch_payload:
            patch_bundle = patch_payload.get("dry_run_bundle")
            if patch_bundle is not None:
                patch_bundle_path.write_text(json.dumps(patch_bundle, indent=2, ensure_ascii=False) + "\n")

        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--compare-dry-run-bundles", str(audit_bundle_path), str(patch_bundle_path)])
        require(errors, code == 0, f"--compare-dry-run-bundles failed: rc={code}, stderr={err}")
        comparison = parse_json_output(out, "--compare-dry-run-bundles", errors)
        if comparison:
            require(errors, comparison.get("comparison_version") == "0.7.0", "comparison version must be 0.7.0")
            require(errors, comparison.get("comparison_status") == "CHANGED", "comparison status must be CHANGED")
            require(errors, comparison.get("before_summary") is not None, "comparison must include before_summary")
            require(errors, comparison.get("after_summary") is not None, "comparison must include after_summary")
            require(errors, comparison.get("patch_preview_comparison") is not None, "comparison must include patch_preview_comparison")
            require(errors, comparison.get("baseline_preserved") is True, "comparison baseline_preserved must be true")
            require(errors, comparison.get("external_actions_taken") is False, "comparison external_actions_taken must be false")
            require(errors, comparison.get("live_worker_agents_activated") is False, "comparison live_worker_agents_activated must be false")

        code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--compare-against-dry-run-bundle", str(audit_bundle_path), "--approval-handoff"])
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
        target_rel = "runtime_patch_preview/station_chief_patch_output.txt"

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
            target_rel,
            "--approval-handoff",
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
        require(errors, isinstance(run_id, str) and run_id.startswith("station-chief-v0-7-check-please-"), "artifact run_id must start with station-chief-v0-7-check-please-")
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
            "runtime_index_entry.json",
            "manifest.json",
            "full_result.json",
        }
        require(errors, required_files.issubset(files_written), "artifact write must include all required files")

        manifest = json.loads((artifact_dir / "manifest.json").read_text())
        require(errors, manifest.get("artifact_type") == "station_chief_runtime_v0_7_artifacts", "manifest artifact_type must be station_chief_runtime_v0_7_artifacts")
        require(errors, manifest.get("runtime_version") == "0.7.0", "manifest runtime_version must be 0.7.0")
        require(errors, manifest.get("baseline_preserved") is True, "manifest baseline_preserved must be true")
        require(errors, manifest.get("external_actions_taken") is False, "manifest external_actions_taken must be false")
        require(errors, manifest.get("live_worker_agents_activated") is False, "manifest live_worker_agents_activated must be false")
        require(errors, manifest.get("deterministic_demo_mode") is True, "manifest deterministic_demo_mode must be true")
        require(errors, manifest.get("dry_run_bundle_comparison") is True, "manifest dry_run_bundle_comparison must be true")
        require(errors, manifest.get("approval_ux_handoff") is True, "manifest approval_ux_handoff must be true")
        require(errors, manifest.get("risk_summary_artifacts") is True, "manifest risk_summary_artifacts must be true")
        require(errors, manifest.get("next_action_recommendations") is True, "manifest next_action_recommendations must be true")

        registry = json.loads((registry_root / "run_registry.json").read_text())
        require(errors, registry.get("registry_version") == "0.7.0", "registry_version must be 0.7.0")
        require(errors, len(registry.get("runs", [])) >= 1, "registry must contain runs")
        require(errors, any(run.get("run_id") == run_id for run in registry.get("runs", [])), "registry must contain the run_id")

        runtime_index = json.loads((registry_root / "runtime_index.json").read_text())
        require(errors, runtime_index.get("index_version") == "0.7.0", "runtime_index index_version must be 0.7.0")
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
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v0.7 runtime files.")
    status = run_command(["git", "status", "--short"])[1]
    diff_names = run_command(["git", "diff", "--name-only"])[1]
    allowed = {
        "10_runtime/station_chief_runtime.py",
        "10_runtime/station_chief_runtime_readme.md",
        "10_runtime/station_chief_adapters.py",
        "10_runtime/station_chief_execution_profiles.py",
        "10_runtime/station_chief_approval_handoff.py",
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v0_7_report.md",
        "scripts/validate_station_chief_runtime_skeleton.py",
        "scripts/validate_station_chief_runtime_v0_2.py",
        "scripts/validate_station_chief_runtime_v0_3.py",
        "scripts/validate_station_chief_runtime_v0_4.py",
        "scripts/validate_station_chief_runtime_v0_5.py",
        "scripts/validate_station_chief_runtime_v0_6.py",
        "scripts/validate_station_chief_runtime_v0_7.py",
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
    validate_dry_run_bundle_flow(errors)
    validate_artifacts_and_registry(errors)
    validate_scope(errors)
    if errors:
        for error in errors:
            print(error)
        print("FAIL")
        raise SystemExit(1)
    print("PASS: Station Chief Runtime v0.7 valid.")


if __name__ == "__main__":
    main()

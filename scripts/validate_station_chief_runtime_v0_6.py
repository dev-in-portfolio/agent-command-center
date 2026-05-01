#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v0_6_report.md",
        "scripts/validate_station_chief_runtime_v0_6.py",
    ]
    for rel in required_files:
        require(errors, (REPO_ROOT / rel).exists(), f"Missing required file: {rel}")


def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    profiles_path = REPO_ROOT / "10_runtime/station_chief_execution_profiles.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    skeleton_report_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    v06_report_path = REPO_ROOT / "09_exports/station_chief_runtime_v0_6_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "0.6.0"',
            "attach_execution_profile_and_dry_run",
            "write_dry_run_bundle",
            "--list-execution-profiles",
            "--execution-profile",
            "--dry-run-bundle",
            "--write-dry-run-bundle",
            "validator_selected_execution_profiles",
            "repo_patch_dry_run_bundles",
            "preflight_gate_records",
            "execution_readiness_scoring",
            "execution_profile",
            "preflight_gate_record",
            "patch_approval_checklist",
            "execution_readiness_score",
            "dry_run_bundle",
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
            'ADAPTER_MODULE_VERSION = "0.6.0"',
            "supports_dry_run_bundle",
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
            'EXECUTION_PROFILE_MODULE_VERSION = "0.6.0"',
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
        readme_path,
        [
            "Station Chief Runtime upgraded to v0.6.0.",
            "validator-selected execution profiles",
            "repo patch dry-run bundles",
            "preflight gate records",
            "execution readiness scoring",
            "dry_run_bundle.json",
            "dry_run_manifest.json",
            "repo_patch_preview.diff",
            "audit_only",
            "dry_run_patch",
            "sandbox_write",
            "scoped_repo_patch",
            "The Station Chief runtime keeps the full 175-family command civilization intact",
        ],
        "station_chief_runtime_readme.md",
    )
    check_not_contains(
        errors,
        readme_path,
        ["Explain that", "Include:", "List:", "Write:"],
        "station_chief_runtime_readme.md",
    )

    check_contains(
        errors,
        skeleton_report_path,
        [
            "Station Chief Runtime upgraded to v0.6.0.",
            "validator-selected execution profiles",
            "repo patch dry-run bundles",
            "preflight gate records",
            "execution readiness scoring",
            "no live API calls",
            "no full workforce animation",
        ],
        "station_chief_runtime_skeleton_report.md",
    )
    check_not_contains(
        errors,
        skeleton_report_path,
        ["Explain that", "Include:", "List:", "Write:"],
        "station_chief_runtime_skeleton_report.md",
    )

    check_contains(
        errors,
        v06_report_path,
        [
            "Station Chief Runtime v0.6.0 Report",
            "Station Chief Runtime upgraded to v0.6.0. Locked 175-family baseline preserved.",
            "validator-selected execution profiles",
            "repo patch dry-run bundles",
            "patch approval checklist artifacts",
            "preflight gate records",
            "execution readiness scoring",
            "dry-run bundle validation",
            "repo_patch_preview.diff",
            "dry_run_manifest.json",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "Station Chief Runtime v0.6.0 keeps execution deterministic",
            "Next recommended build step",
        ],
        "station_chief_runtime_v0_6_report.md",
    )


def validate_demo_and_basic_runtime(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: rc={code}, stderr={err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "0.6.0", "--demo runtime version must be 0.6.0")
        require(errors, demo.get("command_type") == "verification", "--demo command_type must be verification")
        require(errors, demo.get("activation_tier", {}).get("name") == "Tier 4 — Audit / Archive", "--demo activation tier mismatch")
        rc = demo.get("run_capabilities", {})
        require(errors, rc.get("validator_selected_execution_profiles") is True, "--demo validator_selected_execution_profiles must be true")
        require(errors, rc.get("repo_patch_dry_run_bundles") is True, "--demo repo_patch_dry_run_bundles must be true")
        require(errors, rc.get("preflight_gate_records") is True, "--demo preflight_gate_records must be true")
        require(errors, rc.get("execution_readiness_scoring") is True, "--demo execution_readiness_scoring must be true")
        ev = demo.get("evidence", {})
        require(errors, ev.get("baseline_preserved") is True, "--demo evidence.baseline_preserved must be true")
        require(errors, ev.get("external_actions_taken") is False, "--demo evidence.external_actions_taken must be false")
        require(errors, ev.get("live_worker_agents_activated") is False, "--demo evidence.live_worker_agents_activated must be false")
        require(errors, ev.get("deterministic_demo_mode") is True, "--demo evidence.deterministic_demo_mode must be true")
        require(errors, ev.get("dry_run_bundle_available") is True, "--demo evidence.dry_run_bundle_available must be true")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: rc={code}, stderr={err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "--fixture-test status must be PASS")
        require(errors, fixture.get("runtime_version") == "0.6.0", "--fixture-test runtime_version must be 0.6.0")
        require(errors, fixture.get("case_count") == 5, "--fixture-test case_count must be 5")
        require(errors, fixture.get("failed") == 0, "--fixture-test failed must be 0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: rc={code}, stderr={err}")
    fixture_runner = parse_json_output(out, "fixture runner", errors)
    if fixture_runner:
        require(errors, fixture_runner.get("fixture_test_status") == "PASS", "fixture runner status must be PASS")
        require(errors, fixture_runner.get("runtime_version") == "0.6.0", "fixture runner runtime_version must be 0.6.0")
        require(errors, fixture_runner.get("case_count") == 5, "fixture runner case_count must be 5")
        require(errors, fixture_runner.get("failed") == 0, "fixture runner failed must be 0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--json"])
    require(errors, code == 0, f"--json command failed: rc={code}, stderr={err}")
    command_json = parse_json_output(out, "--json command", errors)
    if command_json:
        require(errors, command_json.get("station_chief_runtime_version") == "0.6.0", "--json runtime version must be 0.6.0")

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
            require(
                errors,
                "Devin O’Rourke" in overlay.get("ownership_project_owner", ""),
                f"overlay {overlay.get('id')} must credit Devin O’Rourke",
            )

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: rc={code}, stderr={err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "0.6.0", "--list-adapters adapter_module_version must be 0.6.0")
        supported = adapters.get("supported_adapters", {})
        require(errors, "noop" in supported, "--list-adapters must contain noop adapter")
        require(errors, "sandbox_file_write" in supported, "--list-adapters must contain sandbox_file_write adapter")
        require(errors, "scoped_repo_patch" in supported, "--list-adapters must contain scoped_repo_patch adapter")
        scoped = supported.get("scoped_repo_patch", {})
        require(errors, scoped.get("supports_dry_run_bundle") is True, "scoped_repo_patch.supports_dry_run_bundle must be true")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-execution-profiles"])
    require(errors, code == 0, f"--list-execution-profiles failed: rc={code}, stderr={err}")
    profiles = parse_json_output(out, "--list-execution-profiles", errors)
    if profiles:
        require(errors, profiles.get("execution_profile_module_version") == "0.6.0", "--list-execution-profiles version must be 0.6.0")
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
    with tempfile.TemporaryDirectory() as patch_dir:
        patch_root = Path(patch_dir)
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
            require(errors, dry_only["dry_run_bundle"].get("dry_run_bundle_version") == "0.6.0", "dry_run_bundle_version must be 0.6.0")
            require(errors, dry_only["dry_run_bundle"].get("baseline_preserved") is True, "dry_run_bundle baseline_preserved must be true")

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
            require(errors, "Station Chief Runtime v0.5.0 scoped repo patch" in preview or "Station Chief Runtime v0.6.0 scoped repo patch" in preview, "dry_run_bundle preview must mention Station Chief Runtime scoped repo patch")
            require(errors, not target_file.exists(), "dry-run bundle plan must not write patch file")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--execution-profile",
            "dry_run_patch",
            "--dry-run-bundle",
        ])
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
                require(errors, manifest.get("runtime_version") == "0.6.0", "dry_run_manifest runtime_version must be 0.6.0")
                require(errors, manifest.get("baseline_preserved") is True, "dry_run_manifest baseline_preserved must be true")
                require(errors, manifest.get("external_actions_taken") is False, "dry_run_manifest external_actions_taken must be false")
                require(errors, manifest.get("live_worker_agents_activated") is False, "dry_run_manifest live_worker_agents_activated must be false")
                preview_text = (bundle_dir / "repo_patch_preview.diff").read_text()
                require(errors, "Station Chief Runtime" in preview_text, "repo_patch_preview.diff must contain Station Chief Runtime")


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
            "--dry-run-bundle",
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
        require(errors, isinstance(run_id, str) and run_id.startswith("station-chief-v0-6-check-please-"), "artifact run_id must start with station-chief-v0-6-check-please-")
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
            "runtime_index_entry.json",
            "manifest.json",
            "full_result.json",
        }
        require(errors, required_files.issubset(files_written), "artifact write must include all required files")

        manifest = json.loads((artifact_dir / "manifest.json").read_text())
        require(errors, manifest.get("artifact_type") == "station_chief_runtime_v0_6_artifacts", "manifest artifact_type must be station_chief_runtime_v0_6_artifacts")
        require(errors, manifest.get("runtime_version") == "0.6.0", "manifest runtime_version must be 0.6.0")
        require(errors, manifest.get("baseline_preserved") is True, "manifest baseline_preserved must be true")
        require(errors, manifest.get("external_actions_taken") is False, "manifest external_actions_taken must be false")
        require(errors, manifest.get("live_worker_agents_activated") is False, "manifest live_worker_agents_activated must be false")
        require(errors, manifest.get("deterministic_demo_mode") is True, "manifest deterministic_demo_mode must be true")
        require(errors, manifest.get("validator_selected_execution_profiles") is True, "manifest validator_selected_execution_profiles must be true")
        require(errors, manifest.get("repo_patch_dry_run_bundles") is True, "manifest repo_patch_dry_run_bundles must be true")
        require(errors, manifest.get("preflight_gate_records") is True, "manifest preflight_gate_records must be true")
        require(errors, manifest.get("execution_readiness_scoring") is True, "manifest execution_readiness_scoring must be true")

        registry = json.loads((registry_root / "run_registry.json").read_text())
        require(errors, registry.get("registry_version") == "0.6.0", "run_registry version must be 0.6.0")
        require(errors, len(registry.get("runs", [])) >= 1, "run_registry must contain at least one run")
        require(errors, any(run.get("run_id") == run_id for run in registry.get("runs", [])), "run_registry must contain the artifact run_id")

        runtime_index = json.loads((registry_root / "runtime_index.json").read_text())
        require(errors, runtime_index.get("index_version") == "0.6.0", "runtime_index version must be 0.6.0")
        require(errors, runtime_index.get("run_count", 0) >= 1, "runtime_index run_count must be at least 1")
        require(errors, any(run.get("run_id") == run_id for run in runtime_index.get("runs", [])), "runtime_index must contain the artifact run_id")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--resume-run-id",
            run_id,
            "--registry-dir",
            str(registry_root),
        ])
        require(errors, code == 0, f"resume-run-id failed: rc={code}, stderr={err}")
        resumed = parse_json_output(out, "resume-run-id", errors)
        if resumed:
            require(errors, resumed.get("resume_status") == "FOUND", "resume-run-id must return FOUND")
            require(errors, resumed.get("run_id") == run_id, "resume-run-id must echo run_id")
            require(errors, resumed.get("run_entry", {}).get("run_id") == run_id, "resume-run-id run_entry must echo run_id")


def main() -> None:
    errors: list[str] = []
    validate_required_files(errors)
    validate_source_files(errors)
    validate_demo_and_basic_runtime(errors)
    validate_dry_run_bundle_flow(errors)
    validate_artifacts_and_registry(errors)

    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v0.6 runtime files.")
    if errors:
        for error in errors:
            print(error)
        print("FAIL")
        sys.exit(1)

    print("PASS: Station Chief Runtime v0.6 valid.")


if __name__ == "__main__":
    main()

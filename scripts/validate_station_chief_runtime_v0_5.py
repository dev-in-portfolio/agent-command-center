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
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v0_5_report.md",
        "scripts/validate_station_chief_runtime_v0_5.py",
    ]
    for rel in required_files:
        require(errors, (REPO_ROOT / rel).exists(), f"Missing required file: {rel}")


def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    skeleton_report_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    v05_report_path = REPO_ROOT / "09_exports/station_chief_runtime_v0_5_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "0.5.0"',
            "attach_repo_patch",
            "--plan-repo-patch",
            "--patch-root",
            "--allowed-patch-file",
            "--patch-relative-path",
            "--patch-content",
            "--confirm-patch",
            "--execute-repo-patch",
            "scoped_repo_patch_adapter",
            "changed_file_scope_enforcement",
            "patch_preview_artifacts",
            "patch_approval_records",
            "repo_patch_requires_confirmation",
            "changed_file_scope_enforced",
            "repo_patch_plan",
            "repo_patch_gate",
            "repo_patch_result",
            "changed_file_scope_proof",
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
            'ADAPTER_MODULE_VERSION = "0.5.0"',
            "scoped_repo_patch",
            "YES_I_APPROVE_SCOPED_REPO_PATCH",
            "SAFE_REPO_PATCH_PATH",
            "BLOCKED_NOT_ALLOWLISTED",
            "BLOCKED_FORBIDDEN_REPO_PATH",
            "BLOCKED_OUTSIDE_PATCH_ROOT",
            "normalize_relative_patch_path",
            "is_forbidden_repo_patch_path",
            "classify_repo_patch_safety",
            "create_repo_patch_plan",
            "evaluate_repo_patch_gate",
            "run_scoped_repo_patch_adapter",
            "create_changed_file_scope_proof",
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
        readme_path,
        [
            "Station Chief Runtime upgraded to v0.5.0.",
            "human-approved scoped repo patch planning",
            "changed-file scope enforcement",
            "patch preview artifacts",
            "Blocks unsafe, unconfirmed, non-allowlisted, or forbidden repo patch operations",
            "repo_patch_plan.json",
            "repo_patch_gate.json",
            "repo_patch_result.json",
            "changed_file_scope_proof.json",
            "YES_I_APPROVE_SCOPED_REPO_PATCH",
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
            "Station Chief Runtime upgraded to v0.5.0.",
            "human-approved scoped repo patch planning",
            "changed-file scope enforcement",
            "patch preview artifacts",
            "forbidden repo path blocking",
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
        v05_report_path,
        [
            "Station Chief Runtime v0.5.0 Report",
            "Station Chief Runtime upgraded to v0.5.0. Locked 175-family baseline preserved.",
            "human-approved scoped repo patch planning",
            "changed-file scope enforcement",
            "patch preview artifacts",
            "allowlist validation",
            "forbidden-path blocking",
            "patch audit records",
            "controlled patch-root-only application",
            "repo_patch_plan",
            "repo_patch_gate",
            "repo_patch_result",
            "changed_file_scope_proof",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no full workforce animation",
            "Station Chief Runtime v0.5.0 keeps execution deterministic",
            "Next recommended build step",
        ],
        "station_chief_runtime_v0_5_report.md",
    )


def validate_demo_and_basic_runtime(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: rc={code}, stderr={err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "0.5.0", "--demo runtime version must be 0.5.0")
        require(errors, demo.get("command_type") == "verification", "--demo command_type must be verification")
        require(errors, demo.get("activation_tier", {}).get("name") == "Tier 4 — Audit / Archive", "--demo activation tier mismatch")
        rc = demo.get("run_capabilities", {})
        require(errors, rc.get("scoped_repo_patch_adapter") is True, "--demo run_capabilities.scoped_repo_patch_adapter must be true")
        require(errors, rc.get("changed_file_scope_enforcement") is True, "--demo run_capabilities.changed_file_scope_enforcement must be true")
        require(errors, rc.get("patch_preview_artifacts") is True, "--demo run_capabilities.patch_preview_artifacts must be true")
        require(errors, rc.get("patch_approval_records") is True, "--demo run_capabilities.patch_approval_records must be true")
        ev = demo.get("evidence", {})
        require(errors, ev.get("baseline_preserved") is True, "--demo evidence.baseline_preserved must be true")
        require(errors, ev.get("external_actions_taken") is False, "--demo evidence.external_actions_taken must be false")
        require(errors, ev.get("live_worker_agents_activated") is False, "--demo evidence.live_worker_agents_activated must be false")
        require(errors, ev.get("deterministic_demo_mode") is True, "--demo evidence.deterministic_demo_mode must be true")
        require(errors, ev.get("repo_patch_requires_confirmation") is True, "--demo evidence.repo_patch_requires_confirmation must be true")
        require(errors, ev.get("changed_file_scope_enforced") is True, "--demo evidence.changed_file_scope_enforced must be true")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: rc={code}, stderr={err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "--fixture-test status must be PASS")
        require(errors, fixture.get("runtime_version") == "0.5.0", "--fixture-test runtime_version must be 0.5.0")
        require(errors, fixture.get("case_count") == 5, "--fixture-test case_count must be 5")
        require(errors, fixture.get("failed") == 0, "--fixture-test failed must be 0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: rc={code}, stderr={err}")
    fixture_runner = parse_json_output(out, "fixture runner", errors)
    if fixture_runner:
        require(errors, fixture_runner.get("fixture_test_status") == "PASS", "fixture runner status must be PASS")
        require(errors, fixture_runner.get("runtime_version") == "0.5.0", "fixture runner runtime_version must be 0.5.0")
        require(errors, fixture_runner.get("case_count") == 5, "fixture runner case_count must be 5")
        require(errors, fixture_runner.get("failed") == 0, "fixture runner failed must be 0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--json"])
    require(errors, code == 0, f"--json command failed: rc={code}, stderr={err}")
    command_json = parse_json_output(out, "--json command", errors)
    if command_json:
        require(errors, command_json.get("station_chief_runtime_version") == "0.5.0", "--json runtime version must be 0.5.0")

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
        require(errors, adapters.get("adapter_module_version") == "0.5.0", "--list-adapters adapter_module_version must be 0.5.0")
        supported = adapters.get("supported_adapters", {})
        require(errors, "noop" in supported, "--list-adapters must contain noop adapter")
        require(errors, "sandbox_file_write" in supported, "--list-adapters must contain sandbox_file_write adapter")
        require(errors, "scoped_repo_patch" in supported, "--list-adapters must contain scoped_repo_patch adapter")
        sandbox = supported.get("sandbox_file_write", {})
        scoped = supported.get("scoped_repo_patch", {})
        require(errors, sandbox.get("requires_human_confirmation") is True, "sandbox_file_write.requires_human_confirmation must be true")
        require(errors, sandbox.get("sandbox_only") is True, "sandbox_file_write.sandbox_only must be true")
        require(errors, sandbox.get("live_execution") is False, "sandbox_file_write.live_execution must be false")
        require(errors, sandbox.get("external_actions") is False, "sandbox_file_write.external_actions must be false")
        require(errors, sandbox.get("worker_animation") is False, "sandbox_file_write.worker_animation must be false")
        require(errors, scoped.get("requires_human_confirmation") is True, "scoped_repo_patch.requires_human_confirmation must be true")
        require(errors, scoped.get("patch_root_only") is True, "scoped_repo_patch.patch_root_only must be true")
        require(errors, scoped.get("requires_allowed_file_scope") is True, "scoped_repo_patch.requires_allowed_file_scope must be true")
        require(errors, scoped.get("live_execution") is False, "scoped_repo_patch.live_execution must be false")
        require(errors, scoped.get("external_actions") is False, "scoped_repo_patch.external_actions must be false")
        require(errors, scoped.get("worker_animation") is False, "scoped_repo_patch.worker_animation must be false")

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


def validate_sandbox_file_operation_flow(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory() as exec_dir:
        exec_root = Path(exec_dir)
        target_file = exec_root / "station_chief_sandbox_output.txt"

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-file-operation",
            "--execution-dir",
            str(exec_root),
        ])
        require(errors, code == 0, f"plan-file-operation failed: rc={code}, stderr={err}")
        planned = parse_json_output(out, "plan-file-operation", errors)
        if planned:
            require(errors, "file_operation_plan" in planned, "plan-file-operation must include file_operation_plan")
            require(errors, "execution_gate" in planned, "plan-file-operation must include execution_gate")
            require(errors, "file_operation_result" in planned, "plan-file-operation must include file_operation_result")
            require(errors, planned["file_operation_plan"].get("operation_status") == "PLANNED_SAFE", "plan-file-operation operation_status must be PLANNED_SAFE")
            require(errors, planned["execution_gate"].get("gate_status") == "BLOCKED", "plan-file-operation gate_status must be BLOCKED")
            require(errors, planned["file_operation_result"].get("adapter_result_status") == "PLANNED_ONLY", "plan-file-operation result status must be PLANNED_ONLY")
            require(errors, planned["file_operation_result"].get("file_written") is False, "plan-file-operation file_written must be false")
            require(errors, not target_file.exists(), "plan-file-operation must not write a file")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--execute-sandbox-file-write",
            "--execution-dir",
            str(exec_root),
        ])
        require(errors, code == 0, f"blocked sandbox write failed: rc={code}, stderr={err}")
        blocked = parse_json_output(out, "blocked sandbox write", errors)
        if blocked:
            require(errors, blocked["execution_gate"].get("gate_status") == "BLOCKED", "blocked sandbox write gate_status must be BLOCKED")
            require(errors, blocked["file_operation_result"].get("adapter_result_status") == "BLOCKED", "blocked sandbox write result status must be BLOCKED")
            require(errors, blocked["file_operation_result"].get("file_written") is False, "blocked sandbox write file_written must be false")
            require(errors, not target_file.exists(), "blocked sandbox write must not write a file")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--execute-sandbox-file-write",
            "--execution-dir",
            str(exec_root),
            "--confirm-execution",
            "YES_I_APPROVE_SANDBOX_FILE_WRITE",
        ])
        require(errors, code == 0, f"approved sandbox write failed: rc={code}, stderr={err}")
        approved = parse_json_output(out, "approved sandbox write", errors)
        if approved:
            require(errors, approved["execution_gate"].get("gate_status") == "APPROVED", "approved sandbox write gate_status must be APPROVED")
            require(errors, approved["execution_gate"].get("approved_for_sandbox_write") is True, "approved sandbox write must be approved")
            require(errors, approved["file_operation_result"].get("adapter_result_status") == "PASS", "approved sandbox write result status must be PASS")
            require(errors, approved["file_operation_result"].get("file_written") is True, "approved sandbox write file_written must be true")
            require(errors, target_file.exists(), "approved sandbox write must create the target file")
            if target_file.exists():
                content = target_file.read_text()
                require(
                    errors,
                    "Station Chief Runtime v0.5.0 sandbox file operation" in content
                    or "Station Chief Runtime v0.4.0 sandbox file operation" in content,
                    "sandbox file content missing marker",
                )
                require(errors, "baseline_preserved=true" in content, "sandbox file content missing baseline_preserved=true")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-file-operation",
            "--execution-dir",
            str(exec_root),
            "--target-filename",
            "../04_workflow_templates/bad.json",
        ])
        require(errors, code == 0, f"forbidden sandbox path plan failed: rc={code}, stderr={err}")
        forbidden = parse_json_output(out, "forbidden sandbox path plan", errors)
        if forbidden:
            require(errors, forbidden["file_operation_plan"]["path_safety"]["safety_status"] != "SAFE_SANDBOX_PATH", "forbidden sandbox path must not be SAFE_SANDBOX_PATH")
            require(errors, forbidden["execution_gate"].get("gate_status") == "BLOCKED", "forbidden sandbox path gate_status must be BLOCKED")


def validate_repo_patch_flow(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory() as patch_dir:
        patch_root = Path(patch_dir)
        target_rel = "runtime_patch_preview/station_chief_patch_output.txt"
        target_file = patch_root / target_rel

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
        ])
        require(errors, code == 0, f"plan-repo-patch failed: rc={code}, stderr={err}")
        planned = parse_json_output(out, "plan-repo-patch", errors)
        if planned:
            require(errors, "repo_patch_plan" in planned, "plan-repo-patch must include repo_patch_plan")
            require(errors, "repo_patch_gate" in planned, "plan-repo-patch must include repo_patch_gate")
            require(errors, "repo_patch_result" in planned, "plan-repo-patch must include repo_patch_result")
            require(errors, "changed_file_scope_proof" in planned, "plan-repo-patch must include changed_file_scope_proof")
            require(errors, planned["repo_patch_plan"].get("operation_status") == "PLANNED_SAFE", "plan-repo-patch operation_status must be PLANNED_SAFE")
            require(errors, planned["repo_patch_gate"].get("gate_status") == "BLOCKED", "plan-repo-patch gate_status must be BLOCKED")
            require(errors, planned["repo_patch_result"].get("adapter_result_status") == "PLANNED_ONLY", "plan-repo-patch result status must be PLANNED_ONLY")
            require(errors, planned["repo_patch_result"].get("file_written") is False, "plan-repo-patch file_written must be false")
            require(errors, not target_file.exists(), "plan-repo-patch must not write a file")
            require(errors, "+Station Chief Runtime v0.5.0 scoped repo patch" in planned["repo_patch_plan"].get("patch_preview", ""), "repo patch preview must include the marker line")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--execute-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            target_rel,
        ])
        require(errors, code == 0, f"blocked repo patch failed: rc={code}, stderr={err}")
        blocked = parse_json_output(out, "blocked repo patch", errors)
        if blocked:
            require(errors, blocked["repo_patch_gate"].get("gate_status") == "BLOCKED", "blocked repo patch gate_status must be BLOCKED")
            require(errors, blocked["repo_patch_result"].get("adapter_result_status") == "BLOCKED", "blocked repo patch result status must be BLOCKED")
            require(errors, blocked["repo_patch_result"].get("file_written") is False, "blocked repo patch file_written must be false")
            require(errors, not target_file.exists(), "blocked repo patch must not write a file")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--execute-repo-patch",
            "--patch-root",
            str(patch_root),
            "--allowed-patch-file",
            target_rel,
            "--confirm-patch",
            "YES_I_APPROVE_SCOPED_REPO_PATCH",
        ])
        require(errors, code == 0, f"approved repo patch failed: rc={code}, stderr={err}")
        approved = parse_json_output(out, "approved repo patch", errors)
        if approved:
            require(errors, approved["repo_patch_gate"].get("gate_status") == "APPROVED", "approved repo patch gate_status must be APPROVED")
            require(errors, approved["repo_patch_gate"].get("approved_for_repo_patch") is True, "approved repo patch must be approved")
            require(errors, approved["repo_patch_result"].get("adapter_result_status") == "PASS", "approved repo patch result status must be PASS")
            require(errors, approved["repo_patch_result"].get("file_written") is True, "approved repo patch file_written must be true")
            require(errors, target_file.exists(), "approved repo patch must create the target file")
            if target_file.exists():
                content = target_file.read_text()
                require(errors, "Station Chief Runtime v0.5.0 scoped repo patch" in content, "repo patch file content missing marker")
                require(errors, "changed_file_scope_enforced=true" in content, "repo patch file content missing changed_file_scope_enforced=true")
            require(errors, approved["changed_file_scope_proof"].get("scope_proof_status") == "PASS", "changed file scope proof must PASS")
            require(errors, approved["changed_file_scope_proof"].get("all_changed_files_allowlisted") is True, "changed file scope proof must report allowlisted files")
            require(errors, approved["changed_file_scope_proof"].get("baseline_preserved") is True, "changed file scope proof baseline_preserved must be true")
            require(errors, approved["changed_file_scope_proof"].get("devinization_overlays_preserved") is True, "changed file scope proof devinization_overlays_preserved must be true")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--patch-relative-path",
            "runtime_patch_preview/not_allowlisted.txt",
            "--allowed-patch-file",
            target_rel,
        ])
        require(errors, code == 0, f"not-allowlisted repo patch failed: rc={code}, stderr={err}")
        not_allowed = parse_json_output(out, "not-allowlisted repo patch", errors)
        if not_allowed:
            require(errors, not_allowed["repo_patch_plan"]["path_safety"]["safety_status"] == "BLOCKED_NOT_ALLOWLISTED", "non-allowlisted repo patch must be BLOCKED_NOT_ALLOWLISTED")
            require(errors, not_allowed["repo_patch_gate"].get("gate_status") == "BLOCKED", "non-allowlisted repo patch gate_status must be BLOCKED")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--patch-relative-path",
            "04_workflow_templates/bad.json",
            "--allowed-patch-file",
            "04_workflow_templates/bad.json",
        ])
        require(errors, code == 0, f"forbidden repo patch failed: rc={code}, stderr={err}")
        forbidden = parse_json_output(out, "forbidden repo patch", errors)
        if forbidden:
            require(errors, forbidden["repo_patch_plan"]["path_safety"]["safety_status"] == "BLOCKED_FORBIDDEN_REPO_PATH", "forbidden repo patch must be BLOCKED_FORBIDDEN_REPO_PATH")
            require(errors, forbidden["repo_patch_gate"].get("gate_status") == "BLOCKED", "forbidden repo patch gate_status must be BLOCKED")

        code, out, err = run_command([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-repo-patch",
            "--patch-root",
            str(patch_root),
            "--patch-relative-path",
            "../escape.txt",
            "--allowed-patch-file",
            "../escape.txt",
        ])
        require(errors, code == 0, f"traversal repo patch failed: rc={code}, stderr={err}")
        traversal = parse_json_output(out, "traversal repo patch", errors)
        if traversal:
            require(errors, traversal["repo_patch_plan"]["path_safety"]["safety_status"] != "SAFE_REPO_PATCH_PATH", "path traversal must not be SAFE_REPO_PATCH_PATH")
            require(errors, traversal["repo_patch_gate"].get("gate_status") == "BLOCKED", "path traversal gate_status must be BLOCKED")


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
        require(errors, isinstance(run_id, str) and run_id.startswith("station-chief-v0-5-check-please-"), "artifact run_id must start with station-chief-v0-5-check-please-")
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
            "runtime_index_entry.json",
            "manifest.json",
            "full_result.json",
        }
        require(errors, required_files.issubset(files_written), "artifact write must include all required files")

        manifest = json.loads((artifact_dir / "manifest.json").read_text())
        require(errors, manifest.get("artifact_type") == "station_chief_runtime_v0_5_artifacts", "manifest artifact_type must be station_chief_runtime_v0_5_artifacts")
        require(errors, manifest.get("runtime_version") == "0.5.0", "manifest runtime_version must be 0.5.0")
        require(errors, manifest.get("baseline_preserved") is True, "manifest baseline_preserved must be true")
        require(errors, manifest.get("external_actions_taken") is False, "manifest external_actions_taken must be false")
        require(errors, manifest.get("live_worker_agents_activated") is False, "manifest live_worker_agents_activated must be false")
        require(errors, manifest.get("deterministic_demo_mode") is True, "manifest deterministic_demo_mode must be true")
        require(errors, manifest.get("scoped_repo_patch_supported") is True, "manifest scoped_repo_patch_supported must be true")
        require(errors, manifest.get("human_confirmation_required_for_repo_patch") is True, "manifest human_confirmation_required_for_repo_patch must be true")
        require(errors, manifest.get("changed_file_scope_enforced") is True, "manifest changed_file_scope_enforced must be true")

        registry = json.loads((registry_root / "run_registry.json").read_text())
        require(errors, registry.get("registry_version") == "0.5.0", "run_registry version must be 0.5.0")
        require(errors, len(registry.get("runs", [])) >= 1, "run_registry must contain at least one run")
        require(errors, any(run.get("run_id") == run_id for run in registry.get("runs", [])), "run_registry must contain the artifact run_id")

        runtime_index = json.loads((registry_root / "runtime_index.json").read_text())
        require(errors, runtime_index.get("index_version") == "0.5.0", "runtime_index version must be 0.5.0")
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
    validate_sandbox_file_operation_flow(errors)
    validate_repo_patch_flow(errors)
    validate_artifacts_and_registry(errors)

    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v0.5 runtime files.")
    if errors:
        for error in errors:
            print(error)
        print("FAIL")
        sys.exit(1)

    print("PASS: Station Chief Runtime v0.5 valid.")


if __name__ == "__main__":
    main()

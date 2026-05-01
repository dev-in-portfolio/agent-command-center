#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "10_runtime/station_chief_runtime.py",
    ROOT / "10_runtime/station_chief_demo_cases.json",
    ROOT / "10_runtime/station_chief_runtime_readme.md",
    ROOT / "10_runtime/station_chief_fixture_tests.py",
    ROOT / "10_runtime/station_chief_adapters.py",
    ROOT / "09_exports/station_chief_runtime_skeleton_report.md",
    ROOT / "09_exports/station_chief_runtime_v0_4_report.md",
    ROOT / "scripts/validate_station_chief_runtime_v0_4.py",
]

FORBIDDEN_SNIPPETS = [
    "requests",
    "urllib.request",
    "os.system",
    "pip install",
    "npm install",
    "live API",
    "API key",
]


def run_cmd(args: list[str]) -> str:
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed: {' '.join(args)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc.stdout


def parsed_json_output(args: list[str]) -> dict:
    return json.loads(run_cmd(args))


errors: list[str] = []
for path in REQUIRED_FILES:
    if not path.exists():
        errors.append(f"missing file: {path.relative_to(ROOT)}")

runtime_path = ROOT / "10_runtime/station_chief_runtime.py"
runtime_text = runtime_path.read_text() if runtime_path.exists() else ""
for snippet in [
    'STATION_CHIEF_RUNTIME_VERSION = "0.4.0"',
    "attach_file_operation",
    "--plan-file-operation",
    "--execution-dir",
    "--target-filename",
    "--confirm-execution",
    "--execute-sandbox-file-write",
    "controlled_file_operation_adapter",
    "human_confirmed_execution_gates",
    "sandbox_file_write_adapter",
    "controlled_file_write_requires_confirmation",
    "file_operation_plan",
    "execution_gate",
    "file_operation_result",
]:
    if snippet not in runtime_text:
        errors.append(f"runtime missing snippet: {snippet}")
for forbidden in FORBIDDEN_SNIPPETS:
    if forbidden in runtime_text:
        errors.append(f"runtime contains forbidden snippet: {forbidden}")
if "import subprocess" in runtime_text:
    errors.append("runtime must not import subprocess")

adapter_path = ROOT / "10_runtime/station_chief_adapters.py"
adapter_text = adapter_path.read_text() if adapter_path.exists() else ""
for snippet in [
    'ADAPTER_MODULE_VERSION = "0.4.0"',
    "sandbox_file_write",
    "classify_path_safety",
    "create_file_operation_plan",
    "evaluate_execution_gate",
    "run_sandbox_file_write_adapter",
    "YES_I_APPROVE_SANDBOX_FILE_WRITE",
    "SAFE_SANDBOX_PATH",
    "BLOCKED_FORBIDDEN_PATH",
    "BLOCKED_OUTSIDE_EXECUTION_DIR",
]:
    if snippet not in adapter_text:
        errors.append(f"adapter module missing snippet: {snippet}")
for forbidden in ["requests", "urllib.request", "os.system", "pip install", "npm install", "live API", "API key", "import subprocess"]:
    if forbidden in adapter_text:
        errors.append(f"adapter module contains forbidden snippet: {forbidden}")

fixture_runner_text = (ROOT / "10_runtime/station_chief_fixture_tests.py").read_text() if (ROOT / "10_runtime/station_chief_fixture_tests.py").exists() else ""
for snippet in [
    "from station_chief_runtime import run_fixture_tests",
    "main()",
    'if __name__ == "__main__"',
]:
    if snippet not in fixture_runner_text:
        errors.append(f"fixture runner missing snippet: {snippet}")

readme_text = (ROOT / "10_runtime/station_chief_runtime_readme.md").read_text() if (ROOT / "10_runtime/station_chief_runtime_readme.md").exists() else ""
for snippet in [
    "Station Chief Runtime upgraded to v0.4.0.",
    "human-confirmed sandbox file-operation gates",
    "controlled sandbox file-operation planning",
    "human-confirmed sandbox file writes",
    "Blocks unsafe or unconfirmed file operations",
    "file_operation_plan.json",
    "execution_gate.json",
    "file_operation_result.json",
    "YES_I_APPROVE_SANDBOX_FILE_WRITE",
    "The Station Chief runtime keeps the full 175-family command civilization intact",
]:
    if snippet not in readme_text:
        errors.append(f"README missing required text: {snippet}")
for forbidden in ["Explain that", "Include:", "List:", "Write:"]:
    if forbidden in readme_text:
        errors.append(f"README contains forbidden scaffold text: {forbidden}")

skeleton_report_text = (ROOT / "09_exports/station_chief_runtime_skeleton_report.md").read_text() if (ROOT / "09_exports/station_chief_runtime_skeleton_report.md").exists() else ""
for snippet in [
    "Station Chief Runtime upgraded to v0.4.0.",
    "controlled file-operation adapters",
    "human-confirmed execution gates",
    "controlled sandbox file-operation planning",
    "human-confirmed sandbox file writes",
    "unsafe path blocking",
    "no live API calls",
    "no full workforce animation",
]:
    if snippet not in skeleton_report_text:
        errors.append(f"skeleton report missing required text: {snippet}")
for forbidden in ["Explain that", "Include:", "List:", "Write:"]:
    if forbidden in skeleton_report_text:
        errors.append(f"skeleton report contains forbidden scaffold text: {forbidden}")

report_text = (ROOT / "09_exports/station_chief_runtime_v0_4_report.md").read_text() if (ROOT / "09_exports/station_chief_runtime_v0_4_report.md").exists() else ""
for snippet in [
    "Station Chief Runtime v0.4.0 Report",
    "Station Chief Runtime upgraded to v0.4.0. Locked 175-family baseline preserved.",
    "controlled file-operation adapter planning",
    "human-confirmed sandbox execution gates",
    "path safety checks",
    "execution approval records",
    "file-operation audit artifacts",
    "file_operation_plan.json",
    "execution_gate.json",
    "file_operation_result.json",
    "no baseline mutation",
    "no Devinization overlay mutation",
    "no live API calls",
    "no full workforce animation",
    "Station Chief Runtime v0.4.0 keeps execution deterministic",
    "Next recommended build step",
]:
    if snippet not in report_text:
        errors.append(f"v0.4 report missing required text: {snippet}")
for forbidden in ["Explain that", "Include:", "List:", "Write:"]:
    if forbidden in report_text:
        errors.append(f"v0.4 report contains forbidden scaffold text: {forbidden}")

print("Manual scope check required: confirm git diff contains only the allowed Station Chief v0.4 runtime files.")

try:
    demo = parsed_json_output(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    if demo.get("station_chief_runtime_version") != "0.4.0":
        errors.append("demo runtime version mismatch")
    if demo.get("command_type") != "verification":
        errors.append("demo command_type mismatch")
    if demo.get("activation_tier", {}).get("name") != "Tier 4 — Audit / Archive":
        errors.append("demo activation tier mismatch")
    run_caps = demo.get("run_capabilities", {})
    for key in [
        "persistent_run_logs",
        "command_brief_artifacts",
        "work_order_artifacts",
        "deterministic_fixture_tests",
        "selected_overlay_artifacts",
        "evidence_artifacts",
        "persistent_runtime_index",
        "resumable_run_registry",
        "controlled_execution_adapters",
        "noop_execution_adapter",
        "controlled_file_operation_adapter",
        "human_confirmed_execution_gates",
        "sandbox_file_write_adapter",
    ]:
        if run_caps.get(key) is not True:
            errors.append(f"demo run_capabilities mismatch for {key}")
    evidence = demo.get("evidence", {})
    for key, expected in [
        ("baseline_preserved", True),
        ("external_actions_taken", False),
        ("live_worker_agents_activated", False),
        ("deterministic_demo_mode", True),
        ("controlled_file_write_requires_confirmation", True),
    ]:
        if evidence.get(key) is not expected:
            errors.append(f"demo evidence mismatch for {key}")
except Exception as exc:
    errors.append(str(exc))

try:
    fixture = parsed_json_output(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    if fixture.get("fixture_test_status") != "PASS":
        errors.append("runtime fixture-test status mismatch")
    if fixture.get("runtime_version") != "0.4.0":
        errors.append("runtime fixture-test version mismatch")
    if fixture.get("case_count") != 5:
        errors.append("runtime fixture-test case count mismatch")
    if fixture.get("failed") != 0:
        errors.append("runtime fixture-test failures present")
except Exception as exc:
    errors.append(str(exc))

try:
    fixture_runner = parsed_json_output(["python3", "10_runtime/station_chief_fixture_tests.py"])
    if fixture_runner.get("fixture_test_status") != "PASS":
        errors.append("fixture runner status mismatch")
    if fixture_runner.get("runtime_version") != "0.4.0":
        errors.append("fixture runner version mismatch")
    if fixture_runner.get("case_count") != 5:
        errors.append("fixture runner case count mismatch")
    if fixture_runner.get("failed") != 0:
        errors.append("fixture runner failures present")
except Exception as exc:
    errors.append(str(exc))

try:
    overlays = parsed_json_output(["python3", "10_runtime/station_chief_runtime.py", "--list-overlays"])
    if len(overlays) != 8:
        errors.append(f"overlay count expected 8 got {len(overlays)}")
    for overlay in overlays:
        if overlay.get("exists") is not True:
            errors.append(f"overlay not existing: {overlay.get('id')}")
        if overlay.get("preserves_locked_baseline") is not True:
            errors.append(f"overlay does not preserve baseline: {overlay.get('id')}")
        if "Devin O’Rourke" not in str(overlay.get("ownership_project_owner")):
            errors.append(f"overlay ownership missing Devin O’Rourke: {overlay.get('id')}")
except Exception as exc:
    errors.append(str(exc))

try:
    adapters = parsed_json_output(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    if adapters.get("adapter_module_version") != "0.4.0":
        errors.append("adapter module version mismatch")
    noop = adapters.get("supported_adapters", {}).get("noop")
    sandbox = adapters.get("supported_adapters", {}).get("sandbox_file_write")
    if not noop:
        errors.append("noop adapter missing")
    else:
        if noop.get("live_execution") is not False:
            errors.append("noop live_execution mismatch")
        if noop.get("external_actions") is not False:
            errors.append("noop external_actions mismatch")
        if noop.get("worker_animation") is not False:
            errors.append("noop worker_animation mismatch")
    if not sandbox:
        errors.append("sandbox_file_write adapter missing")
    else:
        if sandbox.get("requires_human_confirmation") is not True:
            errors.append("sandbox adapter confirmation flag mismatch")
        if sandbox.get("sandbox_only") is not True:
            errors.append("sandbox adapter sandbox_only mismatch")
        if sandbox.get("live_execution") is not False:
            errors.append("sandbox adapter live_execution mismatch")
        if sandbox.get("external_actions") is not False:
            errors.append("sandbox adapter external_actions mismatch")
        if sandbox.get("worker_animation") is not False:
            errors.append("sandbox adapter worker_animation mismatch")
except Exception as exc:
    errors.append(str(exc))

try:
    simulate = parsed_json_output(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--simulate-adapter"])
    if "execution_plan" not in simulate:
        errors.append("simulate output missing execution_plan")
    if "adapter_result" not in simulate:
        errors.append("simulate output missing adapter_result")
    adapter_result = simulate.get("adapter_result", {})
    if adapter_result.get("adapter_result_status") != "PASS":
        errors.append("simulate adapter status mismatch")
    if adapter_result.get("live_execution_performed") is not False:
        errors.append("simulate live execution mismatch")
    if adapter_result.get("external_actions_taken") is not False:
        errors.append("simulate external actions mismatch")
    if adapter_result.get("worker_agents_activated") is not False:
        errors.append("simulate worker activation mismatch")
except Exception as exc:
    errors.append(str(exc))

try:
    brief = parsed_json_output(["python3", "10_runtime/station_chief_runtime.py", "--command", "build Station Chief runtime skeleton", "--brief"])
    if brief.get("command_type") != "build":
        errors.append("brief command_type mismatch")
    if brief.get("activation_tier", {}).get("name") != "Tier 3 — Active Operation":
        errors.append("brief activation tier mismatch")
    if brief.get("deterministic_demo_mode") is not True:
        errors.append("brief deterministic_demo_mode mismatch")
    if brief.get("baseline_protection") is not True:
        errors.append("brief baseline_protection mismatch")
    if brief.get("external_actions_allowed") is not False:
        errors.append("brief external_actions_allowed mismatch")
    if brief.get("workforce_animation_allowed") is not False:
        errors.append("brief workforce_animation_allowed mismatch")
except Exception as exc:
    errors.append(str(exc))

try:
    with tempfile.TemporaryDirectory() as tmp_exec_dir:
        plan_only = parsed_json_output([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-file-operation",
            "--execution-dir",
            tmp_exec_dir,
        ])
        plan = plan_only.get("file_operation_plan")
        gate = plan_only.get("execution_gate")
        result = plan_only.get("file_operation_result")
        if not plan:
            errors.append("plan-only missing file_operation_plan")
        if not gate:
            errors.append("plan-only missing execution_gate")
        if not result:
            errors.append("plan-only missing file_operation_result")
        if plan and plan.get("operation_status") != "PLANNED_SAFE":
            errors.append("plan-only operation status mismatch")
        if gate and gate.get("gate_status") != "BLOCKED":
            errors.append("plan-only gate status mismatch")
        if result and result.get("adapter_result_status") != "PLANNED_ONLY":
            errors.append("plan-only adapter status mismatch")
        if result and result.get("file_written") is not False:
            errors.append("plan-only file_written mismatch")
        if plan and Path(plan.get("target_path", "")).exists():
            errors.append("plan-only target unexpectedly exists")

        blocked = parsed_json_output([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--execute-sandbox-file-write",
            "--execution-dir",
            tmp_exec_dir,
        ])
        gate = blocked.get("execution_gate")
        result = blocked.get("file_operation_result")
        if gate and gate.get("gate_status") != "BLOCKED":
            errors.append("blocked execution gate status mismatch")
        if result and result.get("adapter_result_status") != "BLOCKED":
            errors.append("blocked execution adapter status mismatch")
        if result and result.get("file_written") is not False:
            errors.append("blocked execution file_written mismatch")
        if Path(tmp_exec_dir, "station_chief_sandbox_output.txt").exists():
            errors.append("blocked execution target unexpectedly exists")

        approved = parsed_json_output([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--execute-sandbox-file-write",
            "--execution-dir",
            tmp_exec_dir,
            "--confirm-execution",
            "YES_I_APPROVE_SANDBOX_FILE_WRITE",
        ])
        gate = approved.get("execution_gate")
        result = approved.get("file_operation_result")
        target_path = Path(approved["file_operation_plan"]["target_path"]) if approved.get("file_operation_plan") else Path(tmp_exec_dir, "station_chief_sandbox_output.txt")
        if gate and gate.get("gate_status") != "APPROVED":
            errors.append("approved execution gate status mismatch")
        if gate and gate.get("approved_for_sandbox_write") is not True:
            errors.append("approved execution approval flag mismatch")
        if result and result.get("adapter_result_status") != "PASS":
            errors.append("approved execution adapter status mismatch")
        if result and result.get("file_written") is not True:
            errors.append("approved execution file_written mismatch")
        if not target_path.exists():
            errors.append("approved execution target missing")
        else:
            content = target_path.read_text()
            if "Station Chief Runtime v0.4.0 sandbox file operation" not in content:
                errors.append("approved execution content missing runtime line")
            if "baseline_preserved=true" not in content:
                errors.append("approved execution content missing baseline line")

        forbidden = parsed_json_output([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--plan-file-operation",
            "--execution-dir",
            tmp_exec_dir,
            "--target-filename",
            "../04_workflow_templates/bad.json",
        ])
        plan = forbidden.get("file_operation_plan")
        gate = forbidden.get("execution_gate")
        if plan and plan.get("path_safety", {}).get("safety_status") == "SAFE_SANDBOX_PATH":
            errors.append("forbidden path unexpectedly safe")
        if gate and gate.get("gate_status") != "BLOCKED":
            errors.append("forbidden path gate status mismatch")
except Exception as exc:
    errors.append(str(exc))

try:
    with tempfile.TemporaryDirectory() as tmp_run_dir, tempfile.TemporaryDirectory() as tmp_registry_dir, tempfile.TemporaryDirectory() as tmp_exec_dir:
        with_artifacts = parsed_json_output([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--write-artifacts",
            tmp_run_dir,
            "--registry-dir",
            tmp_registry_dir,
            "--plan-file-operation",
            "--execution-dir",
            tmp_exec_dir,
        ])
        summary = with_artifacts.get("artifact_write_summary")
        if not summary:
            errors.append("missing artifact_write_summary")
        else:
            if not str(summary.get("run_id", "")).startswith("station-chief-v0-4-check-please-"):
                errors.append("artifact run_id prefix mismatch")
            artifact_dir = Path(summary.get("artifact_dir", ""))
            if not artifact_dir.exists():
                errors.append("artifact directory missing")
            if summary.get("registry_updated") is not True:
                errors.append("registry_updated flag mismatch")
            files_written = summary.get("files_written", [])
            expected_files = {
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
                "runtime_index_entry.json",
                "manifest.json",
                "full_result.json",
            }
            if set(files_written) != expected_files:
                errors.append(f"artifact files written mismatch: {files_written}")
            manifest = json.loads((artifact_dir / "manifest.json").read_text())
            for key, expected in [
                ("artifact_type", "station_chief_runtime_v0_4_artifacts"),
                ("runtime_version", "0.4.0"),
                ("baseline_preserved", True),
                ("external_actions_taken", False),
                ("live_worker_agents_activated", False),
                ("deterministic_demo_mode", True),
                ("controlled_execution_adapter", "noop"),
                ("controlled_file_operations_supported", True),
                ("human_confirmation_required_for_file_write", True),
            ]:
                if manifest.get(key) != expected:
                    errors.append(f"artifact manifest mismatch for {key}")
            run_log = json.loads((artifact_dir / "run_log.json").read_text())
            for key, expected in [
                ("runtime_version", "0.4.0"),
                ("command", "check please"),
                ("command_type", "verification"),
                ("baseline_preserved", True),
                ("external_actions_taken", False),
                ("live_worker_agents_activated", False),
                ("deterministic_demo_mode", True),
            ]:
                if run_log.get(key) != expected:
                    errors.append(f"run_log mismatch for {key}")
            if run_log.get("activation_tier", {}).get("name") != "Tier 4 — Audit / Archive":
                errors.append("run_log activation tier mismatch")
            if not (artifact_dir / "file_operation_plan.json").exists():
                errors.append("missing file_operation_plan.json")
            if not (artifact_dir / "execution_gate.json").exists():
                errors.append("missing execution_gate.json")
            if not (artifact_dir / "file_operation_result.json").exists():
                errors.append("missing file_operation_result.json")
            registry_dir = Path(summary.get("registry_dir", tmp_registry_dir))
            run_registry = json.loads((registry_dir / "run_registry.json").read_text())
            if run_registry.get("registry_version") != "0.4.0":
                errors.append("registry version mismatch")
            if not any(run.get("run_id") == summary.get("run_id") for run in run_registry.get("runs", [])):
                errors.append("registry missing run entry")
            runtime_index = json.loads((registry_dir / "runtime_index.json").read_text())
            if runtime_index.get("index_version") != "0.4.0":
                errors.append("runtime index version mismatch")
            if runtime_index.get("run_count", 0) < 1:
                errors.append("runtime index count mismatch")
            if not any(run.get("run_id") == summary.get("run_id") for run in runtime_index.get("runs", [])):
                errors.append("runtime index missing run entry")
            found = parsed_json_output([
                "python3",
                "10_runtime/station_chief_runtime.py",
                "--resume-run-id",
                summary.get("run_id", ""),
                "--registry-dir",
                str(registry_dir),
            ])
            if found.get("resume_status") != "FOUND":
                errors.append("resume found status mismatch")
            if found.get("run_id") != summary.get("run_id"):
                errors.append("resume run_id mismatch")
            if found.get("run_entry", {}).get("run_id") != summary.get("run_id"):
                errors.append("resume run_entry mismatch")
except Exception as exc:
    errors.append(str(exc))

if errors:
    for error in errors:
        print(error)
    print("FAIL")
    sys.exit(1)

print("PASS: Station Chief Runtime v0.4 valid.")

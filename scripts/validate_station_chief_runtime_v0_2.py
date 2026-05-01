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
    ROOT / "09_exports/station_chief_runtime_skeleton_report.md",
    ROOT / "09_exports/station_chief_runtime_v0_2_report.md",
    ROOT / "scripts/validate_station_chief_runtime_v0_2.py",
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


errors: list[str] = []
for path in REQUIRED_FILES:
    if not path.exists():
        errors.append(f"missing file: {path.relative_to(ROOT)}")

runtime_path = ROOT / "10_runtime/station_chief_runtime.py"
runtime_text = runtime_path.read_text() if runtime_path.exists() else ""

required_runtime_snippets = [
    'STATION_CHIEF_RUNTIME_VERSION = "0.2.0"',
    "normalize_command_for_id",
    "generate_run_id",
    "build_runtime_artifacts",
    "write_runtime_artifacts",
    "run_fixture_tests",
    "--write-artifacts",
    "--run-label",
    "--fixture-test",
    "persistent_run_logs",
    "command_brief_artifacts",
    "work_order_artifacts",
    "deterministic_fixture_tests",
    "selected_overlay_artifacts",
    "evidence_artifacts",
]
for snippet in required_runtime_snippets:
    if snippet not in runtime_text:
        errors.append(f"runtime missing snippet: {snippet}")
for forbidden in FORBIDDEN_SNIPPETS:
    if forbidden in runtime_text:
        errors.append(f"runtime contains forbidden snippet: {forbidden}")
if "import subprocess" in runtime_text:
    errors.append("runtime must not import subprocess")

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
    "Initial runnable runtime skeleton upgraded to v0.2.0.",
    "optional runtime artifacts",
    "deterministic fixture tests",
    "Runtime Artifacts",
    "run_log.json",
    "command_brief.json",
    "work_orders.json",
    "selected_overlays.json",
    "evidence.json",
    "manifest.json",
    "full_result.json",
    "The Station Chief runtime skeleton keeps the full 175-family command civilization intact",
]:
    if snippet not in readme_text:
        errors.append(f"README missing required text: {snippet}")
for forbidden in [
    "Explain that",
    "Include exact examples:",
    "Include this exact paragraph:",
    "Write:",
]:
    if forbidden in readme_text:
        errors.append(f"README contains forbidden scaffold text: {forbidden}")

report_text = (ROOT / "09_exports/station_chief_runtime_v0_2_report.md").read_text() if (ROOT / "09_exports/station_chief_runtime_v0_2_report.md").exists() else ""
for snippet in [
    "Station Chief Runtime v0.2.0 Report",
    "Station Chief Runtime upgraded to v0.2.0. Locked 175-family baseline preserved.",
    "deterministic run ID generation",
    "optional artifact directory writing",
    "persistent run_log.json",
    "command_brief.json",
    "work_orders.json",
    "selected_overlays.json",
    "evidence.json",
    "manifest.json",
    "full_result.json",
    "deterministic fixture test runner",
    "no baseline mutation",
    "no Devinization overlay mutation",
    "no live API calls",
    "no full workforce animation",
    "Station Chief Runtime v0.2.0 keeps execution deterministic",
    "Next recommended build step",
]:
    if snippet not in report_text:
        errors.append(f"v0.2 report missing required text: {snippet}")

print("Manual scope check required: confirm git diff contains only the allowed Station Chief v0.2 runtime files.")

def parsed_json_output(args: list[str]) -> dict:
    return json.loads(run_cmd(args))

try:
    demo = parsed_json_output(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    if demo.get("station_chief_runtime_version") != "0.2.0":
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
    ]:
        if run_caps.get(key) is not True:
            errors.append(f"demo run_capabilities mismatch for {key}")
    evidence = demo.get("evidence", {})
    for key, expected in [
        ("baseline_preserved", True),
        ("external_actions_taken", False),
        ("live_worker_agents_activated", False),
        ("deterministic_demo_mode", True),
    ]:
        if evidence.get(key) is not expected:
            errors.append(f"demo evidence mismatch for {key}")
except Exception as exc:
    errors.append(str(exc))

try:
    fixture = parsed_json_output(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    if fixture.get("fixture_test_status") != "PASS":
        errors.append("runtime fixture-test status mismatch")
    if fixture.get("runtime_version") != "0.2.0":
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
    if fixture_runner.get("runtime_version") != "0.2.0":
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
    with tempfile.TemporaryDirectory() as tmpdir:
        with_artifacts = parsed_json_output([
            "python3",
            "10_runtime/station_chief_runtime.py",
            "--command",
            "check please",
            "--write-artifacts",
            tmpdir,
        ])
        summary = with_artifacts.get("artifact_write_summary")
        if not summary:
            errors.append("missing artifact_write_summary")
        else:
            if not str(summary.get("run_id", "")).startswith("station-chief-v0-2-check-please-"):
                errors.append("artifact run_id prefix mismatch")
            artifact_dir = Path(summary.get("artifact_dir", ""))
            if not artifact_dir.exists():
                errors.append("artifact directory missing")
            files_written = summary.get("files_written", [])
            expected_files = {
                "run_log.json",
                "command_brief.json",
                "work_orders.json",
                "selected_overlays.json",
                "evidence.json",
                "manifest.json",
                "full_result.json",
            }
            if set(files_written) != expected_files:
                errors.append(f"artifact files written mismatch: {files_written}")
            manifest = json.loads((artifact_dir / "manifest.json").read_text())
            for key, expected in [
                ("artifact_type", "station_chief_runtime_v0_2_artifacts"),
                ("runtime_version", "0.2.0"),
                ("baseline_preserved", True),
                ("external_actions_taken", False),
                ("live_worker_agents_activated", False),
                ("deterministic_demo_mode", True),
            ]:
                if manifest.get(key) is not expected and manifest.get(key) != expected:
                    errors.append(f"artifact manifest mismatch for {key}")
            run_log = json.loads((artifact_dir / "run_log.json").read_text())
            for key, expected in [
                ("runtime_version", "0.2.0"),
                ("command", "check please"),
                ("command_type", "verification"),
                ("baseline_preserved", True),
                ("external_actions_taken", False),
                ("live_worker_agents_activated", False),
                ("deterministic_demo_mode", True),
            ]:
                if run_log.get(key) is not expected and run_log.get(key) != expected:
                    errors.append(f"run_log mismatch for {key}")
            if run_log.get("activation_tier", {}).get("name") != "Tier 4 — Audit / Archive":
                errors.append("run_log activation tier mismatch")
            if not with_artifacts.get("artifact_write_summary"):
                errors.append("printed JSON missing artifact_write_summary")
except Exception as exc:
    errors.append(str(exc))

if errors:
    for error in errors:
        print(error)
    print("FAIL")
    sys.exit(1)

print("PASS: Station Chief Runtime v0.2 valid.")

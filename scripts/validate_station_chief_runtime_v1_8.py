#!/usr/bin/env python3
import json
import re
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
            if s == "deploy":
                if re.search(r"\bdeploy\b", content):
                    errors.append(f"{file_path.name} contains forbidden word: '{s}'")
            elif s in content:
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
        "10_runtime/station_chief_github_patch_hardening.py",
        "10_runtime/station_chief_deployment_packaging.py",
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v1_8_report.md",
        "scripts/validate_station_chief_runtime_v1_8.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    packaging_path = REPO_ROOT / "10_runtime/station_chief_deployment_packaging.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    report_skeleton_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    report_v18_path = REPO_ROOT / "09_exports/station_chief_runtime_v1_8_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "1.8.0"',
            "attach_deployment_packaging",
            "write_deployment_packaging",
            "--deployment-artifact-schema",
            "--deployment-packaging",
            "--write-deployment-packaging",
            "deployment_packaging_bundle",
            "deployment_artifact_schema",
            "portfolio_packaging_manifest",
            "runtime_export_bundle",
            "release_notes",
            "deployment_safety_contract",
            "deployment_readiness_proof",
            "portfolio_handoff_summary",
            "packaging_audit_bundle",
            "first_controlled_worker_execution_readiness_bridge",
            "deployment_packaging_bridge_only",
            "deployment_packaging_does_not_deploy",
            "deployment_packaging_does_not_call_hosting_api",
            "deployment_packaging_does_not_authorize_execution",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess", "netlify", "vercel", "cloudflare", "firebase", "railway", "render"]
    )

    check_contains(
        errors,
        packaging_path,
        [
            'DEPLOYMENT_PACKAGING_MODULE_VERSION = "1.8.0"',
            "DEPLOYMENT_PACKAGING_STATUS",
            "DEPLOYMENT_PACKAGING_PHASE",
            "canonical_json",
            "sha256_digest",
            "normalize_packaging_label",
            "generate_deployment_packaging_id",
            "make_deployment_artifact_schema",
            "create_portfolio_packaging_manifest",
            "create_runtime_export_bundle",
            "create_release_notes",
            "make_deployment_safety_contract",
            "make_deployment_readiness_proof",
            "create_portfolio_handoff_summary",
            "create_packaging_audit_bundle",
            "create_first_controlled_worker_execution_readiness_bridge",
            "make_deployment_packaging_bundle",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess", "netlify", "vercel", "cloudflare", "firebase", "railway", "render", "github pages", "gh api", "git push", "create_deployment", "deploy", "hosting API"]
    )

    check_contains(
        errors,
        adapter_path,
        [
            'ADAPTER_MODULE_VERSION = "1.8.0"',
            'supports_deployment_packaging_bridge',
            'requires_deployment_safety_contract',
            'deployment_blocked_by_default',
            'hosting_api_calls_allowed',
            'live_deployment_allowed'
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v1.8.0.",
            "Deployment/portfolio packaging bridge added.",
            "deployment artifact schema",
            "portfolio packaging manifest",
            "runtime export bundle",
            "release notes generator",
            "deployment safety contract",
            "deployment readiness proof",
            "packaging audit bundle",
            "portfolio handoff summary",
            "first controlled worker-agent execution readiness bridge",
            "no live UI rendering",
            "no live orchestration",
            "no live worker routing",
            "no real worker hiring",
            "no worker animation",
            "no uncontrolled repo edits",
            "no GitHub API mutation",
            "no patch execution authorization",
            "no live deployment",
            "no hosting API calls",
            "no external service mutation",
            "Station Chief Runtime v1.8.0 adds the Deployment / Portfolio Packaging Bridge without deploying or authorizing execution",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_skeleton_path,
        [
            "Station Chief Runtime upgraded to v1.8.0.",
            "Deployment/portfolio packaging bridge added.",
            "deployment artifact schema",
            "portfolio packaging manifest",
            "runtime export bundle",
            "release notes generator",
            "deployment safety contract",
            "deployment readiness proof",
            "packaging audit bundle",
            "portfolio handoff summary",
            "first controlled worker-agent execution readiness bridge",
            "no live deployment",
            "no hosting API calls",
            "no external service mutation",
            "no deployment execution authorization",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_v18_path,
        [
            "Station Chief Runtime v1.8.0 Report",
            "Station Chief Runtime upgraded to v1.8.0. Locked 175-family baseline preserved. Deployment/portfolio packaging bridge added.",
            "deployment artifact schema",
            "portfolio packaging manifest",
            "runtime export bundle",
            "release notes generator",
            "deployment safety contract",
            "deployment readiness proof",
            "packaging audit bundle",
            "portfolio handoff summary",
            "first controlled worker-agent execution readiness bridge",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no hosting API calls",
            "no external hosting mutation",
            "no live deployment",
            "no direct push",
            "no uncontrolled repo edits",
            "Station Chief Runtime v1.8.0 adds the Deployment / Portfolio Packaging Bridge without deploying or authorizing execution",
            "Next recommended build step",
        ]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "1.8.0", "demo runtime version != 1.8.0")
        require(errors, demo.get("runtime_status") == "deployment_packaging_bridge", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "evidence baseline_preserved must be True")
        require(errors, evidence.get("external_actions_taken") is False, "evidence external_actions_taken must be False")
        require(errors, evidence.get("live_worker_agents_activated") is False, "evidence live_worker_agents_activated must be False")
        require(errors, evidence.get("deployment_packaging_available") is True, "evidence packaging_available True")
        require(errors, evidence.get("deployment_packaging_bridge_only") is True, "evidence bridge_only True")
        require(errors, evidence.get("deployment_packaging_does_not_deploy") is True, "evidence no_deploy True")
        require(errors, evidence.get("deployment_packaging_does_not_call_hosting_api") is True, "evidence no_hosting_api True")
        require(errors, evidence.get("deployment_packaging_does_not_authorize_execution") is True, "evidence no_auth True")
        require(errors, evidence.get("first_controlled_worker_execution_not_yet_active") is True, "evidence execution_not_active True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "1.8.0", "fixture runtime_version != 1.8.0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: {err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: {err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "1.8.0", "adapter_module_version != 1.8.0")
        srp = adapters.get("supported_adapters", {}).get("scoped_repo_patch", {})
        require(errors, srp.get("supports_deployment_packaging_bridge") is True, "scoped_repo_patch supports_deployment_packaging_bridge True")
        require(errors, srp.get("requires_deployment_safety_contract") is True, "scoped_repo_patch requires_deployment_safety_contract True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--deployment-artifact-schema"])
    require(errors, code == 0, f"--deployment-artifact-schema failed: {err}")
    schema = parse_json_output(out, "--deployment-artifact-schema", errors)
    if schema:
        require(errors, schema.get("deployment_artifact_schema_version") == "1.8.0", "schema version mismatch")
        require(errors, schema.get("schema_status") == "PACKAGING_BRIDGE_ONLY", "schema status mismatch")
        req = schema.get("required_sections", [])
        require(errors, "portfolio_packaging_manifest" in req, "portfolio_packaging_manifest missing")
        require(errors, "runtime_export_bundle" in req, "runtime_export_bundle missing")
        require(errors, "release_notes" in req, "release_notes missing")
        require(errors, "deployment_readiness_proof" in req, "deployment_readiness_proof missing")
        require(errors, "deployment_safety_contract" in req, "deployment_safety_contract missing")
        require(errors, "packaging_audit_bundle" in req, "packaging_audit_bundle missing")
        require(errors, "portfolio_handoff_summary" in req, "portfolio_handoff_summary missing")
        require(errors, "first_controlled_worker_execution_readiness_bridge" in req, "first_controlled_worker_execution_readiness_bridge missing")
        require(errors, schema.get("baseline_preserved") is True, "baseline preserved mismatch")
        require(errors, schema.get("external_actions_taken") is False, "external actions taken mismatch")
        require(errors, schema.get("deployment_performed") is False, "deployment performed mismatch")
        require(errors, schema.get("hosting_api_called") is False, "hosting api called mismatch")
        require(errors, schema.get("execution_authorized") is False, "execution authorized mismatch")

    # Deployment packaging default
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--deployment-packaging"])
    require(errors, code == 0, f"default deployment-packaging failed: {err}")
    res = parse_json_output(out, "default deployment-packaging", errors)
    if res:
        require(errors, "deployment_packaging_bundle" in res, "deployment_packaging_bundle missing")
        require(errors, "deployment_artifact_schema" in res, "deployment_artifact_schema missing")
        require(errors, "portfolio_packaging_manifest" in res, "portfolio_packaging_manifest missing")
        require(errors, "runtime_export_bundle" in res, "runtime_export_bundle missing")
        require(errors, "release_notes" in res, "release_notes missing")
        require(errors, "deployment_safety_contract" in res, "deployment_safety_contract missing")
        require(errors, "deployment_readiness_proof" in res, "deployment_readiness_proof missing")
        require(errors, "portfolio_handoff_summary" in res, "portfolio_handoff_summary missing")
        require(errors, "packaging_audit_bundle" in res, "packaging_audit_bundle missing")
        require(errors, "first_controlled_worker_execution_readiness_bridge" in res, "first_controlled_worker_execution_readiness_bridge missing")
        
        bundle = res.get("deployment_packaging_bundle", {})
        require(errors, bundle.get("deployment_packaging_bundle_version") == "1.8.0", "bundle version mismatch")
        require(errors, bundle.get("deployment_packaging_status") == "PACKAGING_BRIDGE_ONLY", "packaging status mismatch")
        
        safety = res.get("deployment_safety_contract", {})
        require(errors, safety.get("contract_status") == "DEPLOYMENT_BLOCKED_BY_DEFAULT", "safety status mismatch")
        require(errors, safety.get("deployment_allowed_now") is False, "deployment_allowed_now mismatch")
        
        proof = res.get("deployment_readiness_proof", {})
        require(errors, proof.get("proof_status") == "READY_FOR_REVIEW_PACKAGING", "proof status mismatch")
        
        summary = res.get("portfolio_handoff_summary", {})
        require(errors, summary.get("handoff_status") == "READY_FOR_PORTFOLIO_REVIEW", "handoff status mismatch")
        
        require(errors, res.get("evidence", {}).get("external_actions_taken") is False, "external actions taken True")
        require(errors, res.get("evidence", {}).get("deployment_packaging_does_not_deploy") is True, "evidence no_deploy mismatch")

    # Deployment packaging command for next layer
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build first controlled worker-agent execution release", "--deployment-packaging"])
    require(errors, code == 0, f"next layer command failed: {err}")
    res = parse_json_output(out, "next layer command", errors)
    if res:
        bridge = res.get("first_controlled_worker_execution_readiness_bridge", {})
        require(errors, bridge.get("next_layer") == "First Controlled Worker-Agent Execution Release", "next_layer mismatch")
        require(errors, bridge.get("ready_for_first_controlled_worker_execution_release") is True, "bridge ready mismatch")

    # Write deployment packaging
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-deployment-packaging", str(td_path / "dp")
        ])
        require(errors, code == 0, f"write dp failed: {err}")
        write_res = parse_json_output(out, "write dp", errors)
        if write_res:
            require(errors, "deployment_packaging_write_summary" in write_res, "summary missing")
            summ = write_res["deployment_packaging_write_summary"]
            dpdir = Path(summ.get("deployment_packaging_dir", ""))
            require(errors, dpdir.exists(), "dp dir missing")
            
            fw = summ.get("files_written", [])
            expected = [
                "deployment_packaging_bundle.json", "deployment_artifact_schema.json",
                "portfolio_packaging_manifest.json", "runtime_export_bundle.json",
                "release_notes.json", "deployment_safety_contract.json",
                "deployment_readiness_proof.json", "portfolio_handoff_summary.json",
                "packaging_audit_bundle.json", "first_controlled_worker_execution_readiness_bridge.json",
                "deployment_packaging_manifest.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in files_written")
                
            manifest = json.loads((dpdir / "deployment_packaging_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "1.8.0", "manifest version mismatch")
            require(errors, manifest.get("status") == "PACKAGING_BRIDGE_ONLY", "manifest status mismatch")

    # Artifact writing with registry and deployment packaging
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--deployment-packaging"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v1-8-check-please-"), "run_id format mismatch")
            
            fw = art_sum.get("files_written", [])
            expected_v18 = [
                "deployment_packaging_bundle.json", "deployment_artifact_schema.json",
                "portfolio_packaging_manifest.json", "runtime_export_bundle.json",
                "release_notes.json", "deployment_safety_contract.json",
                "deployment_readiness_proof.json", "portfolio_handoff_summary.json",
                "packaging_audit_bundle.json", "first_controlled_worker_execution_readiness_bridge.json"
            ]
            for f in expected_v18:
                require(errors, f in fw, f"file {f} not in artifact files_written")

            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v1_8_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "1.8.0", "man version mismatch")
                require(errors, man.get("packaging_audit_bundle") is True, "man bundle True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "1.8.0", "rr version mismatch")

    # Regression behavior
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--stable-release-manifest"])
    require(errors, code == 0, f"stable manifest failed: {err}")
    res = parse_json_output(out, "stable manifest", errors)
    if res:
        require(errors, res.get("runtime_version") == "1.8.0", "manifest version mismatch")

def main():
    print("Running validate_station_chief_runtime_v1_8.py...")
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
        
    print("PASS: Station Chief Runtime v1.8 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v1.8 runtime files.")

if __name__ == "__main__":
    main()

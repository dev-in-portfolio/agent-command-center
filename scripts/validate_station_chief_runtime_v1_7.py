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
        "10_runtime/station_chief_github_patch_hardening.py",
        "09_exports/station_chief_runtime_skeleton_report.md",
        "09_exports/station_chief_runtime_v1_7_report.md",
        "scripts/validate_station_chief_runtime_v1_7.py",
    ]
    for rel_path in required:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Required file missing: {rel_path}")

def validate_source_files(errors: list[str]) -> None:
    runtime_path = REPO_ROOT / "10_runtime/station_chief_runtime.py"
    adapter_path = REPO_ROOT / "10_runtime/station_chief_adapters.py"
    hardening_path = REPO_ROOT / "10_runtime/station_chief_github_patch_hardening.py"
    readme_path = REPO_ROOT / "10_runtime/station_chief_runtime_readme.md"
    report_skeleton_path = REPO_ROOT / "09_exports/station_chief_runtime_skeleton_report.md"
    report_v17_path = REPO_ROOT / "09_exports/station_chief_runtime_v1_7_report.md"

    check_contains(
        errors,
        runtime_path,
        [
            'STATION_CHIEF_RUNTIME_VERSION = "1.7.0"',
            "attach_github_patch_hardening",
            "write_github_patch_hardening",
            "--patch-hardening-schema",
            "--github-patch-hardening",
            "--write-github-patch-hardening",
            "--hardening-patch-root",
            "--hardening-allowed-patch-file",
            "--hardening-patch-content",
            "--hardening-original-content",
            "--hardening-changed-file",
            "github_patch_hardening_bundle",
            "patch_hardening_audit_bundle",
            "patch_hardening_schema",
            "protected_path_policy",
            "patch_root_validation",
            "patch_preview_diff_contract",
            "patch_digest_manifest",
            "patch_rollback_preview",
            "changed_file_proof_hardening",
            "human_approval_chain_binding",
            "patch_execution_readiness_score",
            "deployment_packaging_readiness_bridge",
            "github_patch_hardening_contract_only",
            "github_patch_hardening_does_not_apply_patches",
            "github_patch_hardening_does_not_call_github_api",
            "github_patch_hardening_does_not_authorize_execution",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        hardening_path,
        [
            'GITHUB_PATCH_HARDENING_MODULE_VERSION = "1.7.0"',
            "GITHUB_PATCH_HARDENING_STATUS",
            "GITHUB_PATCH_HARDENING_PHASE",
            "canonical_json",
            "sha256_digest",
            "normalize_patch_label",
            "generate_patch_hardening_id",
            "create_patch_hardening_schema",
            "create_protected_path_policy",
            "is_path_protected",
            "create_patch_root_validation",
            "create_patch_preview_diff_contract",
            "create_patch_digest_manifest",
            "create_patch_rollback_preview",
            "create_changed_file_proof_hardening",
            "create_human_approval_chain_binding",
            "create_patch_execution_readiness_score",
            "create_patch_hardening_audit_bundle",
            "create_deployment_packaging_readiness_bridge",
            "create_github_patch_hardening_bundle",
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess", "github.Github", "GraphQL", "gh api", "git push", "create_commit", "update_ref", "create_pull_request"]
    )

    check_contains(
        errors,
        adapter_path,
        [
            'ADAPTER_MODULE_VERSION = "1.7.0"',
            'supports_github_patch_hardening',
            'requires_patch_hardening_review',
            'requires_changed_file_proof',
            'requires_patch_digest_manifest',
            'requires_rollback_preview',
            'requires_human_approval_chain_binding'
        ],
        exclude=["requests", "urllib.request", "os.system", "pip install", "npm install", "API key", "import subprocess"]
    )

    check_contains(
        errors,
        readme_path,
        [
            "Station Chief Runtime upgraded to v1.7.0.",
            "GitHub patch application hardening added.",
            "patch hardening schema",
            "protected path policy expansion",
            "stricter patch-root validation",
            "patch preview diff contract",
            "patch digest manifest",
            "patch rollback preview",
            "changed-file proof hardening",
            "human approval chain binding",
            "patch execution readiness scoring",
            "patch hardening audit bundle",
            "deployment/portfolio packaging readiness bridge",
            "no live UI rendering",
            "no live orchestration",
            "no live worker routing",
            "no real worker hiring",
            "no worker animation",
            "no uncontrolled repo edits",
            "no GitHub API mutation",
            "no patch execution authorization",
            "Station Chief Runtime v1.7.0 adds GitHub Patch Application Hardening without applying patches or authorizing execution",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_skeleton_path,
        [
            "Station Chief Runtime upgraded to v1.7.0.",
            "GitHub patch application hardening added.",
            "patch hardening schema",
            "protected path policy expansion",
            "stricter patch-root validation",
            "patch preview diff contract",
            "patch digest manifest",
            "patch rollback preview",
            "changed-file proof hardening",
            "human approval chain binding",
            "patch execution readiness scoring",
            "patch hardening audit bundle",
            "deployment/portfolio packaging readiness bridge",
            "no uncontrolled repo edits",
            "no GitHub API mutation",
            "no patch execution authorization",
        ],
        exclude=["Explain that", "Include:", "List:", "Write:"]
    )

    check_contains(
        errors,
        report_v17_path,
        [
            "Station Chief Runtime v1.7.0 Report",
            "Station Chief Runtime upgraded to v1.7.0. Locked 175-family baseline preserved. GitHub patch application hardening added.",
            "patch hardening schema",
            "protected path policy expansion",
            "stricter patch-root validation",
            "patch preview diff contract",
            "patch digest manifest",
            "patch rollback preview",
            "changed-file proof hardening",
            "human approval chain binding",
            "patch execution readiness scoring",
            "patch hardening audit bundle",
            "deployment/portfolio packaging readiness bridge",
            "no baseline mutation",
            "no Devinization overlay mutation",
            "no live API calls",
            "no GitHub API mutation",
            "no direct push",
            "no uncontrolled repo edits",
            "Station Chief Runtime v1.7.0 adds GitHub Patch Application Hardening without applying patches or authorizing execution",
            "Next recommended build step",
        ]
    )

def validate_commands_and_behavior(errors: list[str]) -> None:
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--demo"])
    require(errors, code == 0, f"--demo failed: {err}")
    demo = parse_json_output(out, "--demo", errors)
    if demo:
        require(errors, demo.get("station_chief_runtime_version") == "1.7.0", "demo runtime version != 1.7.0")
        require(errors, demo.get("runtime_status") == "github_patch_hardening", "demo runtime_status mismatch")
        require(errors, demo.get("release_status") == "STABLE_LOCKED", "demo release_status mismatch")
        require(errors, demo.get("command_type") == "verification", "demo command_type mismatch")
        evidence = demo.get("evidence", {})
        require(errors, evidence.get("baseline_preserved") is True, "evidence baseline_preserved must be True")
        require(errors, evidence.get("external_actions_taken") is False, "evidence external_actions_taken must be False")
        require(errors, evidence.get("live_worker_agents_activated") is False, "evidence live_worker_agents_activated must be False")
        require(errors, evidence.get("github_patch_hardening_available") is True, "evidence hardening_available True")
        require(errors, evidence.get("github_patch_hardening_contract_only") is True, "evidence contract_only True")
        require(errors, evidence.get("github_patch_hardening_does_not_apply_patches") is True, "evidence no_patches True")
        require(errors, evidence.get("github_patch_hardening_does_not_call_github_api") is True, "evidence no_github_api True")
        require(errors, evidence.get("github_patch_hardening_does_not_authorize_execution") is True, "evidence no_auth True")
        require(errors, evidence.get("deployment_packaging_bridge_not_yet_active") is True, "evidence packaging_bridge_not_active True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--fixture-test"])
    require(errors, code == 0, f"--fixture-test failed: {err}")
    fixture = parse_json_output(out, "--fixture-test", errors)
    if fixture:
        require(errors, fixture.get("fixture_test_status") == "PASS", "fixture_test_status != PASS")
        require(errors, fixture.get("runtime_version") == "1.7.0", "fixture runtime_version != 1.7.0")

    code, out, err = run_command(["python3", "10_runtime/station_chief_fixture_tests.py"])
    require(errors, code == 0, f"fixture runner failed: {err}")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--list-adapters"])
    require(errors, code == 0, f"--list-adapters failed: {err}")
    adapters = parse_json_output(out, "--list-adapters", errors)
    if adapters:
        require(errors, adapters.get("adapter_module_version") == "1.7.0", "adapter_module_version != 1.7.0")
        srp = adapters.get("supported_adapters", {}).get("scoped_repo_patch", {})
        require(errors, srp.get("supports_github_patch_hardening") is True, "scoped_repo_patch supports_github_patch_hardening True")
        require(errors, srp.get("requires_patch_hardening_review") is True, "scoped_repo_patch requires_patch_hardening_review True")

    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--patch-hardening-schema"])
    require(errors, code == 0, f"--patch-hardening-schema failed: {err}")
    schema = parse_json_output(out, "--patch-hardening-schema", errors)
    if schema:
        require(errors, schema.get("patch_hardening_schema_version") == "1.7.0", "schema version mismatch")
        require(errors, schema.get("schema_status") == "PATCH_HARDENING_CONTRACT_ONLY", "schema status mismatch")
        req = schema.get("required_sections", [])
        require(errors, "protected_path_policy" in req, "protected_path_policy missing")
        require(errors, "patch_root_validation" in req, "patch_root_validation missing")
        require(errors, "patch_preview_diff_contract" in req, "patch_preview_diff_contract missing")
        require(errors, "patch_digest_manifest" in req, "patch_digest_manifest missing")
        require(errors, "patch_rollback_preview" in req, "patch_rollback_preview missing")
        require(errors, "changed_file_proof" in req, "changed_file_proof missing")
        require(errors, "human_approval_chain_binding" in req, "human_approval_chain_binding missing")
        require(errors, "patch_execution_readiness_score" in req, "patch_execution_readiness_score missing")
        require(errors, schema.get("baseline_preserved") is True, "baseline preserved mismatch")
        require(errors, schema.get("external_actions_taken") is False, "external actions taken mismatch")
        require(errors, schema.get("repo_patch_applied") is False, "repo patch applied mismatch")
        require(errors, schema.get("github_api_called") is False, "github api called mismatch")
        require(errors, schema.get("execution_authorized") is False, "execution authorized mismatch")

    # GitHub patch hardening default
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "check please", "--github-patch-hardening"])
    require(errors, code == 0, f"default github-patch-hardening failed: {err}")
    res = parse_json_output(out, "default github-patch-hardening", errors)
    if res:
        require(errors, "github_patch_hardening_bundle" in res, "github_patch_hardening_bundle missing")
        require(errors, "patch_hardening_audit_bundle" in res, "patch_hardening_audit_bundle missing")
        require(errors, "patch_hardening_schema" in res, "patch_hardening_schema missing")
        require(errors, "protected_path_policy" in res, "protected_path_policy missing")
        require(errors, "patch_root_validation" in res, "patch_root_validation missing")
        require(errors, "patch_preview_diff_contract" in res, "patch_preview_diff_contract missing")
        require(errors, "patch_digest_manifest" in res, "patch_digest_manifest missing")
        require(errors, "patch_rollback_preview" in res, "patch_rollback_preview missing")
        require(errors, "changed_file_proof_hardening" in res, "changed_file_proof_hardening missing")
        require(errors, "human_approval_chain_binding" in res, "human_approval_chain_binding missing")
        require(errors, "patch_execution_readiness_score" in res, "patch_execution_readiness_score missing")
        require(errors, "deployment_packaging_readiness_bridge" in res, "deployment_packaging_readiness_bridge missing")
        
        bundle = res.get("github_patch_hardening_bundle", {})
        require(errors, bundle.get("github_patch_hardening_bundle_version") == "1.7.0", "bundle version mismatch")
        require(errors, bundle.get("patch_hardening_status") == "PATCH_HARDENING_CONTRACT_ONLY", "patch status mismatch")
        
        policy = res.get("protected_path_policy", {})
        require(errors, policy.get("policy_status") == "ACTIVE_CONTRACT", "policy status mismatch")
        
        readiness = res.get("patch_execution_readiness_score", {})
        require(errors, readiness.get("readiness_score", 0) >= 0, "readiness score missing")
        
        bridge = res.get("deployment_packaging_readiness_bridge", {})
        require(errors, bridge.get("next_layer") == "Deployment / Portfolio Packaging Bridge", "next_layer mismatch")
        
        require(errors, res.get("evidence", {}).get("external_actions_taken") is False, "external actions taken True")
        require(errors, res.get("evidence", {}).get("github_patch_hardening_does_not_apply_patches") is True, "evidence no_patches mismatch")

    # GitHub patch hardening with valid preview inputs
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--github-patch-hardening",
        "--hardening-patch-root", "/tmp/patch-root",
        "--hardening-allowed-patch-file", "runtime_patch_preview/station_chief_patch_output.txt",
        "--hardening-patch-content", "hello",
        "--hardening-original-content", "old",
        "--hardening-changed-file", "runtime_patch_preview/station_chief_patch_output.txt"
    ])
    require(errors, code == 0, f"valid hardening review failed: {err}")
    res = parse_json_output(out, "valid hardening review", errors)
    if res:
        val = res.get("patch_root_validation", {})
        require(errors, val.get("validation_status") == "PASS", "validation_status != PASS")
        proof = res.get("changed_file_proof_hardening", {})
        require(errors, proof.get("proof_status") == "PASS", "proof_status != PASS")
        score = res.get("patch_execution_readiness_score", {})
        require(errors, score.get("readiness_score", 0) >= 80, f"readiness_score {score.get('readiness_score')} < 80")

    # GitHub patch hardening blocks protected path
    code, out, err = run_command([
        "python3", "10_runtime/station_chief_runtime.py",
        "--command", "check please",
        "--github-patch-hardening",
        "--hardening-patch-root", "/tmp/patch-root",
        "--hardening-allowed-patch-file", "02_departments/bad.json",
        "--hardening-changed-file", "02_departments/bad.json"
    ])
    require(errors, code == 0, f"blocked hardening review failed: {err}")
    res = parse_json_output(out, "blocked hardening review", errors)
    if res:
        val = res.get("patch_root_validation", {})
        require(errors, val.get("validation_status") == "BLOCKED", "validation_status != BLOCKED")
        proof = res.get("changed_file_proof_hardening", {})
        require(errors, proof.get("proof_status") == "BLOCKED", "proof_status != BLOCKED")
        require(errors, any("02_departments/bad.json" in f for f in proof.get("blocked_files", [])), "02_departments/bad.json not in blocked_files")

    # GitHub patch hardening command for next layer
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--command", "build deployment portfolio packaging bridge", "--github-patch-hardening"])
    require(errors, code == 0, f"next layer command failed: {err}")
    res = parse_json_output(out, "next layer command", errors)
    if res:
        bridge = res.get("deployment_packaging_readiness_bridge", {})
        require(errors, bridge.get("next_layer") == "Deployment / Portfolio Packaging Bridge", "next_layer mismatch")
        require(errors, bridge.get("ready_for_deployment_packaging_bridge") is True, "bridge ready mismatch")

    # Write GitHub patch hardening
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-github-patch-hardening", str(td_path / "ph")
        ])
        require(errors, code == 0, f"write ph failed: {err}")
        write_res = parse_json_output(out, "write ph", errors)
        if write_res:
            require(errors, "github_patch_hardening_write_summary" in write_res, "summary missing")
            summ = write_res["github_patch_hardening_write_summary"]
            phdir = Path(summ.get("github_patch_hardening_dir", ""))
            require(errors, phdir.exists(), "ph dir missing")
            
            fw = summ.get("files_written", [])
            expected = [
                "github_patch_hardening_bundle.json", "patch_hardening_audit_bundle.json",
                "patch_hardening_schema.json", "protected_path_policy.json",
                "patch_root_validation.json", "patch_preview_diff_contract.json",
                "patch_digest_manifest.json", "patch_rollback_preview.json",
                "changed_file_proof_hardening.json", "human_approval_chain_binding.json",
                "patch_execution_readiness_score.json", "deployment_packaging_readiness_bridge.json",
                "github_patch_hardening_manifest.json"
            ]
            for f in expected:
                require(errors, f in fw, f"file {f} not in files_written")
                
            manifest = json.loads((phdir / "github_patch_hardening_manifest.json").read_text())
            require(errors, manifest.get("runtime_version") == "1.7.0", "manifest version mismatch")
            require(errors, manifest.get("status") == "PATCH_HARDENING_CONTRACT_ONLY", "manifest status mismatch")

    # Artifact writing with registry and GitHub patch hardening
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        code, out, err = run_command([
            "python3", "10_runtime/station_chief_runtime.py",
            "--command", "check please",
            "--write-artifacts", str(td_path / "runs"),
            "--registry-dir", str(td_path / "registry"),
            "--github-patch-hardening"
        ])
        require(errors, code == 0, f"artifact write failed: {err}")
        art_res = parse_json_output(out, "artifact write", errors)
        if art_res:
            art_sum = art_res["artifact_write_summary"]
            run_id = art_sum.get("run_id", "")
            require(errors, run_id.startswith("station-chief-v1-7-check-please-"), "run_id format mismatch")
            
            fw = art_sum.get("files_written", [])
            expected_v17 = [
                "github_patch_hardening_bundle.json", "patch_hardening_audit_bundle.json",
                "patch_hardening_schema.json", "protected_path_policy.json",
                "patch_root_validation.json", "patch_preview_diff_contract.json",
                "patch_digest_manifest.json", "patch_rollback_preview.json",
                "changed_file_proof_hardening.json", "human_approval_chain_binding.json",
                "patch_execution_readiness_score.json", "deployment_packaging_readiness_bridge.json"
            ]
            for f in expected_v17:
                require(errors, f in fw, f"file {f} not in artifact files_written")

            art_dir = Path(art_sum.get("artifact_dir"))
            man_path = art_dir / "manifest.json"
            if man_path.exists():
                man = json.loads(man_path.read_text())
                require(errors, man.get("artifact_type") == "station_chief_runtime_v1_7_artifacts", "man artifact_type mismatch")
                require(errors, man.get("runtime_version") == "1.7.0", "man version mismatch")
                require(errors, man.get("patch_hardening_audit_bundle") is True, "man bundle True")

            rr = json.loads((td_path / "registry" / "run_registry.json").read_text())
            require(errors, rr.get("registry_version") == "1.7.0", "rr version mismatch")

    # Regression behavior
    code, out, err = run_command(["python3", "10_runtime/station_chief_runtime.py", "--stable-release-manifest"])
    require(errors, code == 0, f"stable manifest failed: {err}")
    res = parse_json_output(out, "stable manifest", errors)
    if res:
        require(errors, res.get("runtime_version") == "1.7.0", "manifest version mismatch")

def main():
    print("Running validate_station_chief_runtime_v1_7.py...")
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
        
    print("PASS: Station Chief Runtime v1.7 valid.")
    print("Manual scope check required: confirm git diff contains only the allowed Station Chief v1.7 runtime files.")

if __name__ == "__main__":
    main()

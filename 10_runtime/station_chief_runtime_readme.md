# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v1.7.0. Locked 175-family baseline preserved. GitHub patch application hardening added.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, writes deterministic artifacts, supports registry/resume, supports gated sandbox and scoped repo patch operations, supports dry-run/approval/ledger/release-lock flows, supports controlled execution profile expansion, supports a dry-run-only work order executor skeleton, supports worker hiring registry preview, supports department routing runtime preview, supports a multi-agent orchestration sandbox, supports UI/operator console schemas, and now adds GitHub patch application hardening.

## What This Adds
- patch hardening schema
- protected path policy expansion
- stricter patch-root validation
- patch preview diff contract
- patch digest manifest
- patch rollback preview
- changed-file proof hardening
- human approval chain binding
- patch execution readiness scoring
- patch hardening audit bundle
- deployment/portfolio packaging readiness bridge
- GitHub patch hardening artifact writing
- GitHub patch hardening manifest

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not animate all 47,250 worker agents
- Does not hire real worker agents
- Does not execute uncontrolled repo work orders
- Does not execute live work orders
- Does not assign live workers
- Does not route live workers
- Does not perform live orchestration
- Does not render a live UI
- Does not start a server
- Does not call GitHub APIs
- Does not apply uncontrolled repo patches
- Does not push commits
- no live UI rendering
- no live orchestration
- no live worker routing
- no real worker hiring
- no worker animation
- no uncontrolled repo edits
- no GitHub API mutation
- no patch execution authorization
- Does not write to protected baseline or overlay paths
- Does not treat patch hardening artifacts as execution permission
- Does not build deployment/portfolio packaging bridge yet
- Does not claim full Agent Command Center production completion

## Commands

python3 10_runtime/station_chief_runtime.py --demo

python3 10_runtime/station_chief_runtime.py --patch-hardening-schema

python3 10_runtime/station_chief_runtime.py --command "check please" --github-patch-hardening

python3 10_runtime/station_chief_runtime.py --command "build deployment portfolio packaging bridge" --github-patch-hardening

python3 10_runtime/station_chief_runtime.py --command "check please" --github-patch-hardening --hardening-patch-root /tmp/patch-root --hardening-allowed-patch-file runtime_patch_preview/station_chief_patch_output.txt --hardening-changed-file runtime_patch_preview/station_chief_patch_output.txt

python3 10_runtime/station_chief_runtime.py --command "check please" --write-github-patch-hardening /tmp/station_chief_patch_hardening

python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry --github-patch-hardening

python3 10_runtime/station_chief_runtime.py --fixture-test

python3 10_runtime/station_chief_fixture_tests.py

## GitHub Patch Hardening Artifacts

When --write-github-patch-hardening is used, the runtime creates:
- github_patch_hardening_bundle.json
- patch_hardening_audit_bundle.json
- patch_hardening_schema.json
- protected_path_policy.json
- patch_root_validation.json
- patch_preview_diff_contract.json
- patch_digest_manifest.json
- patch_rollback_preview.json
- changed_file_proof_hardening.json
- human_approval_chain_binding.json
- patch_execution_readiness_score.json
- deployment_packaging_readiness_bridge.json
- github_patch_hardening_manifest.json

## Runtime Doctrine

Station Chief Runtime v1.7.0 adds GitHub Patch Application Hardening without applying patches or authorizing execution. It creates patch hardening schemas, protected path policies, stricter patch-root validation records, patch preview diff contracts, patch digest manifests, rollback previews, changed-file proof hardening records, human approval chain bindings, patch execution readiness scores, patch hardening audit bundles, and deployment/portfolio packaging handoff records while preserving the locked 175-family baseline, avoiding live external actions, avoiding uncontrolled repo edits, avoiding GitHub API mutation, avoiding baseline mutation, avoiding Devinization overlay mutation, and avoiding repo file modification.

## Next Recommended Step
Next recommended step: build deployment/portfolio packaging bridge.

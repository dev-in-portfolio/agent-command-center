# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v0.7.0. Locked 175-family baseline preserved.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, optionally writes runtime artifacts, optionally updates a persistent run registry, supports resume-by-run-id lookup, supports controlled no-op adapter simulation, supports human-confirmed sandbox file-operation gates, supports human-approved scoped repo patch planning with changed-file scope enforcement, supports validator-selected execution profiles with repo patch dry-run bundles, and supports approval UX handoff packets with dry-run bundle comparison.

## What This Does
- Loads Family 7 and Devinization Packs 1 through 7
- Confirms overlays exist
- Preserves baseline architecture
- Supports one-command intake
- Supports command classification
- Supports activation-tier selection
- Selects relevant overlays
- Creates command briefs
- Creates non-executing work orders
- Produces deterministic JSON output
- Writes optional runtime artifacts
- Writes optional runtime_index.json
- Writes optional run_registry.json
- Supports resume-by-run-id lookup
- Supports controlled no-op execution adapter simulation
- Supports controlled sandbox file-operation planning
- Supports human-confirmed sandbox file writes
- Supports human-approved scoped repo patch planning
- Supports changed-file scope enforcement
- Supports validator-selected execution profiles
- Supports repo patch dry-run bundles
- Supports dry-run bundle comparison
- Supports approval UX handoff packets
- Supports human approval summaries
- Supports risk summary artifacts
- Supports next-action recommendations
- Blocks unsafe, unconfirmed, non-allowlisted, or forbidden repo patch operations
- Runs deterministic fixture tests
- Supports check please, blueberry pancakes, Square Block Square Hole, Speed Racer, build, route, repair, governance, and final output command types

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not animate all 47,250 worker agents
- Does not execute uncontrolled repo work orders
- Does not write to protected baseline or overlay paths
- Does not build UI yet
- Does not claim production readiness

## Commands
```bash
python3 10_runtime/station_chief_runtime.py --demo
python3 10_runtime/station_chief_runtime.py --command "check please" --json
python3 10_runtime/station_chief_runtime.py --command "build Station Chief runtime skeleton" --brief
python3 10_runtime/station_chief_runtime.py --list-overlays
python3 10_runtime/station_chief_runtime.py --list-adapters
python3 10_runtime/station_chief_runtime.py --list-execution-profiles
python3 10_runtime/station_chief_runtime.py --command "check please" --dry-run-bundle
python3 10_runtime/station_chief_runtime.py --command "check please" --approval-handoff
python3 10_runtime/station_chief_runtime.py --command "check please" --plan-repo-patch --patch-root /tmp/station_chief_patch_root --allowed-patch-file runtime_patch_preview/station_chief_patch_output.txt --dry-run-bundle
python3 10_runtime/station_chief_runtime.py --command "check please" --plan-repo-patch --patch-root /tmp/station_chief_patch_root --allowed-patch-file runtime_patch_preview/station_chief_patch_output.txt --write-dry-run-bundle /tmp/station_chief_dry_runs
python3 10_runtime/station_chief_runtime.py --compare-dry-run-bundles before.json after.json
python3 10_runtime/station_chief_runtime.py --command "check please" --compare-against-dry-run-bundle before.json --approval-handoff
python3 10_runtime/station_chief_runtime.py --command "check please" --plan-repo-patch --patch-root /tmp/station_chief_patch_root --allowed-patch-file runtime_patch_preview/station_chief_patch_output.txt --write-approval-handoff /tmp/station_chief_handoffs
python3 10_runtime/station_chief_runtime.py --command "check please" --execute-repo-patch --patch-root /tmp/station_chief_patch_root --allowed-patch-file runtime_patch_preview/station_chief_patch_output.txt --confirm-patch YES_I_APPROVE_SCOPED_REPO_PATCH
python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry
python3 10_runtime/station_chief_runtime.py --resume-run-id RUN_ID --registry-dir /tmp/station_chief_registry
python3 10_runtime/station_chief_runtime.py --fixture-test
python3 10_runtime/station_chief_fixture_tests.py
```

## Runtime Artifacts
When `--write-artifacts` is used, the runtime creates a deterministic run directory containing:
- run_log.json
- command_brief.json
- work_orders.json
- selected_overlays.json
- evidence.json
- execution_plan.json
- adapter_result.json
- file_operation_plan.json
- execution_gate.json
- file_operation_result.json
- repo_patch_plan.json
- repo_patch_gate.json
- repo_patch_result.json
- changed_file_scope_proof.json
- execution_profile.json
- preflight_gate_record.json
- patch_approval_checklist.json
- execution_readiness_score.json
- dry_run_bundle.json
- dry_run_bundle_comparison.json
- approval_handoff_packet.json
- runtime_index_entry.json
- manifest.json
- full_result.json

When `--write-dry-run-bundle` is used, the runtime creates:
- dry_run_bundle.json
- execution_profile.json
- preflight_gate_record.json
- patch_approval_checklist.json
- execution_readiness_score.json
- repo_patch_preview.diff
- dry_run_manifest.json

When `--write-approval-handoff` is used, the runtime creates:
- approval_handoff_packet.json
- human_approval_summary.json
- risk_summary.json
- next_action_recommendation.json
- dry_run_bundle_comparison.json
- patch_preview.diff
- approval_handoff_manifest.json

When `--registry-dir` is used with `--write-artifacts`, the runtime also writes:
- run_registry.json
- runtime_index.json

## Approval Handoff
Runtime v0.7.0 adds approval UX handoff packets. These packets summarize dry-run readiness, repo patch risk, human approval requirements, patch preview content, comparison status, and next recommended actions before any confirmed scoped repo patch execution.

## Execution Profiles
Runtime v0.7.0 includes execution profiles:
- audit_only
- dry_run_patch
- sandbox_write
- scoped_repo_patch

Execution profiles help the validator and runtime choose safer behavior before any human-approved execution step.

## Runtime Doctrine
The Station Chief runtime keeps the full 175-family command civilization intact while activating only the logic needed for a specific task. Runtime v0.7.0 proves command intake, classification, overlay loading, activation-tier selection, command-brief creation, deterministic artifact output, run registry tracking, resume lookup, controlled no-op adapter behavior, human-confirmed sandbox file-operation gates, human-approved scoped repo patch planning, validator-selected execution profiles, repo patch dry-run bundles, dry-run bundle comparison, and approval UX handoff packets without waking the full workforce as live execution.

## Next Recommended Step
Next recommended step: add approval handoff review UI schema and signed approval records.

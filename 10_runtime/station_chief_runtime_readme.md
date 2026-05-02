# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v1.0.0. Locked 175-family baseline preserved. Stable runtime foundation locked.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, optionally writes runtime artifacts, optionally updates a persistent run registry, supports resume-by-run-id lookup, supports controlled no-op adapter simulation, supports human-confirmed sandbox file-operation gates, supports human-approved scoped repo patch planning with changed-file scope enforcement, supports validator-selected execution profiles with repo patch dry-run bundles, supports approval UX handoff packets with dry-run bundle comparison, supports signed approval records that document human review without executing patches, supports approval ledger indexing with signed approval comparison, and now includes a stable v1.0 release lock.

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
- Supports approval review UI schema
- Supports deterministic signed approval records
- Supports approval record verification
- Supports approval audit manifests
- Supports approval ledger indexing
- Supports signed approval comparison
- Supports approval history lookup
- Supports duplicate approval detection
- Supports stable runtime contract
- Supports stable release manifest
- Supports stable capability inventory
- Supports stable artifact contract
- Supports stable adapter boundary contract
- Supports stable safety doctrine lock
- Supports stable approval flow lock
- Supports stable known limitations record
- Supports stable next-phase handoff
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
- Does not treat signed approval records as automatic execution permission
- Does not treat approval ledgers as automatic execution permission
- Does not treat the v1.0 release lock as automatic execution permission
- Does not build UI yet
- Does not claim full Agent Command Center production completion

## Commands

python3 10_runtime/station_chief_runtime.py --demo

python3 10_runtime/station_chief_runtime.py --command "check please" --json

python3 10_runtime/station_chief_runtime.py --command "build Station Chief runtime skeleton" --brief

python3 10_runtime/station_chief_runtime.py --list-overlays

python3 10_runtime/station_chief_runtime.py --list-adapters

python3 10_runtime/station_chief_runtime.py --list-execution-profiles

python3 10_runtime/station_chief_runtime.py --approval-review-ui-schema

python3 10_runtime/station_chief_runtime.py --stable-release-manifest

python3 10_runtime/station_chief_runtime.py --command "check please" --release-lock

python3 10_runtime/station_chief_runtime.py --command "check please" --write-release-lock /tmp/station_chief_release_locks

python3 10_runtime/station_chief_runtime.py --verify-release-manifest stable_release_manifest.json

python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry --release-lock

python3 10_runtime/station_chief_runtime.py --resume-run-id RUN_ID --registry-dir /tmp/station_chief_registry

python3 10_runtime/station_chief_runtime.py --fixture-test

python3 10_runtime/station_chief_fixture_tests.py

## Runtime Artifacts

When --write-artifacts is used, the runtime creates a deterministic run directory containing the full stable artifact set, including:
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
- approval_review_ui_schema.json
- signed_approval_record.json
- approval_record_verification.json
- approval_record_audit_manifest.json
- approval_record_sources.json
- approval_ledger_bundle.json
- approval_ledger_index.json
- approval_ledger_verification.json
- approval_status_summary.json
- duplicate_approval_signals.json
- approval_ledger_lookup.json
- approval_record_comparison.json
- release_lock_bundle.json
- stable_release_manifest.json
- stable_release_verification.json
- stable_runtime_contract.json
- stable_capability_inventory.json
- stable_artifact_contract.json
- stable_adapter_boundary_contract.json
- stable_safety_doctrine_lock.json
- stable_approval_flow_lock.json
- known_limitations.json
- next_phase_handoff.json
- release_readiness_summary.json
- runtime_index_entry.json
- manifest.json
- full_result.json

When --write-release-lock is used, the runtime creates:
- release_lock_bundle.json
- stable_release_manifest.json
- stable_release_verification.json
- stable_runtime_contract.json
- stable_capability_inventory.json
- stable_artifact_contract.json
- stable_adapter_boundary_contract.json
- stable_safety_doctrine_lock.json
- stable_approval_flow_lock.json
- known_limitations.json
- next_phase_handoff.json
- release_readiness_summary.json
- release_lock_manifest.json

When --registry-dir is used with --write-artifacts, the runtime also writes:
- run_registry.json
- runtime_index.json

## Stable Release Lock

Runtime v1.0.0 is the stable release lock for the Station Chief Runtime foundation. It locks the runtime contract, artifact contract, adapter boundaries, safety doctrine, approval flow, known limitations, release readiness summary, and next-phase handoff. It does not execute repo patches by itself.

## Runtime Doctrine

The Station Chief runtime keeps the full 175-family command civilization intact while activating only the logic needed for a specific task. Runtime v1.0.0 proves command intake, classification, overlay loading, activation-tier selection, command-brief creation, deterministic artifact output, run registry tracking, resume lookup, controlled no-op adapter behavior, human-confirmed sandbox file-operation gates, human-approved scoped repo patch planning, validator-selected execution profiles, repo patch dry-run bundles, approval UX handoff packets, signed approval records, approval ledger indexing, stable release manifest generation, and stable runtime contract locking without waking the full workforce as live execution.

## Next Recommended Step
Next recommended step: begin controlled execution engine and worker hiring layer.

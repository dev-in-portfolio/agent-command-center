# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v1.1.0. Locked 175-family baseline preserved. Controlled execution profile expansion added.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, writes deterministic artifacts, supports registry/resume, supports gated sandbox and scoped repo patch operations, supports dry-run/approval/ledger/release-lock flows, and now adds controlled execution profile expansion as the first layer of the controlled execution engine and worker hiring phase.

## What This Adds
- controlled execution profile catalog
- controlled execution profile selection
- execution permission matrix
- execution mode contract
- blocked-action ledger
- controlled execution preflight contract
- controlled execution readiness summary
- work order executor readiness bridge
- controlled execution artifact writing
- controlled execution manifest

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not animate all 47,250 worker agents (no worker animation)
- Does not hire real worker agents (no real worker hiring)
- Does not execute uncontrolled repo work orders
- Does not write to protected baseline or overlay paths
- Does not treat controlled execution profiles as automatic execution permission
- Does not build the work order executor yet
- Does not build UI yet
- Does not claim full Agent Command Center production completion

## Commands

python3 10_runtime/station_chief_runtime.py --demo

python3 10_runtime/station_chief_runtime.py --list-controlled-execution-profiles

python3 10_runtime/station_chief_runtime.py --command "check please" --controlled-execution

python3 10_runtime/station_chief_runtime.py --command "build work order executor skeleton" --controlled-execution --controlled-execution-profile work_order_preview

python3 10_runtime/station_chief_runtime.py --command "route this task" --controlled-execution --controlled-execution-profile department_routing_preview

python3 10_runtime/station_chief_runtime.py --command "check please" --controlled-execution --attempted-action live_external_api_action

python3 10_runtime/station_chief_runtime.py --command "check please" --write-controlled-execution /tmp/station_chief_controlled_execution

python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry --controlled-execution

python3 10_runtime/station_chief_runtime.py --fixture-test

python3 10_runtime/station_chief_fixture_tests.py

## Controlled Execution Artifacts

When --write-controlled-execution is used, the runtime creates:
- controlled_execution_bundle.json
- controlled_execution_profile_catalog.json
- controlled_execution_selection.json
- execution_permission_matrix.json
- execution_mode_contract.json
- blocked_action_ledger.json
- controlled_execution_preflight_contract.json
- controlled_execution_readiness_summary.json
- work_order_executor_readiness_bridge.json
- controlled_execution_manifest.json

## Runtime Doctrine

Station Chief Runtime v1.1.0 begins the controlled execution engine and worker hiring phase without performing live execution. It expands controlled execution profiles, permission matrices, mode contracts, blocked-action ledgers, preflight contracts, readiness summaries, and work-order-executor handoff records while preserving the locked 175-family baseline, avoiding live external actions, avoiding worker animation, and avoiding real worker hiring.

## Next Recommended Step
Next recommended step: build work order executor skeleton.

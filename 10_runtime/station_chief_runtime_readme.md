# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v1.4.0. Locked 175-family baseline preserved. Department routing runtime preview added.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, writes deterministic artifacts, supports registry/resume, supports gated sandbox and scoped repo patch operations, supports dry-run/approval/ledger/release-lock flows, supports controlled execution profile expansion, supports a dry-run-only work order executor skeleton, supports worker hiring registry preview, and now adds department routing runtime preview.

## What This Adds
- department routing schema
- deterministic route ID generation
- department route candidate generation
- family-to-department routing map
- worker-to-department assignment map
- department routing conflict detector
- department routing dry-run engine
- department routing ledger
- department routing completion proofs
- department routing readiness summary
- multi-agent orchestration readiness bridge
- department routing artifact writing
- department routing manifest

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not animate all 47,250 worker agents
- Does not hire real worker agents
- Does not execute uncontrolled repo work orders
- Does not execute live work orders
- Does not assign live workers
- Does not route live workers (no live worker routing)
- Does not write to protected baseline or overlay paths
- Does not treat department routing previews as real routing
- Does not build the multi-agent orchestration sandbox yet
- Does not build UI yet
- Does not claim full Agent Command Center production completion
- Does not hire real worker agents (no real worker hiring)
- Does not animate all 47,250 worker agents (no worker animation)

## Commands

python3 10_runtime/station_chief_runtime.py --demo

python3 10_runtime/station_chief_runtime.py --department-routing-schema

python3 10_runtime/station_chief_runtime.py --command "check please" --department-routing

python3 10_runtime/station_chief_runtime.py --command "build multi-agent orchestration sandbox" --department-routing

python3 10_runtime/station_chief_runtime.py --command "check please" --write-department-routing /tmp/station_chief_department_routing

python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry --department-routing

python3 10_runtime/station_chief_runtime.py --fixture-test

python3 10_runtime/station_chief_fixture_tests.py

## Department Routing Artifacts

When --write-department-routing is used, the runtime creates:
- department_routing_bundle.json
- department_routing_schema.json
- department_route_candidates.json
- family_to_department_routing_map.json
- worker_to_department_assignment_map.json
- department_routing_conflict_detector.json
- department_routing_dry_run_results.json
- department_routing_ledger.json
- department_routing_completion_proofs.json
- department_routing_readiness_summary.json
- multi_agent_orchestration_readiness_bridge.json
- department_routing_manifest.json

## Runtime Doctrine

Station Chief Runtime v1.4.0 adds the Department Routing Runtime preview without performing live routing or worker animation. It creates department routing schemas, deterministic route IDs, route candidate records, family-to-department maps, worker-to-department assignment maps, conflict detectors, dry-run routing results, routing ledgers, completion proofs, readiness summaries, and multi-agent orchestration handoff records while preserving the locked 175-family baseline, avoiding live external actions, avoiding worker animation, avoiding real worker hiring, avoiding live worker routing, and avoiding repo file modification.

## Next Recommended Step
Next recommended step: build multi-agent orchestration sandbox.

# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v1.3.0. Locked 175-family baseline preserved. Worker hiring registry preview added.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, writes deterministic artifacts, supports registry/resume, supports gated sandbox and scoped repo patch operations, supports dry-run/approval/ledger/release-lock flows, supports controlled execution profile expansion, supports a dry-run-only work order executor skeleton, and now adds a worker hiring registry preview layer.

## What This Adds
- worker role schema
- deterministic worker ID generation
- worker candidate generation from work orders
- worker registry status lifecycle
- worker assignment planning
- worker registry ledger
- worker hiring preview records
- worker hiring readiness summary
- department routing readiness bridge
- worker hiring registry artifact writing
- worker hiring registry manifest

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not animate all 47,250 worker agents (no worker animation)
- Does not hire real worker agents (no real worker hiring)
- Does not execute uncontrolled repo work orders
- Does not execute live work orders (no live work order execution)
- Does not assign live workers (no live worker assignment)
- Does not write to protected baseline or overlay paths
- Does not treat worker hiring registry previews as real hiring
- Does not build the department routing runtime yet
- Does not build UI yet
- Does not claim full Agent Command Center production completion

## Commands

python3 10_runtime/station_chief_runtime.py --demo

python3 10_runtime/station_chief_runtime.py --worker-role-schema

python3 10_runtime/station_chief_runtime.py --command "check please" --worker-hiring-registry

python3 10_runtime/station_chief_runtime.py --command "build department routing runtime" --worker-hiring-registry

python3 10_runtime/station_chief_runtime.py --command "check please" --write-worker-hiring-registry /tmp/station_chief_worker_registry

python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry --worker-hiring-registry

python3 10_runtime/station_chief_runtime.py --fixture-test

python3 10_runtime/station_chief_fixture_tests.py

## Worker Hiring Registry Artifacts

When --write-worker-hiring-registry is used, the runtime creates:
- worker_hiring_registry_bundle.json
- worker_role_schema.json
- worker_candidates.json
- worker_registry_status_lifecycle.json
- worker_assignment_plan.json
- worker_registry_ledger.json
- worker_hiring_preview_records.json
- worker_hiring_readiness_summary.json
- department_routing_readiness_bridge.json
- worker_hiring_registry_manifest.json

## Runtime Doctrine

Station Chief Runtime v1.3.0 adds the Worker Hiring Registry preview without performing real hiring or worker animation. It creates worker role schemas, deterministic worker IDs, worker candidate records, assignment plans, registry ledgers, hiring preview records, readiness summaries, and department-routing handoff records while preserving the locked 175-family baseline, avoiding live external actions, avoiding worker animation, avoiding real worker hiring, and avoiding repo file modification.

## Next Recommended Step
Next recommended step: build department routing runtime.

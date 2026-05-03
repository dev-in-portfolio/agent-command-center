# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v2.4.0. Locked 175-family baseline preserved. Multi-worker sandbox coordination added.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, writes deterministic artifacts, supports registry/resume, supports gated sandbox and scoped repo patch operations, supports dry-run/approval/ledger/release-lock flows, supports controlled execution profile expansion, supports a dry-run-only work order executor skeleton, supports worker hiring registry preview, supports department routing runtime preview, supports a multi-agent orchestration sandbox, supports UI/operator console schemas, supports GitHub patch application hardening, supports a deployment/portfolio packaging bridge, supports first controlled single-worker sandbox execution, supports single-worker tool permission binding, supports live execution telemetry and abort controls, supports post-run audit proof expansion, and now adds multi-worker sandbox coordination.

## What This Adds
- multi-worker sandbox coordination schema
- multi-worker coordination approval gate
- sandbox worker roster
- worker coordination graph
- inter-worker handoff contract
- multi-worker dry-run ledger
- coordination conflict detector
- coordination abort contract
- coordination quarantine contract
- coordination audit proof
- coordination readiness summary
- controlled external tool adapter preview readiness bridge
- multi-worker sandbox coordination artifact writing
- multi-worker sandbox coordination manifest

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not fetch external artifacts
- Does not send external telemetry
- Does not call hosting APIs
- Does not deploy to Netlify, Vercel, Cloudflare, Firebase, Railway, Render, GitHub Pages, or external platforms
- Does not animate all 47,250 worker agents
- Does not hire real worker agents
- Does not start worker processes
- Does not execute uncontrolled repo work orders
- Does not execute arbitrary code
- Does not run shell commands
- Does not execute live external tools
- Does not invoke external tools
- Does not terminate processes
- Does not start background monitoring
- Does not perform actual replay execution
- Does not assign broad live workers
- Does not route live workers
- Does not perform live orchestration
- Does not render a live UI
- Does not start a server
- Does not call GitHub APIs
- Does not apply uncontrolled repo patches
- Does not push commits
- Does not write to protected baseline or overlay paths
- Does not treat multi-worker sandbox coordination as broad execution permission
- Does not build controlled external tool adapter preview yet
- Does not claim full Agent Command Center production completion
- no broad workforce animation
- no external API calls
- no external artifact fetching
- no actual replay execution
- no process termination
- no shell command execution
- no arbitrary code execution
- no repo mutation
- no deployment

## Commands

python3 10_runtime/station_chief_runtime.py --demo

python3 10_runtime/station_chief_runtime.py --multi-worker-coordination-schema

python3 10_runtime/station_chief_runtime.py --command "check please" --multi-worker-sandbox-coordination

python3 10_runtime/station_chief_runtime.py --command "check please" --multi-worker-sandbox-coordination --multi-worker-confirm-token YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION

python3 10_runtime/station_chief_runtime.py --command "build controlled external tool adapter preview" --multi-worker-sandbox-coordination --multi-worker-confirm-token YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION

python3 10_runtime/station_chief_runtime.py --command "check please" --multi-worker-sandbox-coordination --multi-worker-confirm-token YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION --multi-worker-role planner --multi-worker-role verifier --multi-worker-count 2

python3 10_runtime/station_chief_runtime.py --command "check please" --multi-worker-sandbox-coordination --multi-worker-confirm-token YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION --multi-worker-shared-resource same-box --multi-worker-shared-resource same-box

python3 10_runtime/station_chief_runtime.py --command "check please" --write-multi-worker-sandbox-coordination /tmp/station_chief_multi_worker_coordination --multi-worker-confirm-token YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION

python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry --multi-worker-sandbox-coordination --multi-worker-confirm-token YES_I_APPROVE_MULTI_WORKER_SANDBOX_COORDINATION

python3 10_runtime/station_chief_runtime.py --fixture-test

python3 10_runtime/station_chief_fixture_tests.py

## Multi-Worker Sandbox Coordination Artifacts

When --write-multi-worker-sandbox-coordination is used, the runtime creates:
- multi_worker_sandbox_coordination_bundle.json
- multi_worker_sandbox_coordination_schema.json
- multi_worker_coordination_approval_gate.json
- sandbox_worker_roster.json
- worker_coordination_graph.json
- inter_worker_handoff_contract.json
- multi_worker_dry_run_ledger.json
- coordination_conflict_detector.json
- coordination_abort_contract.json
- coordination_quarantine_contract.json
- coordination_audit_proof.json
- coordination_readiness_summary.json
- controlled_external_tool_adapter_preview_readiness_bridge.json
- multi_worker_sandbox_coordination_manifest.json

## Runtime Doctrine

Station Chief Runtime v2.4.0 adds Multi-Worker Sandbox Coordination without full workforce animation, real worker hiring, worker process creation, live routing, live orchestration, external API calls, or broad execution. It creates deterministic sandbox worker rosters, worker coordination graphs, inter-worker handoff contracts, dry-run ledgers, conflict detectors, abort contracts, quarantine contracts, coordination audit proofs, readiness summaries, and controlled external tool adapter preview handoff records while preserving the locked 175-family baseline, avoiding live external actions, avoiding real worker hiring, avoiding worker process starts, avoiding live worker routing, avoiding live orchestration, avoiding shell commands, avoiding arbitrary code execution, avoiding hosting API calls, avoiding live deployment, avoiding uncontrolled repo edits, avoiding baseline mutation, avoiding Devinization overlay mutation, and avoiding repo file modification.

## Next Recommended Step
Next recommended step: build controlled external tool adapter preview.

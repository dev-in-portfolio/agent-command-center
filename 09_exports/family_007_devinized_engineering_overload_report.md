# Family 7 — Devinized Engineering Overload Pack

## Status
Overlay created. Locked baseline preserved.

## Ownership / Attribution

Project owner, system architect, and operating-doctrine author: Devin O’Rourke.

This attribution applies to the Agent Command Center Devinization overlay architecture. The locked 175-family baseline remains preserved; this metadata identifies Devin O’Rourke as owner/architect of the Devinization overlay stack.
## Purpose
This pack turns Engineering & Automation into the runnable-build engine for the Agent Command Center. It defines the specialized engineering crews needed for runtime, tool wiring, command routing, and developer workflows.

## What This Does Not Do
- Does not modify Family 7 baseline files
- Does not alter the 175-family lock
- Does not regenerate exports
- Does not create runtime yet
- Does not build a UI yet

## What This Enables
- Station Chief runtime
- routing/dispatch
- executable prompt templates
- work orders
- tool adapters
- GitHub verification workflows
- local Termux/Android workflows
- deterministic demo mode
- deployment planning
- portfolio packaging

## Devinized Crews

### 7.DV.001 Station Chief Runtime Core Crew
- **Baseline Anchor**: 7.6 Agent Engineering
- **Mission**: Build the runnable Station Chief command agent that receives one user instruction and routes it to the correct family, department, unit, and worker layer.
- **Primary Outputs**: station_chief.py, routing decision schema, command interpretation logs, master dispatch packet

### 7.DV.002 Agent Router & Dispatcher Crew
- **Baseline Anchor**: 7.6 Agent Engineering
- **Mission**: Route tasks from Station Chief into the correct family/department/unit chain.
- **Primary Outputs**: routing table, dispatch plan, target family list, department handoff packet

### 7.DV.003 Work Order Schema Crew
- **Baseline Anchor**: 7.1 Software Engineering
- **Mission**: Define the JSON/Markdown structures that represent work orders, assignments, handoffs, status, and results.
- **Primary Outputs**: work_order.schema.json, run_packet.schema.json, handoff_packet.schema.json, result_packet.schema.json

### 7.DV.004 Prompt Template Engineering Crew
- **Baseline Anchor**: 7.6 Agent Engineering
- **Mission**: Create reusable executable prompts for Station Chief, family chiefs, department chiefs, scribes, auditors, and worker agents.
- **Primary Outputs**: station_chief_prompt.md, department_chief_prompt.md, scribe_prompt.md, auditor_prompt.md, worker_agent_prompt.md

### 7.DV.005 Runtime State & Memory Crew
- **Baseline Anchor**: 7.3 Backend Engineering
- **Mission**: Build the folder/file-based memory layer for runs, logs, checkpoints, outputs, and resumability.
- **Primary Outputs**: runtime/runs/, runtime/logs/, runtime/checkpoints/, runtime/outputs/, runtime/state_index.json

### 7.DV.006 Execution Engine Crew
- **Baseline Anchor**: 7.1 Software Engineering
- **Mission**: Build the core execution loop that receives work orders, runs agent prompts, collects outputs, and returns results.
- **Primary Outputs**: execution_engine.py, agent_runner.py, result_collector.py, execution_log.md

### 7.DV.007 Tool Adapter Crew
- **Baseline Anchor**: 7.8 Tool Integration
- **Mission**: Create adapters for tools, APIs, local scripts, file operations, GitHub operations, browser/search operations, and future MCP connectors.
- **Primary Outputs**: tools/adapters/, tool_manifest.json, adapter_interface.py, tool_permission_notes.md

### 7.DV.008 Git Operations Crew
- **Baseline Anchor**: 7.5 DevOps
- **Mission**: Handle repo commits, diffs, branch checks, validation runs, rollback prompts, GitHub issue/PR workflows, and “check Gemini’s work” workflows.
- **Primary Outputs**: git_checklist.md, commit_audit_report.md, rollback_plan.md, validation_summary.md

### 7.DV.009 Android / Termux Runtime Crew
- **Baseline Anchor**: 7.10 Developer Experience
- **Mission**: Support Android-first Termux/Debian development workflows, local scripts, shell helpers, Codex/Gemini CLI usage, and lightweight local runtime patterns.
- **Primary Outputs**: termux_setup.md, debian_runtime_notes.md, local_agent_launcher.sh, android_dev_workflow.md

### 7.DV.010 API Integration Crew
- **Baseline Anchor**: 7.4 API Engineering
- **Mission**: Design and wire API contracts for external tools, internal endpoints, OpenAI-style model calls, storage APIs, and future service integrations.
- **Primary Outputs**: api_contracts.md, endpoint_map.json, request_response_examples.md, integration_test_plan.md

### 7.DV.011 Frontend Control Room Crew
- **Baseline Anchor**: 7.2 Frontend Engineering
- **Mission**: Build the optional dashboard/control-room interface for viewing families, dispatching tasks, monitoring runs, and reviewing outputs.
- **Primary Outputs**: dashboard_wireframe.md, react_component_plan.md, control_room_routes.json, ui_state_model.json

### 7.DV.012 Backend Service Crew
- **Baseline Anchor**: 7.3 Backend Engineering
- **Mission**: Build backend service routes, local server patterns, storage interfaces, queue handlers, and runtime APIs.
- **Primary Outputs**: backend_service_plan.md, route_map.json, storage_interface.py, queue_handler.py

### 7.DV.013 QA Harness Crew
- **Baseline Anchor**: 7.1 Software Engineering
- **Mission**: Build tests, validators, smoke checks, regression checks, fake-run tests, and deterministic demo validation.
- **Primary Outputs**: test_plan.md, smoke_test.py, regression_checklist.md, demo_run_validation.md

### 7.DV.014 Error Recovery Crew
- **Baseline Anchor**: 7.1 Software Engineering
- **Mission**: Detect failures, propose fixes, create rollback paths, preserve logs, and recover broken runs without losing context.
- **Primary Outputs**: error_report.md, recovery_plan.md, rollback_command_notes.md, failure_pattern_log.md

### 7.DV.015 Security & Permission Crew
- **Baseline Anchor**: 7.8 Tool Integration
- **Mission**: Define permission boundaries, sandbox rules, external-action gates, secret-handling rules, and human confirmation requirements.
- **Primary Outputs**: permission_model.md, sandbox_policy.md, secret_handling_rules.md, human_confirmation_gates.md

### 7.DV.016 Release Management Crew
- **Baseline Anchor**: 7.5 DevOps
- **Mission**: Package releases, create version notes, coordinate deployment checks, tag stable baselines, and prepare production handoffs.
- **Primary Outputs**: release_notes.md, version_manifest.json, deployment_checklist.md, release_audit.md

### 7.DV.017 Local Model Runtime Crew
- **Baseline Anchor**: 7.9 Infrastructure Engineering
- **Mission**: Support local model runtime planning for llama.cpp, small coder models, offline fallback, and resource-aware execution.
- **Primary Outputs**: local_model_runtime_plan.md, model_inventory.md, launch_commands.md, resource_limits_notes.md

### 7.DV.018 Data / RAG Engineering Crew
- **Baseline Anchor**: 7.3 Backend Engineering
- **Mission**: Build retrieval, file indexing, knowledge lookup, vector/RAG planning, source tracking, and evidence-backed output support.
- **Primary Outputs**: retrieval_plan.md, source_index_schema.json, rag_pipeline_notes.md, evidence_trace_format.md

### 7.DV.019 Documentation & Developer Manual Crew
- **Baseline Anchor**: 7.10 Developer Experience
- **Mission**: Write developer docs, operator manuals, setup guides, command references, and plain-English explanation pages.
- **Primary Outputs**: developer_manual.md, operator_manual.md, command_reference.md, setup_guide.md

### 7.DV.020 Portfolio Packaging Crew
- **Baseline Anchor**: 7.10 Developer Experience
- **Mission**: Package the system into portfolio-facing explanations, architecture diagrams, proof assets, demos, and recruiter/client-friendly summaries.
- **Primary Outputs**: case_study.md, architecture_summary.md, demo_script.md, recruiter_friendly_explanation.md

### 7.DV.021 App Factory Crew
- **Baseline Anchor**: 7.1 Software Engineering
- **Mission**: Turn ideas into scoped app builds with requirements, file structure, MVP plan, testing plan, and deployment plan.
- **Primary Outputs**: app_blueprint.md, file_tree_plan.md, mvp_scope.md, build_sequence.md

### 7.DV.022 Refactor & Cleanup Crew
- **Baseline Anchor**: 7.1 Software Engineering
- **Mission**: Clean messy code, reduce duplication, improve naming, separate concerns, and stabilize fragile files without rewriting everything.
- **Primary Outputs**: refactor_plan.md, changed_file_risk_map.md, cleanup_patch_notes.md, before_after_summary.md

### 7.DV.023 Bug Hunt Crew
- **Baseline Anchor**: 7.1 Software Engineering
- **Mission**: Diagnose bugs, trace causes, isolate failing code paths, and propose minimal safe fixes.
- **Primary Outputs**: bug_report.md, root_cause_notes.md, minimal_fix_plan.md, verification_steps.md

### 7.DV.024 Database & Schema Crew
- **Baseline Anchor**: 7.3 Backend Engineering
- **Mission**: Design local JSON, SQLite, Postgres, Supabase, or future database schemas for runtime state and app data.
- **Primary Outputs**: data_schema.json, table_plan.md, migration_notes.md, schema_validation_plan.md

### 7.DV.025 Deployment & Hosting Crew
- **Baseline Anchor**: 7.5 DevOps
- **Mission**: Prepare deployment paths for Netlify, GitHub Pages, local servers, Android-hosted workflows, or other hosting targets.
- **Primary Outputs**: deployment_target_plan.md, hosting_config_notes.md, env_var_checklist.md, post_deploy_test_plan.md

### 7.DV.026 Command-Line Tooling Crew
- **Baseline Anchor**: 7.10 Developer Experience
- **Mission**: Build CLI commands, shell scripts, aliases, launcher commands, and developer shortcuts for running the system quickly.
- **Primary Outputs**: cli_command_map.md, launcher_script.sh, alias_notes.md, command_examples.md

### 7.DV.027 Demo Mode Crew
- **Baseline Anchor**: 7.1 Software Engineering
- **Mission**: Build deterministic demo mode so the system can be tested without paid API keys, external credentials, or live integrations.
- **Primary Outputs**: demo_mode_plan.md, fake_agent_outputs.json, demo_run_script.py, demo_validation_notes.md

### 7.DV.028 Configuration & Environment Crew
- **Baseline Anchor**: 7.5 DevOps
- **Mission**: Manage config files, environment variables, local paths, safe defaults, and no-key fallback behavior.
- **Primary Outputs**: config_schema.json, env_example.md, safe_defaults.md, path_resolution_notes.md

### 7.DV.029 Architecture Diagram Crew
- **Baseline Anchor**: 7.2 Frontend Engineering
- **Mission**: Turn the system architecture into diagrams, maps, command-flow visuals, and explanation graphics.
- **Primary Outputs**: architecture_diagram_spec.md, station_chief_flow.md, command_routing_map.md, portfolio_visual_notes.md

### 7.DV.030 Devin Override / Speed Racer Crew
- **Baseline Anchor**: 7.6 Agent Engineering
- **Mission**: Encode Devin-specific operating preferences for fast execution: minimize repeated explanations, use deterministic demo mode, avoid credential stalls, and drive execution.
- **Primary Outputs**: devin_execution_rules.md, speed_racer_mode.md, credential_fallback_rules.md, minimal_question_policy.md

## Recommended Next Build Step
Next recommended build step: create the Station Chief runtime skeleton using crews 7.DV.001 through 7.DV.006, with deterministic demo mode support from 7.DV.027.

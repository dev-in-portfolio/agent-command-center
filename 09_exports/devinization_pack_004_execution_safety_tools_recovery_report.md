# Devinization Pack 4 — Execution Safety, Tools & Recovery

## Status
Overlay created. Locked 175-family baseline preserved.

## Included Families
58. Tool Operations & External Access
102. Error Recovery, Apology & Repair Systems
125. Integration Testing & End-to-End Validation
126. Agent Observability, Telemetry & Run Analytics
134. External Action Governance
144. Agent Tool Safety, Sandboxing & Permission Firewalls
150. Completion Architecture & Definition of Done

## Purpose
This pack defines how the Agent Command Center executes safely, uses tools responsibly, governs external actions, recovers from errors, validates integrations, tracks run evidence, prevents unsafe actions, and refuses fake completion.

## What This Does Not Do
- Does not modify baseline family files
- Does not alter the 175-family lock
- Does not regenerate exports
- Does not hire or animate worker agents yet
- Does not build runtime yet
- Does not build UI yet

## What This Enables
- safe tool operations
- GitHub verification workflows
- file scope enforcement
- external action permission gates
- credential and secret boundaries
- deterministic demo fallback
- sandbox policy
- dangerous command blocking
- integration testing
- smoke testing
- validator chains
- run telemetry
- cost / credit budget awareness
- error recovery
- rollback planning
- post-repair validation
- definition of done
- changed-file proof
- final report / commit proof
- no-output failure handling

## Devinization Crews
| crew_id | crew_name | family_anchor | mission | primary_outputs |
| --- | --- | --- | --- | --- |
| DV.P4.001 | Tool Capability Registry Crew | 58. Tool Operations & External Access | Maintain a registry of available tools, what each tool can do, what it cannot do, permission requirements, risk level, and expected output evidence. | tool_capability_registry.json, tool_limitations.md, tool_risk_index.json |
| DV.P4.002 | Tool Adapter Boundary Crew | 58. Tool Operations & External Access | Define safe adapter boundaries for file operations, GitHub operations, browser/search operations, local scripts, APIs, and future MCP-style connectors. | tool_adapter_boundary.md, adapter_contracts.json, safe_tool_interface_notes.md |
| DV.P4.003 | GitHub Tool Operations Crew | 58. Tool Operations & External Access | Handle GitHub-specific verification workflows including commit checks, diffs, file scope, status, rollback evidence, and commit-hash reporting. | github_operation_report.md, commit_scope_check.md, changed_file_evidence.txt, commit_hash_record.md |
| DV.P4.004 | File System Operations Crew | 58. Tool Operations & External Access | Control file reads, writes, deletes, generated artifacts, untracked files, scope checks, and file-system cleanup rules. | file_operation_plan.md, allowed_file_list.json, forbidden_file_list.json, untracked_file_report.md |
| DV.P4.005 | External API Access Crew | 58. Tool Operations & External Access | Govern API calls, request/response logging, rate limits, credential boundaries, fallback behavior, and no-key demo-mode alternatives. | api_access_plan.md, request_response_log_schema.json, no_key_fallback_plan.md, rate_limit_notes.md |
| DV.P4.006 | Tool Failure Detection Crew | 58. Tool Operations & External Access | Detect failed, partial, unavailable, misleading, or stale tool results and route them into recovery instead of pretending success. | tool_failure_report.md, partial_tool_output_record.json, retry_or_stop_decision.md |
| DV.P4.007 | Error Intake Classification Crew | 102. Error Recovery, Apology & Repair Systems | Classify errors as scope drift, wrong file mutation, validator failure, missing output, tool failure, prompt failure, runtime failure, or user-intent mismatch. | error_intake_record.json, error_type_classification.md, affected_area_summary.md |
| DV.P4.008 | Overreach Detection Crew | 102. Error Recovery, Apology & Repair Systems | Detect when the system changed more than requested, edited forbidden files, expanded scope, normalized content, or “improved” beyond instruction. | overreach_report.md, unauthorized_change_list.json, scope_violation_summary.md |
| DV.P4.009 | Rollback Plan Crew | 102. Error Recovery, Apology & Repair Systems | Create safe rollback, revert, or cleanup plans that isolate the bad change without damaging valid work. | rollback_plan.md, revert_command_notes.md, preserved_valid_work_notes.md |
| DV.P4.010 | Repair Prompt Crew | 102. Error Recovery, Apology & Repair Systems | Generate precise repair prompts that fix only the failed portion, preserve valid work, and enforce allowed-file scope. | repair_prompt.md, allowed_repair_scope.json, repair_success_criteria.md |
| DV.P4.011 | No-Drama Repair Reporting Crew | 102. Error Recovery, Apology & Repair Systems | Report failures and repairs plainly without fake certainty, over-apologizing, burying the problem, or using apology as a substitute for correction. | repair_status_report.md, failure_summary.md, honest_next_step.md |
| DV.P4.012 | Post-Repair Validation Crew | 102. Error Recovery, Apology & Repair Systems | Run or require validation after repair, including validators, changed-file checks, report checks, and confirmation that the original error is fixed. | post_repair_validation.md, repair_validator_results.txt, resolved_error_confirmation.md |
| DV.P4.013 | Integration Test Plan Crew | 125. Integration Testing & End-to-End Validation | Define integration test plans that verify connected pieces work together across prompts, runtime, files, validators, reports, and tool operations. | integration_test_plan.md, integration_test_matrix.json, test_scope_notes.md |
| DV.P4.014 | End-to-End Smoke Test Crew | 125. Integration Testing & End-to-End Validation | Create or run quick smoke tests proving the system can complete the smallest valid workflow from input to output evidence. | smoke_test_plan.md, smoke_test_result.txt, e2e_minimal_path.md |
| DV.P4.015 | Deterministic Demo Test Crew | 125. Integration Testing & End-to-End Validation | Validate workflows with deterministic demo data before using live APIs, paid model calls, credentials, or external actions. | deterministic_demo_test.md, demo_fixture_manifest.json, demo_test_result.txt |
| DV.P4.016 | Regression Test Crew | 125. Integration Testing & End-to-End Validation | Check that new changes do not break prior packs, validators, baseline locks, reports, or already-working runtime behavior. | regression_test_plan.md, regression_results.txt, breakage_risk_report.md |
| DV.P4.017 | Validator Chain Crew | 125. Integration Testing & End-to-End Validation | Define and verify the correct chain of validators for each task, including pack validators, baseline validators, runtime validators, and report validators. | validator_chain.md, validator_result_log.txt, required_validator_map.json |
| DV.P4.018 | Test Evidence Packet Crew | 125. Integration Testing & End-to-End Validation | Bundle test results, validator outputs, run logs, failure notes, changed files, and proof artifacts into a reviewable evidence packet. | test_evidence_packet.md, validator_output_archive.txt, proof_artifact_manifest.json |
| DV.P4.019 | Run Telemetry Crew | 126. Agent Observability, Telemetry & Run Analytics | Track each run’s objective, selected crews, tools used, commands run, outputs created, validators run, errors, and final state. | run_telemetry.json, run_summary.md, selected_crew_log.json |
| DV.P4.020 | Execution Log Crew | 126. Agent Observability, Telemetry & Run Analytics | Maintain readable execution logs that show what happened, in what order, what succeeded, what failed, and what remains. | execution_log.md, ordered_event_log.json, remaining_work_notes.md |
| DV.P4.021 | Cost / Credit Budget Crew | 126. Agent Observability, Telemetry & Run Analytics | Track and limit expensive model calls, tool calls, retries, long-running sessions, and no-output loops so runtime execution stays useful. | credit_budget_report.md, call_budget.json, no_output_loop_warning.md |
| DV.P4.022 | Model / Tool Call Trace Crew | 126. Agent Observability, Telemetry & Run Analytics | Record which model/tool calls happened, why they were needed, what they returned, and whether the result was used. | model_tool_call_trace.json, call_reason_log.md, call_result_usage_notes.md |
| DV.P4.023 | Performance Bottleneck Crew | 126. Agent Observability, Telemetry & Run Analytics | Identify runtime slowdowns, repeated failures, unnecessary calls, redundant validation, oversized context, and inefficient execution loops. | performance_bottleneck_report.md, runtime_efficiency_notes.md, optimization_without_scope_drift.md |
| DV.P4.024 | Observability Dashboard Crew | 126. Agent Observability, Telemetry & Run Analytics | Summarize active run health, validator health, error health, budget health, output health, and completion readiness. | observability_dashboard.md, run_health_summary.json, completion_readiness_report.md |
| DV.P4.025 | External Action Permission Crew | 134. External Action Governance | Decide whether the system is allowed to perform external actions such as API calls, pushes, deletes, sends, deployments, or irreversible changes. | external_action_permission.md, permission_decision.json, action_risk_notes.md |
| DV.P4.026 | Human Confirmation Gate Crew | 134. External Action Governance | Require human confirmation for risky, irreversible, external, sensitive, or scope-expanding actions. | confirmation_gate_decision.md, human_approval_needed.json, approval_prompt.md |
| DV.P4.027 | Credential / Secret Boundary Crew | 134. External Action Governance | Protect API keys, tokens, secrets, credentials, private data, environment files, and sensitive values from exposure or unsafe use. | credential_boundary_policy.md, secret_handling_report.md, redaction_requirement_notes.md |
| DV.P4.028 | Network / Write Action Gate Crew | 134. External Action Governance | Gate network access, writes, commits, pushes, file deletes, deployments, and external mutations based on task scope and permission level. | network_write_gate.md, allowed_external_actions.json, blocked_external_actions.json |
| DV.P4.029 | External Change Audit Crew | 134. External Action Governance | Audit any external change after it happens, including what changed, where, why, with what proof, and how to revert. | external_change_audit.md, external_change_evidence.json, external_revert_notes.md |
| DV.P4.030 | Safe Fallback / No-Key Crew | 134. External Action Governance | Provide deterministic demo, local-only, no-key, no-credential, or offline fallback paths when live credentials are missing or expensive. | safe_fallback_plan.md, no_key_execution_mode.json, demo_mode_recommendation.md |
| DV.P4.031 | Sandbox Policy Crew | 144. Agent Tool Safety, Sandboxing & Permission Firewalls | Define sandbox levels, allowed directories, allowed commands, blocked commands, safe defaults, and escalation rules. | sandbox_policy.md, sandbox_levels.json, command_permission_map.json |
| DV.P4.032 | Allowed / Forbidden File Guard Crew | 144. Agent Tool Safety, Sandboxing & Permission Firewalls | Enforce allowed and forbidden file scopes before execution, during execution, before commit, and after repair. | file_guard_report.md, allowed_forbidden_file_scope.json, file_scope_violation_alert.md |
| DV.P4.033 | Dangerous Command Blocker Crew | 144. Agent Tool Safety, Sandboxing & Permission Firewalls | Block or escalate dangerous shell commands, destructive file operations, broad deletes, uncontrolled installs, and unsafe network commands. | dangerous_command_alert.md, blocked_command_list.json, safer_command_recommendation.md |
| DV.P4.034 | Scope Drift Runtime Guard Crew | 144. Agent Tool Safety, Sandboxing & Permission Firewalls | Monitor runtime execution for actions, files, goals, or outputs that drift beyond the approved operation brief. | runtime_scope_drift_report.md, unexpected_action_log.json, stop_execution_recommendation.md |
| DV.P4.035 | Data / Secret Leak Prevention Crew | 144. Agent Tool Safety, Sandboxing & Permission Firewalls | Prevent secrets, credentials, private data, hidden tokens, sensitive paths, or unsafe content from being exposed in outputs, logs, commits, or reports. | leak_prevention_report.md, redaction_plan.md, sensitive_output_warning.md |
| DV.P4.036 | Permission Firewall QA Crew | 144. Agent Tool Safety, Sandboxing & Permission Firewalls | Validate that sandbox rules, file guards, command blockers, external gates, and secret boundaries are applied before and after execution. | permission_firewall_qa.md, safety_gate_results.txt, firewall_gap_report.md |
| DV.P4.037 | Definition of Done Crew | 150. Completion Architecture & Definition of Done | Define the completion standard for each task, including objective satisfied, artifacts created, validators passed, scope verified, and report delivered. | definition_of_done.md, task_completion_standard.json, done_done_checklist.md |
| DV.P4.038 | Artifact Requirement Crew | 150. Completion Architecture & Definition of Done | Require every execution task to produce a durable artifact, changed file, diagnostic report, validator result, or blocked-reason artifact. | artifact_requirement.md, artifact_manifest.json, missing_artifact_alert.md |
| DV.P4.039 | Validator Completion Gate Crew | 150. Completion Architecture & Definition of Done | Block completion claims until required validators pass or a valid blocked-reason explanation is produced. | validator_completion_gate.md, validator_pass_fail_summary.txt, blocked_validator_reason.md |
| DV.P4.040 | Changed File Proof Crew | 150. Completion Architecture & Definition of Done | Require repository tasks to provide changed-file lists, staged-file lists, commit diffs, and confirmation that no forbidden files changed. | changed_file_proof.md, changed_files.txt, forbidden_file_check.md |
| DV.P4.041 | Final Report / Commit Proof Crew | 150. Completion Architecture & Definition of Done | Assemble final reports with files created/modified, validators run, pass/fail status, commit hash, scope confirmation, and next step. | final_execution_report.md, commit_proof.md, validator_and_scope_summary.md, next_step_recommendation.md |
| DV.P4.042 | No Output Failure & Blocked Reason Crew | 150. Completion Architecture & Definition of Done | Treat no-output runs as failures unless a clear blocked-reason artifact explains what stopped, what was attempted, and what exact next step is needed. | no_output_failure_report.md, blocked_reason_artifact.md, exact_next_step.md |

## Execution Safety Layers
Layer 1 — Permission Boundary
Layer 2 — Scope Boundary
Layer 3 — Tool Safety Boundary
Layer 4 — Execution Evidence Boundary
Layer 5 — Recovery Boundary
Layer 6 — Completion Boundary

## Operating Doctrine
The Agent Command Center does not treat execution as success just because a tool ran. Execution is only successful when the requested objective is satisfied, scope is preserved, required artifacts exist, validators or justified blocked reasons are present, and the final report provides proof. Safety controls protect the whole command civilization without shrinking the art piece.

## Recommended Next Build Step
Next recommended build step: create Devinization Pack 5 — Quality, Standards & Human Review, then build the Station Chief runtime skeleton after Packs 1, 2, 3, 4, and 5 are validated.

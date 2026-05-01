# Devinization Pack 2 — Runtime Routing & Work Control

## Status
Overlay created. Locked 175-family baseline preserved.

## Ownership / Attribution

Project owner, system architect, and operating-doctrine author: Devin O’Rourke.

This attribution applies to the Agent Command Center Devinization overlay architecture. The locked 175-family baseline remains preserved; this metadata identifies Devin O’Rourke as owner/architect of the Devinization overlay stack.
## Included Families
35. Workflow Control Tower
57. Multi-Agent Orchestration & Swarm Control
127. State Management & Workflow Memory
135. Work Intake, Scoping & Triage
136. Task Decomposition & Work Package Design
137. Department Dependency Graph & Routing Matrix
139. Long-Running Work, Checkpointing & Resumability

## Purpose
This pack defines how one Station Chief command becomes intake, routing, operation brief, work packets, active queue, checkpoints, execution state, and resumable task flow without waking the entire agency as expensive live execution.

## What This Does Not Do
- Does not modify baseline family files
- Does not alter the 175-family lock
- Does not regenerate exports
- Does not hire or animate worker agents yet
- Does not build runtime yet
- Does not build UI yet

## What This Enables
- active work queues
- workflow status tracking
- whole-agency routing scans
- family and department coordination
- task intake and scope boundaries
- work package design
- ownership assignment
- dependency graph routing
- checkpoint planning
- progress state capture
- resumability design
- long-running task governance
- partial output preservation
- no-output failure prevention

## Devinization Crews
| crew_id | crew_name | family_anchor | mission | primary_outputs |
| --- | --- | --- | --- | --- |
| DV.P2.001 | Active Work Queue Crew | 35. Workflow Control Tower | Maintain the active work queue, paused tasks, blocked tasks, next tasks, and review-ready tasks for the Station Chief runtime. | active_work_queue.json, paused_task_register.md, blocked_task_register.md, next_action_list.md |
| DV.P2.002 | Workflow Status Crew | 35. Workflow Control Tower | Track whether each operation is intake, scoped, routed, assigned, executing, blocked, verifying, complete, or archived. | workflow_status_board.json, status_summary.md, operation_state_log.md |
| DV.P2.003 | Blocker Control Crew | 35. Workflow Control Tower | Identify blockers, classify whether they are missing info, tool failure, validator failure, scope conflict, permission issue, or credential issue, and recommend a path forward. | blocker_report.md, blocker_type.json, unblock_plan.md |
| DV.P2.004 | Review Gate Crew | 35. Workflow Control Tower | Decide when work must pause for human review, validator review, auditor review, or final lock review. | review_gate_decision.md, approval_needed_record.json, ready_for_review_packet.md |
| DV.P2.005 | Operation Brief Control Crew | 35. Workflow Control Tower | Ensure every operation has a clear brief before execution: objective, context, scope, constraints, outputs, validators, and stop conditions. | operation_brief.md, stop_conditions.md, required_artifacts.md, validator_plan.md |
| DV.P2.006 | Workflow Continuity Crew | 35. Workflow Control Tower | Preserve continuity across “ok,” “next,” “check please,” interruptions, thread moves, and long gaps without losing task order. | active_task_pointer.json, continuity_notes.md, resumed_context_packet.md |
| DV.P2.007 | Swarm Activation Crew | 57. Multi-Agent Orchestration & Swarm Control | Decide which command layers, family chiefs, department chiefs, or worker crews should become active for a task while preserving whole-agency awareness. | activation_plan.json, selected_agents.md, activation_tier_record.md |
| DV.P2.008 | Family Chief Coordination Crew | 57. Multi-Agent Orchestration & Swarm Control | Coordinate family-level chiefs so relevant families provide routing judgment without turning every family into live execution. | family_chief_brief.md, family_relevance_scores.json, family_coordination_notes.md |
| DV.P2.009 | Department Chief Coordination Crew | 57. Multi-Agent Orchestration & Swarm Control | Coordinate department-level managers, scribes, and auditors for selected families and convert command guidance into assignable work. | department_coordination_packet.md, department_assignment_map.json, scribe_auditor_plan.md |
| DV.P2.010 | Worker Activation Crew | 57. Multi-Agent Orchestration & Swarm Control | Activate only the worker roles needed for execution, with defined task packets, budgets, and reporting requirements. | worker_activation_packet.json, worker_task_cards.md, live_execution_budget.md |
| DV.P2.011 | Parallel Work Coordination Crew | 57. Multi-Agent Orchestration & Swarm Control | Decide which work can run in parallel, which work must be sequential, and which outputs depend on prior steps. | parallel_work_plan.md, sequence_map.json, dependency_warning_notes.md |
| DV.P2.012 | Swarm Containment Crew | 57. Multi-Agent Orchestration & Swarm Control | Prevent uncontrolled agent sprawl, duplicated work, runaway execution, redundant outputs, and pointless model calls. | containment_decision.md, redundant_agent_report.md, live_execution_limit_notes.md |
| DV.P2.013 | Routing Matrix Crew | 137. Department Dependency Graph & Routing Matrix | Maintain the map that translates task types into likely families, departments, overlays, crews, and validators. | routing_matrix.json, task_type_to_family_map.md, route_explanation.md |
| DV.P2.014 | Cross-Department Handoff Crew | 137. Department Dependency Graph & Routing Matrix | Define handoff packets between families/departments so context, outputs, and constraints do not get lost. | handoff_packet.md, handoff_context.json, receiving_department_notes.md |
| DV.P2.015 | Dependency Graph Crew | 137. Department Dependency Graph & Routing Matrix | Represent dependencies between families, departments, crews, outputs, validators, files, tools, and approvals. | dependency_graph.json, dependency_notes.md, prerequisite_map.md |
| DV.P2.016 | Escalation Route Crew | 137. Department Dependency Graph & Routing Matrix | Route unresolved conflicts, blockers, validator failures, tool failures, or scope disputes to the right command/governance layer. | escalation_route.md, escalation_decision.json, escalation_summary.md |
| DV.P2.017 | Routing Conflict Crew | 137. Department Dependency Graph & Routing Matrix | Resolve cases where multiple families could own the work or where ownership is ambiguous. | routing_conflict_report.md, ownership_decision.json, alternate_route_notes.md |
| DV.P2.018 | Dependency Risk Crew | 137. Department Dependency Graph & Routing Matrix | Identify dependency risks before execution, including missing files, missing tools, unknown context, unsafe writes, unavailable credentials, or validator gaps. | dependency_risk_report.md, preflight_warning_list.md, mitigation_plan.md |
| DV.P2.019 | Work Intake Crew | 135. Work Intake, Scoping & Triage | Convert raw user input into a structured intake record with task type, project context, urgency, risk level, and likely next action. | work_intake_record.json, task_type_summary.md, intake_risk_notes.md |
| DV.P2.020 | Scope Boundary Crew | 135. Work Intake, Scoping & Triage | Define exactly what is in scope, out of scope, allowed, forbidden, required, and optional for a task. | scope_boundary.md, allowed_actions.json, forbidden_actions.json |
| DV.P2.021 | Requirement Clarification Crew | 135. Work Intake, Scoping & Triage | Detect missing requirements and decide whether to resolve from context, proceed with assumptions, or ask one necessary question. | requirement_gap_report.md, resolved_assumptions.md, minimal_question.md |
| DV.P2.022 | Work Type Classification Crew | 135. Work Intake, Scoping & Triage | Classify work as question, verification, prompt-writing, build, patch, audit, research, file operation, memory capture, planning, or correction. | work_type_classification.json, action_mode_recommendation.md, verification_or_execution_decision.md |
| DV.P2.023 | Acceptance Criteria Crew | 135. Work Intake, Scoping & Triage | Define the testable conditions that make a task complete, including required artifacts, validators, scope check, and final report. | acceptance_criteria.md, completion_checklist.md, evidence_requirements.md |
| DV.P2.024 | Intake Handoff Crew | 135. Work Intake, Scoping & Triage | Package intake results into a handoff-ready operation packet for decomposition, routing, or execution. | intake_handoff_packet.md, task_context_bundle.json, initial_route_recommendation.md |
| DV.P2.025 | Task Boundary Crew | 136. Task Decomposition & Work Package Design | Convert scope into precise task boundaries so the system does not mix planning, coding, validating, committing, and reporting unless requested. | task_boundary_record.md, phase_split_plan.md, action_boundary_notes.md |
| DV.P2.026 | Work Breakdown Crew | 136. Task Decomposition & Work Package Design | Break the task into major steps, subtasks, deliverables, validators, dependencies, and stop points. | work_breakdown_structure.md, subtask_list.json, deliverable_map.md |
| DV.P2.027 | Work Package Crew | 136. Task Decomposition & Work Package Design | Create assignable work packages with owner, objective, scope, inputs, outputs, budget, validators, and reporting rules. | work_package.json, worker_task_card.md, package_success_criteria.md |
| DV.P2.028 | Ownership Assignment Crew | 136. Task Decomposition & Work Package Design | Assign ownership to family chiefs, department chiefs, overlay crews, workers, scribes, or auditors based on task type and routing matrix. | ownership_assignment.json, responsible_party_notes.md, accountability_map.md |
| DV.P2.029 | Sequencing Logic Crew | 136. Task Decomposition & Work Package Design | Decide the order of work, what must happen first, what can happen in parallel, and when verification should occur. | sequence_plan.md, dependency_order.json, parallelization_notes.md |
| DV.P2.030 | Decomposition QA Crew | 136. Task Decomposition & Work Package Design | Detect missing steps, overlapping steps, vague outputs, impossible task packets, and hidden scope creep before execution. | decomposition_qa_report.md, missing_step_list.md, corrected_work_package.md |
| DV.P2.031 | Checkpoint Planning Crew | 127. State Management & Workflow Memory | Decide where checkpoints should occur before, during, and after a task so work can resume without losing context. | checkpoint_plan.md, checkpoint_triggers.json, save_state_instructions.md |
| DV.P2.032 | Progress State Capture Crew | 127. State Management & Workflow Memory | Capture current state, completed work, pending work, blockers, changed files, validators run, and next action. | progress_state.json, completed_pending_blocked.md, current_run_summary.md |
| DV.P2.033 | Resumability Design Crew | 127. State Management & Workflow Memory | Define how tasks restart after interruption, tool failure, model limit, thread move, or user pause. | resumability_plan.md, resume_context_packet.json, restart_instructions.md |
| DV.P2.034 | Scope Guard Crew | 127. State Management & Workflow Memory | Compare current work against original scope and stop the run if unexpected files, actions, or goals appear. | scope_guard_report.md, unexpected_change_list.md, stop_or_continue_recommendation.md |
| DV.P2.035 | Interruption Handling Crew | 127. State Management & Workflow Memory | Handle user interruptions, task pivots, tool errors, context loss, and message cutoffs while preserving active state. | interruption_record.md, recovery_context.md, paused_state.json |
| DV.P2.036 | Partial Output Crew | 127. State Management & Workflow Memory | Preserve partial outputs as artifacts instead of letting unfinished work disappear or become “no output.” | partial_output_record.md, partial_artifact_manifest.json, completion_gap_notes.md |
| DV.P2.037 | Continuity Bridge Crew | 139. Long-Running Work, Checkpointing & Resumability | Create compact bridge summaries that let future runs continue from prior work without rereading the entire project. | continuity_bridge.md, resume_packet.json, prior_work_summary.md |
| DV.P2.038 | Completion Forecast Crew | 139. Long-Running Work, Checkpointing & Resumability | Estimate remaining work, identify next milestones, flag likely blockers, and recommend whether to split the task. | completion_forecast.md, remaining_work_map.json, split_recommendation.md |
| DV.P2.039 | Long Task Governance Crew | 139. Long-Running Work, Checkpointing & Resumability | Enforce long-task rules: checkpoints, progress reports, output artifacts, stop conditions, validators, and no fake completion. | long_task_governance_report.md, checkpoint_compliance.md, long_task_rules.json |
| DV.P2.040 | Run Log Crew | 139. Long-Running Work, Checkpointing & Resumability | Record run history, commands, decisions, outputs, errors, validators, and continuation notes. | run_log.md, run_event_history.json, decision_log.md |
| DV.P2.041 | Resume Command Crew | 139. Long-Running Work, Checkpointing & Resumability | Generate exact next commands or prompts needed to resume a task from the current checkpoint. | resume_command.md, next_prompt.txt, continuation_instructions.md |
| DV.P2.042 | Resumability Dashboard Crew | 139. Long-Running Work, Checkpointing & Resumability | Summarize resumability health across active tasks, including checkpoint status, blocked items, partial outputs, and next actions. | resumability_dashboard.md, active_checkpoint_index.json, next_action_dashboard.md |

## Operating Doctrine
The Agent Command Center does not shrink the full agency to a tiny task bot. The whole 175-family agency remains available for awareness, routing, governance, memory, and context. This pack defines how the Station Chief turns one command into scoped, routed, checkpointed, resumable work while budgeting only expensive live execution.

## Runtime Activation Tiers
Tier 0 — Passive Whole-Org Awareness
Tier 1 — Council Scan
Tier 2 — Command Brief
Tier 3 — Active Operation
Tier 4 — Audit, Archive & Continuity Lock

## Recommended Next Build Step
Next recommended build step: create Devinization Pack 3 — Prompt, Memory & Context Architecture, then build the Station Chief runtime skeleton after Packs 1, 2, and 3 are validated.


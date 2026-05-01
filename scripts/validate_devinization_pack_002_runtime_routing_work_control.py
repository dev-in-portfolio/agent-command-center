import json
import os
import sys

JSON_PATH = "04_workflow_templates/devinization_pack_002_runtime_routing_work_control.json"
REPORT_PATH = "09_exports/devinization_pack_002_runtime_routing_work_control_report.md"
EXPECTED_FAMILIES = [
    {"family_id": 35, "family_name": "Workflow Control Tower"},
    {"family_id": 57, "family_name": "Multi-Agent Orchestration & Swarm Control"},
    {"family_id": 127, "family_name": "State Management & Workflow Memory"},
    {"family_id": 135, "family_name": "Work Intake, Scoping & Triage"},
    {"family_id": 136, "family_name": "Task Decomposition & Work Package Design"},
    {"family_id": 137, "family_name": "Department Dependency Graph & Routing Matrix"},
    {"family_id": 139, "family_name": "Long-Running Work, Checkpointing & Resumability"},
]
EXPECTED_CREWS = [
    ("DV.P2.001", "Active Work Queue Crew"),
    ("DV.P2.002", "Workflow Status Crew"),
    ("DV.P2.003", "Blocker Control Crew"),
    ("DV.P2.004", "Review Gate Crew"),
    ("DV.P2.005", "Operation Brief Control Crew"),
    ("DV.P2.006", "Workflow Continuity Crew"),
    ("DV.P2.007", "Swarm Activation Crew"),
    ("DV.P2.008", "Family Chief Coordination Crew"),
    ("DV.P2.009", "Department Chief Coordination Crew"),
    ("DV.P2.010", "Worker Activation Crew"),
    ("DV.P2.011", "Parallel Work Coordination Crew"),
    ("DV.P2.012", "Swarm Containment Crew"),
    ("DV.P2.013", "Routing Matrix Crew"),
    ("DV.P2.014", "Cross-Department Handoff Crew"),
    ("DV.P2.015", "Dependency Graph Crew"),
    ("DV.P2.016", "Escalation Route Crew"),
    ("DV.P2.017", "Routing Conflict Crew"),
    ("DV.P2.018", "Dependency Risk Crew"),
    ("DV.P2.019", "Work Intake Crew"),
    ("DV.P2.020", "Scope Boundary Crew"),
    ("DV.P2.021", "Requirement Clarification Crew"),
    ("DV.P2.022", "Work Type Classification Crew"),
    ("DV.P2.023", "Acceptance Criteria Crew"),
    ("DV.P2.024", "Intake Handoff Crew"),
    ("DV.P2.025", "Task Boundary Crew"),
    ("DV.P2.026", "Work Breakdown Crew"),
    ("DV.P2.027", "Work Package Crew"),
    ("DV.P2.028", "Ownership Assignment Crew"),
    ("DV.P2.029", "Sequencing Logic Crew"),
    ("DV.P2.030", "Decomposition QA Crew"),
    ("DV.P2.031", "Checkpoint Planning Crew"),
    ("DV.P2.032", "Progress State Capture Crew"),
    ("DV.P2.033", "Resumability Design Crew"),
    ("DV.P2.034", "Scope Guard Crew"),
    ("DV.P2.035", "Interruption Handling Crew"),
    ("DV.P2.036", "Partial Output Crew"),
    ("DV.P2.037", "Continuity Bridge Crew"),
    ("DV.P2.038", "Completion Forecast Crew"),
    ("DV.P2.039", "Long Task Governance Crew"),
    ("DV.P2.040", "Run Log Crew"),
    ("DV.P2.041", "Resume Command Crew"),
    ("DV.P2.042", "Resumability Dashboard Crew"),
]
EXPECTED_ROLES = [
    "Realist",
    "Overachiever",
    "Dreamer",
    "Timid",
    "Overprotective",
    "Wildcard Intern",
    "Team Lead / Manager",
    "Scribe / Shower of Work",
    "Auditor / Revision Director",
]
REQUIRED_JSON_PHRASES = [
    "Station Chief",
    "runtime routing",
    "work queue",
    "whole agency",
    "selective live deployment",
    "checkpoint",
    "resumability",
    "work packet",
    "operation brief",
    "scope drift",
    "no output",
    "active task pointer",
    "dependency graph",
    "Council Scan",
    "Passive Whole-Org Awareness",
]
REQUIRED_REPORT_PHRASES = [
    "Overlay created. Locked 175-family baseline preserved.",
    "The Agent Command Center does not shrink the full agency to a tiny task bot.",
    "active work queues",
    "checkpoint planning",
    "resumability design",
    "no-output failure prevention",
    "Next recommended build step",
]


def add_error(errors, message):
    errors.append(message)


def main():
    errors = []
    print("Manual scope check required: confirm git diff contains only the three allowed files.")

    if not os.path.exists(JSON_PATH):
        add_error(errors, f"File missing: {JSON_PATH}")
    if not os.path.exists(REPORT_PATH):
        add_error(errors, f"File missing: {REPORT_PATH}")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    if data.get("extension_id") != "devinization_pack_002_runtime_routing_work_control":
        add_error(errors, "JSON: extension_id mismatch")
    if data.get("extension_name") != "Devinization Pack 2 — Runtime Routing & Work Control":
        add_error(errors, "JSON: extension_name mismatch")
    if data.get("mode") != "overlay":
        add_error(errors, "JSON: mode mismatch")
    if data.get("preserves_locked_baseline") is not True:
        add_error(errors, "JSON: preserves_locked_baseline must be true")
    if data.get("baseline_status") != "175-family expansion locked":
        add_error(errors, "JSON: baseline_status mismatch")

    included_families = data.get("included_families", [])
    if len(included_families) != 7:
        add_error(errors, f"JSON: expected 7 included families, found {len(included_families)}")
    if included_families != EXPECTED_FAMILIES:
        add_error(errors, "JSON: included_families mismatch")

    crews = data.get("crews", [])
    if len(crews) != 42:
        add_error(errors, f"JSON: expected 42 crews, found {len(crews)}")

    found_crews = {crew.get("crew_id"): crew.get("crew_name") for crew in crews}
    expected_map = dict(EXPECTED_CREWS)
    for crew_id, crew_name in EXPECTED_CREWS:
        actual_name = found_crews.get(crew_id)
        if actual_name is None:
            add_error(errors, f"JSON: required crew ID {crew_id} missing")
        elif actual_name != crew_name:
            add_error(errors, f"JSON: crew name mismatch for {crew_id}. Expected '{crew_name}', found '{actual_name}'")

    extra_crews = sorted(set(found_crews) - set(expected_map))
    for crew_id in extra_crews:
        add_error(errors, f"JSON: unexpected crew ID {crew_id} present")

    for crew in crews:
        crew_id = crew.get("crew_id", "<missing crew_id>")
        required_fields = [
            "crew_id",
            "crew_name",
            "family_anchor",
            "mission",
            "triggers",
            "primary_outputs",
            "handoff_targets",
            "roles",
        ]
        missing_fields = [field for field in required_fields if field not in crew]
        if missing_fields:
            add_error(errors, f"Crew {crew_id}: missing fields {', '.join(missing_fields)}")
            continue

        roles = crew.get("roles", [])
        if len(roles) != 9:
            add_error(errors, f"Crew {crew_id}: expected 9 roles, found {len(roles)}")
        else:
            for index, expected_role in enumerate(EXPECTED_ROLES):
                role_obj = roles[index]
                expected_role_id = f"{crew_id}.1{chr(ord('A') + index)}"
                if not isinstance(role_obj, dict):
                    add_error(errors, f"Crew {crew_id}: role {index} is not an object")
                    continue
                if role_obj.get("id") != expected_role_id:
                    add_error(errors, f"Crew {crew_id}: role {index} id mismatch")
                if role_obj.get("role") != expected_role:
                    add_error(errors, f"Crew {crew_id}: role {index} name mismatch")

    json_text = json.dumps(data, ensure_ascii=False)
    json_text_lower = json_text.lower()
    for phrase in REQUIRED_JSON_PHRASES:
        if phrase.lower() not in json_text_lower:
            add_error(errors, f"JSON: required phrase '{phrase}' missing")

    with open(REPORT_PATH, "r", encoding="utf-8") as handle:
        report_text = handle.read()
    report_text_lower = report_text.lower()
    for phrase in REQUIRED_REPORT_PHRASES:
        if phrase.lower() not in report_text_lower:
            add_error(errors, f"Report: required phrase '{phrase}' missing")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print("PASS: Devinization Pack 2 Runtime Routing & Work Control valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()

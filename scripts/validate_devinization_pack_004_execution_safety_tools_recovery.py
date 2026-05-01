import json
import os
import sys

JSON_PATH = "04_workflow_templates/devinization_pack_004_execution_safety_tools_recovery.json"
REPORT_PATH = "09_exports/devinization_pack_004_execution_safety_tools_recovery_report.md"
EXPECTED_FAMILIES = [
    {
        "family_id": 58,
        "family_name": "Tool Operations & External Access"
    },
    {
        "family_id": 102,
        "family_name": "Error Recovery, Apology & Repair Systems"
    },
    {
        "family_id": 125,
        "family_name": "Integration Testing & End-to-End Validation"
    },
    {
        "family_id": 126,
        "family_name": "Agent Observability, Telemetry & Run Analytics"
    },
    {
        "family_id": 134,
        "family_name": "External Action Governance"
    },
    {
        "family_id": 144,
        "family_name": "Agent Tool Safety, Sandboxing & Permission Firewalls"
    },
    {
        "family_id": 150,
        "family_name": "Completion Architecture & Definition of Done"
    }
]
EXPECTED_EXECUTION_SAFETY_LAYERS = [
    {
        "layer": 1,
        "name": "Permission Boundary",
        "purpose": "Decide whether the system may answer, inspect, edit, run, commit, push, or perform an external action."
    },
    {
        "layer": 2,
        "name": "Scope Boundary",
        "purpose": "Restrict execution to allowed files, allowed commands, allowed tools, and declared outputs."
    },
    {
        "layer": 3,
        "name": "Tool Safety Boundary",
        "purpose": "Prevent unsafe, irrelevant, expensive, or unauthorized tool calls."
    },
    {
        "layer": 4,
        "name": "Execution Evidence Boundary",
        "purpose": "Require changed-file lists, validator output, run logs, commit hashes, and proof artifacts."
    },
    {
        "layer": 5,
        "name": "Recovery Boundary",
        "purpose": "Detect failures, isolate overreach, repair only the broken area, and validate after repair."
    },
    {
        "layer": 6,
        "name": "Completion Boundary",
        "purpose": "Block fake completion unless required artifacts, validators, reports, and final proof are present."
    }
]
EXPECTED_CREWS = [
    [
        "DV.P4.001",
        "Tool Capability Registry Crew"
    ],
    [
        "DV.P4.002",
        "Tool Adapter Boundary Crew"
    ],
    [
        "DV.P4.003",
        "GitHub Tool Operations Crew"
    ],
    [
        "DV.P4.004",
        "File System Operations Crew"
    ],
    [
        "DV.P4.005",
        "External API Access Crew"
    ],
    [
        "DV.P4.006",
        "Tool Failure Detection Crew"
    ],
    [
        "DV.P4.007",
        "Error Intake Classification Crew"
    ],
    [
        "DV.P4.008",
        "Overreach Detection Crew"
    ],
    [
        "DV.P4.009",
        "Rollback Plan Crew"
    ],
    [
        "DV.P4.010",
        "Repair Prompt Crew"
    ],
    [
        "DV.P4.011",
        "No-Drama Repair Reporting Crew"
    ],
    [
        "DV.P4.012",
        "Post-Repair Validation Crew"
    ],
    [
        "DV.P4.013",
        "Integration Test Plan Crew"
    ],
    [
        "DV.P4.014",
        "End-to-End Smoke Test Crew"
    ],
    [
        "DV.P4.015",
        "Deterministic Demo Test Crew"
    ],
    [
        "DV.P4.016",
        "Regression Test Crew"
    ],
    [
        "DV.P4.017",
        "Validator Chain Crew"
    ],
    [
        "DV.P4.018",
        "Test Evidence Packet Crew"
    ],
    [
        "DV.P4.019",
        "Run Telemetry Crew"
    ],
    [
        "DV.P4.020",
        "Execution Log Crew"
    ],
    [
        "DV.P4.021",
        "Cost / Credit Budget Crew"
    ],
    [
        "DV.P4.022",
        "Model / Tool Call Trace Crew"
    ],
    [
        "DV.P4.023",
        "Performance Bottleneck Crew"
    ],
    [
        "DV.P4.024",
        "Observability Dashboard Crew"
    ],
    [
        "DV.P4.025",
        "External Action Permission Crew"
    ],
    [
        "DV.P4.026",
        "Human Confirmation Gate Crew"
    ],
    [
        "DV.P4.027",
        "Credential / Secret Boundary Crew"
    ],
    [
        "DV.P4.028",
        "Network / Write Action Gate Crew"
    ],
    [
        "DV.P4.029",
        "External Change Audit Crew"
    ],
    [
        "DV.P4.030",
        "Safe Fallback / No-Key Crew"
    ],
    [
        "DV.P4.031",
        "Sandbox Policy Crew"
    ],
    [
        "DV.P4.032",
        "Allowed / Forbidden File Guard Crew"
    ],
    [
        "DV.P4.033",
        "Dangerous Command Blocker Crew"
    ],
    [
        "DV.P4.034",
        "Scope Drift Runtime Guard Crew"
    ],
    [
        "DV.P4.035",
        "Data / Secret Leak Prevention Crew"
    ],
    [
        "DV.P4.036",
        "Permission Firewall QA Crew"
    ],
    [
        "DV.P4.037",
        "Definition of Done Crew"
    ],
    [
        "DV.P4.038",
        "Artifact Requirement Crew"
    ],
    [
        "DV.P4.039",
        "Validator Completion Gate Crew"
    ],
    [
        "DV.P4.040",
        "Changed File Proof Crew"
    ],
    [
        "DV.P4.041",
        "Final Report / Commit Proof Crew"
    ],
    [
        "DV.P4.042",
        "No Output Failure & Blocked Reason Crew"
    ]
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
    "Auditor / Revision Director"
]
REQUIRED_JSON_PHRASES = [
    "safe execution",
    "tool operations",
    "external action",
    "permission",
    "sandbox",
    "GitHub",
    "changed-file",
    "validator results",
    "deterministic demo",
    "credit budget",
    "no output",
    "rollback",
    "repair",
    "secret",
    "credential",
    "scope drift",
    "definition of done",
    "final report",
    "commit proof",
    "done-done"
]
REQUIRED_REPORT_PHRASES = [
    "Overlay created. Locked 175-family baseline preserved.",
    "safe tool operations",
    "external action permission gates",
    "deterministic demo fallback",
    "validator chains",
    "cost / credit budget awareness",
    "changed-file proof",
    "final report / commit proof",
    "no-output failure handling",
    "The Agent Command Center does not treat execution as success just because a tool ran.",
    "Next recommended build step"
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

    if data.get("extension_id") != "devinization_pack_004_execution_safety_tools_recovery":
        add_error(errors, "JSON: extension_id mismatch")
    if data.get("extension_name") != "Devinization Pack 4 — Execution Safety, Tools & Recovery":
        add_error(errors, "JSON: extension_name mismatch")
    if data.get("mode") != "overlay":
        add_error(errors, "JSON: mode mismatch")
    if data.get("preserves_locked_baseline") is not True:
        add_error(errors, "JSON: preserves_locked_baseline must be true")
    if data.get("baseline_status") != "175-family expansion locked":
        add_error(errors, "JSON: baseline_status mismatch")

    if data.get("included_families") != EXPECTED_FAMILIES:
        add_error(errors, "JSON: included_families mismatch")
    if len(data.get("included_families", [])) != 7:
        add_error(errors, f"JSON: expected 7 included families, found {len(data.get('included_families', []))}")

    if data.get("execution_safety_layers") != EXPECTED_EXECUTION_SAFETY_LAYERS:
        add_error(errors, "JSON: execution_safety_layers mismatch")
    if len(data.get("execution_safety_layers", [])) != 6:
        add_error(errors, f"JSON: expected 6 execution safety layers, found {len(data.get('execution_safety_layers', []))}")

    depends_on = data.get("depends_on", [])
    for required in ["family_007_devinized_engineering_overload", "devinization_pack_001_command_brain", "devinization_pack_002_runtime_routing_work_control", "devinization_pack_003_prompt_memory_context_architecture"]:
        if required not in depends_on:
            add_error(errors, f"JSON: depends_on missing {required}")

    crews = data.get("crews", [])
    if len(crews) != 42:
        add_error(errors, f"JSON: expected 42 crews, found {len(crews)}")

    found_crews = {crew.get("crew_id"): crew.get("crew_name") for crew in crews}
    expected_ids = {crew_id for crew_id, _ in EXPECTED_CREWS}
    for crew_id, crew_name in EXPECTED_CREWS:
        actual_name = found_crews.get(crew_id)
        if actual_name is None:
            add_error(errors, f"JSON: required crew ID {crew_id} missing")
        elif actual_name != crew_name:
            add_error(errors, f"JSON: crew name mismatch for {crew_id}. Expected '{crew_name}', found '{actual_name}'")

    required_fields = ["crew_id", "crew_name", "family_anchor", "mission", "triggers", "primary_outputs", "handoff_targets", "roles"]
    for crew in crews:
        crew_id = crew.get("crew_id", "<missing crew_id>")
        missing = [field for field in required_fields if field not in crew]
        if missing:
            add_error(errors, f"Crew {crew_id}: missing fields {', '.join(missing)}")
            continue
        roles = crew.get("roles", [])
        if len(roles) != 9:
            add_error(errors, f"Crew {crew_id}: expected 9 roles, found {len(roles)}")
            continue
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

    json_text_lower = json.dumps(data, ensure_ascii=False).lower()
    for phrase in REQUIRED_JSON_PHRASES:
        if phrase.lower() not in json_text_lower:
            add_error(errors, f"JSON: required phrase '{phrase}' missing")

    with open(REPORT_PATH, "r", encoding="utf-8") as handle:
        report = handle.read().lower()
    for phrase in REQUIRED_REPORT_PHRASES:
        if phrase.lower() not in report:
            add_error(errors, f"Report: required phrase '{phrase}' missing")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print("PASS: Devinization Pack 4 Execution Safety, Tools & Recovery valid.")
    sys.exit(0)

if __name__ == "__main__":
    main()

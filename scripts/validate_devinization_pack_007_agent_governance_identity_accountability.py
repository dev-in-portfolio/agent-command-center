import json
import os
import sys

JSON_PATH = "04_workflow_templates/devinization_pack_007_agent_governance_identity_accountability.json"
REPORT_PATH = "09_exports/devinization_pack_007_agent_governance_identity_accountability_report.md"
EXPECTED_FAMILIES = [
    {
        "family_id": 141,
        "family_name": "Agent Governance Testing & Constitutional Simulation"
    },
    {
        "family_id": 142,
        "family_name": "Agent Identity, Role Clarity & Persona Control"
    },
    {
        "family_id": 149,
        "family_name": "Agent Reputation, Reliability & Trust Scoring"
    },
    {
        "family_id": 174,
        "family_name": "Agent Incident Court"
    }
]
EXPECTED_GOVERNANCE_LAYERS = [
    {
        "layer": 1,
        "name": "Identity & Role Boundary Layer",
        "purpose": "Define each agent’s identity, scope, authority, limits, handoffs, and forbidden behaviors."
    },
    {
        "layer": 2,
        "name": "Persona & Tone Control Layer",
        "purpose": "Keep agent tone, persona, confidence, and behavior aligned with task role and Devin-specific preferences."
    },
    {
        "layer": 3,
        "name": "Governance Simulation Layer",
        "purpose": "Test agent behavior against constitutional rules, strict execution rules, safety constraints, and scope boundaries."
    },
    {
        "layer": 4,
        "name": "Reliability & Trust Layer",
        "purpose": "Track agent performance, mistake patterns, validator pass rates, scope discipline, and proof quality."
    },
    {
        "layer": 5,
        "name": "Incident Intake Layer",
        "purpose": "Capture incidents, failures, overreach, bad outputs, broken scope, missing proof, and user-caught mistakes."
    },
    {
        "layer": 6,
        "name": "Agent Court & Accountability Layer",
        "purpose": "Review incidents, assign responsibility, order repair, preserve evidence, and create prevention rules."
    },
    {
        "layer": 7,
        "name": "Rehabilitation & Learning Layer",
        "purpose": "Convert failures into improved prompts, validators, routing rules, training notes, and future behavior corrections."
    }
]
EXPECTED_CREWS = [
    [
        "DV.P7.001",
        "Governance Test Harness Crew"
    ],
    [
        "DV.P7.002",
        "Constitutional Simulation Crew"
    ],
    [
        "DV.P7.003",
        "Strict Execution Compliance Crew"
    ],
    [
        "DV.P7.004",
        "Proof Requirement Simulation Crew"
    ],
    [
        "DV.P7.005",
        "Scope Discipline Test Crew"
    ],
    [
        "DV.P7.006",
        "Authority Boundary Test Crew"
    ],
    [
        "DV.P7.007",
        "Agent Identity Card Crew"
    ],
    [
        "DV.P7.008",
        "Role Clarity Crew"
    ],
    [
        "DV.P7.009",
        "Authority Declaration Crew"
    ],
    [
        "DV.P7.010",
        "Persona Boundary Crew"
    ],
    [
        "DV.P7.011",
        "Handoff Identity Crew"
    ],
    [
        "DV.P7.012",
        "Persona Alignment Crew"
    ],
    [
        "DV.P7.013",
        "Reliability Metric Crew"
    ],
    [
        "DV.P7.014",
        "Trust Score Crew"
    ],
    [
        "DV.P7.015",
        "Reliability History Crew"
    ],
    [
        "DV.P7.016",
        "Reliability Event Crew"
    ],
    [
        "DV.P7.017",
        "Trust Decay Crew"
    ],
    [
        "DV.P7.018",
        "Trust Recovery Crew"
    ],
    [
        "DV.P7.019",
        "Incident Evidence Crew"
    ],
    [
        "DV.P7.020",
        "Incident Findings Crew"
    ],
    [
        "DV.P7.021",
        "Responsibility Assignment Crew"
    ],
    [
        "DV.P7.022",
        "Repair Order Crew"
    ],
    [
        "DV.P7.023",
        "Incident Archive Crew"
    ],
    [
        "DV.P7.024",
        "Prevention Rule Crew"
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
    "agent identity",
    "role clarity",
    "persona control",
    "governance test",
    "constitutional simulation",
    "strict execution",
    "proof requirement",
    "reliability metric",
    "trust score",
    "trust decay",
    "trust recovery",
    "incident evidence",
    "incident findings",
    "responsibility assignment",
    "repair order",
    "incident archive",
    "prevention rule",
    "agent court",
    "accountability"
]
REQUIRED_REPORT_PHRASES = [
    "Overlay created. Locked 175-family baseline preserved.",
    "agent identity cards",
    "role clarity",
    "authority boundaries",
    "persona control",
    "governance testing",
    "constitutional simulation",
    "reliability metrics",
    "trust scoring",
    "incident evidence packets",
    "responsibility assignment",
    "repair orders",
    "prevention rules",
    "agent court accountability",
    "The Agent Command Center does not treat agents as trustworthy just because they have names, roles, or confident output.",
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

    if data.get("extension_id") != "devinization_pack_007_agent_governance_identity_accountability":
        add_error(errors, "JSON: extension_id mismatch")
    if data.get("extension_name") != "Devinization Pack 7 — Agent Governance, Identity & Accountability":
        add_error(errors, "JSON: extension_name mismatch")
    if data.get("mode") != "overlay":
        add_error(errors, "JSON: mode mismatch")
    if data.get("preserves_locked_baseline") is not True:
        add_error(errors, "JSON: preserves_locked_baseline must be true")
    if data.get("baseline_status") != "175-family expansion locked":
        add_error(errors, "JSON: baseline_status mismatch")

    if data.get("included_families") != EXPECTED_FAMILIES:
        add_error(errors, "JSON: included_families mismatch")
    if len(data.get("included_families", [])) != 4:
        add_error(errors, f"JSON: expected 4 included families, found {len(data.get('included_families', []))}")

    if data.get("governance_layers") != EXPECTED_GOVERNANCE_LAYERS:
        add_error(errors, "JSON: governance_layers mismatch")
    if len(data.get("governance_layers", [])) != 7:
        add_error(errors, f"JSON: expected 7 governance layers, found {len(data.get('governance_layers', []))}")

    depends_on = data.get("depends_on", [])
    for required in ["family_007_devinized_engineering_overload", "devinization_pack_001_command_brain", "devinization_pack_002_runtime_routing_work_control", "devinization_pack_003_prompt_memory_context_architecture", "devinization_pack_004_execution_safety_tools_recovery", "devinization_pack_005_quality_standards_human_review", "devinization_pack_006_output_assembly_delivery_intelligence"]:
        if required not in depends_on:
            add_error(errors, f"JSON: depends_on missing {required}")

    crews = data.get("crews", [])
    if len(crews) != 24:
        add_error(errors, f"JSON: expected 24 crews, found {len(crews)}")

    found_crews = {crew.get("crew_id"): crew.get("crew_name") for crew in crews}
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

    print("PASS: Devinization Pack 7 Agent Governance, Identity & Accountability valid.")
    sys.exit(0)

if __name__ == "__main__":
    main()

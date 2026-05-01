import json
import os
import sys

def main():
    json_path = "04_workflow_templates/devinization_pack_002_runtime_routing_work_control.json"
    report_path = "09_exports/devinization_pack_002_runtime_routing_work_control_report.md"
    errors = []

    if not os.path.exists(json_path):
        errors.append(f"File missing: {json_path}")
    if not os.path.exists(report_path):
        errors.append(f"File missing: {report_path}")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if data.get("extension_id") != "devinization_pack_002_runtime_routing_work_control":
        errors.append("JSON: extension_id mismatch")
    if data.get("extension_name") != "Devinization Pack 2 — Runtime Routing & Work Control":
        errors.append("JSON: extension_name mismatch")
    if data.get("mode") != "overlay":
        errors.append("JSON: mode mismatch")
    if data.get("preserves_locked_baseline") is not True:
        errors.append("JSON: preserves_locked_baseline must be true")
    if data.get("baseline_status") != "175-family expansion locked":
        errors.append("JSON: baseline_status mismatch")
    
    included_families = data.get("included_families", [])
    if len(included_families) != 7:
        errors.append(f"JSON: expected 7 included families, found {len(included_families)}")
    
    expected_family_ids = [35, 57, 127, 135, 136, 137, 139]
    found_family_ids = [f.get("family_id") for f in included_families]
    if sorted(found_family_ids) != sorted(expected_family_ids):
        errors.append(f"JSON: included_families IDs mismatch. Expected {expected_family_ids}")

    crews = data.get("crews", [])
    if len(crews) != 25:
        errors.append(f"JSON: expected 25 crews (checked list), found {len(crews)}")

    required_crew_checks = [
        ("DV.P2.001", "Active Work Queue Crew"),
        ("DV.P2.002", "Workflow Status Crew"),
        ("DV.P2.003", "Blocker Control Crew"),
        ("DV.P2.007", "Swarm Activation Crew"),
        ("DV.P2.008", "Family Chief Coordination Crew"),
        ("DV.P2.009", "Department Chief Coordination Crew"),
        ("DV.P2.012", "Swarm Containment Crew"),
        ("DV.P2.013", "Routing Matrix Crew"),
        ("DV.P2.014", "Cross-Department Handoff Crew"),
        ("DV.P2.015", "Dependency Graph Crew"),
        ("DV.P2.019", "Work Intake Crew"),
        ("DV.P2.020", "Scope Boundary Crew"),
        ("DV.P2.023", "Acceptance Criteria Crew"),
        ("DV.P2.026", "Work Breakdown Crew"),
        ("DV.P2.027", "Work Package Crew"),
        ("DV.P2.028", "Ownership Assignment Crew"),
        ("DV.P2.031", "Checkpoint Planning Crew"),
        ("DV.P2.032", "Progress State Capture Crew"),
        ("DV.P2.033", "Resumability Design Crew"),
        ("DV.P2.034", "Scope Guard Crew"),
        ("DV.P2.036", "Partial Output Crew"),
        ("DV.P2.037", "Continuity Bridge Crew"),
        ("DV.P2.039", "Long Task Governance Crew"),
        ("DV.P2.041", "Resume Command Crew"),
        ("DV.P2.042", "Resumability Dashboard Crew")
    ]
    
    found_crews = {c.get("crew_id"): c.get("crew_name") for c in crews}
    for cid, cname in required_crew_checks:
        if cid not in found_crews:
            errors.append(f"JSON: required crew ID {cid} missing")
        elif found_crews[cid] != cname:
            errors.append(f"JSON: crew name mismatch for {cid}. Expected '{cname}', found '{found_crews[cid]}'")

    expected_roles = [
        "Realist", "Overachiever", "Dreamer", "Timid", "Overprotective",
        "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"
    ]

    for crew in crews:
        cid = crew.get("crew_id")
        roles = crew.get("roles", [])
        if len(roles) != 9:
            errors.append(f"Crew {cid}: expected 9 roles, found {len(roles)}")
        else:
            for i, r in enumerate(roles):
                if not isinstance(r, dict):
                    errors.append(f"Crew {cid}: role {i} is not a dict")
                    continue
                if r.get("role") != expected_roles[i]:
                    errors.append(f"Crew {cid}: role {i} mismatch")

    json_text = json.dumps(data)
    required_json_phrases = [
        "Station Chief", "runtime routing", "work queue", "whole agency", 
        "selective live deployment", "checkpoint", "resumability", "work packet", 
        "operation brief", "scope drift", "no output", "active task pointer", 
        "dependency graph", "Council Scan", "Passive Whole-Org Awareness"
    ]
    for p in required_json_phrases:
        if p.lower() not in json_text.lower():
            errors.append(f"JSON: required phrase '{p}' missing")

    with open(report_path, 'r', encoding='utf-8') as f:
        report = f.read()

    required_report_phrases = [
        "Overlay created. Locked 175-family baseline preserved.",
        "The Agent Command Center does not shrink the full agency to a tiny task bot.",
        "active work queues",
        "checkpoint planning",
        "resumability design",
        "no-output failure prevention",
        "Next recommended build step"
    ]
    for p in required_report_phrases:
        if p.lower() not in report.lower():
            errors.append(f"Report: required phrase '{p}' missing")

    print("Manual scope check required: confirm git diff contains only the three allowed files.")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    else:
        print("PASS: Devinization Pack 2 Runtime Routing & Work Control valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()

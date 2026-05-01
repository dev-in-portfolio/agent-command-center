import json
import os
import sys

def main():
    json_path = "04_workflow_templates/devinization_pack_001_command_brain.json"
    report_path = "09_exports/devinization_pack_001_command_brain_report.md"
    errors = []

    # 1. File existence
    if not os.path.exists(json_path):
        errors.append(f"File missing: {json_path}")
    if not os.path.exists(report_path):
        errors.append(f"File missing: {report_path}")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    # 2. JSON Validation
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if data.get("extension_id") != "devinization_pack_001_command_brain":
        errors.append("JSON: extension_id mismatch")
    if data.get("extension_name") != "Devinization Pack 1 — Command Brain / Devin Operating System":
        errors.append("JSON: extension_name mismatch")
    if data.get("mode") != "overlay":
        errors.append("JSON: mode mismatch")
    if data.get("preserves_locked_baseline") is not True:
        errors.append("JSON: preserves_locked_baseline must be true")
    if data.get("baseline_status") != "175-family expansion locked":
        errors.append("JSON: baseline_status mismatch")
    
    included_families = data.get("included_families", [])
    if len(included_families) != 6:
        errors.append(f"JSON: expected 6 included families, found {len(included_families)}")
    
    expected_family_ids = [1, 100, 104, 105, 106, 140]
    found_family_ids = [f.get("family_id") for f in included_families]
    if sorted(found_family_ids) != sorted(expected_family_ids):
        errors.append(f"JSON: included_families IDs mismatch. Expected {expected_family_ids}")

    crews = data.get("crews", [])
    if len(crews) != 36:
        errors.append(f"JSON: expected 36 crews, found {len(crews)}")

    required_crew_checks = [
        ("DV.P1.001", "Station Chief Command Intake Crew"),
        ("DV.P1.002", "Station Chief Routing Decision Crew"),
        ("DV.P1.003", "Council Scan Crew"),
        ("DV.P1.007", "Constitution Enforcement Crew"),
        ("DV.P1.008", "Baseline Preservation Crew"),
        ("DV.P1.013", "Intent vs Interpretation Crew"),
        ("DV.P1.016", "SIR Error Pattern Crew"),
        ("DV.P1.019", "Preference Capture Crew"),
        ("DV.P1.025", "Command Alias Crew"),
        ("DV.P1.026", "Mode Switchboard Crew"),
        ("DV.P1.028", "Strict Execution Crew"),
        ("DV.P1.029", "Speed Racer Mode Crew"),
        ("DV.P1.030", "Remember-Only Signal Crew"),
        ("DV.P1.031", "Final Rule Arbitration Crew"),
        ("DV.P1.034", "Scope Drift Stopper Crew"),
        ("DV.P1.035", "Final Lock Crew"),
        ("DV.P1.036", "Whole-Agency Preservation Crew")
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
        for key in ["crew_id", "crew_name", "family_anchor", "mission", "triggers", "primary_outputs", "handoff_targets", "roles"]:
            if key not in crew:
                errors.append(f"Crew {cid}: missing key '{key}'")
        
        roles = crew.get("roles", [])
        if len(roles) != 9:
            errors.append(f"Crew {cid}: expected 9 roles, found {len(roles)}")
        else:
            for i, r in enumerate(roles):
                if not isinstance(r, dict):
                    errors.append(f"Crew {cid}: role {i} is not a dict")
                    continue
                if r.get("role") != expected_roles[i]:
                    errors.append(f"Crew {cid}: role {i} name mismatch")
                if not r.get("id", "").startswith(cid):
                    errors.append(f"Crew {cid}: role {i} ID mismatch")

    # Required phrases in JSON
    json_text = json.dumps(data)
    required_json_phrases = [
        "Station Chief", "Devin", "Square Block Square Hole", "Speed Racer", 
        "blueberry pancakes", "check please", "strict execution", "baseline", 
        "overlay", "scope drift", "final boss", "whole agency", 
        "massive command civilization", "selective live deployment"
    ]
    for p in required_json_phrases:
        if p.lower() not in json_text.lower():
            errors.append(f"JSON: required phrase '{p}' missing")

    # 3. Report Validation
    with open(report_path, 'r', encoding='utf-8') as f:
        report = f.read()

    required_report_phrases = [
        "Overlay created. Locked 175-family baseline preserved.",
        "massive command civilization with selective live deployment",
        "Station Chief command interpretation",
        "Speed Racer mode",
        "strict execution mode",
        "final-boss arbitration",
        "Next recommended build step"
    ]
    for p in required_report_phrases:
        if p.lower() not in report.lower():
            errors.append(f"Report: required phrase '{p}' missing")

    # 4. Manual Scope Check Notice
    print("Manual scope check required: confirm git diff contains only the three allowed files.")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    else:
        print("PASS: Devinization Pack 1 Command Brain valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()

import json
import os
import sys
import re

def validate_batch():
    spec_path = "04_workflow_templates/family_expansion_batch_135_144.json"
    with open(spec_path, 'r') as f:
        batch_spec = json.load(f)

    required_strings = [
        "Work Intake, Scoping & Triage",
        "Requirement Clarification",
        "Acceptance Criteria",
        "Task Decomposition & Work Package Design",
        "Work Breakdown Structure",
        "Decomposition QA",
        "Department Dependency Graph & Routing Matrix",
        "Escalation Route Design",
        "Routing Conflict Review",
        "Output Assembly, Synthesis & Final Answer Design",
        "Multi-Source Integration",
        "Citation And Evidence Placement",
        "Long-Running Work, Checkpointing & Resumability",
        "Resumability Design",
        "Continuity Bridge",
        "Final Boss Layer: System-of-Systems Governance",
        "System-of-Systems Intake",
        "Recursive Governance Review",
        "Agent Governance Testing & Constitutional Simulation",
        "Constitutional Scenario Design",
        "Governance Red Teaming",
        "Agent Identity, Role Clarity & Persona Control",
        "Identity Drift Detection",
        "Persona Safety Review",
        "Agent Contracting & Service-Level Agreements",
        "Breach And Remedy Handling",
        "SLA Dashboard",
        "Agent Tool Safety, Sandboxing & Permission Firewalls",
        "Permission Firewall Rules",
        "Sandbox Escape Prevention"
    ]

    errors = []
    
    # Fidelity Check
    spec_content = json.dumps(batch_spec)
    for s in required_strings:
        if s not in spec_content:
            errors.append(f"Prompt fidelity failure: missing string '{s}' in spec.")

    for family_spec in batch_spec:
        family_id_str = family_spec['id']
        family_id_int = int(family_id_str)
        family_name = family_spec['name']
        slug = family_name.lower().replace(" & ", "_and_").replace(" ", "_").replace(",", "").replace("-", "_").replace(":", "")
        
        # Explicit handling for family 140
        if family_id_int == 140:
            family_dir = "02_departments/140_final_boss_layer_system_of_systems_governance"
        else:
            family_dir = os.path.join("02_departments", f"{family_id_str}_{slug}")
        
        family_json_path = os.path.join(family_dir, "family.json")
        if not os.path.exists(family_json_path):
            errors.append(f"Missing file: {family_json_path}")
            continue

        with open(family_json_path, 'r') as f:
            family_json = json.load(f)

        # Structural check: Family ID MUST be an integer
        if not isinstance(family_json['id'], int):
            errors.append(f"ID type error in {family_json_path}: expected int, found {type(family_json['id']).__name__}")

        if str(family_json['id']) != family_id_str:
            errors.append(f"ID mismatch in {family_json_path}: expected {family_id_str}, found {family_json['id']}")
        if family_json['name'] != family_name:
            errors.append(f"Name mismatch in {family_json_path}: expected {family_name}, found {family_json['name']}")
        
        if family_json.get('manager') != f"{family_id_str}.M": errors.append(f"Invalid family manager in {family_id_str}")
        if family_json.get('scribe') != f"{family_id_str}.H": errors.append(f"Invalid family scribe in {family_id_str}")
        if family_json.get('auditor') != f"{family_id_str}.I": errors.append(f"Invalid family auditor in {family_id_str}")

        if len(family_json['departments']) != 10:
            errors.append(f"Department count mismatch in {family_id_str}: expected 10, found {len(family_json['departments'])}")

        for dept in family_json['departments']:
            dept_id = dept['id']
            if dept['manager'] != f"{dept_id}.M": errors.append(f"Invalid manager for dept {dept_id}")
            if dept['scribe'] != f"{dept_id}.H": errors.append(f"Invalid scribe for dept {dept_id}")
            if dept['auditor'] != f"{dept_id}.I": errors.append(f"Invalid auditor for dept {dept_id}")
            
            if len(dept['units']) != 3:
                errors.append(f"Unit count mismatch in dept {dept_id}: expected 3, found {len(dept['units'])}")

            for unit in dept['units']:
                unit_id = unit['id']
                if len(unit['team']) != 9:
                    errors.append(f"Team size mismatch in unit {unit_id}: expected 9, found {len(unit['team'])}")
                
                roles = ["Realist", "Overachiever", "Dreamer", "Timid", "Overprotective", "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"]
                suffixes = ["1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H", "1I"]
                
                for i, member in enumerate(unit['team']):
                    if not isinstance(member, dict):
                        errors.append(f"Team member in unit {unit_id} is not an object: {member}")
                        continue
                    expected_id = f"{unit_id}.{suffixes[i]}"
                    expected_role = roles[i]
                    if member.get('id') != expected_id:
                        errors.append(f"Team member ID mismatch in unit {unit_id}: expected {expected_id}, found {member.get('id')}")
                    if member.get('role') != expected_role:
                        errors.append(f"Team member role mismatch in unit {unit_id}: expected {expected_role}, found {member.get('role')}")

        # README check
        readme_path = os.path.join(family_dir, "README.md")
        if not os.path.exists(readme_path):
            errors.append(f"Missing file: {readme_path}")
        else:
            with open(readme_path, 'r') as f:
                content = f.read()
            if f"# {family_name}" not in content: errors.append(f"README title mismatch in {family_id_str}")
            if "## Departments" not in content: errors.append(f"README missing Departments section in {family_id_str}")
            
            # Check for incorrect formatting patterns
            if re.search(r"### .* \(\d+\.\d+\)", content):
                errors.append(f"README formatting error in {family_id_str}: Found '### Name (ID)' format")
            if re.search(r"- .* \(\d+\.\d+\.\d+\)", content):
                errors.append(f"README formatting error in {family_id_str}: Found '- Name (ID)' format")
            
            # Check for required formatting patterns
            for dept in family_json['departments']:
                expected_heading = f"### {dept['id']} {dept['name']}"
                if expected_heading not in content:
                    errors.append(f"README missing correct dept format in {family_id_str}: '{expected_heading}'")
                for unit in dept['units']:
                    expected_bullet = f"- {unit['id']} {unit['name']}"
                    if expected_bullet not in content:
                        errors.append(f"README missing correct unit format in {family_id_str}: '{expected_bullet}'")

    if errors:
        for error in errors:
            print(error)
        print("FAIL")
        sys.exit(1)
    else:
        print("PASS: Family batch 135-144 expansion valid.")

if __name__ == "__main__":
    validate_batch()

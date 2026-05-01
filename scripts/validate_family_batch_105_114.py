# Family batch 105-114 expansion validator
import json
import os
import sys

def validate_batch():
    spec_path = "04_workflow_templates/family_expansion_batch_105_114.json"
    with open(spec_path, 'r') as f:
        batch_spec = json.load(f)

    required_strings = [
        "User Preference Engine",
        "Preference Conflict Review",
        "Preference Audit Trail",
        "Command Language & Shortcut Systems",
        "Command Variant Recognition",
        "Command Lifecycle Management",
        "Personal Archive, Vaults & Shelving Systems",
        "Vault Structure Design",
        "Personal Archive Map",
        "Client-Facing Asset Factory",
        "Objection Asset Production",
        "Print-Ready Packaging",
        "Agent-Based Business Process Outsourcing",
        "Service-Level Monitoring",
        "BPO Cost Modeling",
        "System Map, Visualization & Architecture Diagrams",
        "Architecture Diagramming",
        "System Legend Design",
        "Knowledge Monetization & Asset Commercialization",
        "Licensing Opportunity Review",
        "Revenue Model Design",
        "Enterprise Knowledge Base & Internal Wiki",
        "Internal Search Optimization",
        "Knowledge Base Governance",
        "Scenario Library & Playbook Systems",
        "Decision Tree Development",
        "Playbook Versioning",
        "Marketplace Intelligence & Commercial Positioning",
        "Go-To-Market Intelligence",
        "Marketplace Dashboard"
    ]

    errors = []
    
    # Fidelity Check
    spec_content = json.dumps(batch_spec)
    for s in required_strings:
        if s not in spec_content:
            errors.append(f"Prompt fidelity failure: missing string '{s}' in spec.")

    for family_spec in batch_spec:
        family_id = family_spec['id']
        family_name = family_spec['name']
        folder_name = family_name.lower().replace(" & ", "_and_").replace(" ", "_").replace(",", "").replace("-", "_")
        family_dir = os.path.join("02_departments", f"{family_id}_{folder_name}")
        
        family_json_path = os.path.join(family_dir, "family.json")
        if not os.path.exists(family_json_path):
            errors.append(f"Missing file: {family_json_path}")
            continue

        with open(family_json_path, 'r') as f:
            family_json = json.load(f)

        if family_json['id'] != family_id:
            errors.append(f"ID mismatch in {family_json_path}: expected {family_id}, found {family_json['id']}")
        if family_json['name'] != family_name:
            errors.append(f"Name mismatch in {family_json_path}: expected {family_name}, found {family_json['name']}")
        
        if family_json.get('manager') != f"{family_id}.M": errors.append(f"Invalid family manager in {family_id}")
        if family_json.get('scribe') != f"{family_id}.H": errors.append(f"Invalid family scribe in {family_id}")
        if family_json.get('auditor') != f"{family_id}.I": errors.append(f"Invalid family auditor in {family_id}")

        if len(family_json['departments']) != 10:
            errors.append(f"Department count mismatch in {family_id}: expected 10, found {len(family_json['departments'])}")

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
                    expected_id = f"{unit_id}.{suffixes[i]}"
                    expected_role = roles[i]
                    if member['id'] != expected_id:
                        errors.append(f"Team member ID mismatch in unit {unit_id}: expected {expected_id}, found {member['id']}")
                    if member['role'] != expected_role:
                        errors.append(f"Team member role mismatch in unit {unit_id}: expected {expected_role}, found {member['role']}")

        # README check
        readme_path = os.path.join(family_dir, "README.md")
        if not os.path.exists(readme_path):
            errors.append(f"Missing file: {readme_path}")
        else:
            with open(readme_path, 'r') as f:
                content = f.read()
            if f"# {family_name}" not in content: errors.append(f"README title mismatch in {family_id}")
            if "## Departments" not in content: errors.append(f"README missing Departments section in {family_id}")

    if errors:
        for error in errors:
            print(error)
        print("FAIL")
        sys.exit(1)
    else:
        print("PASS: Family batch 105-114 expansion valid.")

if __name__ == "__main__":
    validate_batch()


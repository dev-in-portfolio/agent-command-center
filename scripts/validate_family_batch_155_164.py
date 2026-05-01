import json
import os
import sys
import re

def validate_batch():
    spec_path = "04_workflow_templates/family_expansion_batch_155_164.json"
    with open(spec_path, 'r') as f:
        batch_spec = json.load(f)

    required_strings = [
        "Franchise, Replication & Scaling Systems",
        "Replication Playbook",
        "Scaling Risk Review",
        "Licensing & White-Label Operations",
        "White-Label Configuration",
        "Licensing Revenue Tracking",
        "Agent App Store & Plugin Ecosystem",
        "Plugin Compatibility Testing",
        "Compatibility Result Notes",
        "Plugin Security Review",
        "Security Review Notes",
        "Client Portal Operations",
        "Client Document Delivery",
        "Delivery Confirmation Notes",
        "Portal Security Review",
        "Portal Security Notes",
        "Knowledge Graph Visualization Studio",
        "Graph Interaction Design",
        "Interaction Design Notes",
        "Graph Visualization Governance",
        "Governance Record Update",
        "AI Safety Red-Team Lab",
        "Refusal Boundary Testing",
        "Boundary Test Summary",
        "Safety Regression Testing",
        "Regression Result Notes",
        "Prompt Injection Defense Office",
        "Tool-Use Injection Defense",
        "Tool Defense Notes",
        "Data Exfiltration Prevention",
        "Prevention Control Notes",
        "Data Backup & Cold Storage",
        "Cold Storage Classification",
        "Storage Class Decision",
        "Restore Testing",
        "Restore Test Summary",
        "Digital Legacy Planning",
        "Digital Estate Inventory",
        "Estate Inventory Update",
        "Legacy Privacy Review",
        "Legacy Privacy Notes",
        "Reputation Fire Drill Team",
        "Crisis Message Drafting",
        "Crisis Message QA",
        "Fire Drill Execution",
        "Drill Result Notes"
    ]

    errors = []
    
    # Fidelity Check
    spec_content = json.dumps(batch_spec)
    for s in required_strings:
        if s not in spec_content:
            errors.append(f"Prompt fidelity failure: missing string '{s}' in spec.")

    # Unit-level exact corrections
    unit_corrections = {
        "157.3.3": "Compatibility Result Notes",
        "157.5.3": "Security Review Notes",
        "158.4.3": "Delivery Confirmation Notes",
        "158.8.3": "Portal Security Notes",
        "159.5.3": "Interaction Design Notes",
        "159.9.3": "Governance Record Update",
        "160.5.3": "Boundary Test Summary",
        "160.8.3": "Regression Result Notes",
        "161.5.3": "Tool Defense Notes",
        "161.6.3": "Prevention Control Notes",
        "162.3.3": "Storage Class Decision",
        "162.5.3": "Restore Test Summary",
        "163.2.3": "Estate Inventory Update",
        "163.7.3": "Legacy Privacy Notes",
        "164.3.3": "Crisis Message QA",
        "164.8.3": "Drill Result Notes"
    }

    for family_spec in batch_spec:
        family_id_str = family_spec['id']
        family_name = family_spec['name']
        slug = family_name.lower().replace(" & ", "_and_").replace(" ", "_").replace(",", "").replace("-", "_")
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
                if unit_id in unit_corrections:
                    if unit['name'] != unit_corrections[unit_id]:
                        errors.append(f"Unit {unit_id} name mismatch: expected '{unit_corrections[unit_id]}', found '{unit['name']}'")
                
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
        print("PASS: Family batch 155-164 expansion valid.")

if __name__ == "__main__":
    validate_batch()

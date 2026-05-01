import json
import os
import sys

def validate():
    spec_path = "04_workflow_templates/family_expansion_batch_105_114.json"
    if not os.path.exists(spec_path):
        print(f"FAIL: {spec_path} not found")
        sys.exit(1)

    with open(spec_path, "r") as f:
        batch_data = json.load(f)

    # Hardcoded string checks
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

    spec_text = json.dumps(batch_data)
    missing_strings = [s for s in required_strings if s not in spec_text]
    if missing_strings:
        for s in missing_strings:
            print(f"FAIL: Missing required string in spec: {s}")
        sys.exit(1)

    errors = []
    
    for family in batch_data:
        family_id = family["id"]
        family_name = family["name"]
        folder_name = family_name.lower().replace(" ", "_").replace("&", "and").replace(",", "").replace("-", "_")
        family_dir = f"02_departments/{family_id}_{folder_name}"
        
        json_path = os.path.join(family_dir, "family.json")
        readme_path = os.path.join(family_dir, "README.md")
        
        if not os.path.exists(json_path):
            errors.append(f"{json_path} missing")
            continue
            
        with open(json_path, "r") as f:
            data = json.load(f)
            
        if data["id"] != family_id:
            errors.append(f"{json_path} ID mismatch: {data['id']} != {family_id}")
        if data["name"] != family_name:
            errors.append(f"{json_path} Name mismatch: {data['name']} != {family_name}")
            
        if not data["manager"].endswith(".M"): errors.append(f"{json_path} manager invalid")
        if not data["scribe"].endswith(".H"): errors.append(f"{json_path} scribe invalid")
        if not data["auditor"].endswith(".I"): errors.append(f"{json_path} auditor invalid")
        
        if len(data["departments"]) != 10:
            errors.append(f"{json_path} department count mismatch: {len(data['departments'])} != 10")
            
        for dept in data["departments"]:
            dept_id = dept["id"]
            if not dept_id.startswith(family_id + "."): errors.append(f"Dept {dept_id} ID invalid")
            if dept["manager"] != f"{dept_id}.M": errors.append(f"Dept {dept_id} manager invalid")
            if dept["scribe"] != f"{dept_id}.H": errors.append(f"Dept {dept_id} scribe invalid")
            if dept["auditor"] != f"{dept_id}.I": errors.append(f"Dept {dept_id} auditor invalid")
            
            if len(dept["units"]) != 3:
                errors.append(f"Dept {dept_id} unit count mismatch: {len(dept['units'])} != 3")
                
            for unit in dept["units"]:
                unit_id = unit["id"]
                if not unit_id.startswith(dept_id + "."): errors.append(f"Unit {unit_id} ID invalid")
                
                if len(unit["team"]) != 9:
                    errors.append(f"Unit {unit_id} team size mismatch: {len(unit['team'])} != 9")
                    
                roles = ["Realist", "Overachiever", "Dreamer", "Timid", "Overprotective", "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"]
                suffixes = ["1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H", "1I"]
                
                for i, member in enumerate(unit["team"]):
                    if not isinstance(member, dict):
                        errors.append(f"Unit {unit_id} team member {i} is not a dict")
                        continue
                    
                    expected_id = f"{unit_id}.{suffixes[i]}"
                    expected_role = roles[i]
                    
                    if member.get("id") != expected_id:
                        errors.append(f"Unit {unit_id} team member {i} ID mismatch: {member.get('id')} != {expected_id}")
                    if member.get("role") != expected_role:
                        errors.append(f"Unit {unit_id} team member {i} role mismatch: {member.get('role')} != {expected_role}")

        # README check
        if not os.path.exists(readme_path):
            errors.append(f"{readme_path} missing")
        else:
            with open(readme_path, "r") as f:
                content = f.read()
            if f"# {family_name}" not in content: errors.append(f"{readme_path} title missing")
            if "## Departments" not in content: errors.append(f"{readme_path} departments section missing")
            for dept in data["departments"]:
                if f"### {dept['name']} ({dept['id']})" not in content:
                    errors.append(f"{readme_path} missing dept: {dept['name']}")
                for unit in dept["units"]:
                    if f"- {unit['name']} ({unit['id']})" not in content:
                        errors.append(f"{readme_path} missing unit: {unit['name']}")

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        sys.exit(1)
    else:
        print("PASS: Family batch 105-114 expansion valid.")

if __name__ == "__main__":
    validate()

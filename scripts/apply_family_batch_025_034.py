import json
import os

BATCH_FILE = "04_workflow_templates/family_expansion_batch_025_034.json"

def main():
    if not os.path.exists(BATCH_FILE):
        print(f"Error: {BATCH_FILE} not found")
        return
        
    with open(BATCH_FILE, 'r', encoding='utf-8') as f:
        spec = json.load(f)
        
    for family_spec in spec.get("families", []):
        fid = family_spec["id"]
        if not (25 <= fid <= 34):
            continue
            
        folder = family_spec["folder"]
        family_json_path = os.path.join(folder, "family.json")
        readme_path = os.path.join(folder, "README.md")
        
        if not os.path.exists(family_json_path):
            print(f"Error: {family_json_path} not found.")
            continue
            
        with open(family_json_path, 'r', encoding='utf-8') as f:
            family_data = json.load(f)
            
        new_departments = []
        for dept_spec in family_spec.get("departments", []):
            did = dept_spec["id"]
            dname = dept_spec["name"]
            
            new_dept = {
                "id": did,
                "name": dname,
                "manager": f"{did}.M",
                "scribe": f"{did}.H",
                "auditor": f"{did}.I",
                "units": []
            }
            
            for i, uname in enumerate(dept_spec.get("units", []), 1):
                uid = f"{did}.{i}"
                new_unit = {
                    "id": uid,
                    "name": uname,
                    "team": [
                        {"id": f"{uid}.1A", "role": "Realist"},
                        {"id": f"{uid}.1B", "role": "Overachiever"},
                        {"id": f"{uid}.1C", "role": "Dreamer"},
                        {"id": f"{uid}.1D", "role": "Timid"},
                        {"id": f"{uid}.1E", "role": "Overprotective"},
                        {"id": f"{uid}.1F", "role": "Wildcard Intern"},
                        {"id": f"{uid}.1G", "role": "Team Lead / Manager"},
                        {"id": f"{uid}.1H", "role": "Scribe / Shower of Work"},
                        {"id": f"{uid}.1I", "role": "Auditor / Revision Director"}
                    ]
                }
                new_dept["units"].append(new_unit)
                
            new_departments.append(new_dept)
            
        family_data["departments"] = new_departments
        
        with open(family_json_path, 'w', encoding='utf-8') as f:
            json.dump(family_data, f, indent=2)
        print(f"Wrote {family_json_path}")
        
        # Write README.md
        fname = family_spec["name"]
        readme_lines = [
            f"# {fname}",
            "## Purpose",
            f"## Family Manager ({fid}.M)",
            f"## Family Scribe ({fid}.H)",
            f"## Family Auditor ({fid}.I)",
            "## Departments"
        ]
        
        for dept in new_departments:
            readme_lines.append("")
            readme_lines.append(f"### {dept['id']} {dept['name']}")
            for unit in dept["units"]:
                readme_lines.append(f"- {unit['id']} {unit['name']}")
                
        # To ensure the file ends with a newline
        readme_content = "\n".join(readme_lines) + "\n"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"Wrote {readme_path}")

if __name__ == "__main__":
    main()

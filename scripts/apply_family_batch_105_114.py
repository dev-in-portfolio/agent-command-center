import json
import os

def apply_batch():
    spec_path = "04_workflow_templates/family_expansion_batch_105_114.json"
    with open(spec_path, "r") as f:
        batch_data = json.load(f)

    for family in batch_data:
        family_id = family["id"]
        family_name = family["name"]
        
        # Determine folder name
        folder_name = family_name.lower().replace(" ", "_").replace("&", "and").replace(",", "").replace("-", "_")
        family_dir = f"02_departments/{family_id}_{folder_name}"
        
        json_path = os.path.join(family_dir, "family.json")
        readme_path = os.path.join(family_dir, "README.md")
        
        if not os.path.exists(json_path):
            print(f"Skipping {family_id} - {json_path} not found")
            continue

        with open(json_path, "r") as f:
            existing_family = json.load(f)
            
        # Preserve top-level
        new_family = {
            "id": str(existing_family["id"]),
            "name": existing_family["name"],
            "manager": existing_family.get("manager", f"{family_id}.M"),
            "scribe": existing_family.get("scribe", f"{family_id}.H"),
            "auditor": existing_family.get("auditor", f"{family_id}.I"),
            "departments": []
        }
        
        for dept in family["departments"]:
            dept_id = dept["id"]
            new_dept = {
                "id": dept_id,
                "name": dept["name"],
                "manager": f"{dept_id}.M",
                "scribe": f"{dept_id}.H",
                "auditor": f"{dept_id}.I",
                "units": []
            }
            
            for unit in dept["units"]:
                unit_id = unit["id"]
                new_unit = {
                    "id": unit_id,
                    "name": unit["name"],
                    "team": [
                        { "id": f"{unit_id}.1A", "role": "Realist" },
                        { "id": f"{unit_id}.1B", "role": "Overachiever" },
                        { "id": f"{unit_id}.1C", "role": "Dreamer" },
                        { "id": f"{unit_id}.1D", "role": "Timid" },
                        { "id": f"{unit_id}.1E", "role": "Overprotective" },
                        { "id": f"{unit_id}.1F", "role": "Wildcard Intern" },
                        { "id": f"{unit_id}.1G", "role": "Team Lead / Manager" },
                        { "id": f"{unit_id}.1H", "role": "Scribe / Shower of Work" },
                        { "id": f"{unit_id}.1I", "role": "Auditor / Revision Director" }
                    ]
                }
                new_dept["units"].append(new_unit)
            
            new_family["departments"].append(new_dept)
            
        with open(json_path, "w") as f:
            json.dump(new_family, f, indent=2)
        print(f"Wrote {json_path}")
        
        # Write README.md
        readme_content = f"# {family_name}\n\n"
        readme_content += "## Purpose\n\n"
        readme_content += f"## Family Manager ({new_family['manager']})\n\n"
        readme_content += f"## Family Scribe ({new_family['scribe']})\n\n"
        readme_content += f"## Family Auditor ({new_family['auditor']})\n\n"
        readme_content += "## Departments\n"
        
        for dept in new_family["departments"]:
            readme_content += f"\n### {dept['name']} ({dept['id']})\n"
            for unit in dept["units"]:
                readme_content += f"- {unit['name']} ({unit['id']})\n"
        
        with open(readme_path, "w") as f:
            f.write(readme_content)
        print(f"Wrote {readme_path}")

if __name__ == "__main__":
    apply_batch()

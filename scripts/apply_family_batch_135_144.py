import json
import os

def apply_batch():
    spec_path = "04_workflow_templates/family_expansion_batch_135_144.json"
    with open(spec_path, 'r') as f:
        batch_spec = json.load(f)

    for family_spec in batch_spec:
        family_id_str = family_spec['id']
        family_id_int = int(family_id_str)
        family_name = family_spec['name']
        
        # Prepare slug for folder name
        slug = family_name.lower().replace(" & ", "_and_").replace(" ", "_").replace(",", "").replace("-", "_").replace(":", "")
        
        # Explicit handling for family 140
        if family_id_int == 140:
            family_dir = "02_departments/140_final_boss_layer_system_of_systems_governance"
        else:
            family_dir = os.path.join("02_departments", f"{family_id_str}_{slug}")
        
        family_json_path = os.path.join(family_dir, "family.json")
        with open(family_json_path, 'r') as f:
            family_json = json.load(f)

        # Preserve top-level, but ensure ID is integer
        new_family_json = {
            "id": family_id_int,
            "name": family_json['name'],
            "manager": family_json.get('manager', f"{family_id_str}.M"),
            "scribe": family_json.get('scribe', f"{family_id_str}.H"),
            "auditor": family_json.get('auditor', f"{family_id_str}.I"),
            "departments": []
        }

        for dept_spec in family_spec['departments']:
            dept_id = dept_spec['id']
            new_dept = {
                "id": dept_id,
                "name": dept_spec['name'],
                "manager": f"{dept_id}.M",
                "scribe": f"{dept_id}.H",
                "auditor": f"{dept_id}.I",
                "units": []
            }
            for unit_spec in dept_spec['units']:
                unit_id = unit_spec['id']
                new_unit = {
                    "id": unit_id,
                    "name": unit_spec['name'],
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
                new_dept['units'].append(new_unit)
            new_family_json['departments'].append(new_dept)

        with open(family_json_path, 'w') as f:
            json.dump(new_family_json, f, indent=2)
        print(f"Wrote {family_json_path}")

        # Write README.md
        readme_path = os.path.join(family_dir, "README.md")
        readme_content = f"# {family_name}\n\n"
        readme_content += "## Purpose\n\n"
        readme_content += f"## Family Manager ({new_family_json['manager']})\n\n"
        readme_content += f"## Family Scribe ({new_family_json['scribe']})\n\n"
        readme_content += f"## Family Auditor ({new_family_json['auditor']})\n\n"
        readme_content += "## Departments\n"
        
        for dept in new_family_json['departments']:
            readme_content += f"\n### {dept['id']} {dept['name']}\n"
            for unit in dept['units']:
                readme_content += f"- {unit['id']} {unit['name']}\n"
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        print(f"Wrote {readme_path}")

if __name__ == "__main__":
    apply_batch()

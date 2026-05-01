import json
import os
import sys

# Ensure we are in project root
project_root = os.getcwd()
if os.path.basename(project_root) == 'scripts':
    os.chdir('..')

SPEC_PATH = '04_workflow_templates/family_expansion_batch_095_104.json'

def apply_expansion():
    if not os.path.exists(SPEC_PATH):
        print(f"Error: Spec file not found at {SPEC_PATH}")
        sys.exit(1)

    with open(SPEC_PATH, 'r', encoding='utf-8') as f:
        spec = json.load(f)

    for family in spec['families']:
        family_id = family['id']
        family_name = family['name']
        folder = family['folder']
        
        family_json_path = os.path.join(folder, 'family.json')
        readme_path = os.path.join(folder, 'README.md')
        
        if not os.path.exists(family_json_path):
            print(f"Error: family.json not found at {family_json_path}")
            continue

        # Update family.json
        with open(family_json_path, 'r', encoding='utf-8') as f:
            family_data = json.load(f)
            
        new_departments = []
        for dept in family['departments']:
            dept_id = dept['id']
            dept_name = dept['name']
            
            new_dept = {
                "id": dept_id,
                "name": dept_name,
                "manager": f"{dept_id}.M",
                "scribe": f"{dept_id}.H",
                "auditor": f"{dept_id}.I",
                "units": []
            }
            
            for i, unit_name in enumerate(dept['units'], 1):
                unit_id = f"{dept_id}.{i}"
                new_unit = {
                    "id": unit_id,
                    "name": unit_name,
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
            
            new_departments.append(new_dept)
            
        family_data['departments'] = new_departments
        
        with open(family_json_path, 'w', encoding='utf-8') as f:
            json.dump(family_data, f, indent=2)
        print(f"Updated {family_json_path}")
        
        # Update README.md
        readme_content = f"# {family_name}\n\n"
        readme_content += "## Purpose\n\n"
        readme_content += f"## Family Manager ({family_id}.M)\n\n"
        readme_content += f"## Family Scribe ({family_id}.H)\n\n"
        readme_content += f"## Family Auditor ({family_id}.I)\n\n"
        readme_content += "## Departments\n"
        
        for dept in new_departments:
            readme_content += f"\n### {dept['id']} {dept['name']}\n"
            for unit in dept['units']:
                readme_content += f"- {unit['id']} {unit['name']}\n"
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"Updated {readme_path}")

if __name__ == "__main__":
    apply_expansion()

#!/usr/bin/env python3
import json
import os
import sys
import re

def slugify(text):
    text = text.lower()
    text = text.replace("&", "and")
    for char in [",", "/", "'", "(", ")", ":", ";", ".", "!", "?", '"', "`", "[", "]", "{", "}", "|", "\\"]:
        text = text.replace(char, "")
    text = text.replace("-", "_")
    text = text.replace(" ", "_")
    text = re.sub(r'_+', '_', text)
    text = text.strip('_')
    return text

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    registry_file = os.path.join(base_dir, '01_registry', 'department_families.json')
    exports_dir = os.path.join(base_dir, '09_exports')
    
    if not os.path.exists(registry_file):
        print(f"FAIL: Registry file not found at {registry_file}")
        sys.exit(1)
        
    try:
        with open(registry_file, 'r', encoding='utf-8') as f:
            families = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FAIL: Invalid JSON in registry file: {e}")
        sys.exit(1)
        
    if not isinstance(families, list) or len(families) != 175:
        print("FAIL: Registry must contain exactly 175 families.")
        sys.exit(1)
        
    unsafe_chars = [":", ";", "!", "?", '"', "`", "[", "]", "{", "}", "|", "\\"]
    
    missing_folders = []
    missing_family_files = []
    missing_readmes = []
    unsafe_folders = []
    
    org_chart = {
        "system_name": "Agent Command Center",
        "version": "0.1.0",
        "total_families": 175,
        "families": []
    }
    
    dashboard_seed = {
        "title": "Agent Command Center",
        "families": []
    }
    
    md_list = ["# Master Department Family List\n"]
    
    for family in families:
        fid = family.get("id")
        fname = family.get("name")
        
        slug = slugify(fname)
        padded_id = f"{fid:03d}"
        folder_name = f"{padded_id}_{slug}"
        
        for char in unsafe_chars:
            if char in folder_name:
                unsafe_folders.append(folder_name)
                break
                
        folder_rel_path = f"02_departments/{folder_name}"
        folder_abs_path = os.path.join(base_dir, '02_departments', folder_name)
        
        family_file_rel = f"{folder_rel_path}/family.json"
        family_file_abs = os.path.join(folder_abs_path, 'family.json')
        
        readme_rel = f"{folder_rel_path}/README.md"
        readme_abs = os.path.join(folder_abs_path, 'README.md')
        
        if not os.path.isdir(folder_abs_path):
            missing_folders.append(folder_rel_path)
        if not os.path.isfile(family_file_abs):
            missing_family_files.append(family_file_rel)
        if not os.path.isfile(readme_abs):
            missing_readmes.append(readme_rel)
            
        org_chart["families"].append({
            "id": fid,
            "name": fname,
            "manager": f"{fid}.M",
            "scribe": f"{fid}.H",
            "auditor": f"{fid}.I",
            "folder": folder_rel_path,
            "family_file": family_file_rel,
            "readme": readme_rel,
            "departments": []
        })
        
        dashboard_seed["families"].append({
            "id": fid,
            "label": fname,
            "folder": folder_rel_path,
            "status": "shell_created"
        })
        
        md_list.append(f"{fid}. {fname}")
        
    print(f"Total families exported: {len(families)}")
    print(f"Missing folders: {len(missing_folders)}")
    print(f"Missing family files: {len(missing_family_files)}")
    print(f"Missing README files: {len(missing_readmes)}")
    print(f"Unsafe folder names: {len(unsafe_folders)}")
    
    if missing_folders or missing_family_files or missing_readmes or unsafe_folders:
        print("FAIL")
        sys.exit(1)
        
    print("PASS")
    
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
        
    with open(os.path.join(exports_dir, 'org_chart_export.json'), 'w', encoding='utf-8') as f:
        json.dump(org_chart, f, indent=2)
        
    with open(os.path.join(exports_dir, 'dashboard_seed.json'), 'w', encoding='utf-8') as f:
        json.dump(dashboard_seed, f, indent=2)
        
    with open(os.path.join(exports_dir, 'master_department_list.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(md_list) + "\n")

if __name__ == '__main__':
    main()

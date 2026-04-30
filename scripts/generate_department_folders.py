#!/usr/bin/env python3
import json
import os
import sys
import argparse
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
    parser = argparse.ArgumentParser(description="Generate department family folders")
    parser.add_argument("--force", action="store_true", help="Force overwrite of existing files")
    args = parser.parse_args()

    base_dir = os.path.join(os.path.dirname(__file__), '..')
    registry_file = os.path.join(base_dir, '01_registry', 'department_families.json')
    departments_dir = os.path.join(base_dir, '02_departments')

    if not os.path.exists(registry_file):
        print(f"FAIL: Registry file not found at {registry_file}")
        sys.exit(1)

    try:
        with open(registry_file, 'r', encoding='utf-8') as f:
            families = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FAIL: Invalid JSON in registry file: {e}")
        sys.exit(1)

    if not isinstance(families, list):
        print("FAIL: Registry root must be a list.")
        sys.exit(1)

    folders_created = 0
    files_created = 0
    files_skipped = 0

    if not os.path.exists(departments_dir):
        os.makedirs(departments_dir)

    for family in families:
        fid = family.get("id")
        fname = family.get("name")

        if not fid or not fname:
            print(f"SKIP: Missing id or name in family: {family}")
            continue

        slug = slugify(fname)
        padded_id = f"{fid:03d}"
        folder_name = f"{padded_id}_{slug}"
        folder_path = os.path.join(departments_dir, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            folders_created += 1

        # family.json
        family_json_content = {
            "id": fid,
            "name": fname,
            "manager": f"{fid}.M",
            "scribe": f"{fid}.H",
            "auditor": f"{fid}.I",
            "departments": []
        }
        family_json_str = json.dumps(family_json_content, indent=2) + "\n"
        family_json_path = os.path.join(folder_path, "family.json")

        if os.path.exists(family_json_path):
            with open(family_json_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            if existing_content.strip() != family_json_str.strip():
                if args.force:
                    with open(family_json_path, 'w', encoding='utf-8') as f:
                        f.write(family_json_str)
                    files_created += 1
                else:
                    print(f"SKIP changed file: {os.path.relpath(family_json_path, base_dir)}")
                    files_skipped += 1
            else:
                pass # Identical, do nothing
        else:
            with open(family_json_path, 'w', encoding='utf-8') as f:
                f.write(family_json_str)
            files_created += 1

        # README.md
        readme_str = f"""# {fname}

## Purpose

Placeholder purpose for {fname}.

## Family Manager ({fid}.M)

Routes family-level work, resolves escalations, and coordinates subordinate departments.

## Family Scribe ({fid}.H)

Records family-level decisions, assumptions, handoffs, and work trails.

## Family Auditor ({fid}.I)

Reviews family-level output and marks items as keep, fix, remove, redo, or escalate.

## Departments

Not populated yet.
"""
        readme_path = os.path.join(folder_path, "README.md")

        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            if existing_content.strip() != readme_str.strip():
                if args.force:
                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(readme_str)
                    files_created += 1
                else:
                    print(f"SKIP changed file: {os.path.relpath(readme_path, base_dir)}")
                    files_skipped += 1
            else:
                pass # Identical, do nothing
        else:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_str)
            files_created += 1

    print(f"folders created: {folders_created}")
    print(f"files created: {files_created}")
    print(f"files skipped: {files_skipped}")

if __name__ == "__main__":
    main()

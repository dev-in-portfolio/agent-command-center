import json
import os
import sys
import re

EXPECTED = {
    "175": {
        "name": "Master Archive / Library of Alexandria",
        "departments": {
            "175.1": {
                "name": "Master Archive Intake",
                "units": {
                    "175.1.1": "Archive Request Capture",
                    "175.1.2": "Collection Scope Review",
                    "175.1.3": "Archive Intake Summary"
                }
            },
            "175.2": {
                "name": "Universal Indexing System",
                "units": {
                    "175.2.1": "Index Field Definition",
                    "175.2.2": "Cross-Reference Mapping",
                    "175.2.3": "Index Update Notes"
                }
            },
            "175.3": {
                "name": "Collection Classification",
                "units": {
                    "175.3.1": "Collection Category Assignment",
                    "175.3.2": "Shelf Taxonomy Review",
                    "175.3.3": "Classification Record Update"
                }
            },
            "175.4": {
                "name": "Source Preservation",
                "units": {
                    "175.4.1": "Preservation Requirement Capture",
                    "175.4.2": "File Integrity Review",
                    "175.4.3": "Preservation Action Notes"
                }
            },
            "175.5": {
                "name": "Retrieval Pathways",
                "units": {
                    "175.5.1": "Retrieval Need Capture",
                    "175.5.2": "Search Route Mapping",
                    "175.5.3": "Retrieval Path QA"
                }
            },
            "175.6": {
                "name": "Archive Continuity",
                "units": {
                    "175.6.1": "Continuity Context Capture",
                    "175.6.2": "Historical Thread Linking",
                    "175.6.3": "Continuity Summary Update"
                }
            },
            "175.7": {
                "name": "Library Governance",
                "units": {
                    "175.7.1": "Archive Rule Definition",
                    "175.7.2": "Access Boundary Review",
                    "175.7.3": "Governance Record Update"
                }
            },
            "175.8": {
                "name": "Alexandria Catalog",
                "units": {
                    "175.8.1": "Catalog Entry Capture",
                    "175.8.2": "Collection Metadata Review",
                    "175.8.3": "Catalog Update Notes"
                }
            },
            "175.9": {
                "name": "Legacy Archive Packaging",
                "units": {
                    "175.9.1": "Archive Package Assembly",
                    "175.9.2": "Export Format Review",
                    "175.9.3": "Legacy Package QA"
                }
            },
            "175.10": {
                "name": "Master Archive Dashboard",
                "units": {
                    "175.10.1": "Archive Signal Collection",
                    "175.10.2": "Library Status Summary",
                    "175.10.3": "Dashboard Update"
                }
            }
        }
    }
}

def validate():
    spec_path = "04_workflow_templates/family_expansion_batch_175.json"
    with open(spec_path, 'r') as f:
        batch_spec = json.load(f)

    errors = []
    
    # Fidelity strings
    required_strings = [
        "Master Archive / Library of Alexandria",
        "Master Archive Intake",
        "Universal Indexing System",
        "Collection Classification",
        "Source Preservation",
        "Retrieval Pathways",
        "Archive Continuity",
        "Library Governance",
        "Alexandria Catalog",
        "Legacy Archive Packaging",
        "Master Archive Dashboard",
        "Archive Request Capture",
        "Cross-Reference Mapping",
        "Shelf Taxonomy Review",
        "File Integrity Review",
        "Retrieval Path QA",
        "Historical Thread Linking",
        "Access Boundary Review",
        "Collection Metadata Review",
        "Legacy Package QA",
        "Library Status Summary"
    ]
    spec_text = json.dumps(batch_spec)
    for s in required_strings:
        if s not in spec_text:
            errors.append(f"Prompt fidelity string missing from spec: '{s}'")

    # Validate Batch Spec
    if len(batch_spec) != 1:
        errors.append(f"Batch spec length mismatch: expected 1, found {len(batch_spec)}")
        
    for family in batch_spec:
        fid = family["id"]
        if fid not in EXPECTED:
            errors.append(f"Family {fid} not in EXPECTED")
            continue
        if family["name"] != EXPECTED[fid]["name"]:
            errors.append(f"Family {fid} name mismatch")
            
        depts = {d["id"]: d for d in family["departments"]}
        for did, dexpect in EXPECTED[fid]["departments"].items():
            if did not in depts:
                errors.append(f"Department {did} missing from batch spec")
                continue
            if depts[did]["name"] != dexpect["name"]:
                errors.append(f"Department {did} name mismatch")
                
            units = {u["id"]: u for u in depts[did]["units"]}
            for uid, uname in dexpect["units"].items():
                if uid not in units:
                    errors.append(f"Unit {uid} missing from batch spec")
                elif units[uid]["name"] != uname:
                    errors.append(f"Unit {uid} name mismatch in spec")

    # Validate Files
    fid = "175"
    fexpect = EXPECTED[fid]
    fdir = f"02_departments/175_master_archive_library_of_alexandria"
    fjson_path = os.path.join(fdir, "family.json")
    readme_path = os.path.join(fdir, "README.md")
    
    if not os.path.exists(fjson_path):
        errors.append(f"File missing: {fjson_path}")
    else:
        with open(fjson_path, 'r') as f:
            fjson = json.load(f)
            
        if not isinstance(fjson["id"], int):
            errors.append(f"Family {fid} ID is not an integer in family.json")
        if str(fjson["id"]) != fid:
            errors.append(f"Family ID mismatch in {fjson_path}")
        if fjson["name"] != fexpect["name"]:
            errors.append(f"Family name mismatch in {fjson_path}")
            
        depts = {d["id"]: d for d in fjson["departments"]}
        for did, dexpect in fexpect["departments"].items():
            if did not in depts:
                errors.append(f"Department {did} missing from {fjson_path}")
                continue
            dept = depts[did]
            if dept["name"] != dexpect["name"]:
                errors.append(f"Department {did} name mismatch in {fjson_path}")
            
            for u in dept["units"]:
                uid = u["id"]
                if uid not in dexpect["units"]:
                    errors.append(f"Unit {uid} not expected")
                    continue
                uname = dexpect["units"][uid]
                if u["name"] != uname:
                    errors.append(f"Unit {uid} name mismatch in {fjson_path}")
                
                if len(u["team"]) != 9:
                    errors.append(f"Unit {uid} team size mismatch")
                for i, role in enumerate(["Realist", "Overachiever", "Dreamer", "Timid", "Overprotective", "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"]):
                    suffix = ["1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H", "1I"][i]
                    tm = u["team"][i]
                    if tm.get("id") != f"{uid}.{suffix}":
                        errors.append(f"Team member ID mismatch for {uid} {suffix}")
                    if tm.get("role") != role:
                        errors.append(f"Team member role mismatch for {uid} {suffix}")

    if not os.path.exists(readme_path):
        errors.append(f"File missing: {readme_path}")
    else:
        with open(readme_path, 'r') as f:
            readme = f.read()
            
        if f"# {fexpect['name']}" not in readme:
            errors.append(f"README title mismatch for {fid}")
            
        # Check forbidden formatting
        if re.search(r"### .* \(.*\)", readme):
            errors.append(f"README {fid} uses forbidden '### Name (ID)' format")
        if re.search(r"- .* \(.*\)", readme):
            errors.append(f"README {fid} uses forbidden '- Name (ID)' format")
            
        for did, dexpect in fexpect["departments"].items():
            expected_h3 = f"### {did} {dexpect['name']}"
            if expected_h3 not in readme:
                errors.append(f"README {fid} missing correctly formatted department {did}: '{expected_h3}'")
            for uid, uname in dexpect["units"].items():
                expected_bullet = f"- {uid} {uname}"
                if expected_bullet not in readme:
                    errors.append(f"README {fid} missing correctly formatted unit {uid}: '{expected_bullet}'")

    if errors:
        for e in errors:
            print(e)
        print("FAIL")
        sys.exit(1)
    else:
        print("PASS: Family batch 175 expansion valid.")

if __name__ == "__main__":
    validate()

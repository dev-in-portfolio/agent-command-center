#!/usr/bin/env python3
import json
import os
import sys

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    family_file = os.path.join(base_dir, '02_departments', '004_research_and_intelligence', 'family.json')
    errors = []

    if not os.path.exists(family_file):
        print("FAIL")
        print(f"File not found: {family_file}")
        sys.exit(1)

    try:
        with open(family_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print("FAIL")
        print(f"Invalid JSON: {e}")
        sys.exit(1)

    if data.get("id") != 4: errors.append("Family id is not 4.")
    if data.get("name") != "Research & Intelligence": errors.append("Family name is not 'Research & Intelligence'.")
    if data.get("manager") != "4.M" or data.get("scribe") != "4.H" or data.get("auditor") != "4.I":
        errors.append("Manager/Scribe/Auditor fields are incorrect.")
        
    depts = data.get("departments", [])
    if not isinstance(depts, list) or len(depts) != 15:
        errors.append(f"Expected exactly 15 departments, found {len(depts) if isinstance(depts, list) else type(depts)}.")
    
    depts_expected = [
        ("4.1", "General Research", ["Research Question Framing", "Background Scan", "Finding Summary"]),
        ("4.2", "Web Research", ["Search Strategy", "Source Collection", "Web Evidence Review"]),
        ("4.3", "Market Research", ["Market Category Mapping", "Demand Signal Review", "Market Opportunity Summary"]),
        ("4.4", "Competitive Intelligence", ["Competitor Identification", "Competitor Capability Review", "Competitive Positioning Summary"]),
        ("4.5", "Academic Research", ["Literature Search", "Study Quality Review", "Academic Findings Summary"]),
        ("4.6", "Technical Research", ["Technical Topic Breakdown", "Technical Source Review", "Implementation Implication Summary"]),
        ("4.7", "Regulatory Research", ["Regulation Identification", "Requirement Extraction", "Regulatory Impact Summary"]),
        ("4.8", "Product Research", ["Product Feature Mapping", "Product Comparison Review", "Product Fit Summary"]),
        ("4.9", "User Research", ["User Need Discovery", "User Pain Point Mapping", "User Insight Summary"]),
        ("4.10", "Vendor Research", ["Vendor Identification", "Vendor Capability Review", "Vendor Risk Summary"]),
        ("4.11", "Investment Research", ["Company Research", "Sector Research", "Catalyst And Risk Summary"]),
        ("4.12", "Industry Trend Research", ["Trend Detection", "Signal Strength Review", "Trend Implication Summary"]),
        ("4.13", "Source Verification", ["Source Credibility Review", "Claim Cross-Check", "Verification Decision"]),
        ("4.14", "Citation Management", ["Citation Capture", "Citation Formatting", "Citation Completeness Review"]),
        ("4.15", "Evidence Review", ["Evidence Inventory", "Evidence Strength Grading", "Evidence Gap Report"])
    ]

    expected_roles = [
        "Realist", "Overachiever", "Dreamer", "Timid", "Overprotective",
        "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"
    ]
    role_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    
    if isinstance(depts, list):
        for i, dept in enumerate(depts):
            if i >= len(depts_expected): break
            exp_d_id, exp_d_name, exp_u_names = depts_expected[i]
            
            if dept.get("id") != exp_d_id: errors.append(f"Department ID expected {exp_d_id}, found {dept.get('id')}.")
            if dept.get("name") != exp_d_name: errors.append(f"Department name expected {exp_d_name}, found {dept.get('name')}.")
            
            d_id = dept.get("id")
            if dept.get("manager") != f"{d_id}.M": errors.append(f"Manager incorrect for {d_id}")
            if dept.get("scribe") != f"{d_id}.H": errors.append(f"Scribe incorrect for {d_id}")
            if dept.get("auditor") != f"{d_id}.I": errors.append(f"Auditor incorrect for {d_id}")
            
            units = dept.get("units", [])
            if not isinstance(units, list) or len(units) != 3:
                errors.append(f"Expected 3 units in {d_id}, found {len(units) if isinstance(units, list) else type(units)}.")
            
            if isinstance(units, list):
                for j, unit in enumerate(units):
                    if j >= len(exp_u_names): break
                    expected_u_id = f"{d_id}.{j+1}"
                    expected_u_name = exp_u_names[j]
                    
                    if unit.get("id") != expected_u_id:
                        errors.append(f"Unit ID expected {expected_u_id}, found {unit.get('id')}.")
                    if unit.get("name") != expected_u_name:
                        errors.append(f"Unit name expected {expected_u_name}, found {unit.get('name')}.")
                    
                    u_id = unit.get("id")
                    team = unit.get("team", [])
                    if not isinstance(team, list) or len(team) != 9:
                        errors.append(f"Expected exactly 9 team roles in {u_id}, found {len(team) if isinstance(team, list) else type(team)}.")
                    
                    if isinstance(team, list):
                        for k, member in enumerate(team):
                            if k >= len(expected_roles): break
                            expected_t_id = f"{u_id}.1{role_letters[k]}"
                            if member.get("id") != expected_t_id:
                                errors.append(f"Team ID expected {expected_t_id}, found {member.get('id')}.")
                            if member.get("role") != expected_roles[k]:
                                errors.append(f"Team role expected {expected_roles[k]}, found {member.get('role')}.")

    if errors:
        print("FAIL")
        for err in errors:
            print("- " + err)
        sys.exit(1)
        
    print("PASS: Research & Intelligence family expansion valid.")
    sys.exit(0)

if __name__ == '__main__':
    main()

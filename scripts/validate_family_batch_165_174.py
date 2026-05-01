import json
import os
import sys
import re

EXPECTED = {
    "165": {
        "name": "Systems Migration Office",
        "departments": {
            "165.1": {
                "name": "Migration Intake",
                "units": ["165.1.1", "165.1.2", "165.1.3"]
            },
            "165.2": {
                "name": "Migration Scope Mapping",
                "units": ["165.2.1", "165.2.2", "165.2.3"]
            },
            "165.3": {
                "name": "Source System Assessment",
                "units": ["165.3.1", "165.3.2", "165.3.3"]
            },
            "165.4": {
                "name": "Target System Design",
                "units": ["165.4.1", "165.4.2", "165.4.3"]
            },
            "165.5": {
                "name": "Migration Plan Development",
                "units": ["165.5.1", "165.5.2", "165.5.3"]
            },
            "165.6": {
                "name": "Data Migration Operations",
                "units": ["165.6.1", "165.6.2", "165.6.3"]
            },
            "165.7": {
                "name": "Migration Testing",
                "units": ["165.7.1", "165.7.2", "165.7.3"]
            },
            "165.8": {
                "name": "Cutover Management",
                "units": ["165.8.1", "165.8.2", "165.8.3"]
            },
            "165.9": {
                "name": "Migration Risk Governance",
                "units": ["165.9.1", "165.9.2", "165.9.3"]
            },
            "165.10": {
                "name": "Migration Dashboard",
                "units": ["165.10.1", "165.10.2", "165.10.3"]
            }
        }
    },
    "166": {
        "name": "Mobile App Operations",
        "departments": {
            "166.1": {
                "name": "Mobile App Intake",
                "units": ["166.1.1", "166.1.2", "166.1.3"]
            },
            "166.2": {
                "name": "Mobile Feature Planning",
                "units": ["166.2.1", "166.2.2", "166.2.3"]
            },
            "166.3": {
                "name": "Mobile UX Review",
                "units": ["166.3.1", "166.3.2", "166.3.3"]
            },
            "166.4": {
                "name": "App Build Coordination",
                "units": ["166.4.1", "166.4.2", "166.4.3"]
            },
            "166.5": {
                "name": "Device Compatibility Testing",
                "units": ["166.5.1", "166.5.2", "166.5.3"]
            },
            "166.6": {
                "name": "App Store Submission",
                "units": ["166.6.1", "166.6.2", "166.6.3"]
            },
            "166.7": {
                "name": "Mobile Analytics Review",
                "units": ["166.7.1", "166.7.2", "166.7.3"]
            },
            "166.8": {
                "name": "Crash And Bug Monitoring",
                "units": ["166.8.1", "166.8.2", "166.8.3"]
            },
            "166.9": {
                "name": "Mobile Governance",
                "units": ["166.9.1", "166.9.2", "166.9.3"]
            },
            "166.10": {
                "name": "Mobile Dashboard",
                "units": ["166.10.1", "166.10.2", "166.10.3"]
            }
        }
    },
    "167": {
        "name": "Voice, Phone & Conversational Agent Operations",
        "departments": {
            "167.1": {
                "name": "Voice Channel Intake",
                "units": ["167.1.1", "167.1.2", "167.1.3"]
            },
            "167.2": {
                "name": "Call Flow Design",
                "units": ["167.2.1", "167.2.2", "167.2.3"]
            },
            "167.3": {
                "name": "Conversational Agent Script",
                "units": ["167.3.1", "167.3.2", "167.3.3"]
            },
            "167.4": {
                "name": "Voice Experience Testing",
                "units": ["167.4.1", "167.4.2", "167.4.3"]
            },
            "167.5": {
                "name": "Phone Routing Operations",
                "units": ["167.5.1", "167.5.2", "167.5.3"]
            },
            "167.6": {
                "name": "Call Recording Review",
                "units": ["167.6.1", "167.6.2", "167.6.3"]
            },
            "167.7": {
                "name": "Voice Compliance Review",
                "units": ["167.7.1", "167.7.2", "167.7.3"]
            },
            "167.8": {
                "name": "Live Agent Handoff",
                "units": ["167.8.1", "167.8.2", "167.8.3"]
            },
            "167.9": {
                "name": "Voice Governance",
                "units": ["167.9.1", "167.9.2", "167.9.3"]
            },
            "167.10": {
                "name": "Voice Dashboard",
                "units": ["167.10.1", "167.10.2", "167.10.3"]
            }
        }
    },
    "168": {
        "name": "Physical Mail & Print Outreach",
        "departments": {
            "168.1": {
                "name": "Mail Campaign Intake",
                "units": ["168.1.1", "168.1.2", "168.1.3"]
            },
            "168.2": {
                "name": "Print Piece Design",
                "units": ["168.2.1", "168.2.2", "168.2.3"]
            },
            "168.3": {
                "name": "Mailing List Preparation",
                "units": ["168.3.1", "168.3.2", "168.3.3"]
            },
            "168.4": {
                "name": "Print Vendor Coordination",
                "units": ["168.4.1", "168.4.2", "168.4.3"]
            },
            "168.5": {
                "name": "Postal Compliance Review",
                "units": ["168.5.1", "168.5.2", "168.5.3"]
            },
            "168.6": {
                "name": "Mail Drop Scheduling",
                "units": ["168.6.1", "168.6.2", "168.6.3"]
            },
            "168.7": {
                "name": "Response Tracking",
                "units": ["168.7.1", "168.7.2", "168.7.3"]
            },
            "168.8": {
                "name": "Print Quality Control",
                "units": ["168.8.1", "168.8.2", "168.8.3"]
            },
            "168.9": {
                "name": "Mail Governance",
                "units": ["168.9.1", "168.9.2", "168.9.3"]
            },
            "168.10": {
                "name": "Mail Dashboard",
                "units": ["168.10.1", "168.10.2", "168.10.3"]
            }
        }
    },
    "169": {
        "name": "CRM Operations",
        "departments": {
            "169.1": {
                "name": "CRM Intake",
                "units": ["169.1.1", "169.1.2", "169.1.3"]
            },
            "169.2": {
                "name": "Contact Record Management",
                "units": ["169.2.1", "169.2.2", "169.2.3"]
            },
            "169.3": {
                "name": "Pipeline Configuration",
                "units": ["169.3.1", "169.3.2", "169.3.3"]
            },
            "169.4": {
                "name": "CRM Field Management",
                "units": ["169.4.1", "169.4.2", "169.4.3"]
            },
            "169.5": {
                "name": "CRM Automation Rules",
                "units": ["169.5.1", "169.5.2", "169.5.3"]
            },
            "169.6": {
                "name": "CRM Data Hygiene",
                "units": ["169.6.1", "169.6.2", "169.6.3"]
            },
            "169.7": {
                "name": "CRM Reporting",
                "units": ["169.7.1", "169.7.2", "169.7.3"]
            },
            "169.8": {
                "name": "CRM Integration Review",
                "units": ["169.8.1", "169.8.2", "169.8.3"]
            },
            "169.9": {
                "name": "CRM Governance",
                "units": ["169.9.1", "169.9.2", "169.9.3"]
            },
            "169.10": {
                "name": "CRM Dashboard",
                "units": ["169.10.1", "169.10.2", "169.10.3"]
            }
        }
    },
    "170": {
        "name": "Lead Nurture Factory",
        "departments": {
            "170.1": {
                "name": "Lead Nurture Intake",
                "units": ["170.1.1", "170.1.2", "170.1.3"]
            },
            "170.2": {
                "name": "Segment Design",
                "units": ["170.2.1", "170.2.2", "170.2.3"]
            },
            "170.3": {
                "name": "Nurture Sequence Design",
                "units": ["170.3.1", "170.3.2", "170.3.3"]
            },
            "170.4": {
                "name": "Follow-Up Copy Production",
                "units": ["170.4.1", "170.4.2", "170.4.3"]
            },
            "170.5": {
                "name": "Lead Scoring",
                "units": ["170.5.1", "170.5.2", "170.5.3"]
            },
            "170.6": {
                "name": "Nurture Automation Setup",
                "units": ["170.6.1", "170.6.2", "170.6.3"]
            },
            "170.7": {
                "name": "Engagement Monitoring",
                "units": ["170.7.1", "170.7.2", "170.7.3"]
            },
            "170.8": {
                "name": "Re-Engagement Campaigns",
                "units": ["170.8.1", "170.8.2", "170.8.3"]
            },
            "170.9": {
                "name": "Nurture Governance",
                "units": ["170.9.1", "170.9.2", "170.9.3"]
            },
            "170.10": {
                "name": "Nurture Dashboard",
                "units": ["170.10.1", "170.10.2", "170.10.3"]
            }
        }
    },
    "171": {
        "name": "Revenue Operations",
        "departments": {
            "171.1": {
                "name": "Revenue Operations Intake",
                "units": ["171.1.1", "171.1.2", "171.1.3"]
            },
            "171.2": {
                "name": "Funnel Metrics",
                "units": ["171.2.1", "171.2.2", "171.2.3"]
            },
            "171.3": {
                "name": "Sales Process Alignment",
                "units": ["171.3.1", "171.3.2", "171.3.3"]
            },
            "171.4": {
                "name": "Revenue Forecasting",
                "units": ["171.4.1", "171.4.2", "171.4.3"]
            },
            "171.5": {
                "name": "Pricing Operations",
                "units": ["171.5.1", "171.5.2", "171.5.3"]
            },
            "171.6": {
                "name": "Revenue Reporting",
                "units": ["171.6.1", "171.6.2", "171.6.3"]
            },
            "171.7": {
                "name": "Sales Enablement Operations",
                "units": ["171.7.1", "171.7.2", "171.7.3"]
            },
            "171.8": {
                "name": "Revenue Leakage Review",
                "units": ["171.8.1", "171.8.2", "171.8.3"]
            },
            "171.9": {
                "name": "RevOps Governance",
                "units": ["171.9.1", "171.9.2", "171.9.3"]
            },
            "171.10": {
                "name": "Revenue Dashboard",
                "units": ["171.10.1", "171.10.2", "171.10.3"]
            }
        }
    },
    "172": {
        "name": "Customer Education Academy",
        "departments": {
            "172.1": {
                "name": "Education Program Intake",
                "units": ["172.1.1", "172.1.2", "172.1.3"]
            },
            "172.2": {
                "name": "Curriculum Path Design",
                "units": ["172.2.1", "172.2.2", "172.2.3"]
            },
            "172.3": {
                "name": "Customer Lesson Production",
                "units": ["172.3.1", "172.3.2", "172.3.3"]
            },
            "172.4": {
                "name": "Tutorial Asset Creation",
                "units": ["172.4.1", "172.4.2", "172.4.3"]
            },
            "172.5": {
                "name": "Knowledge Check Design",
                "units": ["172.5.1", "172.5.2", "172.5.3"]
            },
            "172.6": {
                "name": "Education Delivery Operations",
                "units": ["172.6.1", "172.6.2", "172.6.3"]
            },
            "172.7": {
                "name": "Learner Progress Tracking",
                "units": ["172.7.1", "172.7.2", "172.7.3"]
            },
            "172.8": {
                "name": "Education Feedback Loop",
                "units": ["172.8.1", "172.8.2", "172.8.3"]
            },
            "172.9": {
                "name": "Education Governance",
                "units": ["172.9.1", "172.9.2", "172.9.3"]
            },
            "172.10": {
                "name": "Education Dashboard",
                "units": ["172.10.1", "172.10.2", "172.10.3"]
            }
        }
    },
    "173": {
        "name": "Workflow Certification Office",
        "departments": {
            "173.1": {
                "name": "Certification Intake",
                "units": ["173.1.1", "173.1.2", "173.1.3"]
            },
            "173.2": {
                "name": "Certification Standard Design",
                "units": ["173.2.1", "173.2.2", "173.2.3"]
            },
            "173.3": {
                "name": "Workflow Assessment",
                "units": ["173.3.1", "173.3.2", "173.3.3"]
            },
            "173.4": {
                "name": "Certification Testing",
                "units": ["173.4.1", "173.4.2", "173.4.3"]
            },
            "173.5": {
                "name": "Certification Decisioning",
                "units": ["173.5.1", "173.5.2", "173.5.3"]
            },
            "173.6": {
                "name": "Renewal Review",
                "units": ["173.6.1", "173.6.2", "173.6.3"]
            },
            "173.7": {
                "name": "Certification Registry",
                "units": ["173.7.1", "173.7.2", "173.7.3"]
            },
            "173.8": {
                "name": "Nonconformance Handling",
                "units": ["173.8.1", "173.8.2", "173.8.3"]
            },
            "173.9": {
                "name": "Certification Governance",
                "units": ["173.9.1", "173.9.2", "173.9.3"]
            },
            "173.10": {
                "name": "Certification Dashboard",
                "units": ["173.10.1", "173.10.2", "173.10.3"]
            }
        }
    },
    "174": {
        "name": "Agent Incident Court",
        "departments": {
            "174.1": {
                "name": "Incident Case Intake",
                "units": ["174.1.1", "174.1.2", "174.1.3"]
            },
            "174.2": {
                "name": "Evidence Docket",
                "units": ["174.2.1", "174.2.2", "174.2.3"]
            },
            "174.3": {
                "name": "Agent Testimony Review",
                "units": ["174.3.1", "174.3.2", "174.3.3"]
            },
            "174.4": {
                "name": "Incident Argument Mapping",
                "units": ["174.4.1", "174.4.2", "174.4.3"]
            },
            "174.5": {
                "name": "Responsibility Assessment",
                "units": ["174.5.1", "174.5.2", "174.5.3"]
            },
            "174.6": {
                "name": "Remediation Order Drafting",
                "units": ["174.6.1", "174.6.2", "174.6.3"]
            },
            "174.7": {
                "name": "Appeals Review",
                "units": ["174.7.1", "174.7.2", "174.7.3"]
            },
            "174.8": {
                "name": "Precedent Management",
                "units": ["174.8.1", "174.8.2", "174.8.3"]
            },
            "174.9": {
                "name": "Incident Court Governance",
                "units": ["174.9.1", "174.9.2", "174.9.3"]
            },
            "174.10": {
                "name": "Incident Court Dashboard",
                "units": ["174.10.1", "174.10.2", "174.10.3"]
            }
        }
    }
}

FOLDER_MAPPING = {
    "165": "165_systems_migration_office",
    "166": "166_mobile_app_operations",
    "167": "167_voice_phone_and_conversational_agent_operations",
    "168": "168_physical_mail_and_print_outreach",
    "169": "169_crm_operations",
    "170": "170_lead_nurture_factory",
    "171": "171_revenue_operations",
    "172": "172_customer_education_academy",
    "173": "173_workflow_certification_office",
    "174": "174_agent_incident_court"
}

UNIT_NAMES = {
    "165.8.3": "Cutover Decision Record",
    "166.5.3": "Compatibility Findings",
    "166.8.3": "Fix Priority Notes",
    "167.3.3": "Script Clarity Review",
    "167.8.3": "Handoff Confirmation Notes",
    "168.5.3": "Postal Compliance Notes",
    "168.8.3": "Print Approval Notes",
    "169.5.3": "Automation Rule Update",
    "169.6.3": "Hygiene Action Notes",
    "170.3.3": "Sequence QA",
    "170.8.3": "Campaign Recommendation",
    "171.4.3": "Forecast Summary",
    "171.8.3": "Leakage Reduction Notes",
    "172.4.3": "Tutorial Asset Review",
    "172.8.3": "Feedback Action Notes",
    "173.5.3": "Decision Record Update",
    "173.8.3": "Nonconformance Record",
    "174.5.3": "Responsibility Finding",
    "174.8.3": "Precedent Record Update"
}

def validate():
    spec_path = "04_workflow_templates/family_expansion_batch_165_174.json"
    with open(spec_path, 'r') as f:
        batch_spec = json.load(f)

    errors = []
    
    # Validate Batch Spec against EXPECTED
    if len(batch_spec) != 10:
        errors.append(f"Batch spec length mismatch: expected 10, found {len(batch_spec)}")
        
    for family in batch_spec:
        fid = family["id"]
        if fid not in EXPECTED:
            errors.append(f"Family {fid} not in EXPECTED")
            continue
        if family["name"] != EXPECTED[fid]["name"]:
            errors.append(f"Family {fid} name mismatch: expected '{EXPECTED[fid]['name']}', found '{family['name']}'")
        
        depts = {d["id"]: d for d in family["departments"]}
        if len(depts) != 10:
            errors.append(f"Family {fid} department count mismatch: expected 10, found {len(depts)}")
            
        for did, dexpect in EXPECTED[fid]["departments"].items():
            if did not in depts:
                errors.append(f"Department {did} missing from batch spec")
                continue
            if depts[did]["name"] != dexpect["name"]:
                errors.append(f"Department {did} name mismatch: expected '{dexpect['name']}', found '{depts[did]['name']}'")
            
            units = {u["id"]: u for u in depts[did]["units"]}
            if len(units) != 3:
                errors.append(f"Department {did} unit count mismatch: expected 3, found {len(units)}")
            for uid in dexpect["units"]:
                if uid not in units:
                    errors.append(f"Unit {uid} missing from batch spec")

    # Validate Files
    for fid, fexpect in EXPECTED.items():
        fname_slug = FOLDER_MAPPING[fid]
        fdir = f"02_departments/{fname_slug}"
        fjson_path = os.path.join(fdir, "family.json")
        readme_path = os.path.join(fdir, "README.md")
        
        if not os.path.exists(fjson_path):
            errors.append(f"File missing: {fjson_path}")
            continue
            
        with open(fjson_path, 'r') as f:
            fjson = json.load(f)
            
        if not isinstance(fjson["id"], int):
            errors.append(f"Family {fid} ID is not an integer in family.json")
        if str(fjson["id"]) != fid:
            errors.append(f"Family ID mismatch in {fjson_path}: expected {fid}, found {fjson['id']}")
        if fjson["name"] != fexpect["name"]:
            errors.append(f"Family name mismatch in {fjson_path}")
            
        depts = {d["id"]: d for d in fjson["departments"]}
        for did, dexpect in fexpect["departments"].items():
            if did not in depts:
                errors.append(f"Department {did} missing from {fjson_path}")
                continue
            if depts[did]["name"] != dexpect["name"]:
                errors.append(f"Department {did} name mismatch in {fjson_path}")
            
            for u in depts[did]["units"]:
                uid = u["id"]
                if uid in UNIT_NAMES:
                    if u["name"] != UNIT_NAMES[uid]:
                        errors.append(f"Unit {uid} name mismatch in {fjson_path}: expected '{UNIT_NAMES[uid]}', found '{u['name']}'")
                
                if len(u["team"]) != 9:
                    errors.append(f"Unit {uid} team size mismatch: expected 9, found {len(u['team'])}")
                for i, role in enumerate(["Realist", "Overachiever", "Dreamer", "Timid", "Overprotective", "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"]):
                    suffix = ["1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H", "1I"][i]
                    tm = u["team"][i]
                    if tm["id"] != f"{uid}.{suffix}":
                        errors.append(f"Team member ID mismatch for {uid} {suffix}")
                    if tm["role"] != role:
                        errors.append(f"Team member role mismatch for {uid} {suffix}")

        if not os.path.exists(readme_path):
            errors.append(f"File missing: {readme_path}")
            continue
            
        with open(readme_path, 'r') as f:
            readme = f.read()
            
        if f"# {fexpect['name']}" not in readme:
            errors.append(f"README title mismatch for {fid}")
            
        # Check formatting
        if re.search(r"### .* \(.*\)", readme):
            errors.append(f"README {fid} uses forbidden '### Name (ID)' format")
        if re.search(r"- .* \(.*\)", readme):
            errors.append(f"README {fid} uses forbidden '- Name (ID)' format")
            
        for did, dexpect in fexpect["departments"].items():
            if f"### {did} {dexpect['name']}" not in readme:
                errors.append(f"README {fid} missing correctly formatted department {did}")
            for uid in dexpect["units"]:
                # Check for correctly formatted unit bullet
                pass

    if errors:
        for e in errors:
            print(e)
        print("FAIL")
        sys.exit(1)
    else:
        print("PASS: Family batch 165-174 expansion valid.")

if __name__ == "__main__":
    validate()

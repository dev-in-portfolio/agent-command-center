import os
import sys

NOTE_PATH = "09_exports/pre_hiring_devinization_note.md"
REQUIRED_PHRASES = [
    "Agent Command Center — Pre-Hiring Devinization Note",
    "The 175-family Agent Command Center baseline is locked.",
    "The agents are currently defined as architecture, not yet hired or animated as runnable employees.",
    "Family 7 — Engineering & Automation was Devinized first as the build engine.",
    "Devinization must be done as overlay/extension packs",
    "The locked baseline remains the official org chart.",
    "All employees exist.",
    "All families can be considered.",
    "All governance applies.",
    "The Station Chief can consult the full map.",
    "Only expensive live execution is budgeted.",
    "Do not run 47,250 live model calls.",
    "selective live deployment",
    "Tier 0 — Passive Whole-Org Awareness",
    "Tier 1 — Council Scan",
    "Tier 2 — Command Brief",
    "Tier 3 — Active Operation",
    "Tier 4 — Audit / Archive",
    "Family 7 — Devinized Engineering Overload Pack",
    "Pack 1 — Command Brain / Devin Operating System",
    "Pack 2 — Runtime Routing & Work Control",
    "Pack 3 — Prompt, Memory & Context Architecture",
    "Pack 4 — Execution Safety, Tools & Recovery",
    "Pack 5 — Quality, Standards & Human Review",
    "Pack 6 — Output Assembly & Delivery Intelligence",
    "Pack 7 — Agent Governance, Identity & Accountability",
    "The Station Chief brain pack.",
    "The traffic-control tower pack.",
    "The memory palace / instruction engine pack.",
    "The safety cage / rollback goblin pack.",
    "The QA / compliance / grown-up supervision pack.",
    "The final packaging and version-control layer.",
    "The internal affairs / agent court pack.",
    "Do not mutate the locked baseline unless explicitly instructed.",
    "Use deterministic demo mode before expensive live execution.",
    "Require output artifacts.",
    "Require changed-file lists.",
    "Require validator results.",
    "Stop on scope drift.",
    "We are building a massive command civilization with selective live deployment — not shrinking the art piece into a tiny task bot.",
    "Station Chief runtime skeleton",
]
EXPECTED_HEADINGS = [
    "### Family 7 — Devinized Engineering Overload Pack",
    "### Pack 1 — Command Brain / Devin Operating System",
    "### Pack 2 — Runtime Routing & Work Control",
    "### Pack 3 — Prompt, Memory & Context Architecture",
    "### Pack 4 — Execution Safety, Tools & Recovery",
    "### Pack 5 — Quality, Standards & Human Review",
    "### Pack 6 — Output Assembly & Delivery Intelligence",
    "### Pack 7 — Agent Governance, Identity & Accountability",
]


def add_error(errors, message):
    errors.append(message)


def main():
    errors = []
    print("Manual scope check required: confirm git diff contains only the two allowed files.")

    if not os.path.exists(NOTE_PATH):
        add_error(errors, f"File missing: {NOTE_PATH}")
        print('FAIL')
        for err in errors:
            print(f'- {err}')
        sys.exit(1)

    text = open(NOTE_PATH, 'r', encoding='utf-8').read()

    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            add_error(errors, f"Missing required phrase: {phrase}")

    for heading in EXPECTED_HEADINGS:
        if heading not in text:
            add_error(errors, f"Missing required heading: {heading}")

    for tier in ["Tier 0", "Tier 1", "Tier 2", "Tier 3", "Tier 4"]:
        if tier not in text:
            add_error(errors, f"Missing activation tier: {tier}")

    for step in [str(i) + "." for i in range(1, 12)]:
        if step not in text:
            add_error(errors, f"Missing build order step marker: {step}")

    if errors:
        print('FAIL')
        for err in errors:
            print(f'- {err}')
        sys.exit(1)

    print('PASS: Pre-Hiring Devinization Note valid.')
    sys.exit(0)


if __name__ == '__main__':
    main()

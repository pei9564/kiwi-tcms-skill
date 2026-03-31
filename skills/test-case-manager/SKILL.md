---
name: test-case-manager
description: Manage test cases for Kiwi TCMS. Use "gen" to generate YAML test cases through a guided conversation — first clarifying feature details and reproduce steps, then generating category by category (Function → Integration → Exception → Boundary → others) with user confirmation at each step. Use "import" to import a YAML file into a Kiwi TCMS test plan by running tc_import.py.
references:
  - name: generate-test-cases
    description: Generate a YAML test case file from a feature or user flow description.
    file: references/generate-test-cases.md
  - name: import-to-kiwi
    description: Import a YAML test case file into Kiwi TCMS via import_test_cases.py.
    file: references/import-to-kiwi.md
  - name: export-from-kiwi
    description: Export test cases from a Kiwi TCMS test plan to a local YAML or CSV file.
    file: references/export-from-kiwi.md
---

# Kiwi TCMS

A skill for managing test cases with Kiwi TCMS.

- **generate-test-cases**: Given a feature description, generate a structured YAML test case file ready for import.
- **import-to-kiwi**: Import a YAML file into a Kiwi TCMS test plan.
- **export-from-kiwi**: Export test cases from a Kiwi TCMS test plan to a local YAML or CSV file.

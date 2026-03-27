"""
Import test cases from a YAML file into Kiwi TCMS.

Each test case in the YAML is created and added to the specified test plan.
Use --dry-run to preview what would be imported without making any changes.

Usage:
    python tc_import.py --file workflow_mcp_test_cases.yaml --plan-id 12
    python tc_import.py --file workflow_mcp_test_cases.yaml --plan-id 12 --tag "dify-workflow"
    python tc_import.py --file workflow_mcp_test_cases.yaml --plan-id 12 --dry-run
    python tc_import.py --file workflow_mcp_test_cases.yaml --plan-id 12 --offset 5
"""

import argparse

import yaml

from kiwi_controller import get_kiwi_ctr

PRODUCT_ID = 55        # AI Assistant
CASE_STATUS_ID = 1     # PROPOSED

PRIORITY_MAP = {1: 1, 2: 2, 3: 3}  # YAML priority → Kiwi priority ID (adjust if needed)


def format_text(steps: list[str], expected: list[str]) -> str:
    steps_text = "\n".join(steps)
    expected_text = "\n".join(f"- {e}" for e in expected)
    return (
        f"**Steps to reproduce**:\n\n{steps_text}\n\n"
        f"**Expected results**:\n\n{expected_text}"
    )


def load_yaml(file_path: str) -> list[dict]:
    with open(file_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("test_cases", [])


def get_category_map(rpc, product_id: int) -> dict[str, int]:
    """Return {category_name: category_id} for the given product."""
    categories = rpc.Category.filter({"product": product_id})
    return {c["name"]: c["id"] for c in categories}


def import_test_cases(args):
    rpc = get_kiwi_ctr()
    test_cases = load_yaml(args.file)
    category_map = get_category_map(rpc, args.product_id)

    dry_run = args.dry_run
    print(f"{'[DRY RUN] ' if dry_run else ''}Importing {len(test_cases)} test cases into plan {args.plan_id} (starting from index {args.offset}) ...")

    for tc in test_cases[args.offset:]:
        summary = tc["test_case"]
        priority = PRIORITY_MAP.get(tc.get("priority", 2), 2)
        text = format_text(tc.get("steps", []), tc.get("expected_result", []))
        category_name = tc.get("category", "")
        category_id = category_map.get(category_name) or category_map.get("--default--")
        if category_id is None:
            print(f"  [WARN] #{summary}: category '{category_name}' not found and '--default--' missing, skipping")
            continue

        if dry_run:
            print(f"  [DRY RUN] {summary} (priority={priority}, category={category_name})")
            continue

        created = rpc.TestCase.create(
            {
                "summary": summary,
                "product": args.product_id,
                "category": category_id,
                "priority": priority,
                "case_status": CASE_STATUS_ID,
                "text": text,
            }
        )
        case_id = created["id"]

        if args.tag:
            rpc.TestCase.add_tag(case_id, args.tag)

        rpc.TestPlan.add_case(args.plan_id, case_id)
        print(f"  [OK] #{case_id} {summary}")

    print("Done.")


def main():
    parser = argparse.ArgumentParser(description="Import YAML test cases into Kiwi TCMS")
    parser.add_argument("--file", required=True, help="Path to YAML test case file")
    parser.add_argument("--plan-id", required=True, type=int, help="Target test plan ID")
    parser.add_argument("--product-id", default=PRODUCT_ID, type=int, help=f"Kiwi product ID (default: {PRODUCT_ID} = AI Assistant)")
    parser.add_argument("--tag", default="", help="Tag to attach to every imported case")
    parser.add_argument("--offset", default=0, type=int, help="Skip first N test cases (default: 0)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be imported without inserting")
    args = parser.parse_args()

    import_test_cases(args)


if __name__ == "__main__":
    main()

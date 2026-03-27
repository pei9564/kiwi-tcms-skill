"""
Upsert test cases from a YAML file into a Kiwi TCMS test plan.

Match is done by summary (test_case name). If a case with the same summary
already exists in the plan, its text and priority are updated. Otherwise a
new case is created and added to the plan.

Usage:
    python tc_upsert.py --file workflow_mcp_test_cases.yaml --plan-id 12
    python tc_upsert.py --file workflow_mcp_test_cases.yaml --plan-id 12 --tag "dify-workflow"
"""

import argparse

import yaml

from kiwi_controller import get_kiwi_ctr

PRODUCT_ID = 55        # AI Assistant
CASE_STATUS_ID = 1     # PROPOSED

PRIORITY_MAP = {1: 1, 2: 2, 3: 3}


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


def get_plan_cases_by_summary(rpc, plan_id: int) -> dict[str, dict]:
    """Return a dict of {summary: case} for all cases in the plan."""
    cases = rpc.TestPlan.get_cases(plan_id)
    return {c["summary"]: c for c in cases}


def upsert_test_cases(args):
    rpc = get_kiwi_ctr()
    test_cases = load_yaml(args.file)
    existing = get_plan_cases_by_summary(rpc, args.plan_id)
    category_map = get_category_map(rpc, args.product_id)

    created_count = 0
    updated_count = 0

    for tc in test_cases:
        summary = tc["test_case"]
        priority = PRIORITY_MAP.get(tc.get("priority", 2), 2)
        text = format_text(tc.get("steps", []), tc.get("expected_result", []))

        if summary in existing:
            case_id = existing[summary]["id"]
            rpc.TestCase.update(case_id, {"priority": priority, "text": text})
            print(f"  [UPDATE] #{case_id} {summary}")
            updated_count += 1
        else:
            category_name = tc.get("category", "")
            category_id = category_map.get(category_name) or category_map.get("--default--")
            if category_id is None:
                print(f"  [WARN] {summary}: category '{category_name}' not found and '--default--' missing, skipping")
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
            print(f"  [CREATE] #{case_id} {summary}")
            created_count += 1

    print(f"\nDone. Created: {created_count}, Updated: {updated_count}")


def main():
    parser = argparse.ArgumentParser(description="Upsert YAML test cases into a Kiwi TCMS test plan")
    parser.add_argument("--file", required=True, help="Path to YAML test case file")
    parser.add_argument("--plan-id", required=True, type=int, help="Target test plan ID")
    parser.add_argument("--product-id", default=PRODUCT_ID, type=int, help=f"Kiwi product ID (default: {PRODUCT_ID} = AI Assistant)")
    parser.add_argument("--tag", default="", help="Tag to attach to newly created cases")
    args = parser.parse_args()

    upsert_test_cases(args)


if __name__ == "__main__":
    main()

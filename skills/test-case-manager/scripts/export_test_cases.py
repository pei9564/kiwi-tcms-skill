"""
Export test cases from a Kiwi TCMS test plan to YAML or CSV.

Usage:
    uv run skills/test-case-manager/scripts/export_test_cases.py --plan-id 12 --output test-cases/exported.yaml
    uv run skills/test-case-manager/scripts/export_test_cases.py --plan-id 12 --format csv --output test-cases/exported.csv
"""
# /// script
# dependencies = [
#   "tcms-api",
#   "pyyaml",
# ]
# ///

import argparse
import csv
import re

import yaml

from kiwi_controller import get_kiwi_ctr

PRIORITY_ID_MAP = {1: 1, 2: 2, 3: 3}  # Kiwi priority ID → YAML priority (adjust if needed)


def parse_text(text: str) -> tuple[list[str], list[str]]:
    """Parse Kiwi text field back into steps and expected_result lists."""
    steps, expected = [], []

    steps_match = re.search(r"\*\*Steps to reproduce\*\*:\s*\n+(.*?)(?=\n\n\*\*|\Z)", text, re.DOTALL)
    expected_match = re.search(r"\*\*Expected results\*\*:\s*\n+(.*?)(?=\n\n\*\*|\Z)", text, re.DOTALL)

    if steps_match:
        for line in steps_match.group(1).strip().splitlines():
            line = line.strip()
            if line:
                steps.append(line)

    if expected_match:
        for line in expected_match.group(1).strip().splitlines():
            line = line.strip().lstrip("- ").strip()
            if line:
                expected.append(line)

    return steps, expected


def fetch_test_cases(rpc, plan_id: int) -> list[dict]:
    cases = rpc.TestCase.filter({"plan": plan_id})
    result = []

    for case in cases:
        text = case.get("text", "")
        if text:
            steps, expected = parse_text(text)
        else:
            raw_steps = case.get("steps", "") or ""
            raw_expected = case.get("expected_result", "") or ""
            steps = [line.strip() for line in raw_steps.strip().splitlines() if line.strip()]
            expected = [line.strip() for line in raw_expected.strip().splitlines() if line.strip()]

        priority_id = case.get("priority_id") or case.get("priority", {})
        if isinstance(priority_id, dict):
            priority_id = priority_id.get("id", 2)

        cat_name = case.get("category__name") or case.get("category", {})
        if isinstance(cat_name, dict):
            cat_name = cat_name.get("name", "")

        entry = {
            "category": cat_name or "",
            "test_case": case["summary"],
            "priority": PRIORITY_ID_MAP.get(priority_id, 2),
        }

        if steps and expected:
            entry["steps"] = steps
            entry["expected_result"] = expected
        elif text:
            entry["raw_text"] = text

        result.append(entry)

    return result


def export_yaml(test_cases: list[dict], output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(
            {"test_cases": test_cases},
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )
    print(f"Exported {len(test_cases)} test cases to {output_path}")


def export_csv(test_cases: list[dict], output_path: str):
    fieldnames = ["category", "test_case", "priority", "steps", "expected_result"]
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for tc in test_cases:
            writer.writerow(
                {
                    "category": tc["category"],
                    "test_case": tc["test_case"],
                    "priority": tc["priority"],
                    "steps": "\n".join(tc["steps"]),
                    "expected_result": "\n".join(tc["expected_result"]),
                }
            )
    print(f"Exported {len(test_cases)} test cases to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Export Kiwi TCMS test cases to YAML or CSV")
    parser.add_argument("--plan-id", required=True, type=int, help="Source test plan ID")
    parser.add_argument("--format", choices=["yaml", "csv"], default="yaml", help="Output format (default: yaml)")
    parser.add_argument("--output", required=True, help="Output file path")
    args = parser.parse_args()

    rpc = get_kiwi_ctr()
    print(f"Fetching test cases from plan {args.plan_id} ...")
    test_cases = fetch_test_cases(rpc, args.plan_id)

    if args.format == "csv":
        export_csv(test_cases, args.output)
    else:
        export_yaml(test_cases, args.output)


if __name__ == "__main__":
    main()

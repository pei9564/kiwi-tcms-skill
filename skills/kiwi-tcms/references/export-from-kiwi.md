# export — Export Test Cases from Kiwi TCMS

Export test cases from a Kiwi TCMS test plan to a local YAML or CSV file by running `export_test_cases.py`.

---

## Step 0 — Environment Check

Before running anything:

1. Read `skills/kiwi-tcms/scripts/kiwi_controller.py` and show the user the current values of `KIWI_URL`, `KIWI_USERNAME`, and `KIWI_PASSWORD`. Ask:

   > 目前連線設定如下，是否正確？
   > - URL: `<current KIWI_URL>`
   > - 帳號: `<current KIWI_USERNAME>`
   > - 密碼: `<current KIWI_PASSWORD>`

   If any value is wrong, edit `skills/kiwi-tcms/scripts/kiwi_controller.py` before proceeding.

2. Run `uv --version` to verify uv is installed. If the command fails, tell the user to install uv first: `curl -LsSf https://astral.sh/uv/install.sh | sh`

---

## Step 1 — Collect Parameters

Ask the user for any missing required parameters:
- `--plan-id`: source test plan ID in Kiwi TCMS (required)
- `--output`: output file path (required). Suggest `test-cases/<feature-name>.yaml` as default
- `--format`: output format — `yaml` (default) or `csv`

---

## Step 2 — Run

Run from the project root:

```bash
uv run skills/kiwi-tcms/scripts/export_test_cases.py --plan-id <plan_id> --output <output> [--format csv]
```

---

## Step 3 — Review Output

The script prints `Exported N test cases to <path>`. Show the result to the user and tell them the output file path so they can review or pass it to the `gen` or `import` skill.

---

## Notes

- Default format is `yaml`, which is compatible with `import_test_cases.py` and `upsert_test_cases.py`.
- Use `--format csv` if the user needs to review or edit in a spreadsheet.

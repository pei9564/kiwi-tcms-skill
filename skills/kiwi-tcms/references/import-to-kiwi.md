# import — Import Test Cases into Kiwi TCMS

Import a YAML test case file into Kiwi TCMS by running `scripts/tc_import.py` via `uv run` (isolated environment, no global installs required).

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
- `--file`: path to the YAML test case file (required). Generated files are saved under `test-cases/<feature-name>.yaml`
- `--plan-id`: target test plan ID in Kiwi TCMS (required)

Optionally ask or accept:
- `--tag`: tag to attach to every imported case
- `--offset N`: skip first N test cases, useful for resuming a partial import

Always run with `--dry-run` on the first execution. Only remove it after the user confirms the dry-run output looks correct.

---

## Step 2 — Run

Run from the project root using `uv run` so dependencies are resolved in an isolated environment:

```bash
uv run skills/kiwi-tcms/scripts/import_test_cases.py --file <file> --plan-id <plan_id> [--tag <tag>] [--offset <N>] [--dry-run]
```

---

## Step 3 — Review Output

Each imported case prints `[OK] #<id> <summary>`. Show the output to the user.

If `--dry-run` was used, ask: 「結果看起來正確嗎？可以正式執行了嗎？」 and rerun without `--dry-run`.

---

## Notes

- Default product ID is `55` (AI Assistant). Pass `--product-id` only if importing into a different product.
- If a category name in the YAML doesn't match Kiwi, the case is skipped with `[WARN]` — check category names in Kiwi if this happens.

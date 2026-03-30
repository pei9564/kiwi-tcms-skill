# auto-kiwi-tcms

Claude Code skill for managing test cases with Kiwi TCMS.

## Skills

### `kiwi-tcms`

Located at `skills/kiwi-tcms/`. Contains two references:

| Reference | Description |
|-----------|-------------|
| `generate-test-cases` | Generate YAML test cases through a guided conversation — clarifies feature details step by step, then produces test cases by category (Function → Integration → Exception → Boundary → others) with confirmation at each step. Saves output to `test-cases/<feature-name>.yaml`. |
| `import-to-kiwi` | Import a YAML file into a Kiwi TCMS test plan via `import_test_cases.py`. Checks credentials and runs `--dry-run` first. |
| `export-from-kiwi` | Export test cases from a Kiwi TCMS test plan to a local YAML or CSV file via `export_test_cases.py`. |

## Scripts

Located at `skills/kiwi-tcms/scripts/`. Run with `uv run` — no global installs required.

| Script | Description |
|--------|-------------|
| `import_test_cases.py` | Create test cases from a YAML file and add them to a test plan |
| `export_test_cases.py` | Export test cases from a test plan to YAML or CSV |
| `upsert_test_cases.py` | Create or update test cases by matching on summary name |
| `kiwi_controller.py` | Shared Kiwi TCMS client setup (credentials, SSL) |

## YAML Format

Generated files are saved to `test-cases/<feature-name>.yaml`:

```yaml
test_cases:
  - category: "3.Function Test"
    test_case: "描述性的測試案例名稱"
    priority: 1
    steps:
      - "1. User 執行某操作"
      - "2. User 確認結果"
    expected_result:
      - "User 看到成功訊息"
      - "資料庫狀態更新"
```

## Requirements

- [uv](https://github.com/astral-sh/uv) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Kiwi TCMS access — configure credentials in `skills/kiwi-tcms/scripts/kiwi_controller.py`

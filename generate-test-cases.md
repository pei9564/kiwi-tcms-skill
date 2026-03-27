# Generate Test Cases

Generate a YAML test case file for the target feature based on the following guidelines.

---

## Platform Flow Context

Before generating, understand how the end user interacts with the system:

$ARGUMENTS

If no context is provided above, ask the user to describe:
1. What the platform does
2. How a user typically sets it up (e.g., create a tool, bind an API key)
3. How a user operates it day-to-day (e.g., chat with an assistant, submit a job, check status)

---

## Output Format

Generate a YAML file with the following structure:

```yaml
test_cases:
  - category: "<category code>"
    test_case: "<descriptive name from user's perspective>"
    priority: <1|2|3>
    steps:
      - "1. <action>"
      - "2. <action>"
    expected_result:
      - "<observable outcome>"
      - "<system state change>"
```

---

## Category Codes

Use exactly one of the following values for `category`:

| Code | Name |
|------|------|
| `2.Integration Test` | Cross-component or end-to-end flows |
| `3.Function Test` | Core feature behavior (happy path) |
| `4.Exception Test` | Error handling, invalid input, service failures |
| `5.Boundary Test` | Edge values, permission boundaries, empty states |
| `6.Compatibility Test` | Cross-browser, cross-device, version compatibility |
| `7.Reliability Test` | Retry, recovery, long-running stability |
| `8.Load test / Stress test` | High concurrency, queue saturation |
| `9.UX Interaction` | User-facing message clarity, flow continuity |
| `10.Performance Test` | Response time, throughput benchmarks |

---

## Priority Scale

| Value | Meaning |
|-------|---------|
| `1` | Must test — core flow or high-impact failure |
| `2` | Should test — common edge case or moderate risk |
| `3` | Nice to test — low-frequency or low-impact scenario |

---

## Writing Guidelines

**Always write from the user's perspective:**
- Steps describe what the **user does**, not what the system calls internally
- Expected results describe what the **user sees** in the interface, followed by the corresponding system state (e.g., database status)
- Avoid internal terms like "呼叫 API", "enqueue", "upsert" in steps — use natural user actions instead
- Each test case should be self-contained: include the setup (tool creation, binding) in step 1

**Style rules:**
- `test_case`: short, descriptive, no ID prefix (no "T1-1", "TC001", etc.)
- `steps`: numbered as `"1. ..."`, `"2. ..."` inside the YAML list
- `expected_result`: list each observable outcome as a separate item
- Write in Traditional Chinese (繁體中文) unless the user specifies otherwise

**Coverage checklist — make sure to include:**
- [ ] At least one full E2E happy path (`2.Integration Test`, priority 1)
- [ ] Core function tests for each major feature (`3.Function Test`, priority 1)
- [ ] Invalid input / auth failure cases (`4.Exception Test`)
- [ ] Permission boundary cases if multi-user (`5.Boundary Test`)
- [ ] Retry / failure recovery if the system has async jobs (`7.Reliability Test`)
- [ ] Cancel / stop on already-ended state (`4.Exception Test`)
- [ ] Empty state query (`5.Boundary Test`)
- [ ] Concurrent submissions if applicable (`3.Function Test`)

---

## Example Output

```yaml
test_cases:

  - category: "2.Integration Test"
    test_case: "User 完整走完一個 Workflow 從建立到取得結果"
    priority: 1
    steps:
      - "1. User 建立 Workflow Tool，填入有效的 api_key，並綁定至 Assistant"
      - "2. User 建立 Chat Topic，選擇綁定該 Assistant"
      - "3. User 詢問：「這個 Workflow 需要哪些參數？」，Agent 回覆參數列表"
      - "4. User 根據參數說：「幫我執行 Workflow，內容是 hello」"
      - "5. Workflow 執行完成後，User 詢問結果"
    expected_result:
      - "步驟 3：Agent 正確回覆參數列表"
      - "步驟 5：Agent 回覆「任務已完成」並帶出 result 內容"

  - category: "4.Exception Test"
    test_case: "User 送出 Workflow 但未提供必填參數"
    priority: 1
    steps:
      - "1. User 建立 Workflow Tool，填入有效的 api_key，並綁定至 Assistant"
      - "2. User 建立 Chat Topic，選擇綁定該 Assistant"
      - "3. User 說：「幫我執行 Workflow」（未提供必填輸入）"
    expected_result:
      - "Agent 回覆「缺少必填參數，請提供 xxx」"
      - "不寫入資料庫，不進入任務佇列"

  - category: "5.Boundary Test"
    test_case: "User 嘗試取消其他 User 建立的任務"
    priority: 1
    steps:
      - "1. User A 送出 Workflow，取得 job_id"
      - "2. User B 建立 Chat Topic，選擇綁定相同 Assistant"
      - "3. User B 說：「取消任務 xxx（User A 的 job_id）」"
    expected_result:
      - "Agent 回覆「你沒有權限取消此任務」"
      - "資料庫狀態不變"
```

---

Now generate the full test case YAML based on the platform context provided.

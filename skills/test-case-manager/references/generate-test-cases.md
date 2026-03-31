# gen — Generate Test Cases

Generate YAML test cases through a structured conversation with the user. Do NOT output any YAML until the final step.

---

## Step 0 — Feature Overview

If the user already provided a description via arguments: `$ARGUMENTS`, use it as the feature context and skip directly to Step 1.

Otherwise, ask:

> 這次要測的功能是什麼？請給一個名稱和一句話描述（之後會用名稱作為檔名）。

---

## Step 1 — Operational Detail Interview

Before writing any test cases, you need enough detail to write accurate reproduce steps. Ask the following questions **grouped into one message**:

> 為了幫你寫出具體的操作步驟，我需要多了解一些：
>
> 1. 使用介面是什麼？（Web UI / API / CLI / 其他）
> 2. 使用前需要哪些前置設定？請描述完整順序（e.g., 建立 tool → 填入 api_key → 綁定至 assistant）
> 3. 正常操作流程是什麼？User 會做哪些動作、看到哪些畫面或訊息？
> 4. 有哪些系統狀態是 user 可以觀察到的？（成功提示、錯誤訊息、資料庫狀態、頁面變化）
> 5. 有沒有多個使用者角色？（e.g., admin / 一般 user，資料是否隔離）
> 6. 有沒有非同步行為？（e.g., 背景跑任務、排隊、重試機制）

Wait for the user's answers. If any answer is unclear or too vague to write a concrete step, ask a focused follow-up before moving on.

---

## Step 2 — Function Test

Generate **Function Test** cases first and present them as a readable list:

```
### 3.Function Test — 核心功能（Happy Path）

- [ ] <test case name>（priority 1）
- [ ] <test case name>（priority 2）
...
```

Ask: 「以上 Function Test 是否符合？有要增加或移除的嗎？」

Wait for confirmation before moving to the next step.

---

## Step 3 — Integration Test

Generate **Integration Test** cases based on the confirmed Function Tests:

```
### 2.Integration Test — 完整 E2E 流程

- [ ] <test case name>（priority 1）
...
```

Ask: 「以上 Integration Test 是否符合？」

Wait for confirmation.

---

## Step 4 — Exception Test

Generate **Exception Test** cases covering error handling and invalid inputs:

```
### 4.Exception Test — 錯誤處理 / 非法輸入

- [ ] <test case name>（priority 1）
...
```

Ask: 「以上 Exception Test 是否符合？」

Wait for confirmation.

---

## Step 5 — Boundary Test

Generate **Boundary Test** cases for edge values, permissions, and empty states:

```
### 5.Boundary Test — 邊界 / 權限 / 空狀態

- [ ] <test case name>（priority 1 or 2）
...
```

Ask: 「以上 Boundary Test 是否符合？」

Wait for confirmation.

---

## Step 6 — Remaining Categories (Conditional)

Based on what you learned in Step 1, evaluate the remaining categories. For each one, explicitly tell the user whether you're including or skipping it and why. Example:

> - `7.Reliability Test`：你提到任務是非同步執行的，**納入**。
> - `6.Compatibility Test`：這次功能是純 API，無跨瀏覽器問題，**跳過**。
> - `8.Load test / Stress test`：沒有提到高併發需求，**跳過**。
> - `9.UX Interaction`：有提到錯誤訊息的呈現方式，**納入**。
> - `10.Performance Test`：沒有 response time 要求，**跳過**。
>
> 如果你認為某個類別判斷有誤，請告訴我，我會補上。

For each **included** category, present the test case list and wait for confirmation before continuing.

---

## Final — Output YAML

After all categories are confirmed, write the complete YAML file to `test-cases/<feature-name>.yaml` using the feature name established in Step 0. Tell the user the output path so they can pass it directly to the import skill.

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

## Writing Guidelines

**Always write from the user's perspective:**
- Steps describe what the **user does**, not what the system calls internally
- Expected results describe what the **user sees**, followed by the system state (e.g., database status)
- Avoid internal terms like "呼叫 API", "enqueue", "upsert" — use natural user actions instead
- Each test case must be self-contained: include the full setup in step 1

**Style rules:**
- `test_case`: short, descriptive, no ID prefix (no "T1-1", "TC001")
- `steps`: numbered as `"1. ..."`, `"2. ..."` inside the YAML list
- `expected_result`: each observable outcome as a separate list item
- Write in Traditional Chinese (繁體中文) unless the user specifies otherwise

**Priority scale:**
| Value | Meaning |
|-------|---------|
| `1` | Must test — core flow or high-impact failure |
| `2` | Should test — common edge case or moderate risk |
| `3` | Nice to test — low-frequency or low-impact scenario |

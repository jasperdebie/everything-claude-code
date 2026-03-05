---
name: portfolio-dashboard
description: >-
  Weekly innovations and solutions status dashboard for the SAP Platform Unit.
  Use this skill whenever the user mentions innovations, solutions, the innovation
  pipeline, solution status, solution health, or the innovations portfolio. Triggers
  on phrases like: "status of innovations", "solutions overview", "innovation
  dashboard", "how are our solutions doing", "solution health check", "innovations
  sweep", "which innovations are stale", "prep innovations for MT", "innovation
  pipeline", "solutions report", "what's happening with our innovations",
  "innovation audit", "solutions dashboard", "show me inactive innovations",
  "stale solutions", "weekly innovations update", or any request to review the
  state of innovations and solutions tracked in Airtable, cross-referenced with
  Notion and Outlook activity. This skill replaces manual check-ins by
  automatically sweeping all sources and producing an actionable summary.
---

# Portfolio Dashboard

Generates a cross-source portfolio status report by sweeping Airtable projects, Notion activity, and Outlook email threads. Designed for weekly cadence but can run on demand.

## Constants

- Airtable base ID: `appobZwKJ0JMUTZbc`
- Projects table ID: `tblz7PlpTC5NXiSzV`
- Solutions table ID: `tblwJJjYdnolJxA1x`
- Goals table ID: `tblkvB91qtDgJIhzK`
- Status reports table ID: `tbltwuqRroP2OG0GT`
- Stale threshold: 14 days (no detectable activity across any source)

## Phase 1: Load the full project portfolio from Airtable

### Step 1: Fetch all projects

Call `Airtable MCP Server:list_records` with:
- `baseId`: `appobZwKJ0JMUTZbc`
- `tableId`: `tblz7PlpTC5NXiSzV`
- `maxRecords`: 100

### Step 2: Fetch Solutions for grouping context

Call `Airtable MCP Server:list_records` with:
- `baseId`: `appobZwKJ0JMUTZbc`
- `tableId`: `tblwJJjYdnolJxA1x`
- `maxRecords`: 50

Build a lookup map: solution record ID → solution name. This allows grouping projects by solution in the final report.

### Step 3: Classify projects

For each project, extract and store:
- Name
- Project status (Idea / Concept / Validation / Implementation / Delivery & Scale)
- Solution name (resolved via lookup)
- Owner (record IDs — resolve names if possible)
- Start date, End date, Original End Date
- Risk level
- Budget, ETC, Invested Mandays
- Type (Development / Research / Implementation / etc.)
- Project Nature (Time-bound / Continuous / Recurring)
- Complete (checkbox)
- To be discussed (checkbox)
- Blocked By (linked records)
- Description of Project (first 200 chars for context)

Partition projects into:
1. **Active**: not marked Complete, has a Project status that is not empty
2. **Completed**: marked Complete
3. **Flagged for discussion**: "To be discussed" = true

---

## Phase 2: Cross-source activity detection

For each active project (or a representative sample if >30 projects — pick top 20 by recency of dates + all in Implementation/Delivery & Scale), check for recent activity across Notion and Outlook. The goal is to determine which projects have had meaningful activity in the past 14 days and which are stale.

### 2a: Notion activity scan

For each project (batch by searching 3-5 project names per query to reduce tool calls):

Call `notionMCP:notion-search` with:
- `query`: the project name (or a distinctive keyword from the name)

Record whether any Notion pages were found with recent edits (within past 14 days based on page metadata). Note the most recent page title and edit date.

Limit: do not exceed 15 Notion search calls total. Prioritize projects in Implementation/Delivery & Scale, then Validation, then Concept, then Idea.

### 2b: Outlook activity scan

For each project (or group of related projects):

Call `Microsoft 365:outlook_email_search` with:
- `query`: project name keywords (use the most distinctive 2-3 words)
- `afterDateTime`: 14 days ago
- `limit`: 3

Record whether any emails were found. Note the most recent email subject and date.

Limit: do not exceed 15 Outlook search calls total. Same priority order as Notion.

### 2c: Activity determination

For each project, classify activity status:
- **Active**: Notion page edit or Outlook email found within 14 days
- **Low activity**: activity found but only 1 signal (either Notion or Outlook, not both)
- **Stale**: no activity found in either source within 14 days
- **Not scanned**: project was deprioritized in the sampling (mention this in the report)

---

## Phase 3: Compute portfolio health metrics

Calculate:
1. Total project count (active, completed, by status)
2. Projects per Solution
3. Projects per status stage (pipeline funnel: Idea → Concept → Validation → Implementation → Delivery & Scale)
4. Stale project count and percentage
5. Budget utilization: sum of Invested Mandays vs. sum of Budget (#days) for projects with data
6. Overdue projects: End date < today and not Complete
7. Risk distribution: count per risk level
8. Projects flagged "To be discussed"
9. Blocked projects: any with non-empty "Blocked By"

---

## Phase 4: Generate the report

Present the report in the following structure. Use the user's language (Dutch if the request was in Dutch, English otherwise).

---

### Portfolio Status Dashboard — [Date]

**Summary metrics** (present as a compact table or key-value pairs):
- Total active projects: [n]
- By stage: Idea [n] · Concept [n] · Validation [n] · Implementation [n] · Delivery & Scale [n]
- Stale (>14d no activity): [n] ([%])
- Overdue: [n]
- Blocked: [n]
- Budget utilization: [invested]/[budget] mandays ([%])

---

**Stale project alert** (projects with no detected cross-source activity in 14 days):

For each stale project, list:
- Project name
- Solution
- Status stage
- Last known activity (date + source, or "none found")
- Recommended action: archive / re-scope / schedule owner check-in / escalate

---

**Overdue projects** (End date passed, not Complete):

For each:
- Project name, original end date, current status
- Days overdue
- Owner

---

**Blocked projects**:

For each:
- Project name
- Blocked by (project names)
- Status of blocking project

---

**Projects flagged for discussion** ("To be discussed" = true):

List with name, solution, status, and description excerpt.

---

**Pipeline by Solution** (grouped view):

For each Solution with projects:
- Solution name
- Project count
- Stage distribution
- Key highlights or concerns (stale, overdue, blocked projects within this solution)

---

**Budget overview** (only for projects with budget data):

Table: Project name | Budget (days) | Invested | ETC | Utilization % | Status

---

**Recommendations**:

Based on the data, provide 3-5 actionable recommendations. Examples:
- "X projects in Idea stage have been there for >3 months with no activity — consider archiving or scheduling a go/no-go review."
- "Y% of the portfolio is in early stages (Idea/Concept) with no implementation pipeline — consider prioritizing advancement of Z."
- "Project A is blocked by Project B which is itself stale — escalation needed."
- "Budget utilization across Implementation projects is at X% — review resource allocation."

---

## Important behaviors

- Begin data collection immediately upon receiving the request. Do not ask for confirmation.
- If the user asks for a "quick overview" or "summary only", skip Phase 2 (cross-source scanning) and generate the report from Airtable data alone. Note in the report that cross-source activity was not checked.
- Respect tool call budgets: max 15 Notion searches, max 15 Outlook searches, on top of the Airtable calls. This keeps the total under 40 tool calls.
- If the user specifies a scope (e.g., "just the security projects" or "only Implementation stage"), filter accordingly before running Phase 2.
- Dates are relative to today. Calculate staleness and overdue status dynamically.
- Do not create or modify any records. This skill is read-only.
- If the user asks to create a Notion page with the report, offer to do so after presenting it.
- Match language to the user's request language.

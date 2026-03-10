---
name: update-notion-task
description: >-
  Update an existing task in the Notion "All Tasks" database. Use when the user
  wants to update a task, change a property, add an update, mark as done, change
  priority, move kanban state, or modify task content. Triggers on phrases like:
  update task, wijzig taak, change task, mark as done, zet op done, add update,
  update toevoegen, verander prioriteit, change priority, move to doing.
---

# Update Notion Task

This skill updates existing tasks in the Notion "All Tasks" database — properties, body content, or both.

## Database Reference

- **All Tasks** data source: `collection://5f831004-6192-491e-bf5c-0b134a176bd2`
- **Projects** data source: `collection://29b68c24-ec8b-409d-a37d-bde6fc8a9244`

## Phase 1: Find the task

### Step 1: Parse the user's request

Extract from the user's message:
- **Which task** to update — task name, ticket number, or other identifier
- **What to change** — which properties or body sections need updating

### Step 2: Search for the task

Call `notionMCP:notion-search` with the task name or identifier. If multiple results match, present the top matches and ask the user to pick the correct one.

If the user provides a Notion page URL directly, skip the search and use the URL.

### Step 3: Fetch current task state

Call `notionMCP:notion-fetch` with the page URL to retrieve the current properties and body content. This ensures you know the current values before making changes.

Present the current state to the user so they can see what exists.

---

## Phase 2: Determine changes

### Step 1: Compare current vs requested

Based on the user's request, determine which properties and/or body sections need to change. Only modify what the user explicitly asks to change — do not touch other properties or content.

### Step 2: Confirm before updating

Present the changes to the user:

```
Task: [current task name]
Changes:
  - [field]: [old value] → [new value]
  - [field]: [old value] → [new value]
  - Body: [which sections will be updated]
```

Ask: "Klopt dit? Mag ik de taak updaten?" — wait for confirmation before proceeding.

---

## Phase 3: Update the task

### Step 1: Update properties

If properties need to change, call `notionMCP:notion-update-page` with the page URL and only the properties that are changing.

**Properties** (only include fields that are changing):

| Field | How to set |
|-------|-----------|
| **Task** | Title — the task name |
| **Project** | Relation — array of project page URLs. **NEVER create a new project — always use an existing project from the Projects database.** |
| **Priority** | Select — one of: `1. HIGH`, `2. Medium`, `3. Low`, `4. Evening`, `5. Feedback`, `Follow-up` |
| **Kanban - State** | Select — see Kanban State Mapping below |
| **Due** | Date — ISO-8601 format |
| **Final Due** | Date — only if a hard deadline is specified separately from Due |
| **Start** | Date — only if specified |
| **Assignee** | Person — only if specified |
| **Ticket** | Text — Solman ticket number (10-digit) or other external reference |
| **Follow-up** | Checkbox — true/false |
| **Kanban - Tag** | Select — `Follow-up` or `Waiting on input` if applicable |
| **Mail** | Text — email reference if applicable |
| **FUP** | Text — follow-up notes if applicable |
| **Recur Interval** | Number — only for recurring tasks |
| **Recur Unit** | Select — one of: `Day(s)`, `Week(s)`, `Month(s)`, `Month(s) on the Last Day`, `Month(s) on the First Weekday`, `Month(s) on the Last Weekday`, `Year(s)` |
| **Days (Only if Set to 1 Day(s))** | Multi-select — specific weekdays |

### Step 2: Update body content (if requested)

If the user wants to update body content, use `notionMCP:notion-update-page` with `command: "update_content"` using search-and-replace.

**CRITICAL:** Only use `update_content` (search-and-replace), NEVER use `replace_content`. The template contains button elements and AI blocks that must be preserved. Only replace the specific text that needs changing — do not touch any other content in the page.

#### Adding an Update entry

If the user wants to add an update/status note, insert it in the **Updates** section. Updates MUST follow this exact structure (insert after the button element, before existing updates or `<empty-block/>`):

```markdown
### <mention-date start="YYYY-MM-DD" startTime="HH:MM" timeZone="Europe/Brussels"/>  {toggle="true"}
	The update text goes here, indented with a tab.
```

New updates are added at the top (newest first), below the button but above older updates.

#### Updating Check-box Tasks

- To add new checkboxes, append them after existing ones
- To check/uncheck items, replace `- [ ] item` with `- [x] item` or vice versa
- To remove items, replace the line with empty string

#### Updating Summary

Replace the existing summary text with the new summary. Write thorough summaries — include all available context: what the task is about, why it exists, background information, relevant details, links, names of people involved, and any decisions or constraints.

#### Updating Key Points

Add or modify key points inside the toggle.

### Step 3: Confirm success

After updating, present:
- The task name with a link to the Notion page
- A summary of which fields were changed
- Which body sections were updated (if any)

---

## Priority Mapping

When the user describes urgency informally, map it:

| User says | Priority value |
|-----------|---------------|
| urgent, critical, ASAP, belangrijk | `1. HIGH` |
| normal, medium, gewoon | `2. Medium` |
| low, later, kan wachten, niet dringend | `3. Low` |
| tonight, vanavond, 's avonds | `4. Evening` |
| review, feedback, nakijken | `5. Feedback` |
| follow-up, opvolgen | `Follow-up` |

## Kanban State Mapping

| User says | State value |
|-----------|------------|
| small task, quick, klein | `0. To Do Small` |
| to do, nieuw | `1. To Do` |
| planning, moet nog plannen | `2. Planning` |
| working on, bezig | `3. Doing` |
| guard, monitor, bewaken | `4. Guard` |
| waiting, wacht op input | `5. Input Needed` |
| done, klaar, afgerond | `6. Done` |
| project without deadline | `7. Project Wo Due` |
| meeting | `8. Meetings` |

## Common update scenarios

| User says | Action |
|-----------|--------|
| "zet op done" / "mark as done" | Set `Kanban - State` to `6. Done` |
| "verander prioriteit naar high" | Set `Priority` to `1. HIGH` |
| "voeg een update toe" | Add an Update entry with today's date/time |
| "due date naar vrijdag" | Set `Due` to the next Friday's date |
| "koppel aan project Renson" | Search Projects for Renson, set `Project` relation |
| "verwijder de due date" | Clear the `Due` field |
| "zet op doing" / "ik ben ermee bezig" | Set `Kanban - State` to `3. Doing` |
| "voeg checkbox toe: X" | Append `- [ ] X` to Check-box Tasks section |

## Important behaviors

- Always fetch the current task state before updating — never update blindly.
- Always confirm with the user before making changes.
- Match the user's language (Dutch or English).
- Only change what the user asks — do not modify unrelated properties or content.
- If the user says "zet op done" without specifying a task, ask which task to update.
- Solman ticket numbers are 10-digit numbers (e.g. `4000150560`, `8300007744`). Detect these automatically.
- Do NOT modify formula, rollup, or automatic fields (Created, Edited, State, Type, Cold, Late, etc.) — these are computed by Notion.
- NEVER create subtasks or use the Parent Task / Sub-Tasks fields.
- **NEVER create a new project.** Always search and use existing projects from the Projects database. Known customers: **Renson**, **Milcobel**, **Joris Ide**, **delaware**, **Fluvius**. If the project is not found, ask the user — do not create one.
- When adding updates, always use the current date and time with timezone `Europe/Brussels`.

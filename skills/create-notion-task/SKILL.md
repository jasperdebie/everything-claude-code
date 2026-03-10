---
name: create-notion-task
description: >-
  Create a new task in the Notion "All Tasks" database following the established
  task management workflow. Use when the user wants to create a task, add a todo,
  log a ticket, or track work in Notion. Triggers on phrases like: create task,
  new task, add to notion, maak een taak, nieuwe taak, log this in notion,
  create a ticket, track this.
---

# Create Notion Task

This skill creates tasks in the Notion "All Tasks" database with the correct properties and body template.

## Database Reference

- **All Tasks** data source: `collection://5f831004-6192-491e-bf5c-0b134a176bd2`
- **Projects** data source: `collection://29b68c24-ec8b-409d-a37d-bde6fc8a9244`

## Phase 1: Gather task information

### Step 1: Parse the user's request

Extract from the user's message:
- **Task name** (required)
- **Project** — customer or project name
- **Priority** — any urgency indicators
- **Due date** — any mentioned deadlines
- **Ticket number** — Solman ticket (10-digit, e.g. `4000150560`, `8300007744`) or other external reference
- **Recurring** — any mention of recurring/repeating

### Step 2: Resolve the Project relation

If a project is mentioned, search for it in the Projects database:

Call `notionMCP:notion-search` with the project or customer name. Match against known projects. If ambiguous, ask the user to clarify.

Known customers in the Projects database: **Renson**, **Milcobel**, **Joris Ide**, **delaware**, **Fluvius**.

### Step 3: Confirm before creating

Present the task details to the user for confirmation:

```
Task: [name]
Project: [project name]
Priority: [priority]
Kanban State: [state]
Due: [date if any]
Ticket: [ticket if any]
Recurring: [interval + unit if any]
```

Ask: "Klopt dit? Mag ik de taak aanmaken?" — wait for confirmation before proceeding.

---

## Phase 2: Create the task

### Step 1: Create the page

Call `notionMCP:notion-create-pages` with:

**Parent:** The "All Tasks" database URL: `https://www.notion.so/3436c8e925eb4810b85de72948fa9422`

**Properties** (only include fields that have values):

| Field | How to set |
|-------|-----------|
| **Task** | Title — the task name |
| **Project** | Relation — array of project page URLs from Phase 1 |
| **Priority** | Select — one of: `1. HIGH`, `2. Medium`, `3. Low`, `4. Evening`, `5. Feedback`, `Follow-up` |
| **Kanban - State** | Select — default to `1. To Do` unless user specifies otherwise |
| **Due** | Date — ISO-8601 format if provided |
| **Final Due** | Date — only if a hard deadline is specified separately from Due |
| **Start** | Date — only if specified |
| **Assignee** | Person — only if specified |
| **Ticket** | Text — Solman ticket number (10-digit) or other external reference |
| **Follow-up** | Checkbox — set to true if user indicates follow-up needed |
| **Kanban - Tag** | Select — `Follow-up` or `Waiting on input` if applicable |
| **Mail** | Text — email reference if applicable |
| **FUP** | Text — follow-up notes if applicable |
| **Recur Interval** | Number — only for recurring tasks |
| **Recur Unit** | Select — one of: `Day(s)`, `Week(s)`, `Month(s)`, `Month(s) on the Last Day`, `Month(s) on the First Weekday`, `Month(s) on the Last Weekday`, `Year(s)` |
| **Days (Only if Set to 1 Day(s))** | Multi-select — specific weekdays, only when Recur Interval=1 and Recur Unit=Day(s) |

### Step 2: Add the body template

The page body MUST follow the "New page" template structure. Include this content in the page creation:

```markdown
## Key Points
(empty toggle section)

## Check-box Tasks
- [ ] .

## Meetings
(empty section)

## Updates
(empty section)

## Summary
```

**Note:** The AI block and button elements from the original template cannot be created via API. The toggle and checkbox structure is the essential part.

### Step 3: Confirm success

After creation, present:
- The task name with a link to the created Notion page
- A summary of which fields were set

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
| to do, nieuw (default) | `1. To Do` |
| planning, moet nog plannen | `2. Planning` |
| working on, bezig | `3. Doing` |
| guard, monitor, bewaken | `4. Guard` |
| waiting, wacht op input | `5. Input Needed` |
| done, klaar, afgerond | `6. Done` |
| project without deadline | `7. Project Wo Due` |
| meeting | `8. Meetings` |

## Important behaviors

- Always confirm with the user before creating the task.
- Match the user's language (Dutch or English).
- If the user provides minimal info (just a task name), create the task with defaults: `Kanban - State: 1. To Do`, no priority, no due date.
- If the user mentions a customer name, search Projects first to link the correct project.
- Solman ticket numbers are 10-digit numbers (e.g. `4000150560`, `8300007744`). Detect these automatically and put them in the Ticket field.
- Do NOT fill in formula, rollup, or automatic fields (Created, Edited, State, Type, Cold, Late, etc.) — these are computed by Notion.
- NEVER create subtasks or use the Parent Task / Sub-Tasks fields. Always create tasks as top-level items. The user does not use the subtask hierarchy.

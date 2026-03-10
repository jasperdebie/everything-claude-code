---
description: Create a new task in Notion's All Tasks database with the correct properties and body template. Use when you want to quickly add a task, log a ticket, or track work.
---

# Create Task Command

This command invokes the **create-notion-task** skill to create a new task in the Notion "All Tasks" database.

## What This Command Does

1. **Parse your request** — extracts task name, project, priority, due date, ticket number, and other details
2. **Resolve project** — finds the correct project in Notion to link to
3. **Confirm** — shows you what will be created before proceeding
4. **Create the task** — creates the page with properties and the standard body template (Key Points, Check-box Tasks, Meetings, Updates, Summary)

## When to Use

Use `/create-task` when:
- You want to add a new task to Notion
- You want to log a Solman ticket as a task
- You need to track a follow-up as a Notion task
- You want to quickly create a task with the right template

## Example Usage

```
User: /create-task SAP transport voor Renson, priority high, due vrijdag
User: /create-task Solman ticket 4000150560 opvolgen voor Joris Ide
User: /create-task Documentatie schrijven voor het migration project
User: /create-task Weekly status update, recurring elke week op maandag
```

## Related Skills

This command uses the full skill definition at `skills/create-notion-task/SKILL.md`.

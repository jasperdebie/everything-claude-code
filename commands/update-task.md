---
description: Update an existing task in Notion's All Tasks database — change properties, add updates, mark as done, or modify content.
---

# Update Task Command

This command invokes the **update-notion-task** skill to update an existing task in the Notion "All Tasks" database.

## What This Command Does

1. **Find the task** — searches Notion for the task by name, ticket number, or URL
2. **Fetch current state** — retrieves current properties and body content
3. **Confirm changes** — shows you what will change before proceeding
4. **Update the task** — modifies only the requested properties and/or body sections

## When to Use

Use `/update-task` when:
- You want to change a task's status, priority, due date, or other properties
- You want to add an update/status note to a task
- You want to mark a task as done
- You want to add or modify checkbox items
- You want to update the summary or key points
- You want to link a task to a different project

## Example Usage

```
User: /update-task Zet "SAP transport Renson" op done
User: /update-task Verander prioriteit van ticket 4000150560 naar high
User: /update-task Voeg update toe aan "Migration project": vandaag overleg gehad met klant
User: /update-task Due date van "Documentatie schrijven" naar volgende week vrijdag
User: /update-task Mark "Weekly status update" as doing
User: /update-task Voeg checkbox "tests schrijven" toe aan "Renson transport"
```

## Related Skills

This command uses the full skill definition at `skills/update-notion-task/SKILL.md`.

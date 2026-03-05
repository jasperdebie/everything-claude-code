---
description: Automated meeting preparation and pre-meeting briefing. Use when the user wants to prepare for a meeting, get a briefing, or review upcoming calendar events.
---

# Meeting Prep Command

This command invokes the **meeting-prep** skill to generate comprehensive pre-meeting briefings.

## What This Command Does

1. **Identify target meeting(s)** from Outlook calendar
2. **Gather cross-source context** from Outlook email, Notion (pages + meeting notes), and Airtable
3. **Generate a structured briefing** with background, open items, recent developments, talking points, key data, and gaps

## When to Use

Use `/meeting-prep` when:
- Preparing for an upcoming meeting
- You want a briefing before a call
- You need to know what's on your calendar
- You want context pulled from all sources for a specific meeting

Trigger phrases: "prep meeting", "prepare my meeting", "brief me for", "what do I need to know for", "get me ready for", "prep today's meetings", "prepare for tomorrow"

## How It Works

The skill follows three phases:

### Phase 1: Identify the target meeting(s)
- Parses your request for subject keywords, time scope, and attendee names
- Searches Outlook calendar to find matching events
- Reads full meeting details (attendees, body, links)

### Phase 2: Gather cross-source context
Runs in parallel across all available sources:
- **Notion meeting notes** — prior occurrences, action items, decisions
- **Outlook email** — related threads from the past 14 days
- **Notion tasks** — open items related to the meeting topic or project
- **Airtable** — project status if the meeting relates to a tracked initiative

### Phase 3: Generate the briefing
Structured output with:
1. Context and background
2. Open items from last time (with completion status)
3. Recent developments (sourced from email, Notion, Airtable)
4. Suggested talking points (prioritized)
5. Key data points
6. Gaps (what couldn't be found)

## Example Usage

```
User: /meeting-prep prep my next meeting
User: /meeting-prep brief me for tomorrow's meetings
User: /meeting-prep prepare for the LeanIX call
```

## Related Skills

This command uses the full skill definition at `skills/meeting-prep/SKILL.md`.

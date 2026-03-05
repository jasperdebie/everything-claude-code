---
name: meeting-prep
description: >-
  Automated meeting preparation and pre-meeting briefing. Use this skill
  whenever the user wants to prepare for a meeting, get a briefing before a
  meeting, or review what's coming up on their calendar. Triggers on phrases
  like: prepare my meeting, brief me for, prep for, what do I need to know
  for, get me ready for, meeting prep, prepare for my call with, prep my
  next meeting, prep today's meetings, what's on my calendar, prepare for
  tomorrow, brief me on my calls today, what meetings do I have, get me
  ready for the status call. This skill orchestrates Outlook calendar,
  Outlook email, Notion (including meeting notes), and Airtable to build
  comprehensive briefings before any meeting.
---

# Meeting Prep

This skill generates comprehensive pre-meeting briefings by pulling context from Outlook calendar, Outlook email, Notion (pages and meeting notes), and Airtable.

### Phase 1: Identify the target meeting(s)

#### Step 1: Parse the user's request

Extract:
- Meeting subject keywords (if specified)
- Time scope: "my next meeting", "today's meetings", "tomorrow", "the JI status call", a specific date, etc.
- Attendee names (if mentioned)

#### Step 2: Search the calendar

Call `Microsoft 365:outlook_calendar_search` with:
- `query`: subject keywords, or `*` if the user asked about a time range
- `afterDateTime` / `beforeDateTime`: derived from the time scope
- `limit`: 10 (reduce noise)
- `attendee`: if the user specified a person

If time scope is vague ("my next meeting"), search from now to +24h.
If the user said "today's meetings", search from start of today to end of today.

#### Step 3: Select meeting(s)

- Single clear match → proceed.
- Multiple matches and user asked for a specific meeting → list them (subject, time, attendees) and ask which one.
- Multiple matches and user asked for "all" or "today" → process each meeting, presenting briefings sequentially.
- No results → broaden the search window or query. Inform the user if still nothing.

#### Step 4: Read meeting details

Call `Microsoft 365:read_resource` with the calendar event URI to get full details: body, attendees, location, recurrence info, and any attachments or links.

Extract from the meeting details:
- All attendee names and email addresses
- Meeting subject and body content
- Any linked documents or agenda items mentioned in the body
- Recurrence pattern (to determine if this is a regular meeting with prior occurrences)

---

### Phase 2: Gather cross-source context

Run these searches in the same turn. Skip a source if it is clearly irrelevant to the meeting topic.

#### 2a: Previous meeting notes (Notion)

This is the highest-value source — prior meeting notes establish continuity.

Call `notionMCP:notion-search` with:
- The meeting subject or key topic words
- Attendee names if the subject is generic (e.g., "Weekly sync")

Also call `notionMCP:notion-query-meeting-notes` with:
- A title filter matching the meeting subject (break into individual terms, use OR)
- A date filter for the past 30 days (to find the most recent prior occurrence)
- An attendee filter if relevant

If results are found, call `notionMCP:notion-fetch` on the top 1-2 most relevant pages to get full content. Extract:
- Previous action items and their completion status
- Decisions made
- Open questions carried forward
- Topics discussed

#### 2b: Related email threads (Outlook)

Call `Microsoft 365:outlook_email_search` with:
- `query`: meeting subject keywords
- `afterDateTime`: 14 days ago (recent context)
- `limit`: 10

Also search by attendee if the meeting involves a specific external party:
- `sender` or `recipient`: key attendee email
- `query`: refined topic keywords
- `limit`: 5

Read the 1-3 most relevant emails via `read_resource` if their subjects suggest they contain context for this meeting (decisions, requests, open threads).

#### 2c: Related tasks (Notion)

Call `notionMCP:notion-search` with queries targeting:
- Open tasks related to the meeting subject
- Tasks assigned to or involving the attendees

If the meeting is about a specific project, also search for that project name to find its Notion page and linked tasks.

#### 2d: Project status (Airtable)

Only if the meeting relates to a tracked project or initiative:

Call `Airtable MCP Server:search_records` with:
- The project or initiative name
- Search in the user's primary project tracking base

If the base/table is unknown, call `Airtable MCP Server:list_bases` then `Airtable MCP Server:list_tables` to locate the project tracker. Cache this for the conversation.

Extract: current status, phase, owner, recent updates, blockers.

#### Research boundaries

- Do not exceed 25 total tool calls across all sources in Phase 2.
- Prioritize depth on the most relevant source over breadth across all sources.
- Stop searching a source if the first query returns nothing relevant.

---

### Phase 3: Generate the briefing

Present the briefing in this structure:

---

**Meeting briefing: [Meeting Subject]**
[Date] · [Time] · [Duration] · [Location/Link]

**Attendees:** [list with roles if known]

**1. Context and background**
A concise paragraph summarizing what this meeting is about, based on the meeting description and cross-source research. If this is a recurring meeting, note when the last occurrence was and what was discussed.

**2. Open items from last time**
A numbered list of action items or decisions from the previous meeting. For each:
- The item itself
- Current status (completed / in progress / not started / unknown)
- Source: where this was tracked (Notion task, email confirmation, etc.)

If no previous meeting notes were found, state: "No prior meeting notes found in Notion."

**3. Recent developments**
Bullet points of relevant activity since the last meeting, sourced from:
- Email threads (key decisions, requests, escalations)
- Notion task updates
- Airtable project status changes

Each item should reference its source briefly.

**4. Suggested talking points**
Based on the open items and recent developments, suggest 3-5 discussion topics for the meeting, ordered by priority. For each:
- The topic
- Why it matters now
- Any preparation needed (a document to review, a number to look up, a decision to be ready for)

**5. Key data points**
Any specific numbers, dates, or facts that are likely to come up: project milestones, budget figures, deadline dates, system statuses. Only include if found in the research — do not speculate.

**6. Gaps**
Note anything that could not be determined from available sources but would be useful for the meeting. Be explicit about what was searched and not found.

---

If the user asked for briefings on multiple meetings (e.g., "prep today's meetings"), present each briefing as a separate section with a clear separator, ordered chronologically.

---

## Important behaviors

- Never ask permission to search before searching. Begin research immediately after identifying the target meeting.
- Phase 2 research is automatic. Do not ask "shall I look for context?" — just do it.
- If the user says "just the agenda" or "quick prep", skip the deep research and generate a lighter briefing based on the calendar event details alone.
- Match the language of the meeting context: if the meeting subject and participants are Dutch-speaking, the briefing can be in Dutch. If English, use English. Follow the user's language in the request.
- Keep briefings focused on actionability. The user needs to know what to prepare, what to expect, and what to bring up — not a comprehensive history of everything tangentially related.
- Post-meeting notes and action item capture are handled by Notion natively. This skill does not cover post-meeting workflows.

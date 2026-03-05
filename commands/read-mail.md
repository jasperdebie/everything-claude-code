---
description: Read an Outlook email by subject, then automatically research related context across Outlook, Notion, Airtable, and the web. Produces five reply options including a deep-research-informed reply and a challenger reply.
---

# Read Mail Command

This command invokes the **read-email** skill to retrieve an Outlook email and automatically research related context across multiple sources, producing actionable reply drafts.

## What This Command Does

1. **Find and Read Email** - Search Outlook by subject, sender, or date and display full content
2. **Research Context** - Automatically search Outlook threads, Notion, Airtable, and the web
3. **Synthesize Findings** - Present context summary, action items, and knowledge gaps
4. **Draft Replies** - Generate 5 reply options with different tones and approaches

## When to Use

Use `/read-mail` when:
- You want to read and understand a specific email
- You need context from multiple sources to respond effectively
- You want draft replies with different approaches
- You need to identify action items from an email

## How It Works

### Phase 1: Retrieve the Email
1. Parse subject keywords, sender, and date hints from your request
2. Search Outlook and select the correct email
3. Display full email content (From, To, CC, Date, Subject, Body, Attachments)

### Phase 2: Extract Research Targets
- Key topics, entities, project names
- Action items and questions raised
- References to documents, tickets, or prior conversations

### Phase 3: Cross-Source Research (automatic)
- **Outlook** - Related threads and recent emails from the sender
- **Notion** - Related pages, tasks, and projects
- **Airtable** - Related records and entities
- **Web** - External context for deep-research reply (technical specs, industry info, best practices)

### Phase 4: Synthesize and Respond
1. **Context summary** - Organized by relevance, with source attribution
2. **Action items** - Clear actions with deadlines, urgency, and dependencies
3. **Five reply drafts:**
   - **Concise** - Direct and to the point
   - **Detailed** - Covers all aspects thoroughly
   - **Diplomatic** - Cautious tone for sensitive topics
   - **[Deep Research]** - Grounded in external web research with cited sources
   - **[Challenger]** - Constructively questions assumptions and proposes alternatives
4. **Gaps** - Topics where no information was found

## Example Usage

```
User: /read-mail Check the email about the SAP migration timeline

Agent:
## Email Found
From: john.doe@client.com | Date: 2026-03-04
Subject: RE: SAP S/4HANA Migration - Updated Timeline

[Full email content displayed]

## Context Summary
- Prior thread (3 emails) discusses original Q3 deadline...
- Notion project page shows 4 open blockers...
- Airtable resource allocation shows 2 consultants assigned...

## Action Items
1. Respond to timeline change request by Friday (urgent)
2. Update project plan in Notion with new milestones

## Reply Options
1. [Concise] "Thanks John, acknowledged..."
2. [Detailed] "Thank you for the updated timeline..."
3. [Diplomatic] "We appreciate the transparency..."
4. [Deep Research] "Based on SAP's latest migration guide..."
5. [Challenger] "Have we considered an alternative phased approach..."

## Gaps
- No information found regarding budget impact in any source.
```

## Important Notes

- Research happens automatically - no confirmation needed before searching
- If you only want the email content without research, say "just show me the email"
- Reply tone matches the original email thread language (English/Dutch/formal/informal)

## Integration with Other Commands

- Use `/plan` to create an action plan based on email findings
- Use `/md2word` to formalize a response as a Word document

---
name: read-email
description: >-
  Read the full content of an Outlook email by subject line, then automatically
  research related context across Outlook, Notion, Airtable, and the web to help
  the user understand and respond to the email. Produces five reply options
  including one deep-research-informed reply backed by external web sources and
  one challenger reply that questions assumptions and proposes alternatives. Use
  this skill whenever the user says things like help mail, read my email about,
  what does the email about X say, find the email titled, check the mail from
  about, get me the email regarding, handle the email about, help me respond to
  the email about, or any variation where the user wants to see the content of a
  specific email and get context to act on it. Also triggers when the user
  provides an email subject in quotes and expects its content or a suggested
  response. This skill handles the full pipeline from search to read to
  cross-source research to synthesized answer.
---

# Read Email and Research Context

This skill retrieves the full content of an Outlook email, then searches across Outlook, Notion, Airtable, and the web for related information to help the user understand the email and formulate a response. It produces five reply drafts, including one grounded in external deep research and one that challenges the email's approach with better alternatives.

## Workflow

### Phase 1: Retrieve the email

#### Step 1: Parse the user's request

Extract from the user's message:
- Subject keywords: the title, topic, or identifying phrase of the email
- Sender (optional): if the user mentions who sent it
- Date hints (optional): "yesterday", "last week", "from Monday", etc.

#### Step 2: Search for the email

Call `Microsoft 365:outlook_email_search` with:
- `query`: the subject keywords (1-6 significant words)
- `sender`: if specified
- `afterDateTime` / `beforeDateTime`: if date hints given
- `limit`: 5

#### Step 3: Select the correct email

- One result: proceed to Step 4.
- Multiple plausible matches: list them (subject + sender + date) and ask the user which one.
- No results: broaden the query. If still nothing, inform the user.

#### Step 4: Read the full email

Call `Microsoft 365:read_resource` with the email URI (`mail:///messages/{messageId}`).

#### Step 5: Present the email

Show the email content:
- From, To, CC, Date, Subject
- Body (cleaned of excessive HTML/signatures)
- Attachments (list filenames if present)

---

### Phase 2: Extract research targets

Before searching, analyze the email body and extract:

1. Key topics and entities: project names, product names, technical terms, company names, people mentioned
2. Action items or questions: what is being asked or expected
3. References: any mentioned documents, tickets, tasks, or prior conversations
4. Sender context: the sender's name and email for finding related threads

Formulate 2-4 concise search queries from these extractions. Each query should target a different angle (e.g., one for the project name, one for a specific question raised, one for the sender's recent communications).

---

### Phase 3: Cross-source research

Run these searches in the same turn to minimize round-trips. Not every source will be relevant every time — use judgment based on the email content.

#### 3a: Outlook — related emails

Call `Microsoft 365:outlook_email_search` for:
- The email thread (search by subject to find prior messages in the same thread)
- Recent emails from/to the same sender on related topics (use sender filter + topic keywords)
- Limit to 5-10 results per search. Read the most relevant 1-3 via `read_resource` if their snippets suggest they contain useful context.

#### 3b: Notion — related pages, tasks, projects

Call `notionMCP:notion-search` with:
- Key project or topic names extracted from the email
- Any referenced document or task names
- Keep queries specific (one concept per search call). Run 1-3 searches depending on how many distinct topics the email touches.

If search returns relevant pages, call `notionMCP:notion-fetch` on the top 1-2 results to get full content — but only if the search snippet suggests the page contains information that would help answer the email.

#### 3c: Airtable — related records

Call `Airtable MCP Server:search_records` with:
- Key entity names, project names, or identifiers from the email
- This requires knowing which base and table to search. If the user has not specified or if the relevant base/table is unknown, call `Airtable MCP Server:list_bases` and then `Airtable MCP Server:list_tables` to identify the most likely location. Cache this knowledge for subsequent calls in the same conversation.
- If no Airtable context seems relevant to the email content, skip this source entirely rather than making speculative searches.

#### 3d: Web — deep research for reply option 4

This step gathers external context to power the 4th (deep-research-informed) reply draft. Run it after the internal source searches.

1. From the email content and internal research results, identify 1-3 knowledge gaps or topics where external information would materially improve the reply. Examples:
   - Technical questions referencing products, standards, or specifications not fully covered internally
   - Industry trends, regulatory changes, or recent announcements mentioned or implied
   - Vendor/partner information, pricing, or feature details
   - Best practices or reference architectures relevant to the discussion

2. Call `web_search` with focused queries (1-3 searches). Keep queries specific and factual — do not search for opinion or subjective content.

3. If search results surface promising pages, call `web_fetch` on the 1-2 most relevant URLs to get full content.

4. Collect the findings into a structured set of facts with source attribution. These feed directly into reply option 4 in Phase 4.

Skip this phase entirely if:
- The email is purely internal/administrative (meeting scheduling, approvals, status updates) with no external knowledge dimension.
- The internal sources already provide complete coverage of every topic raised.

#### Research boundaries

- Do not exceed 35 total research tool calls across all sources (including web searches). Prioritize the sources most likely to yield useful context based on the email content.
- Stop researching a source if the first search returns nothing relevant — do not retry with increasingly vague queries.
- Prioritize depth over breadth: reading 2 highly relevant items fully is better than skimming 10 marginally related ones.

---

### Phase 4: Synthesize and answer

After gathering context, present the user with:

#### 1. Context summary
A concise synthesis of what was found across sources. Organize by relevance to the email, not by source. Mention which source each piece of information came from (e.g., "a prior email thread from Jan 15", "the project page in Notion", "the client record in Airtable").

#### 2. Action items
Extract any actions required from the user based on the email content and research context. For each action item:
- State the action clearly and concisely.
- Note the deadline or urgency if mentioned or implied.
- Reference the source (the email itself, a related thread, a Notion task, an Airtable record) so the user can trace it.
- Flag dependencies — if an action is blocked by someone else's input or a prerequisite step, say so.

Only list actions that require the user's involvement. Do not list actions assigned to others unless the user needs to follow up on them. If no actions are required beyond replying, state "No additional actions identified beyond responding to this email."

#### 3. Answer or draft response
Based on the email content and gathered context:
- If the email contains questions: provide answers grounded in the research findings.
- If the email requests action: summarize what needs to be done, referencing any related tasks or commitments already tracked.
- If the email is informational: highlight how it connects to or updates existing knowledge.
- Always draft exactly 5 possible reply options for the user to choose from or refine:
  1. Concise and direct — gets to the point quickly.
  2. Detailed and thorough — covers all aspects raised in the email.
  3. Diplomatic or cautious — appropriate when the topic is sensitive or politically charged.
  4. Deep-research-informed — the best-grounded reply, built on external research conducted in Phase 3d (see below). This reply incorporates verified external facts, references, or context that strengthen the response beyond what internal sources provide. Label it clearly as "[Deep Research]" so the user knows it drew on web sources.
  5. Challenger — constructively pushes back on the assumptions, approach, or solutions presented in the email and proposes better alternatives. Label it clearly as "[Challenger]". This reply should:
     - Identify weak points, unstated assumptions, or risks in what the sender proposes.
     - Offer concrete alternative solutions or approaches, grounded in both internal context and deep research findings where available.
     - Remain professional and constructive — frame challenges as "have we considered..." or "an alternative that addresses X risk would be..." rather than blunt disagreement.
     - Quantify the argument where possible (cost, effort, timeline, risk).

For reply option 4 specifically:
- Weave in the external findings naturally — do not just append a list of links.
- Cite the source briefly inline (e.g., "per the SAP Note 3456789" or "according to Microsoft's latest documentation").
- If Phase 3d was skipped (purely administrative email), reply 4 should still exist but be labeled "[Extended Internal]" and instead combine the strongest elements of the other three replies into a single comprehensive draft.

Keep all five replies action-oriented.

#### 4. Gaps
Note anything the email asks about that could not be found in any source. Be explicit: "No information found regarding X in Outlook, Notion, or Airtable."

---

## Important behaviors

- Never ask the user to confirm before searching. Search immediately based on the email subject they provide.
- Phase 2 research happens automatically after reading the email. Do not ask "would you like me to search for related context?" — just do it.
- If the user only wants the email content without research (e.g., "just show me the email"), respect that and skip Phases 2-4.
- Keep the final synthesis focused on actionability. The user wants to know what to do with this email, not a list of everything tangentially related.
- When drafting a reply, match the tone and language of the original email thread (formal/informal, English/Dutch, etc.).

---
description: Create professional PowerPoint presentations using the delaware consulting template. Plan-then-build workflow with hybrid template and generated slide support.
---

# Delaware Slides Command

This command invokes the **delaware-slides** skill to create professionally branded PowerPoint presentations using the delaware consulting template.

## What This Command Does

1. **Assess Content** - Analyze source material, key messages, audience, and context
2. **Plan Slides** - Structure the presentation and plan each slide (template vs. generated)
3. **Build Deck** - Execute using hybrid workflow (template + PptxGenJS) or generated-only
4. **QA and Deliver** - Verify brand compliance and present the final .pptx

## When to Use

Use `/delaware-slides` when:
- Creating client proposals or pitch decks for delaware
- Building internal presentations with delaware branding
- Making workshop materials or handover decks
- Any PowerPoint presentation for delaware or its clients

## How It Works

### Phase 1: Planning (never skipped)
1. Assess content and identify key messages, data, audience
2. Structure the presentation flow to match the purpose
3. Plan each slide: type, template or generated, content
4. Present slide plan as downloadable file for user review
5. **Wait for user approval before building**

### Phase 2: Execution
1. Classify slides into template list and generated list
2. If template slides exist: follow hybrid workflow (template shell + PptxGenJS content + merge)
3. If generated only: single PptxGenJS script
4. QA: convert to images, inspect, fix, re-verify

## Template Catalog

69 curated template slides including:
- Brand openers, closings, Q&A
- Agenda, section dividers, chapter starts
- Stats, callouts, quotes
- Process flows, timelines, roadmaps
- Budget layouts, KPI dashboards
- Team grids, reference cases, maps
- And more (see skill for full catalog)

## Design Principles

- **Less is more** - Match effort to context (client-facing vs. internal vs. workshop)
- **Never generate brand decorations** - Patterns, arcs, logos come only from template slides
- **Content slides use white backgrounds** - Brand identity comes from colors, font, lowercase titles, and footer
- **Century Gothic everywhere** - The only font in delaware presentations
- **All titles lowercase** - "delaware" always lowercase

## Example Usage

```
User: /delaware-slides Create a proposal deck for client X about their SAP migration

Agent (Phase 1):
# Slide Plan: SAP Migration Proposal for Client X

| # | Story beat | Type | Source | Content |
|---|-----------|------|--------|---------|
| 1 | Brand opener | Cover | Template slide 1 | Red bg with delaware wordmark |
| 2 | Agenda | Agenda | Template slide 2 | 4 agenda items |
| 3 | Understanding | Content | Generated | Client's current challenges |
| ...

Awaiting your approval before building.
```

## Integration with Other Commands

- Use `/plan` to outline the content before creating slides
- Use `/md2word` if a Word document is needed instead

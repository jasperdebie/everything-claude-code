---
name: delaware-slides
description: "delaware Consulting presentation workflow for PowerPoint (.pptx) files. Use this skill whenever creating, editing, or styling any PowerPoint presentation for delaware or its clients. Triggers: any mention of 'delaware presentation', 'delaware deck', 'delaware slides', 'delaware template', 'huisstijl', or when creating presentations, pitch decks, or client proposals — if the user works at delaware, this skill applies. This skill requires TWO other skills: read the pptx skill first for technical guidance, then read the delaware-brand-guidelines skill for brand constants (colors, fonts, voice), then apply the presentation-specific workflows and template catalog below."
---

# delaware slides

## dependencies

This skill builds on two other skills:
1. **pptx skill** — read first for technical guidance (PptxGenJS, editing workflow, QA process).
2. **delaware-brand-guidelines skill** — read for all brand constants: colors, fonts, typography rules, brand voice, and the code constants in `references/code-constants.md`.

Everything below is specific to PowerPoint presentations and does not repeat what those skills already cover.

---

## how this skill works

**plan-then-build** approach with two distinct phases:

1. **Planning phase** — understand the content, plan every slide, decide template vs. generated. Share the plan with the user for review.
2. **Execution phase** — build only after the plan is approved.

**Never skip the planning phase.**

---

## phase 1: planning

### step 1 — assess the content
Read and extract all source material. Identify:
- Key messages and what this presentation needs to accomplish
- Data, numbers, and statistics (candidates for stat callout boxes)
- The audience and context — the user will indicate what level of polish is needed
- How much content there is (determines number of slides)

### step 2 — structure the presentation
Think about how the slides should flow. This depends entirely on the purpose:
- A client proposal might need a full narrative arc (open with credibility, build the case, land with a clear ask)
- An internal handover might just need 3 clean information slides
- A workshop deck might need lots of detail slides with minimal framing

**Don't force a fixed structure.** Match the format to the purpose. Sometimes 3 slides is the right answer.

### step 3 — plan each slide
For every slide, decide:
- What type of slide it needs (overview, timeline, grid, process flow, stats, quote...)
- Whether it should come from the **template** or be **generated**
- What content goes on it

**Template slides** are for brand moments: covers, closings, dividers, "about delaware", quotes, maps, budget layouts, reference cases.

**Generated slides** are for content: anything where the layout should serve the specific content.

### step 4 — present the slide plan for review
Create a plan as a downloadable file (Excel or similar) so the user can easily review, annotate, and return it. The plan should include:

| Column | Content |
|--------|---------|
| Slide # | Sequence number |
| Story beat | What this slide accomplishes |
| Slide type | Cover, agenda, content grid, timeline, process flow, etc. |
| Source | "Template slide X" or "Generated" |
| Content summary | What goes on the slide |
| Notes | Any open questions or alternatives |

**Wait for user approval before building.** The user may reorder, add, remove, or swap slides.

---

## phase 2: execution

### step 5 — classify and route (MANDATORY)

**⚠️ STOP. Before writing any code, complete this routing step.**

Look at the approved slide plan and separate slides into two lists:

1. **Template slides** — every slide marked "Template slide X" in the plan
2. **Generated slides** — every slide marked "Generated" in the plan

If the plan contains **only generated slides** (no template slides at all), use a single PptxGenJS script. Skip to "Generated-only workflow" below.

If the plan contains **any template slides** (even just one), you MUST follow the "Hybrid workflow" below. This is the most common case for delaware decks — covers, agendas, and closings almost always come from the template.

#### generated-only workflow
Use a single PptxGenJS script with `LAYOUT_WIDE`. Apply brand constants. Proceed to step 6.

#### hybrid workflow (template + generated slides)
This is a **three-step build process**. All three steps are mandatory. Never collapse them into a single PptxGenJS script.

**Step 5a — Build the template shell:**
1. Unpack the template: `unpack.py`
2. Edit `<p:sldIdLst>` in `presentation.xml` to keep ONLY the template slides you need
3. Edit text content in the kept slide XML files (replace placeholder text with final content)
4. Do NOT modify any decorative/brand elements on template slides
5. Clean: `clean.py`
6. Pack: `pack.py` → produces `template_shell.pptx`

**Step 5b — Build the generated content slides:**
1. Create a PptxGenJS script that generates ONLY the content slides (not covers, agendas, closings, or any other template slide)
2. Use `LAYOUT_WIDE` (13.33" × 7.5")
3. Apply brand constants from `references/code-constants.md`
4. Output to `content_slides.pptx`

**Step 5c — Merge into final deck:**
1. Open `template_shell.pptx` with python-pptx
2. Open `content_slides.pptx` with python-pptx
3. Copy each generated slide into the template file using a **"Blank White Slide"** layout (or equivalent white layout) to avoid inheriting the template's branded layout backgrounds
4. Reorder slides in the `<p:sldIdLst>` to match the approved plan sequence
5. Save the final merged file

**Merge helper (python-pptx):**
```python
from pptx import Presentation
import copy

def copy_slide_clean(src_prs, src_idx, dst_prs, blank_layout_idx):
    """Copy a generated slide into the template file with a clean white background."""
    src_slide = src_prs.slides[src_idx]
    slide_layout = dst_prs.slide_layouts[blank_layout_idx]
    new_slide = dst_prs.slides.add_slide(slide_layout)
    # Clear any layout placeholders
    for shape in list(new_slide.shapes):
        shape._element.getparent().remove(shape._element)
    # Copy all shapes from source
    for shape in src_slide.shapes:
        new_slide.shapes._spTree.append(copy.deepcopy(shape._element))
    return new_slide

# Usage:
template = Presentation('template_shell.pptx')
content = Presentation('content_slides.pptx')

# Find the "Blank White Slide" layout index
blank_idx = next(i for i, l in enumerate(template.slide_layouts) if 'Blank White' in l.name)

# Copy content slides (skip any that are template-sourced)
for i in range(len(content.slides)):
    copy_slide_clean(content, i, template, blank_idx)

# Reorder: move slides in <p:sldIdLst> to match the plan
nsmap = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
sldIdLst = template.part._element.find('.//p:sldIdLst', nsmap)
# ... reorder sldId elements as needed ...

template.save('final_deck.pptx')
```

### step 6 — QA and deliver
- Follow the QA process from the pptx skill (convert to images, inspect, fix, re-verify)
- Check for leftover placeholder text in template slides
- Verify footer on every content slide
- **Verify that template slides retained their brand decoration** (photos, patterns, logos)
- **Verify that content slides have white backgrounds** (not inherited layout backgrounds)
- Present the final file to the user

---

## design principles

### less is more
Match the effort to the context:
- **Client-facing proposal:** High polish, varied layouts, template slides for brand moments
- **Internal handover:** Clean and clear, focus on information, minimal decoration
- **Workshop material:** Dense with content, functional over beautiful

The user will indicate the expected level. When in doubt, lean toward clean and simple.

### never generate decorative brand elements
This overrides the native pptx skill's design advice. Do NOT programmatically create brand decorations like quarter-circle patterns, geometric arcs, pattern strips, or d-logo approximations. These are designed by the brand team and only look right when they come from the template.

- If a template slide has decorative elements: **keep them as-is**
- If generating a slide from scratch: **use clean white backgrounds with content only** — no fake brand decoration

The brand identity on generated slides comes from the correct colors, font, lowercase titles, and the footer. That is enough.

### content slide design
Do NOT follow fixed layout recipes. Design each content slide freely based on what the content requires — let the information shape the layout, not the other way around. Use the pptx skill's general design advice for inspiration, vary layouts across slides, and keep things visually interesting. The brand identity (colors, font, lowercase titles, footer) provides enough consistency; the slide composition should be creative and tailored to the message.

---

## pptx-specific typography

The delaware-brand-guidelines skill covers typography across all formats. For PowerPoint specifically:

- **Century Gothic** is the ONLY font in presentations.
- Sizes: titles 28–40pt, body 12–20pt, captions 8–10pt, stat callouts 36–48pt.

### footer (every content slide)
- Bottom-left: slide number (Mid Gray, ~8pt) + "we commit. we deliver." (bold, Primary Red, ~8pt)
- Bottom-right: delaware "d" logomark in Teal (white bg) or White (dark bg)
- d-logo NOT on same slide as full "delaware" wordmark

### footer helper
```javascript
function addFooter(slide, slideNum) {
  slide.addText([
    { text: `${slideNum}`, options: { fontSize: 8, color: MID_GRAY } },
    { text: "   we commit. we deliver.", options: { fontSize: 8, bold: true, color: PRIMARY_RED } }
  ], { x: 0.3, y: 7.0, w: 4, h: 0.3, fontFace: FONT, margin: 0 });
}
```

---

## template catalog

The master template is located at `assets/delaware-template.pptx`. Generate thumbnails to browse. Here is what is available:

| Slides | Category | Use for |
|--------|----------|---------|
| 1 | Brand opener | Red bg with delaware wordmark + geometric arcs |
| 2 | Agenda | Numbered agenda with red numbers |
| 3 | Break | Coffee cup break slide |
| 4–5 | Stats and callouts | Big number hero (7.2), stat + text layout |
| 6 | Company partnerships | Logos + brand positioning |
| 7 | About delaware | Company overview |
| 8 | Why delaware | Differentiator slide |
| 9 | Our values | Heart + delaware logo |
| 10 | Our personality | Character attributes |
| 11 | Innovation at delaware | Innovation story |
| 12 | Screenshot/device mockup | App/device frame |
| 13–14 | Process and approach | Icon circles (5-step), phased approach (4-step) |
| 15–16 | Step-by-step | Icons + arrows, challenge illustration |
| 17 | Challenge, Solution, Results | Triptych layout |
| 18 | Experienced guides | Team with credentials |
| 19 | Project management | PM diagram |
| 20 | Reference case matrix | Industry mapping |
| 21 | Challenge illustration | Challenge visual |
| 22–25 | Quotes | Customer quote + photo, full-bleed photo, branded marks, inspirational |
| 26 | Q and A | Red bg, delaware wordmark |
| 27 | Engagement | How to engage with clients |
| 28–29 | Expertise and architecture | Market expertise, architecture proposition |
| 30–31 | KPI and dashboard | KPI dashboard, slider/gauge |
| 32 | NPS dashboard | NPS scores |
| 33–35 | Budget and costs | Phase-based budget, licences, proposed vs. requested |
| 36–37 | Bar charts | Percentages, team composition |
| 38 | Team grid | Photos + names + roles |
| 39–42 | Timelines and roadmaps | Milestones, Gantt, next steps, roadmap parts |
| 43–44 | Advanced visuals | Circular chart, pyramid |
| 45 | Numbered priorities | 1-2-3 with descriptions |
| 46 | Decision matrix | Quantitative/qualitative grid |
| 47–48 | Maps | World map, European map |
| 49–50 | Covers | Photo + pattern strip (light bg, dark bg) |
| 51–52 | Brand statements | "we commit. we deliver." (white bg, with pattern) |
| 53–54 | Section dividers | Red bg divider, with subtitle |
| 55 | Chapter with number | Numbered chapter start |
| 56–59 | Image-based dividers | Landscape, globe, portrait photo chapters |
| 60–62 | Quote layouts | Centered marks, left-aligned marks, "we commit" quote |
| 63–64 | Progress and milestones | Percentage milestones (25/50/75/100%), numbered steps |
| 65 | Icon grid | 4-up with descriptions |
| 66–67 | Client proof | Client logos wall, contact info |
| 68–69 | Closing | Contact details, thank-you with photo |

---

## known pitfalls

- **Never generate imitations of template slides.** If the plan says a slide comes from the template, use the actual template slide via the editing workflow. Generating a red background with "delaware" text in PptxGenJS is not a substitute for a template cover slide with proper brand photography, pattern elements, and logo placement. This is the most common execution mistake — taking the shortcut of generating everything in one PptxGenJS script instead of following the hybrid workflow.
- **Never duplicate template slides** for content injection — use `add_slide.py` with a `slideLayout` instead. Duplicated slides carry `<p:timing>` blocks with orphaned shape targets that cause PowerPoint repair errors.
- When injecting generated `<p:cSld>` into template-based slides, only include `<p:cSld>` and `<p:clrMapOvr>`. Strip any `<p:timing>` elements.
- Generated slides (PptxGenJS) never have timing issues — the problem only occurs in hybrid merges.
- **Never generate brand decorations** (patterns, arcs, logos). Use clean white slides. Brand decoration only comes from template slides.
- **Always use a "Blank White Slide" layout** when inserting generated slides into a template-based file. Other layouts may impose branded backgrounds (red, teal, etc.) that override the generated slide's white background.

---

## quick checklist

### planning phase
- [ ] Content assessed and understood
- [ ] Presentation structure matches the purpose (not forced into a fixed format)
- [ ] Slide plan created as downloadable file
- [ ] Each slide marked as template or generated
- [ ] Plan shared with user and approved before building

### execution phase — routing (step 5)
- [ ] Slides separated into template list and generated list
- [ ] If ANY template slides exist → hybrid workflow selected (not single PptxGenJS script)
- [ ] Template shell built first (unpack → trim → edit → clean → pack)
- [ ] Content slides built separately in PptxGenJS
- [ ] Slides merged using python-pptx with blank white layout
- [ ] Slide order matches approved plan

### execution phase — quality (step 6)
- [ ] Century Gothic everywhere
- [ ] All brand rules from delaware-brand-guidelines applied
- [ ] ALL titles lowercase
- [ ] "delaware" always lowercase
- [ ] Footer on every content slide
- [ ] White backgrounds for content, red for dividers
- [ ] No non-brand colors as primary colors
- [ ] No generated decorative elements (patterns, arcs, logos)
- [ ] Template slides retained their brand decoration (photos, patterns, logos)
- [ ] Content slides have white backgrounds (not inherited layout backgrounds)
- [ ] Layouts are varied where appropriate
- [ ] No leftover placeholder text in template slides
- [ ] No `<p:timing>` in slides with replaced content

---

## asset reference

| Asset | Path | Usage |
|-------|------|-------|
| Master template | `assets/delaware-template.pptx` | Curated slides for brand moments |

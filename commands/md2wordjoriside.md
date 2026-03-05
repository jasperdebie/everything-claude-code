---
description: Convert Markdown content to professionally formatted Word documents using the Joris Ide specification template. Auto-detects placeholders for Title, Subtitle, Date, Version, Author, TechnicalAuthor, and ChangeRequest.
---

# MD2Word Joris Ide Command

This command invokes the **md2wordjoriside** skill to convert Markdown to professionally formatted Word documents using the official Joris Ide Functional/Technical Specification template.

## What This Command Does

1. **Generate or Read Markdown** - Create specification content or use existing files
2. **Detect Placeholders** - Auto-fill Title, Subtitle, Date, Version, Author, TechnicalAuthor, ChangeRequest
3. **Convert to Word** - Apply Joris Ide template with JI logo, Century Gothic headings, and Light List Accent 2 tables
4. **Deliver Document** - Present the final .docx file

## When to Use

Use `/md2wordjoriside` when:
- Creating functional or technical specifications for Joris Ide
- Converting existing markdown to Joris Ide branded Word documents
- Writing SAP-related specifications with the JI template
- Any Joris Ide document requiring the official template

## How It Works

### Mode 1: Generate Then Convert
1. Generate markdown following the JI specification structure (Functional, Test scenarios, Pseudo technical, Technical)
2. Save to a temporary file
3. Auto-detect placeholders from content and context
4. Convert using the Joris Ide template

### Mode 2: Convert Existing Markdown
1. Read the provided markdown file
2. Auto-detect placeholders
3. Convert using the Joris Ide template

## Template Sections

The JI specification template defines these sections:
- **Functional** - Context, expected behavior, flows, I/O, assumptions, dependencies
- **Test scenarios** - Scenarios with steps, input/output data
- **Pseudo technical** - Tables, outputs, reports, function modules, transactions, error/auth handling, translations
- **Technical** - Technical description, custom objects, version indicators, enhancement indicators, import actions

## Placeholder Auto-Detection

- `{{Title}}` - Document title on cover page
- `{{Subtitle}}` - Domain and subtitle (format: `<domain> <title>`)
- `{{Version}}` - Version number (default "1")
- `{{Date}}` - Current date in dd-mm-yyyy format
- `{{Author}}` - Functional colleague name
- `{{TechnicalAuthor}}` - Technical colleague (optional)
- `{{ChangeRequest}}` - RFC/Charm number (optional)

## Example Usage

```
User: /md2wordjoriside Create a functional spec for the SD sales order enhancement

Agent:
1. Generating markdown following JI specification structure...
2. Detected placeholders: Title="Functional Technical Specification", Subtitle="SD - Sales Order Enhancement", Version="1", Date="05-03-2026"
3. Converting to Word with Joris Ide template...
4. Document saved: func_spec_sd_sales_order.docx
```

## Style Mapping

- `# Heading` → Century Gothic 16pt bold #345A8A
- `## Heading` → Century Gothic 13pt bold #4F81BD
- `### Heading` → Bold #4F81BD
- Table headers → "tablehead" (Arial 8pt bold)
- Table body → "tabletext" (Arial 8pt)
- Tables → "Light List Accent 2" style

## Integration with Other Commands

- Use `/plan` to outline specification structure first
- Use `/md2word` for Delaware branded documents instead

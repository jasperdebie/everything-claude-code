---
description: Convert Markdown content to professionally formatted Word documents using Delaware template. Generates markdown first if needed, then converts with placeholder auto-detection.
---

# MD2Word Command

This command invokes the **md2word** skill to convert Markdown to professionally formatted Word documents using the Delaware corporate template.

## What This Command Does

1. **Generate or Read Markdown** - Create markdown content or use existing files
2. **Detect Placeholders** - Auto-fill Title, Date, Author, Version, Project, Subtitle
3. **Convert to Word** - Apply Delaware template styles and formatting
4. **Deliver Document** - Present the final .docx file

## When to Use

Use `/md2word` when:
- Creating specifications, reports, or proposals as Word documents
- Converting existing markdown files to formatted .docx
- Generating professional documents with Delaware branding
- Any task requiring a Word document output

## How It Works

### Mode 1: Generate Then Convert
1. Generate markdown content based on the request
2. Save to a temporary file
3. Auto-detect placeholders from content and context
4. Convert using the Delaware template

### Mode 2: Convert Existing Markdown
1. Read the provided markdown file
2. Auto-detect placeholders
3. Convert using the Delaware template

## Placeholder Auto-Detection

The converter fills these placeholders automatically:
- `{{Title}}` - From first heading or context
- `{{Subtitle}}` - From second heading or context
- `{{Date}}` - Current date
- `{{Version}}` - From context or defaults to "1.0"
- `{{Author}}` - From user context/memory
- `{{Project}}` - From context or filename

## Example Usage

```
User: /md2word Create a functional specification for the new reporting module

Agent:
1. Generating markdown content for the functional specification...
2. Detected placeholders: Title="Functional Specification - Reporting Module", Date="2026-03-05", Version="1.0"
3. Converting to Word with Delaware template...
4. Document saved: functional_spec_reporting_module.docx
```

## Style Mapping

- `# Heading` → Word "Heading 1"
- `## Heading` → Word "Heading 2"
- Bullet lists → "List Bullet" style
- Numbered lists → "List Number" style
- Tables → "DLW Table Red" style

## Integration with Other Commands

- Use `/plan` to outline document structure first
- Use `/md2wordjoriside` for Joris Ide branded documents instead

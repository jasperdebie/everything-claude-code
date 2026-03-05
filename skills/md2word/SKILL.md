---
name: md2word
description: Convert Markdown content to professionally formatted Word documents using Delaware template. Use when creating any Word documents (specifications, reports, proposals, documentation) - either by generating markdown first then converting, or by converting existing markdown files. Automatically detects and fills placeholders like {{Title}}, {{Date}}, {{Author}}, etc.
---

# MD2Word Converter

Converts Markdown to professionally formatted Word documents using your corporate template.

## Two Usage Modes

### Mode 1: Generate Markdown, Then Convert
When user asks to "create a functional specification" or "write a report":
1. Generate markdown content first
2. Save markdown to a temporary file
3. Convert to Word using this skill

### Mode 2: Convert Existing Markdown
When user provides markdown file or asks to "convert this to Word":
1. Read the provided markdown
2. Convert directly to Word using this skill

## Placeholder Auto-Detection

The converter automatically detects and fills these placeholders:
- `{{Title}}` - Extract from context, first heading, or filename
- `{{Subtitle}}` - Extract from context or second heading  
- `{{Date}}` - Use current date
- `{{Version}}` - Extract from context or use "1.0"
- `{{Author}}` - Use user's name from context
- `{{Project}}` - Extract from context or filename

**Extract placeholders by:**
- Analyzing the markdown content headings
- Using conversation context (project names, dates mentioned)
- Reading user preferences from memory
- Asking user only if critical information is missing

## Template

The Delaware template is bundled with this skill at `assets/template.docx`.

**Template location:**
- Default: Bundled template at `assets/template.docx`
- Override: User can specify custom template path if needed

## Conversion Workflow

**Platform Compatibility:** This skill works on Linux, Mac, and Windows. Commands are shown for all platforms where they differ.

**Python Command:** Use `python3` on Linux/Mac, `python` on Windows (or whichever command works on your system).

**1. Install dependencies (first use only):**

Linux/Mac:
```bash
cd /mnt/skills/user/md2word/scripts
pip install -r requirements.txt --break-system-packages
```

Windows:
```powershell
cd /mnt/skills/user/md2word/scripts
pip install -r requirements.txt
```

Note: Use `python` or `python3` depending on your system configuration.

**2. Prepare the markdown file:**
- If generating: Save generated content to `/home/claude/temp_input.md`
- If converting existing: Use the provided file path

**3. Detect and prepare placeholder data:**
```python
import json
data = {
    "Title": "Extracted Title",
    "Date": "2025-01-15", 
    "Author": "User Name",  # Extracted from user context/memory
    # ... other detected placeholders
}
with open('/home/claude/placeholders.json', 'w') as f:
    json.dump(data, f)
```

**4. Run the conversion:**

Use `python` or `python3` depending on your system:

Linux/Mac:
```bash
cd /mnt/skills/user/md2word/scripts
python3 md2word_cli.py /home/claude/temp_input.md \
    --template ../assets/template.docx \
    --output /mnt/user-data/outputs/final_document.docx \
    --data /home/claude/placeholders.json
```

Windows:
```powershell
cd /mnt/skills/user/md2word/scripts
python md2word_cli.py /home/claude/temp_input.md --template ../assets/template.docx --output /mnt/user-data/outputs/final_document.docx --data /home/claude/placeholders.json
```

Note: Python handles forward slashes in paths on all platforms.

**5. Present the result:**
Use `present_files` to share the generated Word document.

## Markdown Features Supported

- **Headings**: `# H1`, `## H2`, etc. (mapped to Word heading styles)
- **Bold/Italic**: `**bold**`, `*italic*`
- **Lists**: Bullet and numbered lists (auto-restart numbering)
- **Tables**: Full table support with Delaware table styling
- **Line breaks**: Use `\n` for explicit line breaks within text

## Style Mapping

- `# Heading` → Word "Heading 1"
- `## Heading` → Word "Heading 2"  
- Bullet lists → "List Bullet" style
- Numbered lists → "List Number" style
- Tables → "DLW Table Red" style (Delaware custom)

## Output Location

**Always ask user where to save** unless obvious from context:
- Default: `/mnt/user-data/outputs/document_name.docx`
- Let user specify custom path
- Use descriptive filenames: `functional_spec_agristo.docx`

## Common Patterns

**Functional Specification:**
```markdown
# {{Title}}

**Project:** {{Project}}  
**Date:** {{Date}}  
**Version:** {{Version}}

## 1. Overview
...
```

**Technical Report:**
```markdown
# {{Title}}
## {{Subtitle}}

**Author:** {{Author}}  
**Date:** {{Date}}

## Executive Summary
...
```

## Troubleshooting

**"Module not found"**: 
- Linux/Mac: `pip install -r requirements.txt --break-system-packages`
- Windows: `pip install -r requirements.txt`

**"python3 not found" (Windows)**: Use `python` instead of `python3`

**"Template not found"**: The template should be bundled with the skill. If missing, ask user to provide a template path.

**Placeholders not replaced**: Ensure placeholder data JSON is correctly formatted and passed via `--data`

**List numbering issues**: The converter auto-restarts numbering after interruptions (by design)

**Platform Notes**: All file paths use forward slashes (`/`) which Python handles correctly on Windows, Mac, and Linux.

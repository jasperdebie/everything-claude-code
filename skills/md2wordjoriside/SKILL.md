---
name: md2wordjoriside
description: Convert Markdown content to professionally formatted Word documents using the official Joris Ide Functional/Technical Specification template. Use when creating any Word documents for Joris Ide (specifications, reports, proposals, documentation) - either by generating markdown first then converting, or by converting existing markdown files. Automatically detects and fills placeholders like {{Title}}, {{Subtitle}}, {{Date}}, {{Author}}, {{Version}}, {{TechnicalAuthor}}, {{ChangeRequest}}. Template includes the JI logo, Century Gothic headings, and Light List Accent 2 table styling.
---

# MD2Word Joris Ide Converter

Converts Markdown to professionally formatted Word documents using the official Joris Ide specification template.

## Template Structure

The template is derived from Joris Ide's `Functional_Technical_Specification_template.dotx` and includes:

**Cover page:**
- JI logo (embedded)
- Title (Century Gothic 18pt, #1F497D)
- Subtitle (Century Gothic 18pt)
- Version tracking table (Light List Accent 2 style) with columns: Version, Date, Functional colleague, Technical colleague, Changerequest

**Styles (from the JI template):**
- Title: Century Gothic 18pt #1F497D
- Heading 1: Century Gothic 16pt bold #345A8A
- Heading 2: Century Gothic 13pt bold #4F81BD
- Heading 3: bold #4F81BD
- Normal: Calibri 11pt
- List Bullet / List Paragraph: template-defined numbering
- tablehead: Arial 8pt bold (for table header cells)
- tabletext: Arial 8pt (for table body cells)
- Tables: "Light List Accent 2" style (accent color #C0504D)

**Footer:** Page X of Y

## Section Content Guidance

The JI Functional/Technical Specification template defines the following sections. When generating a spec, Claude should populate each section with the appropriate content as described below. If a section is not relevant, explicitly state "Not applicable" rather than omitting the section.

### ## Functional
Required. Done by functional colleague. Before development is started. When irrelevant, specify the reason why.

Content to include:
- Context / background information
- Expected behavior (if important, also the current behavior)
- Positive and negative flows
- Input and output data
- Assumptions
- Dependencies/constraints: other impacted functionality/domains

### ## Test scenarios
Required. Done by functional colleague. Before development is started. When irrelevant, specify the reason why.

Content to include:
- Scenarios with the tiles/transactions and their steps and their purpose
- Data to be inputted and data to be outputted

### ## Pseudo technical
Required. Done by functional colleague. Before development is started. When irrelevant, specify the reason why.

#### ### Main
Describe the following technical objects where relevant:

**Table:**
- Technical name
- Short description
- Fields included in the table (technical names) with key, data type, length, short description

**Output:**
- Technical name
- Short description
- Conditions
- Restrictions
- Segments
- Layout with visualized example

**Report/program:**
- Technical name
- Underlying logic
- Function modules/methods
- Details about data selection

**Function modules/class/method:**
- Technical name
- How to fill these function modules and methods

**Transaction:**
- Transaction key
- ALV/list
- Column names
- ALV functionality
- Screen (selection)
- Layout elements

#### ### Error handling
Required. Describe error messages and when to throw each error message.

#### ### Authorization handling
Required. Describe authorization objects/checks to hide/display/change/create certain information.

#### ### Translations
Required. Specify languages in which the change should be made available.

Translate the necessary information in:
- English
- Dutch
- French
- German

Applies on:
- New Data elements
- Error handling
- Layout changes
- Selection screens

### ## Technical
Required. Done by technical colleague. After development is finished, before testing by functional colleague starts.

Content: General description of the technical change.

#### ### Custom Objects
If applicable. List:
- Transaction code
- Report name
- Z-authorization objects
- TVARV process parameters

#### ### Version reference indicators
If applicable. Indicators per version to be found in syntax.

#### ### Enhancement activation indicators
If applicable. Enhancement indicators.

#### ### Special actions during import
If applicable. Describe:
- Import together with other objects of other systems?
- Cache clearing?
- Run report RV80HGEN?
- TVARV steering parameters?

## Two Usage Modes

### Mode 1: Generate Markdown, Then Convert
When user asks to "create a functional specification" or "write a report" for Joris Ide:
1. Generate markdown content following the section structure above
2. Save markdown to a temporary file
3. Convert to Word using this skill

### Mode 2: Convert Existing Markdown
When user provides markdown file or asks to "convert this to Word":
1. Read the provided markdown
2. Convert directly to Word using this skill

## Placeholder Auto-Detection

The converter automatically detects and fills these placeholders on the cover page:

**Title & subtitle:**
- `{{Title}}` - Document title (displayed in Title style on cover)
- `{{Subtitle}}` - Domain and subtitle, format: `<domain> <title>` (displayed below title)

**Version tracking table (row 1):**
- `{{Version}}` - Version number (default "1")
- `{{Date}}` - Current date in dd-mm-yyyy format
- `{{Author}}` - Functional colleague name
- `{{TechnicalAuthor}}` - Technical colleague name (optional, use "" if not applicable)
- `{{ChangeRequest}}` - RFC/Charm number (optional, use "" if not applicable)

**Extract placeholders by:**
- Analyzing the markdown content headings
- Using conversation context (project names, dates mentioned)
- Reading user preferences from memory
- Asking user only if critical information is missing
- Default Author for Joris Ide context: "Jasper" (from memory)

## Template

The Joris Ide template is bundled with this skill at `assets/template.docx`.

**Template location:**
- Default: Bundled template at `assets/template.docx`
- Override: User can specify custom template path if needed

## Conversion Workflow

**Platform Compatibility:** This skill works on Linux, Mac, and Windows.

**Python Command:** Use `python3` on Linux/Mac, `python` on Windows.

**1. Install dependencies (first use only):**

Linux/Mac:
```bash
cd /mnt/skills/user/md2wordjoriside/scripts
pip install -r requirements.txt --break-system-packages
```

Windows:
```powershell
cd /mnt/skills/user/md2wordjoriside/scripts
pip install -r requirements.txt
```

**2. Prepare the markdown file:**
- If generating: Save generated content to `/home/claude/temp_input.md`
- If converting existing: Use the provided file path

**3. Detect and prepare placeholder data:**
```python
import json
data = {
    "Title": "Functional Technical Specification",
    "Subtitle": "SD - Sales Order Processing Enhancement",
    "Date": "24-02-2026",
    "Version": "1",
    "Author": "Jasper",
    "TechnicalAuthor": "",
    "ChangeRequest": ""
}
with open('/home/claude/placeholders.json', 'w') as f:
    json.dump(data, f)
```

**4. Run the conversion:**

Linux/Mac:
```bash
cd /mnt/skills/user/md2wordjoriside/scripts
python3 md2word_cli.py /home/claude/temp_input.md \
    --template ../assets/template.docx \
    --output /mnt/user-data/outputs/final_document.docx \
    --data /home/claude/placeholders.json
```

Windows:
```powershell
cd /mnt/skills/user/md2wordjoriside/scripts
python md2word_cli.py /home/claude/temp_input.md --template ../assets/template.docx --output /mnt/user-data/outputs/final_document.docx --data /home/claude/placeholders.json
```

**5. Present the result:**
Use `present_files` to share the generated Word document.

## Markdown Features Supported

- **Headings**: `# H1`, `## H2`, `### H3`, `#### H4` (mapped to Word heading styles)
- **Bold/Italic**: `**bold**`, `*italic*`
- **Lists**: Bullet and numbered lists (auto-restart numbering)
- **Tables**: Full table support with Light List Accent 2 styling and tablehead/tabletext paragraph styles
- **Line breaks**: Use `\n` for explicit line breaks within text

## Style Mapping

- `# Heading` → Word "Heading 1" (Century Gothic 16pt bold #345A8A)
- `## Heading` → Word "Heading 2" (Century Gothic 13pt bold #4F81BD)
- `### Heading` → Word "Heading 3" (bold #4F81BD)
- `#### Heading` → Word "Heading 4" (bold italic #4F81BD)
- Bullet lists → "List Bullet" style (fallback: "List Paragraph")
- Numbered lists → "List Number" style (fallback: "List Paragraph")
- Table header cells → "tablehead" paragraph style (Arial 8pt bold)
- Table body cells → "tabletext" paragraph style (Arial 8pt)
- Tables → "Light List Accent 2" table style

## Output Location

**Always ask user where to save** unless obvious from context:
- Default: `/mnt/user-data/outputs/document_name.docx`
- Let user specify custom path
- Use descriptive filenames: `func_spec_sd_sales_order.docx`

## Example Markdown Structure

When generating a full Functional/Technical Specification, use this heading structure:

```markdown
# Version 1

## Functional

Context and background for the change...

Expected behavior...

## Test scenarios

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1    | ...    | ...             |

## Pseudo technical

### Main

**Table:** ZTABLE_NAME
- Description: ...
- Key fields: MANDT, VBELN
- ...

### Error handling

| Message ID | Type | Text | When triggered |
|------------|------|------|----------------|
| Z001       | E    | ...  | ...            |

### Authorization handling

Authorization object Z_SD_ORD with fields ACTVT (01, 02, 03).

### Translations

Languages: EN, NL, FR, DE
Applies to: data elements, error messages, selection screen texts.

## Technical

General description of the technical implementation.

### Custom Objects

- Transaction: ZSD_REPORT
- Report: ZSD_R_SALES_ENH
- Auth object: Z_SD_ORD

### Version reference indicators

Not applicable.

### Enhancement activation indicators

Not applicable.

### Special actions during import

No special actions required.
```

## Troubleshooting

**"Module not found"**: 
- Linux/Mac: `pip install -r requirements.txt --break-system-packages`
- Windows: `pip install -r requirements.txt`

**"python3 not found" (Windows)**: Use `python` instead of `python3`

**"Template not found"**: The template should be bundled with the skill. If missing, ask user to provide a template path.

**Placeholders not replaced**: Ensure placeholder data JSON is correctly formatted and passed via `--data`. Placeholders use `{{key}}` format.

**List numbering issues**: The converter auto-restarts numbering after interruptions (by design).

**Platform Notes**: All file paths use forward slashes (`/`) which Python handles correctly on Windows, Mac, and Linux.

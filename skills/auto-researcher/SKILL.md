---
name: auto-researcher
description: Automated web research with AI analysis, image generation, and professional PDF reports. Use for: (1) Daily news briefs, (2) Competitor analysis, (3) Topic research, (4) Market trends. Generates: Google Docs (editable), Google Sheets (data), Drive (images), and structured PDF reports with info-graphics.
---

# Auto-Researcher v1.0

Automated research pipeline that generates professional reports with AI analysis, visualizations, and web screenshots.

## Pipeline

```
INPUT: Query → Web Search → Web Fetch → Browser Screenshots → AI Analysis → OUTPUT
                                                                          ↓
                                               Docs + Sheets + Drive Images + PDF
```

## Commands

### Interactive Research

```bash
# Quick research + PDF
python3 {skillDir}/scripts/research.py --query " trends 2024" --type brief

# Full analysis with all outputs
python3 {skillDir}/scripts/research.py --query "competitor analysis" --type analysis --pdf --docs --sheets

# Market trends report
python3 {skillDir}/scripts/research.py --query "AI market trends" --type trends --images 5
```

### Parameters

| Flag | Description |
|------|-------------|
| `--query` | Research topic (required) |
| `--type` | Report type: brief, analysis, trends |
| `--max-sources` | Number of sources (default: 5) |
| `--pdf` | Generate PDF report |
| `--docs` | Create Google Doc |
| `--sheets` | Create Google Sheet |
| `--images` | Generate N info-graphics |
| `--output-dir` | Local output directory |

### Examples

```bash
# Daily news brief
python3 research.py --query "AI news today" --type brief --pdf --images 2

# Competitor analysis
python3 research.py --query "Notion competitors" --type analysis --docs --sheets --images 3

# Market trends
python3 research.py --query "SaaS pricing trends 2024" --type trends --all
```

## Report Types

| Type | Description | Best For |
|------|-------------|----------|
| **brief** | Summary with key points | Daily news, quick updates |
| **analysis** | Deep dive with data | Competitors, topics |
| **trends** | Time-series with charts | Market analysis, forecasts |

## Output Structure

```
{output_dir}/
├── report.pdf              # Complete PDF report
├── report.md               # Markdown source
├── data.json               # Raw research data
├── images/                 # Generated info-graphics
│   ├── chart-1.png
│   └── chart-2.png
└── google-links.json       # Google Docs/Sheets links (if created)
```

## Integration

### Google Workspace (gog)
- **Uses:** `gog` skill (already ✅ ready)
- **Commands:**
  - `gog docs create` → Google Docs
  - `gog sheets create` → Google Sheets
- **Tokens:** OAuth from gog configuration

### Drive (GLM Tools)
- **Uses:** `glm-drive.py` and `glm-workflow.py`
- **Functions:**
  - `upload_to_drive()` → Upload images to Drive
  - `glm-workflow.py` → Full pipeline (generate + download + upload)
- **Folder:** `1DmLPgRlRxFN3sH5J8TXvndMtHmWO-yTY` (GLM-Images)

### Image Generation
- **Uses:** Z.AI GLM-Image API (`/root/.openclaw/tools/glm-image.py`)
- **Functions:** `create_infographic()`, `create_presentation_slide()`
- **Styles:** minimalist, photorealistic, modern, 3d_render
- **API:** `https://api.z.ai/api/paas/v4/images`
- **Cost:** Económica comparada con DALL-E
- **Formats:** PNG hasta 1792x1024

### Browser Screenshots (Chromium)
- **Uses:** Chromium browser with remote debugging (`profile="chrome"`)
- **Functions:**
  - `take_screenshot(url, output_path)` → Full page screenshot
  - `capture_page_analysis(url)` → Screenshot + extracted text
- **Output:** PNG files saved to output directory
- **Integration:** Screenshots included in PDF reports

### AI Analysis
- Uses: MiniMax API (already integrated)
- Fallback: Claude/gemini for summary

## Prompt Engineering

### For Info-Graphics

```python
CHART_PROMPT = """
Create a professional data visualization for: {topic}
Style: Minimalist, corporate, clean lines
Type: {'bar chart' if data else 'infographic'}
Include: Title, axis labels, legend if needed
Output: Detailed prompt for image generation
"""

INFOGRAPHIC_PROMPT = """
Professional infographic about: {topic}
Style: Modern, clean, information-dense
Elements: Icons, key numbers, short text
Color scheme: Professional blue/gray palette
Layout: Vertical flow with clear sections
"""
```

## Configuration

### Environment Variables

```bash
# Optional - uses defaults if not set
export GOOGLE_DOCS_TEMPLATE_ID="..."
export GOOGLE_SHEETS_TEMPLATE_ID="..."
export PDF_THEME="modern|classic|minimal"
export DEFAULT_REPORT_TYPE="brief"
```

## Quality Standards

1. **Sources**: Minimum 3 credible sources
2. **Citations**: Inline links to sources
3. **Images**: 1-5 relevant info-graphics
4. **Structure**: Executive summary → Details → Conclusions
5. **Length**: Brief (~1 page), Analysis (~3 pages), Trends (~5 pages)

## Error Handling

- **Web search fail**: Try alternate queries
- **API rate limits**: Exponential backoff
- **Missing data**: Skip gracefully, note in report
- **Partial failures**: Generate available outputs

## Tips

- Use specific queries for better results
- `--type analysis` for competitor deep-dives
- `--images 3` generates variety of visualizations
- `--all` enables all output formats

Auto-Researcher Core Module
Implements all research pipeline functions
Uses Brave Search API directly (no OpenClaw dependency)
"""

import json
import os
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

# Directory constants
SKILL_DIR = Path(__file__).parent.parent

# Load environment variables from .env
def load_env():
    """Load environment variables from .env file"""
    env_path = Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env()


# ============================================
# BRAVE SEARCH API (Directo)
# ============================================

BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY", "")
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """Search the web using Brave Search API"""
    
    if not BRAVE_API_KEY:
        print("   ⚠️ BRAVE_API_KEY no configurada")
        return []
    
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    
    params = {
        "q": query,
        "count": max_results,
        "search_lang": "en",
        "country": "US"
    }
    
    try:
        response = requests.get(
            BRAVE_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            sources = []
            
            for item in data.get("web", {}).get("results", [])[:max_results]:
                sources.append({
                    "url": item.get("url", ""),
                    "title": item.get("title", ""),
                    "snippet": item.get("description", ""),
                    "source": "brave"
                })
            
            return sources
        else:
            print(f"   ⚠️ Brave API error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"   ⚠️ Web search failed: {e}")
        return []


# ============================================
# WEB FETCH (Requests directo)
    try:
        extract_result = subprocess.run([
            "openclaw", "web", "fetch", 
            "--url", url, 
            "--extract-mode", "text"
        ], capture_output=True, text=True, timeout=15)
        
        if extract_result.returncode == 0:
            content = json.loads(extract_result.stdout).get("content", "")
        else:
            content = ""
            
    except Exception as e:
        content = ""
    
    return {
        "url": url,
        "screenshot": screenshot,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }


# ============================================
# WEB SEARCH (Brave API via web_search tool)
# ============================================

# (La función search_web ya está definida arriba con Brave API)

# ============================================
# WEB FETCH (Requests directo)
# ============================================

def fetch_content(sources: List[Dict]) -> List[Dict]:
    """Fetch and extract content from sources using requests"""
    
    content = []
    
    for source in sources:
        url = source.get("url", "")
        
        if not url:
            continue
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Simple content extraction (first 5000 chars of text)
                text = response.text
                # Try to get main content
                content.append({
                    "url": url,
                    "title": source.get("title", ""),
                    "content": text[:5000],
                    "fetched_at": datetime.now().isoformat()
                })
                print(f"   📄 Fetched: {source.get('title', url)[:50]}")
                
        except Exception as e:
            print(f"   ⚠️ Failed to fetch {url[:50]}: {e}")
            continue
    
    return content


# ============================================
# AI ANALYSIS (MiniMax API)
# ============================================

def analyze_with_ai(query: str, content: List[Dict], report_type: str) -> Dict:
    """Analyze research content using AI"""
    
    # Combine content for analysis
    combined_content = "\n".join([
        f"## {item.get('title', 'Untitled')}\n{item.get('content', '')}"
        f"## {item.get('title', 'Untitled')}\n{item.get('content', '')}"
        for item in content
    ])
    
    # Build analysis prompt based on report type
    prompts = {
Analiza este contenido y genera un resumen ejecutivo:
- Máximo 5 puntos clave
- Conclusiones principales
- Recomendaciones breves
""",
Analiza este contenido para un análisis profundo:
- Resumen ejecutivo
- Datos y métricas clave
- Análisis de tendencias
- Comparación de fuentes
- Conclusiones detalladas
""",
Analiza este contenido para identificar tendencias:
- Tendencias principales
- Datos históricos si existen
- Pronóstico futuro
- Factores de influencia
- Implicaciones
"""
    }
    
    prompt = prompts.get(report_type, prompts["brief"])
    
QUERY: {query}

CONTENT:
{combined_content[:8000]}

{prompt}

Responde en JSON con el formato:
{{
    "summary": "resumen en 2-3 oraciones",
    "key_points": ["punto 1", "punto 2", ...],
    "trends": ["趋势 1", "趋势 2", ...] si aplica,
    "data_points": ["dato 1", "dato 2", ...],
    "recommendations": ["recomendación 1", ...],
    "confidence": 0.0-1.0
}}
"""
    
    # Use MiniMax API directly - Anthropic compatible format
    MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
    MINIMAX_ENDPOINT = os.environ.get("MINIMAX_ENDPOINT", "https://api.minimax.io/anthropic/v1/messages")
    MINIMAX_MODEL = os.environ.get("MINIMAX_MODEL", "MiniMax-M2.1")
    
    if not MINIMAX_API_KEY:
        print("   ⚠️ MINIMAX_API_KEY no configurada")
        return {
            "summary": f"Research on {query}",
            "key_points": ["MINIMAX_API_KEY required"],
            "confidence": 0.0
        }
    
    try:
        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MINIMAX_MODEL,
            "max_tokens": 2000,
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        }
        
        response = requests.post(
            MINIMAX_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # MiniMax format: response.content = [thinking_block, text_block, ...]
            # Ambos SIEMPRE vienen - es el diseño del modelo
            content_blocks = data.get("content", [])
            
            # Si no hay content, intentar choices format (fallback)
            if not content_blocks:
                content_blocks = data.get("choices", [{}])[0].get("message", {}).get("content", [])
            
            # Extraer thinking (block 0) y text (block 1)
            thinking_text = ""
            main_text = ""
            
            for block in content_blocks:
                block_type = block.get("type", "")
                if block_type == "thinking":
                    thinking_text = block.get("thinking", "")
                elif block_type == "text":
                    main_text = block.get("text", "")
            
            # Si main_text está vacío, usar thinking como fallback
            if not main_text.strip():
                main_text = thinking_text
            
            # Limpiar markdown del texto
            clean_text = main_text.strip()
            clean_text = re.sub(r'^```json\s*', '', clean_text)
            clean_text = re.sub(r'\s*```$', '', clean_text)
            clean_text = clean_text.strip()
            
            # Parsear JSON del texto limpio
            import re as re_module
            json_match = re_module.search(r'\{[^{}]+\}', clean_text, re_module.DOTALL)
            
            if json_match:
                try:
                    analysis = json.loads(json_match.group())
                    analysis["_thinking"] = thinking_text[:500]
                    print(f"   🧠 Analysis complete: {len(analysis.get('key_points', []))} key points")
                    return analysis
                except:
                    pass
            
            # Fallback: retornar estructura del texto
            return {
                "summary": main_text[:200],
                "key_points": [p.strip() for p in main_text.split("\n") if p.strip() and len(p.strip()) > 20][:7],
                "confidence": 0.7,
                "_thinking": thinking_text[:500]
            }
            
        else:
            print(f"   ⚠️ MiniMax API error: {response.status_code}")
            print(f"   Detail: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ⚠️ AI analysis failed: {e}")
    
    # Fallback: simple extraction
    return {
        "summary": f"Research on {query}",
        "key_points": ["Analysis unavailable"],
        "confidence": 0.5
    }


# ============================================
# IMAGE GENERATION (Z.AI GLM-Image)
# ============================================

def generate_image(topic: str, analysis: Dict, num_images: int = 1) -> List[Dict]:
    """Generate info-graphics using Z.AI GLM-Image API"""
    
    images = []
    
    # Build data for infographic
    key_points = analysis.get("key_points", [])[:5]
    data_points = analysis.get("data_points", [])[:5]
    trends = analysis.get("trends", [])[:3]
    
    data = {
        "key_findings": key_points,
        "data_metrics": data_points,
        "trends": trends
    }
    
    wrapper_script = str(SKILL_DIR / "scripts" / "glm-wrapper.py")
    
    for i in range(num_images):
        try:
            # Use GLM-Image wrapper
            input_data = json.dumps({
                "action": "infographic",
                "topic": topic,
                "data": data,
                "style": "minimalist"
            })
            
            result = subprocess.run(
                ["python3", wrapper_script],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            if result.returncode == 0:
                img_data = json.loads(result.stdout)
                if img_data.get("success"):
                    images.append({
                        "topic": topic,
                        "data": data,
                        "url": img_data.get("url", ""),
                        "type": "infographic"
                    })
                    print(f"   🖼️ Image {i+1}: Generated")
                elif img_data.get("error"):
                    print(f"   ⚠️ Image {i+1}: {img_data['error']}")
        
        except Exception as e:
            print(f"   ⚠️ Image generation failed: {e}")
            continue
    
    return images


def save_images(images: List[Dict], output_dir: Path) -> None:
    """Save generated images from GLM-Image and upload to Drive"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    workflow_script = "/root/.openclaw/tools/glm-workflow.py"
    
    for i, img in enumerate(images):
        img_url = img.get("url", "")
        
        if img_url:
            # Download locally first
            try:
                import requests
                img_path = output_dir / f"chart-{i+1}.png"
                resp = requests.get(img_url, timeout=60)
                with open(img_path, "wb") as f:
                    f.write(resp.content)
                img["saved_path"] = str(img_path)
                print(f"   💾 Saved: {img_path}")
                
                # Upload to Drive using GLM workflow
                filename = f"research-{img.get('topic', 'image')[:30]}-{i+1}.png"
                subprocess.run([
                    "python3", workflow_script,
                    "--url", img_url,
                    "--filename", filename
                ], capture_output=True, text=True, timeout=60)
                print(f"   ☁️ Uploaded to Drive: {filename}")
                
            except Exception as e:
                print(f"   ⚠️ Failed: {e}")


# ============================================
# PDF GENERATION (ReportLab)
# ============================================

def create_pdf_report(
    query: str,
    analysis: Dict,
    sources: List[Dict],
    images: List[Dict],
    report_type: str,
    output_path: Path
) -> Path:
    """Generate professional PDF report"""
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak, Image
        )
        from reportlab.lib import colors
        
        # Create PDF
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=72
        )
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor("#1a365d")
        )
        
        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor("#2c5282")
        )
        
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=11,
            spaceBefore=6,
            spaceAfter=6,
            leading=14
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph(f"Research Report: {query}", title_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            ParagraphStyle('Date', parent=styles['Normal'], fontSize=10, textColor=colors.gray)
        ))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        story.append(Paragraph(analysis.get("summary", "No summary available"), body_style))
        story.append(Spacer(1, 15))
        
        # Key Points
        if analysis.get("key_points"):
            story.append(Paragraph("Key Findings", heading_style))
            for point in analysis["key_points"][:7]:
                story.append(Paragraph(f"• {point}", body_style))
            story.append(Spacer(1, 15))
        
        # Data Points
        if analysis.get("data_points"):
            story.append(Paragraph("Data & Metrics", heading_style))
            for point in analysis["data_points"][:5]:
                story.append(Paragraph(f"• {point}", body_style))
            story.append(Spacer(1, 15))
        
        # Trends (if applicable)
        if analysis.get("trends"):
            story.append(Paragraph("Trends & Insights", heading_style))
            for trend in analysis["trends"][:5]:
                story.append(Paragraph(f"• {trend}", body_style))
            story.append(Spacer(1, 15))
        
        # Images
        if images:
            story.append(Paragraph("Visualizations", heading_style))
            for i, img in enumerate(images[:3]):
                # Download image from URL if needed
                img_url = img.get("url", "")
                img_path = img.get("saved_path", "")
                
                if img_url and not Path(img_path).exists():
                    # Download from URL
                    try:
                        import requests
                        img_path = f"/tmp/research-image-{i}.png"
                        resp = requests.get(img_url, timeout=60)
                        with open(img_path, "wb") as f:
                            f.write(resp.content)
                    except Exception as e:
                        print(f"   ⚠️ Failed to download image: {e}")
                        continue
                
                if Path(img_path).exists():
                    story.append(Image(img_path, width=5*inch, height=3*inch))
                    story.append(Spacer(1, 10))
        
        # Sources
        if sources:
            story.append(Paragraph("Sources", heading_style))
            for i, source in enumerate(sources[:5], 1):
                story.append(Paragraph(
                    f"{i}. {source.get('title', 'Untitled')}",
                    ParagraphStyle('Source', parent=styles['Normal'], fontSize=9)
                ))
                story.append(Paragraph(
                    f"   <link href='{source.get('url', '')}'>{source.get('url', '')}</link>",
                    ParagraphStyle('URL', parent=styles['Normal'], fontSize=8, textColor=colors.blue)
                ))
        
        # Build PDF
        doc.build(story)
        return output_path
        
    except Exception as e:
        print(f"   ⚠️ PDF generation failed: {e}")
        return output_path


# ============================================
# GOOGLE WORKSPACE (API Directa con Contenido)
# ============================================

GOOGLE_TOKEN = None

def get_google_token():
    """Get Google access token"""
    global GOOGLE_TOKEN
    if GOOGLE_TOKEN:
        return GOOGLE_TOKEN
    try:
        d = json.load(open("/root/.openclaw/google-oauth/tokens/tokens.json"))
        GOOGLE_TOKEN = d["accounts"]["alberto.farah.b@gmail.com"]["access_token"]
        return GOOGLE_TOKEN
    except:
        return None

def fill_google_doc(doc_id: str, query: str, analysis: Dict) -> bool:
    """Fill Google Doc with research content"""
    
    token = get_google_token()
    if not token:
        return False
    
    try:
        # Build content
        content_text = f"""# Research: {query}

## Summary
{analysis.get('summary', 'No summary available')}

## Key Findings
"""
        
        for i, point in enumerate(analysis.get('key_points', []), 1):
            content_text += f"{i}. {point}
"
        
        if analysis.get('data_points'):
## Data Points
"

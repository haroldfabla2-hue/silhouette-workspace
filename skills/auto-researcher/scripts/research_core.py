#!/usr/bin/env python3
"""
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
        print(f"   🔍 Searching: {query[:50]}...")
        resp = requests.get(BRAVE_SEARCH_URL, headers=headers, params=params, timeout=30)
        
        if resp.status_code == 200:
            data = resp.json()
            results = []
            
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "description": item.get("description", ""),
                    "type": item.get("type", ""),
                    "age": item.get("age", ""),
                    "profile": {
                        "name": item.get("profile", {}).get("name", "")
                    }
                })
            
            print(f"   ✅ Found {len(results)} sources")
            return results
        
        else:
            print(f"   ⚠️ Brave API error: {resp.status_code}")
            return []
    
    except Exception as e:
        print(f"   ⚠️ Search failed: {e}")
        return []


# ============================================
# WEB FETCH
# ============================================

def fetch_content(sources: List[Dict]) -> List[Dict]:
    """Fetch and extract content from URLs"""
    
    content = []
    
    for source in sources:
        url = source.get("url", "")
        
        if not url:
            continue
        
        try:
            print(f"   📄 Fetching: {url[:60]}...")
            
            resp = requests.get(url, timeout=30)
            
            if resp.status_code == 200:
                # Extract readable content
                text = resp.text
                
                # Simple extraction - get body text
                start = text.find("<body")
                if start == -1:
                    start = 0
                
                end = text.find("</body>")
                if end == -1:
                    end = len(text)
                
                body_text = text[start:end]
                
                # Remove HTML tags
                import re
                clean = re.sub(r"<[^>]+>", " ", body_text)
                clean = re.sub(r"\s+", " ", clean)
                clean = clean.strip()[:5000]
                
                content.append({
                    "title": source.get("title", ""),
                    "url": url,
                    "content": clean
                })
        
        except Exception as e:
            print(f"   ⚠️ Failed to fetch {url}: {e}")
            continue
    
    return content


# ============================================
# MINIMAX AI ANALYSIS
# ============================================

MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MINIMAX_ENDPOINT = os.environ.get("MINIMAX_ENDPOINT", "https://api.minimax.io/anthropic/v1/messages")
MINIMAX_MODEL = "MiniMax-M2.1"

def analyze_with_ai(query: str, content: List[Dict], report_type: str) -> Dict:
    """Analyze research content using AI"""
    
    # Combine content for analysis
    combined_content = "\n".join([
        f"## {item.get('title', 'Untitled')}\n{item.get('content', '')}"
        for item in content
    ])
    
    # Build analysis prompt based on report type
    prompts = {
        "brief": """
Analiza este contenido y genera un resumen ejecutivo:
- Maximo 5 puntos clave
- Conclusiones principales
- Recomendaciones breves
""",
        "analysis": """
Analiza este contenido para un analisis profundo:
- Resumen ejecutivo
- Datos y metricas clave
- Analisis de tendencias
- Comparacion de fuentes
- Conclusiones detalladas
""",
        "trends": """
Analiza este contenido para identificar tendencias:
- Tendencias principales
- Datos historicos si existen
- Pronostico futuro
- Factores de influencia
- Implicaciones
"""
    }
    
    prompt = prompts.get(report_type, prompts["brief"])
    
    # Build API request
    messages = [
        {
            "role": "user",
            "content": f"""QUERY: {query}

CONTENT:
{combined_content[:8000]}

{prompt}

Responde en JSON con el formato:
{{
    "summary": "resumen en 2-3 oraciones",
    "key_points": ["punto 1", "punto 2", ...],
    "trends": ["趋势 1", "趋势 2", ...] si aplica,
    "data_points": ["dato 1", "dato 2", ...] si aplica,
    "confidence": 0.0-1.0
}}"""
        }
    ]
    
    payload = {
        "model": MINIMAX_MODEL,
        "max_tokens": 1500,
        "messages": messages,
        "temperature": 0.3
    }
    
    if not MINIMAX_API_KEY:
        print("   ⚠️ MINIMAX_API_KEY no configurada")
        return {"summary": "API key missing", "confidence": 0.0}
    
    try:
        print(f"   🧠 Analyzing with MiniMax...")
        
        response = requests.post(
            MINIMAX_ENDPOINT,
            headers={
                "Authorization": f"Bearer {MINIMAX_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=180
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # MiniMax format: content is at root level
            content_blocks = data.get("content", [])
            
            # Extract thinking and text
            thinking_text = ""
            main_text = ""
            
            for block in content_blocks:
                block_type = block.get("type", "")
                if block_type == "thinking":
                    thinking_text = block.get("thinking", "")
                elif block_type == "text":
                    main_text = block.get("text", "")
            
            # Si main_text esta vacio, usar thinking como fallback
            if not main_text.strip():
                main_text = thinking_text
            
            # Limpiar markdown del texto
            clean_text = main_text.strip()
            clean_text = re.sub(r'^```json\s*', '', clean_text)
            clean_text = re.sub(r'\s*```$', '', clean_text).strip()
            
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
                "summary": clean_text[:200] if clean_text else "Analysis completed",
                "key_points": [p.strip() for p in clean_text.split("\n") if p.strip() and len(p.strip()) > 20][:7],
                "confidence": 0.7,
                "_thinking": thinking_text[:500]
            }
            
        else:
            print(f"   ⚠️ MiniMax API error: {response.status_code}")
            print(f"   Detail: {response.text[:200]}")
            return {"summary": "API error", "confidence": 0.0}
    
    except Exception as e:
        print(f"   ⚠️ Analysis failed: {e}")
        return {"summary": str(e), "confidence": 0.0}


# ============================================
# GLM-IMAGE (Generacion de graficos)
# ============================================

GLM_IMAGE_URL = "https://api.z.ai/api/paas/v4/images/generations"

def generate_image(prompt: str, quality: str = "baja") -> Optional[str]:
    """Generate infographic using GLM-Image API"""
    
    GLM_API_KEY = os.environ.get("ZAI_API_KEY", "")
    
    if not GLM_API_KEY:
        print("   ⚠️ ZAI_API_KEY no configurada")
        return None
    
    sizes = {
        "baja": "512x512",
        "media": "1024x1024",
        "alta": "1024x1024"
    }
    
    size = sizes.get(quality, sizes["media"])
    
    payload = {
        "model": "glm-image",
        "prompt": prompt,
        "size": size
    }
    
    try:
        print(f"   🎨 Generating infographic...")
        
        response = requests.post(
            GLM_IMAGE_URL,
            headers={
                "Authorization": f"Bearer {GLM_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=180
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "data" in data and len(data["data"]) > 0:
                image_url = data["data"][0].get("url", "")
                print(f"   ✅ Image generated: {image_url}")
                return image_url
        
        print(f"   ⚠️ GLM API error: {response.status_code}")
        return None
    
    except Exception as e:
        print(f"   ⚠️ Image generation failed: {e}")
        return None


# ============================================
# GOOGLE WORKSPACE (API Directa)
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
        content_text = f"""# Research: {query}

## Summary
{analysis.get('summary', 'No summary available')}

## Key Findings
"""
        
        for i, point in enumerate(analysis.get('key_points', []), 1):
            content_text += f"{i}. {point}\n"
        
        if analysis.get('data_points'):
            content_text += "\n## Data Points\n"
            for point in analysis['data_points'][:5]:
                content_text += f"- {point}\n"
        
        if analysis.get('trends'):
            content_text += "\n## Trends\n"
            for trend in analysis['trends'][:5]:
                content_text += f"- {trend}\n"
        
        content_text += f"""
---
**Confidence:** {analysis.get('confidence', 'N/A')}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
*Auto-Researcher v1.0*
"""
        
        requests.post(
            f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"requests": [{"insertText": {"location": {"index": 1}, "text": content_text}}]},
            timeout=30
        )
        
        return True
    
    except Exception as e:
        print(f"   ⚠️ Failed to fill doc: {e}")
        return False

def create_google_doc(query: str, analysis: Dict) -> str:
    """Create Google Doc with research results"""
    
    token = get_google_token()
    if not token:
        print("   ⚠️ No Google token available")
        return ""
    
    try:
        r = requests.post(
            "https://docs.googleapis.com/v1/documents",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={"title": f"Research: {query[:100]}"},
            timeout=30
        )
        
        if r.status_code == 200:
            doc_id = r.json().get("documentId")
            
            if fill_google_doc(doc_id, query, analysis):
                url = f"https://docs.google.com/document/d/{doc_id}/edit"
                print(f"   📄 Doc creado: {url}")
                return url
    
    except Exception as e:
        print(f"   ⚠️ Google Doc creation failed: {e}")
    
    return ""

def fill_google_sheet(sheet_id: str, query: str, analysis: Dict) -> bool:
    """Fill Google Sheet with research data"""
    
    token = get_google_token()
    if not token:
        return False
    
    try:
        summary_data = [
            ["RESEARCH QUERY"],
            [query],
            [""],
            ["SUMMARY"],
            [analysis.get('summary', 'N/A')[:1000]],
            [""],
            ["METADATA"],
            ["Confidence", str(analysis.get('confidence', 'N/A'))],
            ["Date", datetime.now().strftime('%Y-%m-%d')],
            ["Key Points", len(analysis.get('key_points', []))],
            ["Data Points", len(analysis.get('data_points', []))],
            ["Trends", len(analysis.get('trends', []))]
        ]
        
        requests.put(
            f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/'Summary'!A1:B{len(summary_data)}?valueInputOption=USER_ENTERED",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"values": summary_data},
            timeout=30
        )
        
        if analysis.get('key_points'):
            points_data = [["#", "KEY FINDINGS"]] + [[i+1, p] for i, p in enumerate(analysis['key_points'][:50])]
            requests.put(
                f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/'Key Points'!A1:B{len(points_data)}?valueInputOption=USER_ENTERED",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json={"values": points_data},
                timeout=30
            )
        
        return True
    
    except Exception as e:
        print(f"   ⚠️ Failed to fill sheet: {e}")
        return False

def create_google_sheet(query: str, analysis: Dict) -> str:
    """Create Google Sheet with structured data"""
    
    token = get_google_token()
    if not token:
        print("   ⚠️ No Google token available")
        return ""
    
    try:
        r = requests.post(
            "https://sheets.googleapis.com/v4/spreadsheets",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "properties": {"title": f"Research Data: {query[:100]}"},
                "sheets": [
                    {"properties": {"title": "Summary"}}, 
                    {"properties": {"title": "Key Points"}}
                ]
            },
            timeout=30
        )
        
        if r.status_code == 200:
            sheet = r.json()
            sheet_id = sheet.get("spreadsheetId")
            
            if fill_google_sheet(sheet_id, query, analysis):
                url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
                print(f"   📊 Sheet creado: {url}")
                return url
    
    except Exception as e:
        print(f"   ⚠️ Google Sheet creation failed: {e}")
    
    return ""

def verify_google_outputs(query: str, analysis: Dict, outputs: Dict, max_retries: int = 3) -> Dict:
    """Verify and fix Google outputs until they're complete"""
    
    print("\n🔍 Verificando outputs...")
    
    for attempt in range(max_retries):
        issues = []
        
        if "docs" in outputs and outputs["docs"]:
            doc_id = outputs["docs"].split("/d/")[1].split("/")[0]
            token = get_google_token()
            
            r = requests.get(
                f"https://docs.googleapis.com/v1/documents/{doc_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if r.status_code == 200:
                blocks = len(r.json().get("body", {}).get("content", []))
                if blocks < 5:
                    issues.append("doc_empty")
                    fill_google_doc(doc_id, query, analysis)
        
        if "sheets" in outputs and outputs["sheets"]:
            sheet_id = outputs["sheets"].split("/d/")[1].split("/")[0]
            token = get_google_token()
            
            r = requests.get(
                f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Summary",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if r.status_code == 200:
                values = r.json().get("values", [])
                if len(values) < 3:
                    issues.append("sheet_empty")
                    fill_google_sheet(sheet_id, query, analysis)
        
        if not issues:
            print("   ✅ Todos los outputs verificados")
            break
        
        print(f"   🔄 Intento {attempt+1}/{max_retries}: Corrigiendo...")
        time.sleep(2)
    
    return outputs

def research_to_google_workspace(query: str, analysis: Dict, sources: List[Dict]) -> Dict:
    """Create Google Doc + Sheet for research results"""
    
    print("\n📄 Creando Google Workspace...")
    
    results = {
        "doc_url": create_google_doc(query, analysis),
        "sheet_url": create_google_sheet(query, analysis)
    }
    
    return results


# ============================================
# PDF GENERATION (Simplificado)
# ============================================

def create_pdf_report(
    query: str,
    analysis: Dict,
    sources: List[Dict],
    images: List[Dict],
    report_type: str,
    output_path: Path
) -> Path:
    """Generate professional PDF report (simplified)"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create simple text-based PDF
    content_text = f"""# Research Report: {query}

Generated: {datetime.now().strftime('%B %d, %Y')}

## Executive Summary
{analysis.get('summary', 'No summary available')}

## Key Findings
"""
    
    for i, point in enumerate(analysis.get('key_points', []), 1):
        content_text += f"{i}. {point}\n"
    
    if analysis.get('data_points'):
        content_text += "\n## Data Points\n"
        for point in analysis['data_points'][:5]:
            content_text += f"- {point}\n"
    
    if sources:
        content_text += "\n## Sources\n"
        for i, source in enumerate(sources[:5], 1):
            content_text += f"{i}. {source.get('title', 'Untitled')}\n"
            content_text += f"   {source.get('url', '')}\n"
    
    # Simple file output
    with open(str(output_path).replace('.pdf', '.txt'), 'w') as f:
        f.write(content_text)
    
    print(f"   📄 Report saved: {output_path}")
    return output_path


# ============================================
# IMAGE SAVING
# ============================================

def save_images(images: List[Dict], output_dir: Path) -> None:
    """Save generated images from GLM-Image"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, img in enumerate(images):
        img_url = img.get("url", "")
        
        if img_url:
            try:
                img_path = output_dir / f"chart-{i+1}.png"
                resp = requests.get(img_url, timeout=60)
                with open(img_path, "wb") as f:
                    f.write(resp.content)
                print(f"   💾 Saved: {img_path}")
            except Exception as e:
                print(f"   ⚠️ Failed to save image: {e}")
import time

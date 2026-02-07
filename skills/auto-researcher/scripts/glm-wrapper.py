#!/usr/bin/env python3
"""
GLM-Image Wrapper for Auto-Researcher
Simple interface to GLM-Image API
"""

import json
import sys
import os
import requests

# API Configuration
BASE_URL = "https://api.z.ai/api/paas/v4/images"
ZAI_API_KEY = os.environ.get("ZAI_API_KEY", "")

def generate_image(prompt: str, size: str = "1024x1024") -> dict:
    """Generate image from text using GLM-Image API"""
    
    if not ZAI_API_KEY:
        return {"success": False, "error": "ZAI_API_KEY not configured"}
    
    headers = {
        "Authorization": f"Bearer {ZAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "glm-image",
        "prompt": prompt,
        "size": size
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generations",
            headers=headers,
            json=data,
            timeout=180
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # GLM response format: {"data": [{"url": "..."}]}
            if "data" in result and len(result["data"]) > 0:
                image_url = result["data"][0].get("url", "")
                if image_url:
                    return {"success": True, "url": image_url}
            
            return {"success": False, "error": "No image URL in response", "raw": str(result)}
        else:
            return {"success": False, "error": f"API error: {response.status_code}", "detail": response.text[:200]}
            
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_infographic(topic: str, data: dict, style: str = "minimalist") -> dict:
    """Create professional infographic about topic with data"""
    
    # Build prompt from data
    key_points = data.get("key_findings", [])
    metrics = data.get("data_metrics", [])
    trends = data.get("trends", [])
    
    prompt = f"""
Create a professional infographic about: {topic}

Key findings:
{chr(10).join(f"• {p}" for p in key_points[:5])}

Data metrics:
{chr(10).join(f"• {m}" for m in metrics[:5])}

Trends:
{chr(10).join(f"• {t}" for t in trends[:3])}

Style: {style}, clean design, professional colors, informative.
Include charts, icons, and clear typography.
"""
    
    return generate_image(prompt, size="1792x1024")


if __name__ == "__main__":
    # Read input
    if len(sys.argv) > 1:
        input_data = json.loads(sys.argv[1])
    else:
        input_data = json.load(sys.stdin)
    
    action = input_data.get("action", "generate")
    topic = input_data.get("topic", "")
    data = input_data.get("data", {})
    style = input_data.get("style", "minimalist")
    
    if action == "infographic":
        result = create_infographic(topic, data, style)
    else:
        result = generate_image(topic)
    
    print(json.dumps(result))

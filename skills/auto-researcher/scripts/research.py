#!/usr/bin/env python3
"""
Auto-Researcher v1.0
Automated web research with AI analysis and professional reports
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add skill directory to path
SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

from research_core import (
    search_web,
    fetch_content,
    analyze_with_ai,
    generate_image,
    create_pdf_report,
    create_google_doc,
    create_google_sheet,
    save_images,
    verify_google_outputs,
)


class AutoResearcher:
    """Main research pipeline orchestrator"""
    
    def __init__(self, output_dir: str = "./research-output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.research_data = {}
    
    def run(
        self,
        query: str,
        report_type: str = "brief",
        max_sources: int = 5,
        generate_pdf: bool = False,
        generate_docs: bool = False,
        generate_sheets: bool = False,
        num_images: int = 0,
    ) -> Dict:
        """Execute full research pipeline"""
        
        print(f"\n🔍 AUTO-RESEARCHER v1.0")
        print(f"   Query: {query}")
        print(f"   Type: {report_type}")
        print("=" * 60)
        
        results = {
            "query": query,
            "type": report_type,
            "timestamp": self.timestamp,
            "sources": [],
            "analysis": {},
            "images": [],
            "outputs": {},
        }
        
        try:
            # Step 1: Web Search
            print("\n[1/5] 🔍 Searching web...")
            sources = search_web(query, max_sources)
            results["sources"] = sources
            print(f"   Found {len(sources)} sources")
            
            if not sources:
                results["error"] = "No sources found"
                return results
            
            # Step 2: Fetch Content
            print("\n[2/5] 📄 Fetching content...")
            content = fetch_content(sources)
            results["content"] = content
            print(f"   Fetched {len(content)} articles")
            
            # Step 3: AI Analysis
            print("\n[3/5] 🧠 AI Analysis...")
            analysis = analyze_with_ai(query, content, report_type)
            results["analysis"] = analysis
            print(f"   Analysis complete: {len(analysis.get('key_points', []))} key points")
            
            # Step 4: Image Generation (if requested)
            if num_images > 0:
                print(f"\n[4/5] 🎨 Generating {num_images} info-graphics...")
                images = generate_image(query, analysis, num_images)
                results["images"] = images
                save_images(images, self.output_dir / "images")
                print(f"   Generated {len(images)} images")
            
            # Step 5: Generate Outputs
            print(f"\n[5/5] 📤 Generating outputs...")
            
            outputs = {}
            
            if generate_pdf:
                pdf_path = create_pdf_report(
                    query, analysis, results["sources"], 
                    results.get("images", []), report_type,
                    self.output_dir / f"report-{self.timestamp}.pdf"
                )
                outputs["pdf"] = str(pdf_path)
                print(f"   PDF: {pdf_path.name}")
            
            if generate_docs:
                doc_link = create_google_doc(query, analysis)
                outputs["docs"] = doc_link
                print(f"   Google Doc: {doc_link}")
            
            if generate_sheets:
                sheet_link = create_google_sheet(query, analysis)
                outputs["sheets"] = sheet_link
                print(f"   Google Sheet: {sheet_link}")
            
            results["outputs"] = outputs
            
            # Verify and fix Google outputs
            if generate_docs or generate_sheets:
                results["outputs"] = verify_google_outputs(
                    query, analysis, outputs, max_retries=3
                )
            
            # Save JSON data
            json_path = self.output_dir / f"data-{self.timestamp}.json"
            with open(json_path, "w") as f:
                json.dump(results, f, indent=2, default=str)
            outputs["data"] = str(json_path)
            
            print("\n" + "=" * 60)
            print("✅ RESEARCH COMPLETE")
            print("=" * 60)
            
            if outputs:
                print("\n📁 Outputs:")
                for key, path in outputs.items():
                    print(f"   • {key}: {path}")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            print(f"\n❌ Error: {e}")
            return results


def main():
    parser = argparse.ArgumentParser(
        description="Auto-Researcher: Automated web research with AI reports"
    )
    parser.add_argument("--query", "-q", required=True, help="Research topic")
    parser.add_argument(
        "--type", "-t", default="brief",
        choices=["brief", "analysis", "trends"],
        help="Report type"
    )
    parser.add_argument(
        "--max-sources", "-m", type=int, default=5,
        help="Maximum number of sources"
    )
    parser.add_argument("--pdf", action="store_true", help="Generate PDF report")
    parser.add_argument("--docs", action="store_true", help="Create Google Doc")
    parser.add_argument("--sheets", action="store_true", help="Create Google Sheet")
    parser.add_argument(
        "--images", "-i", type=int, default=0,
        help="Number of info-graphics to generate"
    )
    parser.add_argument(
        "--output-dir", "-o", default="./research-output",
        help="Output directory"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Enable all outputs (PDF, Docs, Sheets, Images)"
    )
    
    args = parser.parse_args()
    
    # Handle --all flag
    if args.all:
        args.pdf = True
        args.docs = True
        args.sheets = True
        args.images = max(args.images, 3)
    
    # Run research
    researcher = AutoResearcher(args.output_dir)
    results = researcher.run(
        query=args.query,
        report_type=args.type,
        max_sources=args.max_sources,
        generate_pdf=args.pdf,
        generate_docs=args.docs,
        generate_sheets=args.sheets,
        num_images=args.images,
    )
    
    # Exit with error code if failed
    if "error" in results:
        sys.exit(1)


if __name__ == "__main__":
    main()

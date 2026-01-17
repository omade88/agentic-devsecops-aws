#!/usr/bin/env python3
"""
AI-Powered PR Reviewer using Ollama (FREE Local AI)
Analyzes Terraform code changes and provides security insights
"""

import os
import sys
import json
import subprocess
import requests
from typing import List, Dict, Tuple
from pathlib import Path

class OllamaAIReviewer:
    """AI code reviewer using local Ollama models"""
    
    def __init__(self, model: str = "llama3.1:8b", endpoint: str = "http://localhost:11434"):
        self.model = model
        self.endpoint = endpoint
        self.api_url = f"{endpoint}/api/generate"
    
    def is_ollama_running(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def analyze_code(self, code: str, filepath: str) -> Dict[str, any]:
        """Analyze code using AI"""
        
        prompt = f"""You are a DevSecOps expert reviewing Terraform infrastructure code.

File: {filepath}

Code:
```terraform
{code}
```

Analyze this code and provide:
1. Security issues (critical vulnerabilities)
2. Best practice violations
3. Cost optimization opportunities
4. Compliance concerns

Format your response as:
SECURITY: [list issues]
BEST_PRACTICES: [list violations]
COST: [list optimizations]
COMPLIANCE: [list concerns]

Be concise and actionable."""

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 500
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "analysis": result.get("response", ""),
                    "model": self.model
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def parse_analysis(self, analysis: str) -> Dict[str, List[str]]:
        """Parse AI response into structured format"""
        
        result = {
            "security": [],
            "best_practices": [],
            "cost": [],
            "compliance": []
        }
        
        lines = analysis.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith("SECURITY:"):
                current_section = "security"
                line = line.replace("SECURITY:", "").strip()
            elif line.startswith("BEST_PRACTICES:"):
                current_section = "best_practices"
                line = line.replace("BEST_PRACTICES:", "").strip()
            elif line.startswith("COST:"):
                current_section = "cost"
                line = line.replace("COST:", "").strip()
            elif line.startswith("COMPLIANCE:"):
                current_section = "compliance"
                line = line.replace("COMPLIANCE:", "").strip()
            
            if current_section and line and line.startswith(('-', '•', '*')):
                result[current_section].append(line.lstrip('-•* '))
        
        return result

    def generate_review_comment(self, files_analyzed: List[Dict]) -> str:
        """Generate formatted review comment"""
        
        comment = "## 🤖 AI-Powered Code Review (Ollama)\n\n"
        comment += f"**Model:** `{self.model}`\n\n"
        
        has_issues = False
        
        for file_data in files_analyzed:
            filepath = file_data['filepath']
            analysis = file_data.get('parsed_analysis', {})
            
            if any(analysis.values()):
                has_issues = True
                comment += f"### 📄 `{filepath}`\n\n"
                
                if analysis.get('security'):
                    comment += "#### 🔒 Security Issues\n"
                    for issue in analysis['security']:
                        comment += f"- ⚠️ {issue}\n"
                    comment += "\n"
                
                if analysis.get('best_practices'):
                    comment += "#### 💡 Best Practices\n"
                    for bp in analysis['best_practices']:
                        comment += f"- 📋 {bp}\n"
                    comment += "\n"
                
                if analysis.get('cost'):
                    comment += "#### 💰 Cost Optimization\n"
                    for cost in analysis['cost']:
                        comment += f"- 💵 {cost}\n"
                    comment += "\n"
                
                if analysis.get('compliance'):
                    comment += "#### 📜 Compliance\n"
                    for comp in analysis['compliance']:
                        comment += f"- ✓ {comp}\n"
                    comment += "\n"
        
        if not has_issues:
            comment += "✅ **No issues found!** Code looks good.\n\n"
        
        comment += "---\n"
        comment += "*AI-powered review using free local models via Ollama. "
        comment += "[Learn more](https://ollama.ai)*\n"
        
        return comment


def get_changed_terraform_files() -> List[str]:
    """Get list of changed Terraform files in git"""
    try:
        # Change to git root directory to ensure paths are correct
        git_root = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD^', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=git_root
        )
        
        files = result.stdout.strip().split('\n')
        # Build full path for file existence check
        tf_files = [f for f in files if f.endswith('.tf') and os.path.exists(os.path.join(git_root, f))]
        # Return paths relative to git root
        return [os.path.join(git_root, f) for f in tf_files]
        
    except Exception as e:
        print(f"Error getting changed files: {e}")
        return []


def main():
    """Main function"""
    
    print("🤖 AI-Powered PR Reviewer (Ollama)")
    print("=" * 50)
    
    # Initialize reviewer
    reviewer = OllamaAIReviewer()
    
    # Check if Ollama is running
    if not reviewer.is_ollama_running():
        print("❌ Error: Ollama is not running!")
        print("Please start Ollama first:")
        print("  - Linux/Mac: ollama serve")
        print("  - Or run: ./ai-assistant/ollama-setup.sh")
        sys.exit(1)
    
    print(f"✅ Connected to Ollama at {reviewer.endpoint}")
    print(f"📦 Using model: {reviewer.model}\n")
    
    # Get changed files
    changed_files = get_changed_terraform_files()
    
    if not changed_files:
        print("ℹ️ No Terraform files changed")
        sys.exit(0)
    
    print(f"📝 Analyzing {len(changed_files)} file(s)...\n")
    
    # Analyze each file
    files_analyzed = []
    
    for filepath in changed_files:
        print(f"🔍 Analyzing: {filepath}")
        
        try:
            with open(filepath, 'r') as f:
                code = f.read()
            
            # Get AI analysis
            result = reviewer.analyze_code(code, filepath)
            
            if result['success']:
                parsed = reviewer.parse_analysis(result['analysis'])
                files_analyzed.append({
                    'filepath': filepath,
                    'analysis': result['analysis'],
                    'parsed_analysis': parsed
                })
                print(f"  ✅ Complete\n")
            else:
                print(f"  ❌ Error: {result.get('error', 'Unknown error')}\n")
                
        except Exception as e:
            print(f"  ❌ Error reading file: {e}\n")
    
    # Generate review comment
    if files_analyzed:
        comment = reviewer.generate_review_comment(files_analyzed)
        
        # Save to file
        output_file = 'ai_review_output.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(comment)
        
        print("=" * 50)
        print(f"✅ Review complete! Output saved to: {output_file}")
        print("\nPreview:")
        print(comment)
        
        # Check for critical security issues
        has_security_issues = any(
            file_data['parsed_analysis'].get('security')
            for file_data in files_analyzed
        )
        
        if has_security_issues:
            print("\n⚠️ WARNING: Security issues detected!")
            sys.exit(1)
    else:
        print("❌ No files were successfully analyzed")
        sys.exit(1)


if __name__ == "__main__":
    main()

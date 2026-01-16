#!/usr/bin/env python3
"""
Discord Bot for Infrastructure Notifications
FREE ChatOps integration for AWS events
"""

import os
import json
import requests
from typing import Dict, Optional
from datetime import datetime

class DiscordNotifier:
    """Send notifications to Discord via webhooks"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send_message(self, content: str, embed: Optional[Dict] = None) -> bool:
        """Send a message to Discord"""
        
        payload = {"content": content}
        
        if embed:
            payload["embeds"] = [embed]
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response.status_code == 204
        except Exception as e:
            print(f"Error sending Discord message: {e}")
            return False
    
    def send_deployment_notification(self, deployment_data: Dict) -> bool:
        """Send deployment notification"""
        
        status = deployment_data.get('status', 'unknown')
        environment = deployment_data.get('environment', 'unknown')
        
        # Choose emoji based on status
        emoji = "✅" if status == "success" else "❌" if status == "failed" else "⏳"
        color = 0x00FF00 if status == "success" else 0xFF0000 if status == "failed" else 0xFFFF00
        
        embed = {
            "title": f"{emoji} Deployment {status.title()}",
            "description": f"Environment: **{environment}**",
            "color": color,
            "fields": [
                {
                    "name": "PR",
                    "value": f"#{deployment_data.get('pr_number', 'N/A')}",
                    "inline": True
                },
                {
                    "name": "Commit",
                    "value": deployment_data.get('commit_sha', 'N/A')[:7],
                    "inline": True
                },
                {
                    "name": "Deployed By",
                    "value": deployment_data.get('deployed_by', 'GitHub Actions'),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if deployment_data.get('resources'):
            resources_text = "\n".join(f"• {r}" for r in deployment_data['resources'])
            embed["fields"].append({
                "name": "Resources",
                "value": resources_text,
                "inline": False
            })
        
        return self.send_message("", embed=embed)
    
    def send_security_alert(self, alert_data: Dict) -> bool:
        """Send security alert"""
        
        severity = alert_data.get('severity', 'medium').lower()
        
        # Color based on severity
        color_map = {
            "critical": 0xFF0000,
            "high": 0xFF6600,
            "medium": 0xFFCC00,
            "low": 0x00CCFF
        }
        color = color_map.get(severity, 0x808080)
        
        embed = {
            "title": f"🚨 Security Alert: {alert_data.get('title', 'Unknown')}",
            "description": alert_data.get('description', ''),
            "color": color,
            "fields": [
                {
                    "name": "Severity",
                    "value": severity.upper(),
                    "inline": True
                },
                {
                    "name": "Resource",
                    "value": alert_data.get('resource', 'N/A'),
                    "inline": True
                },
                {
                    "name": "Action Taken",
                    "value": alert_data.get('action', 'None'),
                    "inline": False
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return self.send_message("@here" if severity in ["critical", "high"] else "", embed=embed)
    
    def send_cost_alert(self, cost_data: Dict) -> bool:
        """Send cost optimization alert"""
        
        embed = {
            "title": "💰 Cost Optimization Alert",
            "description": cost_data.get('message', ''),
            "color": 0xFFCC00,
            "fields": [
                {
                    "name": "Current Cost",
                    "value": f"${cost_data.get('current_cost', 0):.2f}",
                    "inline": True
                },
                {
                    "name": "Projected Cost",
                    "value": f"${cost_data.get('projected_cost', 0):.2f}",
                    "inline": True
                },
                {
                    "name": "Potential Savings",
                    "value": f"${cost_data.get('savings', 0):.2f}",
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if cost_data.get('recommendations'):
            rec_text = "\n".join(f"• {r}" for r in cost_data['recommendations'])
            embed["fields"].append({
                "name": "Recommendations",
                "value": rec_text,
                "inline": False
            })
        
        return self.send_message("", embed=embed)
    
    def send_pr_review(self, pr_data: Dict) -> bool:
        """Send PR review notification"""
        
        issues_count = len(pr_data.get('issues', []))
        color = 0xFF0000 if issues_count > 0 else 0x00FF00
        
        embed = {
            "title": f"🤖 AI Code Review - PR #{pr_data.get('pr_number')}",
            "description": pr_data.get('title', ''),
            "color": color,
            "fields": [
                {
                    "name": "Issues Found",
                    "value": str(issues_count),
                    "inline": True
                },
                {
                    "name": "Files Changed",
                    "value": str(len(pr_data.get('files', []))),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if pr_data.get('issues'):
            issues_text = "\n".join(f"• {i}" for i in pr_data['issues'][:5])
            if len(pr_data['issues']) > 5:
                issues_text += f"\n... and {len(pr_data['issues']) - 5} more"
            
            embed["fields"].append({
                "name": "Top Issues",
                "value": issues_text,
                "inline": False
            })
        
        return self.send_message("", embed=embed)


# Example usage
if __name__ == "__main__":
    # Get webhook URL from environment
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL not set")
        print("Export it first: export DISCORD_WEBHOOK_URL='your-webhook-url'")
        exit(1)
    
    notifier = DiscordNotifier(webhook_url)
    
    # Test message
    print("Sending test notification...")
    success = notifier.send_message("🚀 Discord notifications are working!")
    
    if success:
        print("✅ Test notification sent successfully!")
    else:
        print("❌ Failed to send notification")

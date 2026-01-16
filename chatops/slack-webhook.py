#!/usr/bin/env python3
"""
Slack Webhook Integration
FREE ChatOps notifications for Slack
"""

import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime

class SlackNotifier:
    """Send notifications to Slack via webhooks"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send_message(self, text: str, blocks: Optional[List[Dict]] = None) -> bool:
        """Send a message to Slack"""
        
        payload = {"text": text}
        
        if blocks:
            payload["blocks"] = blocks
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending Slack message: {e}")
            return False
    
    def send_deployment_notification(self, deployment_data: Dict) -> bool:
        """Send deployment notification"""
        
        status = deployment_data.get('status', 'unknown')
        environment = deployment_data.get('environment', 'unknown')
        
        # Choose emoji based on status
        emoji = ":white_check_mark:" if status == "success" else ":x:" if status == "failed" else ":hourglass:"
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} Deployment {status.title()}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Environment:*\n{environment}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*PR:*\n#{deployment_data.get('pr_number', 'N/A')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Commit:*\n{deployment_data.get('commit_sha', 'N/A')[:7]}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Deployed By:*\n{deployment_data.get('deployed_by', 'GitHub Actions')}"
                    }
                ]
            }
        ]
        
        if deployment_data.get('resources'):
            resources_text = "\n".join(f"• {r}" for r in deployment_data['resources'])
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Resources:*\n{resources_text}"
                }
            })
        
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
                }
            ]
        })
        
        return self.send_message(f"Deployment {status}", blocks=blocks)
    
    def send_security_alert(self, alert_data: Dict) -> bool:
        """Send security alert"""
        
        severity = alert_data.get('severity', 'medium').lower()
        
        # Emoji based on severity
        emoji_map = {
            "critical": ":rotating_light:",
            "high": ":warning:",
            "medium": ":large_orange_diamond:",
            "low": ":information_source:"
        }
        emoji = emoji_map.get(severity, ":grey_question:")
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} Security Alert: {alert_data.get('title', 'Unknown')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": alert_data.get('description', '')
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Severity:*\n{severity.upper()}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Resource:*\n{alert_data.get('resource', 'N/A')}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Action Taken:*\n{alert_data.get('action', 'None')}"
                }
            }
        ]
        
        # Mention channel for critical/high
        text = "<!channel>" if severity in ["critical", "high"] else "Security Alert"
        
        return self.send_message(text, blocks=blocks)
    
    def send_cost_alert(self, cost_data: Dict) -> bool:
        """Send cost optimization alert"""
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":moneybag: Cost Optimization Alert"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": cost_data.get('message', '')
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Current Cost:*\n${cost_data.get('current_cost', 0):.2f}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Projected Cost:*\n${cost_data.get('projected_cost', 0):.2f}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Potential Savings:*\n${cost_data.get('savings', 0):.2f}"
                    }
                ]
            }
        ]
        
        if cost_data.get('recommendations'):
            rec_text = "\n".join(f"• {r}" for r in cost_data['recommendations'])
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Recommendations:*\n{rec_text}"
                }
            })
        
        return self.send_message("Cost Optimization Alert", blocks=blocks)
    
    def send_pr_review(self, pr_data: Dict) -> bool:
        """Send PR review notification"""
        
        issues_count = len(pr_data.get('issues', []))
        emoji = ":white_check_mark:" if issues_count == 0 else ":warning:"
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} AI Code Review - PR #{pr_data.get('pr_number')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": pr_data.get('title', '')
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Issues Found:*\n{issues_count}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Files Changed:*\n{len(pr_data.get('files', []))}"
                    }
                ]
            }
        ]
        
        if pr_data.get('issues'):
            issues_text = "\n".join(f"• {i}" for i in pr_data['issues'][:5])
            if len(pr_data['issues']) > 5:
                issues_text += f"\n... and {len(pr_data['issues']) - 5} more"
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Top Issues:*\n{issues_text}"
                }
            })
        
        if pr_data.get('pr_url'):
            blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "View PR"
                        },
                        "url": pr_data['pr_url']
                    }
                ]
            })
        
        return self.send_message(f"PR #{pr_data.get('pr_number')} Review", blocks=blocks)


# Example usage
if __name__ == "__main__":
    # Get webhook URL from environment
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    
    if not webhook_url:
        print("Error: SLACK_WEBHOOK_URL not set")
        print("Export it first: export SLACK_WEBHOOK_URL='your-webhook-url'")
        exit(1)
    
    notifier = SlackNotifier(webhook_url)
    
    # Test message
    print("Sending test notification...")
    success = notifier.send_message(":rocket: Slack notifications are working!")
    
    if success:
        print("✅ Test notification sent successfully!")
    else:
        print("❌ Failed to send notification")

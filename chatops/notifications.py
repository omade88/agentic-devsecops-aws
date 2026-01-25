#!/usr/bin/env python3
"""
Universal Notification Handler
Supports Discord, Slack, and email notifications
"""

import os
import sys
import json
import argparse
from typing import Dict, Optional

try:
    from discord_bot import DiscordNotifier
    from slack_webhook import SlackNotifier
except ImportError:
    print("Error: Required modules not found. Install dependencies first.")
    sys.exit(1)


class NotificationManager:
    """Manage notifications across multiple platforms"""

    def __init__(self):
        self.discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')
        self.slack_webhook = os.environ.get('SLACK_WEBHOOK_URL')

        self.discord = DiscordNotifier(self.discord_webhook) if self.discord_webhook else None
        self.slack = SlackNotifier(self.slack_webhook) if self.slack_webhook else None

    def send_deployment(self, data: Dict):
        """Send deployment notification to all configured platforms"""

        results = {}

        if self.discord:
            results['discord'] = self.discord.send_deployment_notification(data)

        if self.slack:
            results['slack'] = self.slack.send_deployment_notification(data)

        return results

    def send_security_alert(self, data: Dict):
        """Send security alert to all configured platforms"""

        results = {}

        if self.discord:
            results['discord'] = self.discord.send_security_alert(data)

        if self.slack:
            results['slack'] = self.slack.send_security_alert(data)

        return results

    def send_cost_alert(self, data: Dict):
        """Send cost alert to all configured platforms"""

        results = {}

        if self.discord:
            results['discord'] = self.discord.send_cost_alert(data)

        if self.slack:
            results['slack'] = self.slack.send_cost_alert(data)

        return results

    def send_pr_review(self, data: Dict):
        """Send PR review to all configured platforms"""

        results = {}

        if self.discord:
            results['discord'] = self.discord.send_pr_review(data)

        if self.slack:
            results['slack'] = self.slack.send_pr_review(data)

        return results


def main():
    """CLI interface for notifications"""

    parser = argparse.ArgumentParser(description='Send notifications to configured platforms')
    parser.add_argument('--type', '-t', required=True,
                        choices=['deployment', 'security', 'cost', 'pr'],
                        help='Type of notification')
    parser.add_argument('--data', '-d', type=str,
                        help='JSON data for notification')
    parser.add_argument('--file', '-f', type=str,
                        help='JSON file with notification data')

    args = parser.parse_args()

    # Load data
    if args.file:
        with open(args.file, 'r') as f:
            data = json.load(f)
    elif args.data:
        data = json.loads(args.data)
    else:
        print("Error: Either --data or --file must be provided")
        sys.exit(1)

    # Send notification
    manager = NotificationManager()

    if args.type == 'deployment':
        results = manager.send_deployment(data)
    elif args.type == 'security':
        results = manager.send_security_alert(data)
    elif args.type == 'cost':
        results = manager.send_cost_alert(data)
    elif args.type == 'pr':
        results = manager.send_pr_review(data)

    print(f"Notification results: {json.dumps(results, indent=2)}")

    # Exit with error if all failed
    if all(not success for success in results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()

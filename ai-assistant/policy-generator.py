#!/usr/bin/env python3
"""
AI-Powered OPA/Sentinel Policy Generator
Converts natural language requirements into policy-as-code
"""

import os
import sys
import json
import requests
import argparse
from typing import Dict, Optional

class PolicyGenerator:
    """Generate OPA and Sentinel policies using AI"""

    def __init__(self, model: str = "llama3.1:8b", endpoint: str = "http://localhost:11434"):
        self.model = model
        self.endpoint = endpoint
        self.api_url = f"{endpoint}/api/generate"

    def generate_opa_policy(self, requirement: str) -> Optional[str]:
        """Generate OPA policy from natural language requirement"""

        prompt = f"""You are an expert in Open Policy Agent (OPA) and Rego policy language.

Requirement: {requirement}

Generate a complete OPA/Rego policy that enforces this requirement for Terraform infrastructure.

Include:
1. Package declaration
2. Import statements if needed
3. Deny rules with clear messages
4. Comments explaining the logic

Output ONLY the Rego code, no explanations before or after.
"""

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 1000
                    }
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                policy_code = result.get("response", "")

                # Clean up the response
                policy_code = policy_code.strip()
                if "```rego" in policy_code:
                    policy_code = policy_code.split("```rego")[1].split("```")[0].strip()
                elif "```" in policy_code:
                    policy_code = policy_code.split("```")[1].split("```")[0].strip()

                return policy_code
            else:
                print(f"❌ Error: API returned status {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error generating policy: {e}")
            return None

    def generate_sentinel_policy(self, requirement: str) -> Optional[str]:
        """Generate Sentinel policy from natural language requirement"""

        prompt = f"""You are an expert in HashiCorp Sentinel policy language.

Requirement: {requirement}

Generate a complete Sentinel policy that enforces this requirement for Terraform infrastructure.

Include:
1. Import statements
2. Rules with clear conditions
3. Main rule that combines all checks
4. Helpful comments

Output ONLY the Sentinel code, no explanations before or after.
"""

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 1000
                    }
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                policy_code = result.get("response", "")

                # Clean up the response
                policy_code = policy_code.strip()
                if "```sentinel" in policy_code:
                    policy_code = policy_code.split("```sentinel")[1].split("```")[0].strip()
                elif "```" in policy_code:
                    policy_code = policy_code.split("```")[1].split("```")[0].strip()

                return policy_code
            else:
                print(f"❌ Error: API returned status {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error generating policy: {e}")
            return None

    def generate_test_cases(self, policy_type: str, requirement: str) -> Optional[str]:
        """Generate test cases for the policy"""

        prompt = f"""Generate test cases for a {policy_type} policy that enforces: {requirement}

Provide both positive (should pass) and negative (should fail) test scenarios.
Format as JSON with 'pass' and 'fail' arrays.
"""

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
                return result.get("response", "")
            else:
                return None

        except Exception as e:
            print(f"⚠️ Warning: Could not generate test cases: {e}")
            return None


def save_policy(policy_code: str, filename: str, policy_dir: str = "policies") -> bool:
    """Save generated policy to file"""

    try:
        os.makedirs(policy_dir, exist_ok=True)
        filepath = os.path.join(policy_dir, filename)

        with open(filepath, 'w') as f:
            f.write(policy_code)

        print(f"✅ Policy saved to: {filepath}")
        return True

    except Exception as e:
        print(f"❌ Error saving policy: {e}")
        return False


def interactive_mode():
    """Interactive mode for policy generation"""

    print("\n" + "=" * 60)
    print("🤖 AI-Powered Policy Generator (Interactive Mode)")
    print("=" * 60)

    generator = PolicyGenerator()

    print("\nExamples of requirements you can provide:")
    print("  • Block all EC2 instances without IMDSv2")
    print("  • Require encryption for all EBS volumes")
    print("  • Deny security groups with 0.0.0.0/0 on port 22")
    print("  • Enforce mandatory tags: Environment, Owner, CostCenter")
    print()

    requirement = input("📝 Enter your policy requirement: ").strip()

    if not requirement:
        print("❌ No requirement provided")
        return

    print(f"\n🎯 Requirement: {requirement}")
    print("\nSelect policy type:")
    print("  1. OPA (Rego)")
    print("  2. Sentinel")
    print("  3. Both")

    choice = input("\nChoice (1/2/3): ").strip()

    if choice in ['1', '3']:
        print("\n🔨 Generating OPA policy...")
        opa_policy = generator.generate_opa_policy(requirement)

        if opa_policy:
            print("\n" + "=" * 60)
            print("OPA Policy:")
            print("=" * 60)
            print(opa_policy)
            print("=" * 60)

            save = input("\n💾 Save this policy? (y/n): ").strip().lower()
            if save == 'y':
                filename = input("Enter filename (e.g., ec2-imdsv2.rego): ").strip()
                if not filename.endswith('.rego'):
                    filename += '.rego'
                save_policy(opa_policy, filename, "policies/opa")

    if choice in ['2', '3']:
        print("\n🔨 Generating Sentinel policy...")
        sentinel_policy = generator.generate_sentinel_policy(requirement)

        if sentinel_policy:
            print("\n" + "=" * 60)
            print("Sentinel Policy:")
            print("=" * 60)
            print(sentinel_policy)
            print("=" * 60)

            save = input("\n💾 Save this policy? (y/n): ").strip().lower()
            if save == 'y':
                filename = input("Enter filename (e.g., ec2-imdsv2.sentinel): ").strip()
                if not filename.endswith('.sentinel'):
                    filename += '.sentinel'
                save_policy(sentinel_policy, filename, "policies/sentinel")


def main():
    """Main function"""

    parser = argparse.ArgumentParser(
        description='AI-Powered Policy Generator for OPA and Sentinel'
    )
    parser.add_argument(
        '--requirement', '-r',
        type=str,
        help='Policy requirement in natural language'
    )
    parser.add_argument(
        '--type', '-t',
        choices=['opa', 'sentinel', 'both'],
        default='opa',
        help='Policy type to generate'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output filename'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )

    args = parser.parse_args()

    if args.interactive or not args.requirement:
        interactive_mode()
        return

    generator = PolicyGenerator()

    print(f"🎯 Generating policy for: {args.requirement}")

    if args.type in ['opa', 'both']:
        print("\n🔨 Generating OPA policy...")
        opa_policy = generator.generate_opa_policy(args.requirement)

        if opa_policy:
            print(opa_policy)
            if args.output:
                save_policy(opa_policy, args.output, "policies/opa")

    if args.type in ['sentinel', 'both']:
        print("\n🔨 Generating Sentinel policy...")
        sentinel_policy = generator.generate_sentinel_policy(args.requirement)

        if sentinel_policy:
            print(sentinel_policy)
            if args.output:
                save_policy(sentinel_policy, args.output, "policies/sentinel")


if __name__ == "__main__":
    main()

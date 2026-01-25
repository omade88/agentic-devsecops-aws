"""
AWS Lambda Function: Security Response Handler
Responds to security events from AWS Security Hub, GuardDuty, etc.
"""

import json
import boto3
import os
from typing import Dict
from datetime import datetime

# Initialize clients
ec2 = boto3.client('ec2')
sns = boto3.client('sns')
ssm = boto3.client('ssm')

SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')

def lambda_handler(event, context):
    """Main handler for security events"""

    print(f"Security event received: {json.dumps(event)}")

    response = {
        'timestamp': datetime.utcnow().isoformat(),
        'actions_taken': [],
        'alerts_sent': []
    }

    try:
        # Determine event source
        source = event.get('source', '')

        if 'guardduty' in source.lower():
            result = handle_guardduty_finding(event)
            response['actions_taken'].append(result)

        elif 'securityhub' in source.lower():
            result = handle_securityhub_finding(event)
            response['actions_taken'].append(result)

        elif 'config' in source.lower():
            result = handle_config_violation(event)
            response['actions_taken'].append(result)

        # Send alert
        if response['actions_taken']:
            send_security_alert(response)
            response['alerts_sent'].append('SNS notification sent')

    except Exception as e:
        print(f"Error handling security event: {e}")
        response['error'] = str(e)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def handle_guardduty_finding(event: Dict) -> Dict:
    """Handle GuardDuty security findings"""

    detail = event.get('detail', {})
    finding_type = detail.get('type', '')
    severity = detail.get('severity', 0)

    action = {
        'source': 'guardduty',
        'finding_type': finding_type,
        'severity': severity,
        'actions': []
    }

    # High severity findings - take immediate action
    if severity >= 7:
        # Check for compromised instance
        if 'UnauthorizedAccess' in finding_type or 'CryptoCurrency' in finding_type:
            resource = detail.get('resource', {})
            instance_id = resource.get('instanceDetails', {}).get('instanceId')

            if instance_id:
                # Isolate the instance
                try:
                    # Create isolation security group
                    isolation_sg = create_isolation_security_group()

                    # Apply to instance
                    ec2.modify_instance_attribute(
                        InstanceId=instance_id,
                        Groups=[isolation_sg]
                    )

                    action['actions'].append({
                        'action': 'isolated_instance',
                        'instance_id': instance_id,
                        'security_group': isolation_sg
                    })

                    # Create snapshot for forensics
                    volumes = ec2.describe_volumes(
                        Filters=[
                            {'Name': 'attachment.instance-id', 'Values': [instance_id]}
                        ]
                    )

                    for volume in volumes['Volumes']:
                        snapshot = ec2.create_snapshot(
                            VolumeId=volume['VolumeId'],
                            Description=f'Forensic snapshot - GuardDuty finding {finding_type}'
                        )
                        action['actions'].append({
                            'action': 'created_snapshot',
                            'volume_id': volume['VolumeId'],
                            'snapshot_id': snapshot['SnapshotId']
                        })

                except Exception as e:
                    action['error'] = str(e)

    return action


def handle_securityhub_finding(event: Dict) -> Dict:
    """Handle Security Hub findings"""

    detail = event.get('detail', {})
    findings = detail.get('findings', [])

    action = {
        'source': 'securityhub',
        'findings_count': len(findings),
        'actions': []
    }

    for finding in findings:
        severity = finding.get('Severity', {}).get('Label', '')
        title = finding.get('Title', '')

        # Handle specific finding types
        if 'S3' in title and 'public' in title.lower():
            # Block public access on S3 bucket
            resources = finding.get('Resources', [])
            for resource in resources:
                if resource.get('Type') == 'AwsS3Bucket':
                    bucket_name = resource.get('Id', '').split(':')[-1]
                    try:
                        s3 = boto3.client('s3')
                        s3.put_public_access_block(
                            Bucket=bucket_name,
                            PublicAccessBlockConfiguration={
                                'BlockPublicAcls': True,
                                'IgnorePublicAcls': True,
                                'BlockPublicPolicy': True,
                                'RestrictPublicBuckets': True
                            }
                        )
                        action['actions'].append({
                            'action': 'blocked_s3_public_access',
                            'bucket': bucket_name
                        })
                    except Exception as e:
                        action['actions'].append({
                            'action': 'failed',
                            'bucket': bucket_name,
                            'error': str(e)
                        })

    return action


def handle_config_violation(event: Dict) -> Dict:
    """Handle AWS Config compliance violations"""

    detail = event.get('detail', {})
    config_rule_name = detail.get('configRuleName', '')
    compliance_type = detail.get('newEvaluationResult', {}).get('complianceType', '')

    action = {
        'source': 'config',
        'rule': config_rule_name,
        'compliance': compliance_type,
        'actions': []
    }

    if compliance_type == 'NON_COMPLIANT':
        # Log the violation
        action['actions'].append({
            'action': 'logged_violation',
            'rule': config_rule_name
        })

        # Take remediation action based on rule
        if 'encryption' in config_rule_name.lower():
            action['actions'].append({
                'action': 'alert',
                'message': 'Encryption violation detected - manual review required'
            })

    return action


def create_isolation_security_group() -> str:
    """Create a security group that blocks all traffic"""

    try:
        # Get default VPC
        vpcs = ec2.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
        vpc_id = vpcs['Vpcs'][0]['VpcId']

        # Create isolation security group
        sg = ec2.create_security_group(
            GroupName=f'isolation-sg-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
            Description='Isolation security group for compromised instances',
            VpcId=vpc_id
        )

        sg_id = sg['GroupId']

        # Add tags
        ec2.create_tags(
            Resources=[sg_id],
            Tags=[
                {'Key': 'Name', 'Value': 'Isolation-SG'},
                {'Key': 'Purpose', 'Value': 'Security-Incident-Response'},
                {'Key': 'CreatedBy', 'Value': 'AutoRemediation'}
            ]
        )

        return sg_id

    except Exception as e:
        print(f"Error creating isolation SG: {e}")
        raise


def send_security_alert(response: Dict):
    """Send security alert via SNS"""

    if not SNS_TOPIC_ARN:
        print("No SNS topic configured")
        return

    message = f"""🚨 SECURITY ALERT 🚨

Timestamp: {response['timestamp']}

Actions Taken:
{json.dumps(response['actions_taken'], indent=2)}

This is an automated security response from AWS Lambda.
Review the actions taken and investigate the security event.
"""

    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='🚨 AWS Security Alert - Automated Response',
            Message=message
        )
        print("Security alert sent successfully")
    except Exception as e:
        print(f"Error sending security alert: {e}")

"""
AWS Lambda Function: Auto-Remediation for Security Issues
Automatically fixes common security misconfigurations
"""

import json
import boto3
import os
from typing import Dict, List
from datetime import datetime

# Initialize AWS clients
ec2 = boto3.client('ec2')
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Configuration
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')
DRY_RUN = os.environ.get('DRY_RUN', 'false').lower() == 'true'
AUTO_FIX_ENABLED = os.environ.get('AUTO_FIX_ENABLED', 'true').lower() == 'true'

def lambda_handler(event, context):
    """Main Lambda handler"""
    
    print(f"Received event: {json.dumps(event)}")
    
    results = {
        'timestamp': datetime.utcnow().isoformat(),
        'fixes_applied': [],
        'errors': [],
        'dry_run': DRY_RUN
    }
    
    try:
        # Determine event source
        if 'detail-type' in event:
            # EventBridge event
            detail_type = event['detail-type']
            
            if 'Security Group' in detail_type:
                result = fix_security_group_issues(event)
                results['fixes_applied'].append(result)
            
            elif 'EC2 Instance' in detail_type:
                result = fix_ec2_instance_issues(event)
                results['fixes_applied'].append(result)
            
            elif 'S3' in detail_type:
                result = fix_s3_bucket_issues(event)
                results['fixes_applied'].append(result)
        
        # Send notification
        if results['fixes_applied'] and SNS_TOPIC_ARN:
            send_notification(results)
        
    except Exception as e:
        error_msg = f"Error in auto-remediation: {str(e)}"
        print(error_msg)
        results['errors'].append(error_msg)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }


def fix_security_group_issues(event: Dict) -> Dict:
    """Fix security group misconfigurations"""
    
    detail = event.get('detail', {})
    sg_id = detail.get('requestParameters', {}).get('groupId')
    
    if not sg_id:
        return {'action': 'skip', 'reason': 'No security group ID found'}
    
    fixes = []
    
    try:
        # Get security group details
        response = ec2.describe_security_groups(GroupIds=[sg_id])
        sg = response['SecurityGroups'][0]
        
        # Check for overly permissive rules
        for rule in sg.get('IpPermissions', []):
            # Check for SSH (22) open to 0.0.0.0/0
            if rule.get('FromPort') == 22:
                for ip_range in rule.get('IpRanges', []):
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        if AUTO_FIX_ENABLED and not DRY_RUN:
                            # Remove the rule
                            ec2.revoke_security_group_ingress(
                                GroupId=sg_id,
                                IpPermissions=[rule]
                            )
                            fixes.append({
                                'action': 'removed_rule',
                                'sg_id': sg_id,
                                'port': 22,
                                'cidr': '0.0.0.0/0',
                                'reason': 'SSH open to internet'
                            })
                        else:
                            fixes.append({
                                'action': 'detected',
                                'sg_id': sg_id,
                                'port': 22,
                                'issue': 'SSH open to 0.0.0.0/0',
                                'dry_run': DRY_RUN
                            })
            
            # Check for RDP (3389) open to 0.0.0.0/0
            if rule.get('FromPort') == 3389:
                for ip_range in rule.get('IpRanges', []):
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        if AUTO_FIX_ENABLED and not DRY_RUN:
                            ec2.revoke_security_group_ingress(
                                GroupId=sg_id,
                                IpPermissions=[rule]
                            )
                            fixes.append({
                                'action': 'removed_rule',
                                'sg_id': sg_id,
                                'port': 3389,
                                'cidr': '0.0.0.0/0',
                                'reason': 'RDP open to internet'
                            })
                        else:
                            fixes.append({
                                'action': 'detected',
                                'sg_id': sg_id,
                                'port': 3389,
                                'issue': 'RDP open to 0.0.0.0/0',
                                'dry_run': DRY_RUN
                            })
        
        return {
            'resource_type': 'security_group',
            'resource_id': sg_id,
            'fixes': fixes,
            'count': len(fixes)
        }
        
    except Exception as e:
        return {
            'resource_type': 'security_group',
            'resource_id': sg_id,
            'error': str(e)
        }


def fix_ec2_instance_issues(event: Dict) -> Dict:
    """Fix EC2 instance misconfigurations"""
    
    detail = event.get('detail', {})
    instance_id = detail.get('instance-id') or detail.get('requestParameters', {}).get('instanceId')
    
    if not instance_id:
        return {'action': 'skip', 'reason': 'No instance ID found'}
    
    fixes = []
    
    try:
        # Get instance details
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        
        # Check for missing tags
        tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
        required_tags = ['Environment', 'Owner', 'CostCenter']
        missing_tags = [tag for tag in required_tags if tag not in tags]
        
        if missing_tags:
            if AUTO_FIX_ENABLED and not DRY_RUN:
                # Add default tags
                new_tags = [
                    {'Key': 'Environment', 'Value': 'untagged'},
                    {'Key': 'Owner', 'Value': 'auto-remediation'},
                    {'Key': 'CostCenter', 'Value': 'default'}
                ]
                ec2.create_tags(
                    Resources=[instance_id],
                    Tags=[tag for tag in new_tags if tag['Key'] in missing_tags]
                )
                fixes.append({
                    'action': 'added_tags',
                    'instance_id': instance_id,
                    'tags_added': missing_tags
                })
            else:
                fixes.append({
                    'action': 'detected',
                    'instance_id': instance_id,
                    'issue': f'Missing tags: {missing_tags}',
                    'dry_run': DRY_RUN
                })
        
        # Check for IMDSv2
        metadata_options = instance.get('MetadataOptions', {})
        if metadata_options.get('HttpTokens') != 'required':
            if AUTO_FIX_ENABLED and not DRY_RUN:
                ec2.modify_instance_metadata_options(
                    InstanceId=instance_id,
                    HttpTokens='required',
                    HttpPutResponseHopLimit=1
                )
                fixes.append({
                    'action': 'enforced_imdsv2',
                    'instance_id': instance_id
                })
            else:
                fixes.append({
                    'action': 'detected',
                    'instance_id': instance_id,
                    'issue': 'IMDSv2 not enforced',
                    'dry_run': DRY_RUN
                })
        
        return {
            'resource_type': 'ec2_instance',
            'resource_id': instance_id,
            'fixes': fixes,
            'count': len(fixes)
        }
        
    except Exception as e:
        return {
            'resource_type': 'ec2_instance',
            'resource_id': instance_id,
            'error': str(e)
        }


def fix_s3_bucket_issues(event: Dict) -> Dict:
    """Fix S3 bucket misconfigurations"""
    
    detail = event.get('detail', {})
    bucket_name = detail.get('requestParameters', {}).get('bucketName')
    
    if not bucket_name:
        return {'action': 'skip', 'reason': 'No bucket name found'}
    
    fixes = []
    
    try:
        # Check encryption
        try:
            s3.get_bucket_encryption(Bucket=bucket_name)
        except s3.exceptions.ServerSideEncryptionConfigurationNotFoundError:
            if AUTO_FIX_ENABLED and not DRY_RUN:
                s3.put_bucket_encryption(
                    Bucket=bucket_name,
                    ServerSideEncryptionConfiguration={
                        'Rules': [{
                            'ApplyServerSideEncryptionByDefault': {
                                'SSEAlgorithm': 'AES256'
                            }
                        }]
                    }
                )
                fixes.append({
                    'action': 'enabled_encryption',
                    'bucket': bucket_name
                })
            else:
                fixes.append({
                    'action': 'detected',
                    'bucket': bucket_name,
                    'issue': 'Encryption not enabled',
                    'dry_run': DRY_RUN
                })
        
        # Check versioning
        versioning = s3.get_bucket_versioning(Bucket=bucket_name)
        if versioning.get('Status') != 'Enabled':
            if AUTO_FIX_ENABLED and not DRY_RUN:
                s3.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={'Status': 'Enabled'}
                )
                fixes.append({
                    'action': 'enabled_versioning',
                    'bucket': bucket_name
                })
            else:
                fixes.append({
                    'action': 'detected',
                    'bucket': bucket_name,
                    'issue': 'Versioning not enabled',
                    'dry_run': DRY_RUN
                })
        
        # Block public access
        try:
            public_access = s3.get_public_access_block(Bucket=bucket_name)
            config = public_access['PublicAccessBlockConfiguration']
            
            if not all([
                config.get('BlockPublicAcls'),
                config.get('IgnorePublicAcls'),
                config.get('BlockPublicPolicy'),
                config.get('RestrictPublicBuckets')
            ]):
                if AUTO_FIX_ENABLED and not DRY_RUN:
                    s3.put_public_access_block(
                        Bucket=bucket_name,
                        PublicAccessBlockConfiguration={
                            'BlockPublicAcls': True,
                            'IgnorePublicAcls': True,
                            'BlockPublicPolicy': True,
                            'RestrictPublicBuckets': True
                        }
                    )
                    fixes.append({
                        'action': 'blocked_public_access',
                        'bucket': bucket_name
                    })
                else:
                    fixes.append({
                        'action': 'detected',
                        'bucket': bucket_name,
                        'issue': 'Public access not fully blocked',
                        'dry_run': DRY_RUN
                    })
        except:
            pass
        
        return {
            'resource_type': 's3_bucket',
            'resource_id': bucket_name,
            'fixes': fixes,
            'count': len(fixes)
        }
        
    except Exception as e:
        return {
            'resource_type': 's3_bucket',
            'resource_id': bucket_name,
            'error': str(e)
        }


def send_notification(results: Dict):
    """Send SNS notification about fixes"""
    
    message = f"""Auto-Remediation Report

Timestamp: {results['timestamp']}
Dry Run: {results['dry_run']}

Fixes Applied: {len(results['fixes_applied'])}

"""
    
    for fix in results['fixes_applied']:
        message += f"\n{json.dumps(fix, indent=2)}\n"
    
    if results['errors']:
        message += f"\n\nErrors: {len(results['errors'])}\n"
        for error in results['errors']:
            message += f"- {error}\n"
    
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='AWS Auto-Remediation Report',
            Message=message
        )
    except Exception as e:
        print(f"Error sending notification: {e}")

# OPA Policy Template: EC2 Instance Compliance
# Ensures EC2 instances follow security best practices

package terraform.security.ec2_compliance

import future.keywords.in

# Required tags for all EC2 instances
required_tags := {"Environment", "Owner", "CostCenter"}

# Deny EC2 instances without required tags
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"

    provided_tags := {tag | resource.change.after.tags[tag]}
    missing := required_tags - provided_tags
    count(missing) > 0

    msg := sprintf(
        "EC2 instance '%s' missing required tags: %v",
        [resource.address, missing]
    )
}

# Deny EC2 instances with unencrypted EBS volumes
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"

    # Check root block device
    root_device := resource.change.after.root_block_device[0]
    not root_device.encrypted

    msg := sprintf(
        "EC2 instance '%s' has unencrypted root volume - encryption required",
        [resource.address]
    )
}

# Deny EC2 instances without IMDSv2 enforced
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"

    metadata_options := resource.change.after.metadata_options[0]
    metadata_options.http_tokens != "required"

    msg := sprintf(
        "EC2 instance '%s' does not enforce IMDSv2 - security requirement",
        [resource.address]
    )
}

# Deny EC2 instances with public IPs in production
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"

    # Check if environment is production
    resource.change.after.tags.Environment == "prod"
    resource.change.after.associate_public_ip_address == true

    msg := sprintf(
        "EC2 instance '%s' in production should not have public IP",
        [resource.address]
    )
}

# Warn if monitoring is not enabled
warn[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"

    not resource.change.after.monitoring

    msg := sprintf(
        "EC2 instance '%s' should enable detailed monitoring for better observability",
        [resource.address]
    )
}

# Deny instances using deprecated instance types
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"

    deprecated_types := ["t1.micro", "m1.small", "m1.medium", "m1.large"]
    resource.change.after.instance_type in deprecated_types

    msg := sprintf(
        "EC2 instance '%s' uses deprecated instance type '%s'",
        [resource.address, resource.change.after.instance_type]
    )
}

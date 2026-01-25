# OPA Policy Template: Security Group Compliance
# This template checks for common security group misconfigurations

package terraform.security.security_groups

import future.keywords.in

# Deny SSH (port 22) open to 0.0.0.0/0
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_security_group"
    rule := resource.change.after.ingress[_]
    rule.from_port == 22
    rule.to_port == 22
    "0.0.0.0/0" in rule.cidr_blocks

    msg := sprintf(
        "Security group '%s' allows SSH (port 22) from 0.0.0.0/0 - CRITICAL SECURITY RISK",
        [resource.address]
    )
}

# Deny RDP (port 3389) open to 0.0.0.0/0
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_security_group"
    rule := resource.change.after.ingress[_]
    rule.from_port == 3389
    rule.to_port == 3389
    "0.0.0.0/0" in rule.cidr_blocks

    msg := sprintf(
        "Security group '%s' allows RDP (port 3389) from 0.0.0.0/0 - CRITICAL SECURITY RISK",
        [resource.address]
    )
}

# Deny unrestricted access to database ports
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_security_group"
    rule := resource.change.after.ingress[_]

    # Common database ports
    database_ports := [3306, 5432, 1433, 27017, 6379]
    rule.from_port in database_ports
    "0.0.0.0/0" in rule.cidr_blocks

    msg := sprintf(
        "Security group '%s' allows database port %d from 0.0.0.0/0",
        [resource.address, rule.from_port]
    )
}

# Warn if security group allows all ports
warn[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_security_group"
    rule := resource.change.after.ingress[_]
    rule.from_port == 0
    rule.to_port == 65535

    msg := sprintf(
        "Security group '%s' allows all ports - consider restricting",
        [resource.address]
    )
}

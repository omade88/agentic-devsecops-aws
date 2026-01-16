# OPA Policy Template: S3 Bucket Security
# Ensures S3 buckets are secure and compliant

package terraform.security.s3_security

import future.keywords.in

# Deny public S3 buckets
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_public_access_block"
    
    config := resource.change.after
    not config.block_public_acls
    
    msg := sprintf(
        "S3 bucket '%s' does not block public ACLs",
        [resource.address]
    )
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_public_access_block"
    
    config := resource.change.after
    not config.block_public_policy
    
    msg := sprintf(
        "S3 bucket '%s' does not block public policies",
        [resource.address]
    )
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_public_access_block"
    
    config := resource.change.after
    not config.ignore_public_acls
    
    msg := sprintf(
        "S3 bucket '%s' does not ignore public ACLs",
        [resource.address]
    )
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_public_access_block"
    
    config := resource.change.after
    not config.restrict_public_buckets
    
    msg := sprintf(
        "S3 bucket '%s' does not restrict public buckets",
        [resource.address]
    )
}

# Warn if S3 bucket versioning is not enabled
warn[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_versioning"
    
    versioning := resource.change.after.versioning_configuration[0]
    versioning.status != "Enabled"
    
    msg := sprintf(
        "S3 bucket '%s' should enable versioning for data protection",
        [resource.address]
    )
}

# Warn if S3 bucket encryption is not configured
warn[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    
    # Check if there's no corresponding encryption resource
    bucket_name := resource.change.after.bucket
    not has_encryption(bucket_name)
    
    msg := sprintf(
        "S3 bucket '%s' should have encryption configured",
        [resource.address]
    )
}

has_encryption(bucket_name) {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_server_side_encryption_configuration"
    resource.change.after.bucket == bucket_name
}

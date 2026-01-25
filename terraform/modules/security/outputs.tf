output "security_group_ids" {
  description = "The IDs of the security groups created by the security module."
  value       = [aws_security_group.allow_ssh.id, aws_security_group.allow_http.id]
}

output "ec2_role_arn" {
  description = "ARN of the EC2 IAM role"
  value       = aws_iam_role.ec2_role.arn
}

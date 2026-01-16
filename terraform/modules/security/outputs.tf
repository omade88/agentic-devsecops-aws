output "security_group_ids" {
  description = "The IDs of the security groups created by the security module."
  value       = aws_security_group.example.*.id
}
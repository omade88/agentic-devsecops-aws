output "sns_topic_arn" {
  description = "ARN of the SNS topic for notifications"
  value       = aws_sns_topic.notifications.arn
}

output "auto_remediation_function_arn" {
  description = "ARN of the auto-remediation Lambda function"
  value       = aws_lambda_function.auto_remediation.arn
}

output "auto_remediation_function_name" {
  description = "Name of the auto-remediation Lambda function"
  value       = aws_lambda_function.auto_remediation.function_name
}

output "security_response_function_arn" {
  description = "ARN of the security response Lambda function"
  value       = aws_lambda_function.security_response.arn
}

output "security_response_function_name" {
  description = "Name of the security response Lambda function"
  value       = aws_lambda_function.security_response.function_name
}

output "lambda_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_role.arn
}

# Lambda Functions for Agentic AI Auto-Remediation
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

# SNS Topic for Notifications
resource "aws_sns_topic" "notifications" {
  name = "${var.project_name}-${var.environment}-notifications"
  
  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-notifications"
  })
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.notifications.arn
  protocol  = "email"
  endpoint  = var.sns_email
}

# IAM Role for Lambda Functions
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-${var.environment}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = var.tags
}

# IAM Policy for Lambda
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-${var.environment}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeVolumes",
          "ec2:CreateTags",
          "ec2:RevokeSecurityGroupIngress",
          "ec2:ModifyInstanceAttribute",
          "ec2:ModifyInstanceMetadataOptions",
          "ec2:CreateSecurityGroup",
          "ec2:CreateSnapshot",
          "ec2:DescribeVpcs"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetBucketEncryption",
          "s3:PutBucketEncryption",
          "s3:GetBucketVersioning",
          "s3:PutBucketVersioning",
          "s3:GetPublicAccessBlock",
          "s3:PutPublicAccessBlock"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = aws_sns_topic.notifications.arn
      }
    ]
  })
}

# Auto-Remediation Lambda Function
data "archive_file" "auto_remediation" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/auto-remediation/handler.py"
  output_path = "${path.module}/auto-remediation.zip"
}

resource "aws_lambda_function" "auto_remediation" {
  filename      = data.archive_file.auto_remediation.output_path
  function_name = "${var.project_name}-${var.environment}-auto-remediation"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 300
  memory_size   = 256

  source_code_hash = data.archive_file.auto_remediation.output_base64sha256

  environment {
    variables = {
      SNS_TOPIC_ARN     = aws_sns_topic.notifications.arn
      AUTO_FIX_ENABLED  = var.auto_fix_enabled
      DRY_RUN           = var.auto_fix_enabled ? "false" : "true"
      ENVIRONMENT       = var.environment
    }
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-auto-remediation"
  })
}

# CloudWatch Log Group for Auto-Remediation
resource "aws_cloudwatch_log_group" "auto_remediation" {
  name              = "/aws/lambda/${aws_lambda_function.auto_remediation.function_name}"
  retention_in_days = 14

  tags = var.tags
}

# Security Response Lambda Function
data "archive_file" "security_response" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/security-response/handler.py"
  output_path = "${path.module}/security-response.zip"
}

resource "aws_lambda_function" "security_response" {
  filename      = data.archive_file.security_response.output_path
  function_name = "${var.project_name}-${var.environment}-security-response"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 300
  memory_size   = 256

  source_code_hash = data.archive_file.security_response.output_base64sha256

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.notifications.arn
      ENVIRONMENT   = var.environment
    }
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-security-response"
  })
}

# CloudWatch Log Group for Security Response
resource "aws_cloudwatch_log_group" "security_response" {
  name              = "/aws/lambda/${aws_lambda_function.security_response.function_name}"
  retention_in_days = 14

  tags = var.tags
}

# EventBridge Rule for Security Group Changes
resource "aws_cloudwatch_event_rule" "security_group_changes" {
  name        = "${var.project_name}-${var.environment}-sg-changes"
  description = "Capture security group changes"

  event_pattern = jsonencode({
    source      = ["aws.ec2"]
    detail-type = ["AWS API Call via CloudTrail"]
    detail = {
      eventName = [
        "AuthorizeSecurityGroupIngress",
        "AuthorizeSecurityGroupEgress",
        "CreateSecurityGroup"
      ]
    }
  })

  tags = var.tags
}

resource "aws_cloudwatch_event_target" "security_group_changes" {
  rule      = aws_cloudwatch_event_rule.security_group_changes.name
  target_id = "AutoRemediationLambda"
  arn       = aws_lambda_function.auto_remediation.arn
}

resource "aws_lambda_permission" "allow_eventbridge_sg" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auto_remediation.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.security_group_changes.arn
}

# EventBridge Rule for EC2 Instance State Changes
resource "aws_cloudwatch_event_rule" "ec2_state_changes" {
  name        = "${var.project_name}-${var.environment}-ec2-state-changes"
  description = "Capture EC2 instance state changes"

  event_pattern = jsonencode({
    source      = ["aws.ec2"]
    detail-type = ["EC2 Instance State-change Notification"]
    detail = {
      state = ["running", "pending"]
    }
  })

  tags = var.tags
}

resource "aws_cloudwatch_event_target" "ec2_state_changes" {
  rule      = aws_cloudwatch_event_rule.ec2_state_changes.name
  target_id = "AutoRemediationLambda"
  arn       = aws_lambda_function.auto_remediation.arn
}

resource "aws_lambda_permission" "allow_eventbridge_ec2" {
  statement_id  = "AllowExecutionFromEventBridgeEC2"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auto_remediation.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ec2_state_changes.arn
}

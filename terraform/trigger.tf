# trigger

resource "aws_cloudwatch_event_rule" "trigger" {
  name                = format("%s-trigger", var.name)
  schedule_expression = "rate(30 minutes)"
}

resource "aws_cloudwatch_event_target" "trigger" {
  rule      = aws_cloudwatch_event_rule.trigger.name
  target_id = "lambda"
  arn       = module.submit.this_lambda_function_arn
}

resource "aws_lambda_permission" "trigger" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = module.submit.this_lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.trigger.arn
}

resource "aws_cloudwatch_metric_alarm" "high_error_rate" {
  alarm_name          = "HighErrorRate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 5
  alarm_actions       = [aws_sns_topic.alert.arn]
  alarm_description   = "Alert for Lambda errors"
  dimensions = {
    Topic = var.kafka_topic
  }
}

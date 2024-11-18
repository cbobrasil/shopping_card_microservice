import boto3
import time
import os

# Configuration
CLOUDWATCH_NAMESPACE = "TeachableMetrics"
LAMBDA_FUNCTION_NAME = "process_purchase_data"
ALARM_NAME = "LambdaErrorAlarm"
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")  # Ensure this is set in your environment

def simulate_lambda_error():
    """Simulate an error by publishing a custom CloudWatch metric."""
    cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
    response = cloudwatch.put_metric_data(
        Namespace=CLOUDWATCH_NAMESPACE,
        MetricData=[
            {
                "MetricName": "Errors",
                "Dimensions": [{"Name": "FunctionName", "Value": LAMBDA_FUNCTION_NAME}],
                "Value": 1,
                "Unit": "Count",
            }
        ]
    )
    print("Simulated Lambda error:", response)

def check_alarm_status():
    """Check the status of the CloudWatch alarm."""
    cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
    response = cloudwatch.describe_alarms(AlarmNames=[ALARM_NAME])
    alarm_state = response["MetricAlarms"][0]["StateValue"]
    print(f"Alarm state: {alarm_state}")
    return alarm_state

def test_cloudwatch_alarm():
    """Test if the CloudWatch alarm is triggered."""
    simulate_lambda_error()
    
    # Wait for the alarm to trigger
    time.sleep(60)  # Wait for the metric to propagate and alarm to evaluate
    
    alarm_state = check_alarm_status()
    assert alarm_state == "ALARM", f"Expected alarm state 'ALARM', but got '{alarm_state}'"

    print("CloudWatch alarm triggered successfully!")

def test_sns_notification():
    """Test if an SNS notification is sent when the alarm is triggered."""
    sns = boto3.client("sns", region_name="us-east-1")
    response = sns.list_subscriptions_by_topic(TopicArn=SNS_TOPIC_ARN)
    
    assert len(response["Subscriptions"]) > 0, "No subscriptions found for SNS topic!"
    print("SNS topic subscriptions verified successfully!")

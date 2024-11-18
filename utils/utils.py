from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.email import send_email_smtp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password):
    try:
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, message.as_string())

        logging.info(f"Email sent successfully to {to_email} with subject: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email. Error: {e}")

def on_failure_callback(context):
    subject = f"Task Failed: {context['task_instance'].task_id}"
    body = f"""
    DAG: {context['dag_run'].dag_id}
    Task: {context['task_instance'].task_id}
    Log URL: {context['task_instance'].log_url}
    """
    send_email(
        subject=subject,
        body=body,
        to_email="engineer_alers_group@teachable.com",
        from_email="data_engineer@teachable.com",
        smtp_server="smtp.teachable.com",
        smtp_port=587,
        smtp_user="data_engineer@teachable.com",
        smtp_password="password"
    )

def on_success_callback(context):
    subject = f"DAG Success: {context['dag_run'].dag_id}"
    body = f"""
    DAG: {context['dag_run'].dag_id}
    All tasks have been completed successfully.
    """
    send_email(
        subject=subject,
        body=body,
        to_email="engineer_alers_group@teachable.com",
        from_email="data_engineer@teachable.com",
        smtp_server="smtp.teachable.com",
        smtp_port=587,
        smtp_user="data_engineer@teachable.com",
        smtp_password="password"
    )

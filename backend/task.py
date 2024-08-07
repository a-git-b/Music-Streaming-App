import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import csv
from io import StringIO
from datetime import datetime,timedelta
from celery_config import celery
from app import User,db,app
from celery.schedules import crontab
flask_app=app
@celery.task
def generate_monthly_report():
    with flask_app.app_context():
        current_month = datetime.now().strftime('%B')
        current_year = datetime.now().year

        users = User.query.filter_by().all()
        subject = 'Monthly Activity Report'
        for user in users:
            html_content=f"""
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
                <h1>Monthly report - {current_month}
                {current_year}</h1>
                <p>This is your summary
                </p>
            </body>
            </html>
            """
            send_email('anjali8271bansal@gmail.com',html_content,subject)

def send_email(to_email,html_content,subject):
    from_email = 'anjali8271bansal@gmail.com'
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    part1 = MIMEText(html_content,'html')
    msg.attach(part1)
    smtp_server = 'localhost'
    smtp_port = 8025
    with smtplib.SMTP(smtp_server,smtp_port) as server:
        server.send_mesaage(msg)

    



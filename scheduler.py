import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from report import fetch_sales_by_region, create_excel
from mailer import send_mail

load_dotenv()

logger = logging.getLogger(__name__)

stakeholder_emails = [e.strip() for e in os.getenv('STAKEHOLDER_EMAILS', '').split(',') if e.strip()]

scheduler = BlockingScheduler()


def job():
    for email in stakeholder_emails:
        data = fetch_sales_by_region(email)
        report_path = f"report_{email.replace('@', '_')}.xlsx"
        create_excel(data, report_path)
        send_mail(
            to_address=email,
            subject="Daily Sales Report",
            body="Please find attached your daily sales report.",
            attachment_path=report_path,
        )


def schedule_jobs():
    scheduler.add_job(job, 'cron', hour=9, minute=0)
    logger.info("Scheduler configured to run daily at 9am")
    scheduler.start()

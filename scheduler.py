import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from config import load_config
from report import generate_report
from mailer import send_mail

logger = logging.getLogger(__name__)

scheduler = BlockingScheduler()


def job():
    config = load_config()
    for query in config.get('queries', []):
        name = query['name']
        sql = query['sql']
        for email in query.get('recipients', []):
            report_path = generate_report(name, sql, email)
            send_mail(
                to_address=email,
                subject=f"{name} Report",
                body="Please find attached your report.",
                attachment_path=report_path,
            )


def schedule_jobs():
    config = load_config()
    cron = CronTrigger.from_crontab(config.get('schedule_cron', '0 9 * * *'))
    scheduler.add_job(job, cron)
    logger.info("Scheduler configured with cron %s", cron)
    scheduler.start()

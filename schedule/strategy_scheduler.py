
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from repository.service import stock_bar_service


if __name__ == '__main__':
    scheduler = BlockingScheduler(job_defaults={'coalesce': True, 'misfire_grace_time': 2, 'max_instance': 1})

    scheduler.add_job(func=stock_bar_service.sync_stock_bar, name='sync_stock_bar',
                      trigger=CronTrigger.from_crontab("10 16 * * 1-5"))

    scheduler.start()

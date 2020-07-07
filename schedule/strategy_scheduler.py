
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from strategy import scanning_momentum


if __name__ == '__main__':
    scheduler = BlockingScheduler(job_defaults={'coalesce': True, 'misfire_grace_time': 2, 'max_instance': 1})
    # scheduler.add_job(func=scanning_momentum.run, days=60, trigger="interval", name='strategy.scanning_momentum')
    scheduler.add_job(func=scanning_momentum.run, trigger=CronTrigger.from_crontab(""), name='strategy.scanning_momentum')
    scheduler.start()

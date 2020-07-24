
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from com.kino.stock.common_utils import time_utils
from com.kino.stock.repository.service import stock_bar_service


def heartbeat(date_ymd):
    print('--- cur_ymd:', date_ymd, time_utils.format_time(_format="%Y%m%d-%H:%M:%S"))


if __name__ == '__main__':
    scheduler = BlockingScheduler(job_defaults={'coalesce': True, 'misfire_grace_time': 2, 'max_instance': 1})

    cur_ymd = time_utils.delta_and_format_time(_format="%Y%m%d")

    # 定时打印一下
    scheduler.add_job(name='heartbeat', func=heartbeat, args=(cur_ymd,), seconds=50, trigger='interval')

    # 同步每天的股票日K数据
    scheduler.add_job(name='sync_stock_bar', func=stock_bar_service.sync_stock_bar,
                      kwargs={'start_date': cur_ymd, 'end_date': cur_ymd, 'freq': 'D', 'adj': 'qfq'},
                      trigger=CronTrigger.from_crontab("10 16 * * 1-5"))
    scheduler.print_jobs()
    scheduler.start()

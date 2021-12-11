from apscheduler.schedulers.blocking import BlockingScheduler
import realestate_api
import sqlite_apt
from datetime import datetime

sched = BlockingScheduler()
runner_job = sched.add_job(realestate_api.load_data_to_mongo, 
                            'date', run_date=datetime(2021, 12, 11, 15, 25, 1))

sched.add_job(sqlite_apt.insert_json_to_sqlite, 
                            'cron', minute="36", second='5')

sched.start()
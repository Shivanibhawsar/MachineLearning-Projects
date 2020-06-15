from apscheduler.schedulers.background import BackgroundScheduler
from DistrictDailyDataAPI import fetchLatestData
import sys


sched = BackgroundScheduler()

def updateData():
    fetchLatestData()
    print("60 seconds", file=sys.stderr)

def backgroundUpdateData():
    sched.add_job(updateData, 'interval', seconds=3600,max_instances=10)
    sched.start()
    sched.shutdown()



from django_cron import CronJobBase, Schedule
from grnentry.task import generate_notifications

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 3600 # daily

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'myapp.my_cron_job'

    def do(self):
        generate_notifications()
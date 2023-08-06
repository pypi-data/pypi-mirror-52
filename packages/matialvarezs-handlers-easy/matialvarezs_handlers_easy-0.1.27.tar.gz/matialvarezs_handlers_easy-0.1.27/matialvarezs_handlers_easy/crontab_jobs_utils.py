from crontab import CronTab
from . import settings


def find_job_by_comment(comment):
    my_cron = CronTab(user=settings.CRONTAB_USER)
    exist = False
    for job in my_cron:
        if job.comment == comment:
            exist = True
    return exist


def create_cron_execute_between_x_minutes(minutes, command, comment):
    if not find_job_by_comment(comment):
        my_cron = CronTab(user=settings.CRONTAB_USER)
        job = my_cron.new(command=command, comment=comment)
        job.minute.every(minutes)
        my_cron.write()

def create_cron_execute_every_month(command, comment):
    if not find_job_by_comment(comment):
        my_cron = CronTab(user=settings.CRONTAB_USER)
        job = my_cron.new(command=command, comment=comment)
        job.every().month()
        my_cron.write()

def create_cron_execute_by_x_hours(hours, command, comment):
    if not find_job_by_comment(comment):
        my_cron = CronTab(user=settings.CRONTAB_USER)
        job = my_cron.new(command=command, comment=comment)
        job.every(hours).hours()
        my_cron.write()

def create_cron_execute_one_time(hour_start_time, minute_start_time, day_of_week, command, comment):
    # my_cron = CronTab(user=True)
    if not find_job_by_comment(comment):
        my_cron = CronTab(user=settings.CRONTAB_USER)
        job = my_cron.new(command=command, comment=comment)
        job.hour.every(hour_start_time)
        job.minute.every(minute_start_time)
        job.dow.on(day_of_week)
        #job.day.every(day_of_week)
        my_cron.write()


def update_cron(id_fiber_sensor, measuring_frecuency):
    # my_cron = CronTab(user=True)
    print("update cront id_fiber_sensor , measuring_frecuency: ", id_fiber_sensor, measuring_frecuency)
    my_cron = CronTab(user=settings.CRONTAB_USER)
    for job in my_cron:
        print("job comment", job.comment)
        print("buscando: ", 'cs655_sensor_' + str(id_fiber_sensor))
        if job.comment == 'cs655_sensor_' + str(id_fiber_sensor):
            print("job encontrado")
            job.minute.every(measuring_frecuency)
            my_cron.write()


def delete_cron(comment):
    # my_cron = CronTab(user=True)
    my_cron = CronTab(user=settings.CRONTAB_USER)
    for job in my_cron:
        if job.comment == comment:
            my_cron.remove(job)
            my_cron.write()

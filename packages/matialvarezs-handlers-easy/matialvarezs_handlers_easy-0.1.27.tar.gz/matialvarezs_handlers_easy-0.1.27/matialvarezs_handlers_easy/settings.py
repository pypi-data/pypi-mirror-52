from django.conf import settings

SCRIPTS_PATH = getattr(settings, 'SCRIPTS_PATH')
CRON_JOB_LOGS_PATH = getattr(settings, 'CRON_JOB_LOGS_PATH')
CRONTAB_USER = getattr(settings,'CRONTAB_USER')
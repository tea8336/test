# coding:utf-8
# celery_config.py
# yang.wenbo


from datetime import timedelta
from celery.schedules import crontab


CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULE = {
    'homework_celery': {
        'task': 'celery_linux.worker',  # filename.funcname
        # 'schedule':timedelta(seconds=15),
        'schedule': crontab(hour='8,9', minute='*/2', day_of_week='sun'),
        'args': ('homework_celery',)
    }
}

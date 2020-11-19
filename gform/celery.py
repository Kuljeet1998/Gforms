# from __future__ import absolute_import, unicode_literals # for python2

import os
from celery import Celery
from celery.schedules import crontab #later

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gform.settings')


## Get the base REDIS URL, default to redis' default
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://:1234@127.0.0.1:6379')

app = Celery('gform')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

# this allows you to schedule items in the Django admin.
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

id=['92a88134-13da-4de7-8abc-9d36fbb8e745']
id2=['92a88134-13da-4de7-8abc-9d36fbb8e741'] #does not exist
app.conf.beat_schedule = {
    'add-every-minute-contrab': {
        'task': 'copy',
        'schedule': 30,
        'args': id
    	},
    'fail-every-32s':{
    	'task': 'copy',
    	'schedule':32,
    	'args':id2
    	},
    'check-every-35s':{
    	'task':'check_and_rerun',
    	'schedule':35,
    	'args':id
    	}
    }
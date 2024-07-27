# tasks.py
import time
from awd_main.celery import app
from django.core.management import call_command

@app.task
def celery_test_task():
    time.sleep(10)
    return 'Task executed successfully'




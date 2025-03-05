import os
from celery import Celery
from datetime import timedelta
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "A.settings")

app_celery = Celery("A")
app_celery.config_from_object("django.conf:settings", namespace="CELERY")
# بروکر و نتیجه
app_celery.conf.broker_url = "amqp://guest:guest@localhost:5672//" # یا RabbitMQ
app_celery.conf.result_backend = "rpc://"

# تنظیمات Serializer
app_celery.conf.task_serializer = "json"
app_celery.conf.result_serializer = "json"
app_celery.conf.accept_content = ["json"]

# مدیریت زمان و تسک‌ها
app_celery.conf.result_expires = timedelta(days=1)
app_celery.conf.task_always_eager = False
app_celery.conf.worker_prefetch_multiplier = 4
app_celery.conf.timezone = "UTC"

# شناسایی خودکار تسک‌ها
app_celery.autodiscover_tasks(['account'])


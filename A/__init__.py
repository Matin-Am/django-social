# A/__init__.py

from __future__ import absolute_import, unicode_literals

# برای اینکه Django در زمان راه‌اندازی Celery را وارد کند
from .celery_conf import app_celery

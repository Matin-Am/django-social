from celery import shared_task
from .models import Relation
from django.contrib.auth.models import User


@shared_task
def set_admin(user_id):
    user = User.objects.get(id=user_id)
    if user.followers.count() > 4 :
        user.is_staff = True
        user.save()
    return f"this user can now be a admin"

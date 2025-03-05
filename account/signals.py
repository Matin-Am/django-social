from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import signals
from .models import Profile , Relation
from account.tasks import set_admin 

@receiver(signals.post_save , sender=User)
def Create_profile(sender, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])
        

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Relation(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} is following {self.to_user}"
    
    def follower_count(self,user_id):
        user = User.objects.get(id=user_id)
        return user.followers.count()
    


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(blank=True,null=True)

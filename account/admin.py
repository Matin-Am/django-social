from django.contrib import admin
from .models import Relation , Profile
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import User

# Register your models here.

class ProfileStackedInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileStackedInline,)

admin.site.unregister(User)
admin.site.register(User,ExtendedUserAdmin)

admin.site.register(Relation)
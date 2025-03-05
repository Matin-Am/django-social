from django.contrib import admin
from .models import Post , Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("user","slug","created")
    list_filter = ("created",)
    raw_id_fields = ("user",)
    search_fields = ("slug",)


admin.site.register(Post,PostAdmin)
admin.site.register(Comment)


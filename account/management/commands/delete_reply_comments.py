from django.core.management.base import BaseCommand
from home.models import Comment



class Command(BaseCommand):
    help = "removing all reply comments"
    def handle(self, *args, **options):
        Comment.objects.filter(is_reply=True).delete()
        self.stdout.write("all reply comments have been removed.")
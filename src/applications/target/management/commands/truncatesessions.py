from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Truncates Django session table"

    def handle(self, *args, **options):
        Session.objects.all().delete()

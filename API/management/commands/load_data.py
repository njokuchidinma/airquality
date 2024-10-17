from django.core.management.base import BaseCommand
from .healthtips import load_health_tips
from .riskalerts import load_risk_alerts

class Command(BaseCommand):
    help = 'Load health tips and risk alerts into the database'

    def handle(self, *args, **kwargs):
        load_health_tips()
        load_risk_alerts()
        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))

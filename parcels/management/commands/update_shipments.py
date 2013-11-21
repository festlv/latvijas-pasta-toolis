from django.core.management.base import BaseCommand

from parcels.models import Shipment


class Command(BaseCommand):
    help = 'Updates shipments in database'

    def handle(self, *args, **kwargs):
        shipments = Shipment.objects.shipments_to_update()
        for s in shipments:
            s.update()

        self.stdout.write("OK")

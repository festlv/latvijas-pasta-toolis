from django.db import models
from datetime import datetime, timedelta


class ShipmentManager(models.Manager):

    def shipments_to_update(self):
        qo = models.Q(is_received=False) & (
            models.Q(last_check_dt__lt=datetime.now() - timedelta(days=1)) |
            models.Q(last_check_dt__isnull=True))

        return self.filter(qo)

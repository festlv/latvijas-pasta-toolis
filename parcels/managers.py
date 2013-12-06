from django.db import models
from datetime import datetime, timedelta


class ShipmentManager(models.Manager):

    def shipments_to_update(self):
        qo = models.Q(is_received=False)
        return self.filter(qo)

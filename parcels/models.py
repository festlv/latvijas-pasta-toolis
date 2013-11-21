import datetime

from django.db import models, IntegrityError
from django.core.validators import MinLengthValidator
from parcels.managers import ShipmentManager
from parcels.utils import scrape_shipment_status


class Shipment(models.Model):
    tracking_number = models.CharField(max_length=13,
                                       validators=[MinLengthValidator(13), ])
    last_check_dt = models.DateTimeField(null=True, blank=True)
    created_dt = models.DateTimeField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    is_received = models.BooleanField(default=False)

    objects = ShipmentManager()

    def __unicode__(self):
        return self.tracking_number

    def update(self):
        results = scrape_shipment_status(self.tracking_number)
        for r in results:
            try:
                StatusEntry.objects.create(
                    event_dt=r['dt'], place=r['place'], status=r['event'],
                    shipment=self, created_dt=datetime.datetime.now())
            except IntegrityError:
                #such entry already exists
                pass

        self.last_check_dt = datetime.datetime.now()
        self.save()

    def last_status_entry(self):
        return self.statusentry_set.first()


class StatusEntry(models.Model):
    created_dt = models.DateTimeField()
    event_dt = models.DateTimeField()
    place = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    shipment = models.ForeignKey(Shipment)

    def __unicode__(self):
        return self.status

    class Meta:
        unique_together = ['event_dt', 'place', 'status', 'shipment']
        ordering = ['-event_dt']

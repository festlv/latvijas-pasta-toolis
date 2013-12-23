# coding=utf-8
import datetime

from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.core.validators import MinLengthValidator
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from parcels.managers import ShipmentManager
from parcels.utils import scrape_shipment_status, validate_tracking_number, \
    post_statusentry_create

from registration.signals import user_registered


class Shipment(models.Model):
    tracking_number = models.CharField(max_length=13,
                                       validators=[MinLengthValidator(13),
                                                   validate_tracking_number])
    last_check_dt = models.DateTimeField(null=True, blank=True)
    created_user = models.ForeignKey(User)
    created_dt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    comment = models.CharField(max_length=255, blank=True)
    is_received = models.BooleanField(default=False)

    objects = ShipmentManager()

    class Meta:
        ordering = ['-created_dt']

    def __unicode__(self):
        return self.tracking_number

    def get_absolute_url(self):
        return reverse('single_shipment', args=[str(self.id)])

    def update(self):
        results = scrape_shipment_status(self.tracking_number)
        for r in results:
            try:
                se = StatusEntry.objects.create(
                    event_dt=r['dt'], place=r['place'], status=r['event'],
                    shipment=self, created_dt=datetime.datetime.now())

                if se.is_delivered():
                    self.is_received = True
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

    def is_delivered(self):
        """Return True if the related Shipment can be considered as delivered-
            this will fire off an e-mail to user and stop further polling of
            this shipment"""

        return self.status == u"Sūtījums piegādāts"

post_save.connect(post_statusentry_create, sender=StatusEntry)


def post_register(sender, **kwargs):
    obj = Shipment.objects.create(
        tracking_number="RB481393306CN",
        comment="Demo sūtījums",
        created_user=kwargs['user'])
    obj.update()

user_registered.connect(post_register)

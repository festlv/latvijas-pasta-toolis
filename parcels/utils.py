# coding=utf-8
import re
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

import requests
from bs4 import BeautifulSoup


WS_URL = 'http://www.pasts.lv/lv/kategorija/sutijumu_sekosana/'


def scrape_shipment_status(tracking_number):

    payload = {'id': tracking_number}

    req = requests.get(WS_URL, params=payload)
    req.encoding = 'utf8'

    if not req.ok:
        raise Exception(
            "Non-200 response from ws.pasts.lv for %s" % tracking_number)
    bs = BeautifulSoup(req.text)

    entries = []

    delivery_entries = bs.find_all('table', class_='delivery')

    for e in delivery_entries:
        time_data = e.find('td', class_='time')
        place_data = e.find('td', class_='place')
        status_data = e.find('td', class_='status')

        place = place_data.text.strip()
        status = status_data.text.strip()

        try:
            dt = datetime.strptime(time_data.text.strip(), "%H:%M %d.%m.%Y")
        except (TypeError, UnicodeEncodeError):
            dt = datetime.datetime.now()

        entries.append({'place': place, 'event': status, 'dt': dt})

    return entries


TRACKING_NO_REGEX = re.compile(r'[A-Za-z]{2}[0-9]{9}[A-Za-z]{2}')


def validate_tracking_number(value):
    if not TRACKING_NO_REGEX.match(value):
        raise ValidationError("""Sūtījuma numurs ir nekorekts.
                              Tiek pieņemti sūtījuma numuri sekojošā formātā:
                              AA123456789BB""")


def post_statusentry_create(sender, **kwargs):
    if kwargs['created'] and \
       kwargs['instance'].shipment.statusentry_set.all().count() == 1:
        user = kwargs['instance'].shipment.created_user
        subject = "Sūtījums ienācis LV | pasts.wot.lv"
        url = settings.SITE_URL
        content = render_to_string('parcels/emails/shipment_first_seen.txt',
                                   {'shipment': kwargs['instance'].shipment,
                                    'status_entry': kwargs['instance'],
                                    'site_url': url})
        send_mail(subject, content, settings.FROM_EMAIL, [user.email],
                  fail_silently=False)

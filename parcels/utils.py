# coding=utf-8
import re
from datetime import datetime
from django.core.exceptions import ValidationError

import requests
from bs4 import BeautifulSoup


WS_URL = 'http://ws.pasts.lv/webtracking/index?empty=1&lang=lv'


def scrape_shipment_status(tracking_number):

    payload = {'webTrackingForm[fid]': tracking_number, 'yt0': 'Nosutit'}

    req = requests.post(WS_URL, payload)
    req.encoding = 'utf8'
    if not req.ok:
        raise Exception(
            "Non-200 response from ws.pasts.lv for %s" % tracking_number)
    bs = BeautifulSoup(req.text)

    entries = []
    for tr in bs.table.findAll('tr'):
        if tr.td:
            tds = tr.findAll('td')
            try:
                dt = datetime.strptime(tds[0].text, "%d.%m.%Y %H:%M:%S")
            except (TypeError, UnicodeEncodeError):
                continue
            place = tds[2].text
            event = tds[3].text
            entries.append({'place': place, 'event': event, 'dt': dt})

    return entries


TRACKING_NO_REGEX = re.compile(r'[A-Za-z]{2}[0-9]{9}[A-Za-z]{2}')


def validate_tracking_number(value):
    if not TRACKING_NO_REGEX.match(value):
        raise ValidationError("""Sūtījuma numurs ir nekorekts.
                              Tiek pieņemti sūtījuma numuri sekojošā formātā:
                              AA123456789BB""")


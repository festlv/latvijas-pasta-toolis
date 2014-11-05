from django.test import TestCase
from parcels.utils import scrape_shipment_status
from parcels.models import Shipment
from django.contrib.auth.models import User


class ScraperTestCase(TestCase):
    def setUp(self):
        self._user = User.objects.create(username="test")

    def tearDown(self):
        self._user.delete()
        self._user = None

    def test_known_value(self):
        shipment_no = 'RF260227722SG'
        results = scrape_shipment_status(shipment_no)

        self.assertEqual(len(results), 8)

    def test_shipments_to_update(self):
        s = Shipment.objects.create(tracking_number='RB867569192CN',
                                    created_user=self._user)

        shipments_to_update = Shipment.objects.shipments_to_update()
        self.assertIn(s, shipments_to_update)

    def test_status_entries(self):
        s = Shipment.objects.create(tracking_number='RF260227722SG',
                                    created_user=self._user)
        s.update()

        self.assertGreater(s.statusentry_set.count(), 0)

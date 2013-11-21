from django.test import TestCase
from parcels.utils import scrape_shipment_status
from parcels.models import Shipment

class ScraperTestCase(TestCase):

    def test_known_value(self):
        shipment_no = 'RB867569192CN'
        results = scrape_shipment_status(shipment_no)

        self.assertEqual(len(results), 6)

    def test_shipments_to_update(self):
        s = Shipment.objects.create(tracking_number='RB867569192CN')

        shipments_to_update = Shipment.objects.shipments_to_update()
        self.assertIn(s, shipments_to_update)

    def test_status_entries(self):
        s = Shipment.objects.create(tracking_number='RB867569192CN')
        s.update()

        self.assertGreater(s.statusentry_set.count(), 0)

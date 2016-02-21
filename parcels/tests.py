from django.test import TestCase
from parcels.utils import scrape_shipment_status
from parcels.models import Shipment
from django.contrib.auth.models import User


class ScraperTestCase(TestCase):

    def _create_shipment(self, tracking_number):
        (user, created) = User.objects.get_or_create(
            username='test', email='test@example.org')

        return Shipment.objects.create(
            tracking_number=tracking_number, created_user=user)

    def tearDown(self):
        """
        Cleans shipments, because of foreign key constraints which
        will not allow one to add multiple shipments with the same tracking number
        """
        Shipment.objects.all().delete()

    def test_known_value(self):
        shipment_no = 'RI851080089CN'
        results = scrape_shipment_status(shipment_no)

        self.assertEqual(len(results), 6)

    def test_shipments_to_update(self):
        s = self._create_shipment('RB867569192CN')
        shipments_to_update = Shipment.objects.shipments_to_update()
        self.assertIn(s, shipments_to_update)

    def test_status_entries(self):
        s = self._create_shipment('RI851080089CN')
        s.update()

        self.assertGreater(s.statusentry_set.count(), 0)

    def test_shipment_delivered(self):
        s = self._create_shipment('RI851080089CN')
        s.update()
        self.assertTrue(s.is_received)

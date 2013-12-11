from django.db import models


class ShipmentManager(models.Manager):

    def shipments_to_update(self):
        qo = models.Q(is_received=False)
        return self.filter(qo)

    def user_shipments(self, user):
        return self.filter(created_user=user)

    def search_shipments(self, user, q):
        qo = models.Q(created_user=user) & \
            (models.Q(tracking_number__iexact=q)
             | models.Q(comment__icontains=q)
             )
        return self.filter(qo)

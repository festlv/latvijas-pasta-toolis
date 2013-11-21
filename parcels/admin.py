from django.contrib import admin
from parcels.models import Shipment, StatusEntry
# Register your models here.


class ShipmentAdmin(admin.ModelAdmin):
    readonly_fields = ['created_dt', 'last_check_dt']
    list_display = ['tracking_number', 'comment', 'is_received', 'last_status_entry']

    class StatusInline(admin.TabularInline):
        model = StatusEntry
        fields = ['status', 'place', 'event_dt']
        readonly_fields = fields
        extra = 0

    inlines = [StatusInline, ]


admin.site.register(Shipment, ShipmentAdmin)

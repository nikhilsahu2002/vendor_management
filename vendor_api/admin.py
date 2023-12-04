from django.contrib import admin
from vendor_api import models
# Register your models here.
admin.site.register(models.PurchaseOrder)
admin.site.register(models.Vendor)
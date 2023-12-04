# vendor_api/utils.py
from django.db.models import Count, Avg
from django.db import models

def update_on_time_delivery_rate(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=models.F('acknowledgment_date'))
    on_time_delivery_rate = (on_time_deliveries.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0.0
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()

def update_quality_rating_avg(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
    quality_rating_avg = completed_pos.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0.0
    vendor.quality_rating_avg = quality_rating_avg
    vendor.save()

def update_average_response_time(vendor):
    acknowledged_pos = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False)
    avg_response_time = acknowledged_pos.aggregate(avg_time=Avg(models.F('acknowledgment_date') - models.F('issue_date')))['avg_time'] or 0.0
    vendor.average_response_time = avg_response_time.total_seconds() / 3600  # Convert to hours
    vendor.save()

def update_fulfilment_rate(vendor):
    all_pos = vendor.purchaseorder_set.all()
    fulfilled_pos = all_pos.filter(status='completed')
    fulfilment_rate = (fulfilled_pos.count() / all_pos.count()) * 100 if all_pos.count() > 0 else 0.0
    vendor.fulfillment_rate = fulfilment_rate
    vendor.save()

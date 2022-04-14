from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HousingRequest

@receiver(post_save, sender=HousingRequest)
def handler(sender, instance, **kwargs):
    if isinstance(instance, HousingRequest):
    
        adults = 0
        children = 0
        hotel = instance.hotel
        if hotel:
            for request in hotel.requests.all():
                adults += request.adults
                children += request.children
            hotel.adults_free = hotel.beds_adults - adults
            hotel.children_free = hotel.beds_children - children
            hotel.save()
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from serd.views import hotel_list
from .models import HousingRequest, Hotel

@receiver(pre_save, sender=HousingRequest)
def save_handler(sender, instance, **kwargs):
    # we use update on a queryset for hotels, as save would recalculate
    # the occupancy with the old data.
    if isinstance(instance, HousingRequest):
        try:
            db_request = HousingRequest.objects.get(number=instance.number)
        except HousingRequest.DoesNotExist:
            if instance.hotel:
                adults = instance.hotel.adults_free - instance.adults
                children = instance.hotel.children_free - instance.children
                Hotel.objects.filter(number=instance.hotel.number).update(adults_free=adults, children_free=children)
            return
        
        if instance.hotel and db_request.hotel:
            if instance.hotel.number == db_request.hotel.number:
                adults = instance.hotel.adults_free + db_request.adults -instance.adults
                children = instance.hotel.children_free + db_request.children -instance.children
                Hotel.objects.filter(number=instance.hotel.number).update(adults_free=adults, children_free=children)
            else:
                i_adults = instance.hotel.adults_free - instance.adults
                i_children = instance.hotel.children_free - instance.children
                db_adults = db_request.hotel.adults_free + db_request.adults
                db_children = db_request.hotel.children_free + db_request.children
                Hotel.objects.filter(number=instance.hotel.number).update(adults_free=i_adults, children_free=i_children)
                Hotel.objects.filter(number=db_request.hotel.number).update(adults_free=db_adults, children_free=db_children)
                
        elif instance.hotel:
            adults = instance.hotel.adults_free - instance.adults
            children = instance.hotel.children_free - instance.children
            Hotel.objects.filter(number=instance.hotel.number).update(adults_free=adults, children_free=children)
        elif db_request.hotel:
            adults = db_request.hotel.adults_free + db_request.adults
            children = db_request.hotel.children_free + db_request.children
            Hotel.objects.filter(number=db_request.hotel.number).update(adults_free=adults, children_free=children)
        
@receiver(pre_delete, sender=HousingRequest)
def delete_handler(sender, instance, **kwars):
    if isinstance(instance, HousingRequest):
        if instance.hotel:
            adults = instance.hotel.adults_free + instance.adults
            children = instance.hotel.children_free + instance.children
            Hotel.objects.filter(number=instance.hotel.number).update(adults_free=adults, children_free=children)


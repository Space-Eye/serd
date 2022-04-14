from django.contrib import admin
from .models import AnsprechpartnerHotel, HousingRequest, Offer, Hotel
admin.site.register(HousingRequest)
admin.site.register(Offer)
admin.site.register(Hotel)
admin.site.register(AnsprechpartnerHotel)
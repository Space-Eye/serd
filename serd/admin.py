from django.contrib import admin
from .models import AnsprechpartnerHotel, HousingRequest, Offer, Hotel, NewsItem, Profile
admin.site.register(HousingRequest)
admin.site.register(Offer)
admin.site.register(Hotel)
admin.site.register(AnsprechpartnerHotel)
admin.site.register(NewsItem)
admin.site.register(Profile)

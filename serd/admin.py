from django.contrib import admin
from .models import AnsprechpartnerHotel, HousingRequest, Offer, Hotel, NewsItem, Profile, HotelStay, Pate
@admin.register(HousingRequest)
class HousingRequestAdmin(admin.ModelAdmin):
    search_fields =  ['number']

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    search_fields = ['number']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['account__username', 'name']

admin.site.register(Hotel)
admin.site.register(AnsprechpartnerHotel)
admin.site.register(NewsItem)
admin.site.register(HotelStay)
admin.site.register(Pate)
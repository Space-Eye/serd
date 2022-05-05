from  datetime import date
from django.db.models import Q
from django.db.models import Sum
from serd.models import HotelStay, Hotel, HousingRequest


def get_stays(hotel: Hotel, day: date) ->list[HotelStay]:
    stays = HotelStay.objects.filter(hotel=hotel, arrival_date__lte=day)
    stays = stays.filter(Q(departure_date__gt=day)| Q(departure_date__isnull=True))
    return stays

def get_requests(stays) -> list[HousingRequest]:
    requests = HousingRequest.objects.filter(stays__in=stays)
    return requests


def get_persons(stays) -> int:
    adults = stays.aggregate(Sum('request__adults'))['request__adults__sum']
    if not adults:
        adults = 0 # Can't do math with none
    children =  stays.aggregate(Sum('request__children'))['request__children__sum']
    if not children:
            children = 0 # Can't do math with none
    return adults + children

def get_departing_stays(hotel: Hotel, day: date) -> list[HotelStay]:

    return HotelStay.objects.filter(hotel = hotel, departure_date=day)

def get_arriving_stays(hotel: Hotel, day: date) -> list[HotelStay]:
    return HotelStay.objects.filter(hotel = hotel, arrival_date = day)

def get_hotel_from_request(request: HousingRequest, day: date) -> Hotel:
    stays = request.stays
    if not stays:
        return None
    stays = stays.filter(arrival_date__lte=day).filter(Q(departure_date__isnull=True)| Q(departure_date__gt=day))
    if not stays:
        return None
    if len(stays) > 1:
        raise RuntimeError("{}  is in two hotels at {}".format(request, day))
    return stays[0].hotel
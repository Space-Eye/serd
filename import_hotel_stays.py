#!/usr/bin/env python3
import os
import django
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serd.settings")
django.setup()
from serd.models import HotelStay, HousingRequest, Hotel

with open(sys.argv[1] ,'r') as file:
    for line in file:
        nr, arrival_date, hotel_nr = line.split()
        req = HousingRequest.objects.get(number=nr)
        hotel = Hotel.objects.get(number=hotel_nr)
        stay = HotelStay()
        stay.request = req
        stay.hotel =hotel
        stay.arrival_date = arrival_date
        stay.save()
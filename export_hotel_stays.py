#!/usr/bin/env python3
import os
import django
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serd.settings")
django.setup()
from serd.models import HousingRequest
with open(sys.argv[1] ,'w') as file:
    requests = HousingRequest.objects.filter(hotel__isnull=False)
    for request in requests:
        line = "{nr} {date} {hotel_nr}\n".format(nr=request.number, date=request.arrival_date, hotel_nr=request.hotel.number)
        file.write(line)

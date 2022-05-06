#!/usr/bin/env python3
from datetime import date, timedelta
from django.db.models import Sum
from collections import OrderedDict
from itertools import chain
from pyexcel_ods3 import save_data
from io import BytesIO
from .utils.db import get_persons, get_departing_stays, get_arriving_stays

from serd.models import HotelStay, Hotel


def create_ods( begin:date, end:date ):

    assert(begin.day == 1)
    assert(end.day == 1)
    data = OrderedDict()
    hotels = Hotel.objects.all()
    
    for hotel in hotels:
        
        current_date = begin
        month_prev = -1
        hotel_data = OrderedDict()
        month_str = ""
        current_guests = 0
        while(current_date < end):
            
            if current_date.month != month_prev:
                month_prev = current_date.month
                month_str = "-".join([str(current_date.month), str(current_date.year)])
                hotel_data[month_str] = {}
                hotel_data[month_str][0] = ["Ankunft", "Bestand", "Abreise"]

            arriving = get_arriving_stays(hotel, current_date)
            arrivals = get_persons(arriving)

            departing = get_departing_stays(hotel, current_date)
            departures = get_persons(departing)

            current_guests += arrivals - departures
            hotel_data[month_str][current_date.day ] = [arrivals, current_guests, departures]
            current_date += timedelta(days=1)
        hotel_data_printable = [list(chain(*[ (key,"","","") for key in  hotel_data.keys()]))]
        hotel_data_printable.append([])
        for i in range( 33):
            row = []
            for month in hotel_data.keys():
                row.extend(hotel_data[month].get(i) if hotel_data[month].get(i) else ["","",""])
                row.append("")
            hotel_data_printable.append(row)
        data[hotel.name] = hotel_data_printable
    io = BytesIO()
    save_data(io, data)
    return io




            
            


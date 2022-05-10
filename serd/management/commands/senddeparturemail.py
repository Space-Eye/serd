from urllib import request
from django.core.management.base import BaseCommand, CommandError
from serd.mail import Mailer
from serd.models import Hotel, HotelStay
from datetime import date

from serd.utils.db import count_persons, get_departing_stays, get_departure_dates, get_persons, get_requests, get_stays



class Command(BaseCommand):
    help = 'sends e-mail with expected departures'


    def add_arguments(self, parser):
        parser.add_argument('hotel_id', nargs=1, type=int)
        parser.add_argument('mail', nargs=1, type=str)

    def handle(self, *args, **options):
        hotel = Hotel.objects.get(number=int(options['hotel_id'][0]))
        
        mail = options['mail'][0]
        today = date.today()
        stays = get_stays(hotel, today)
        departing_today = get_departing_stays(hotel, today)
        rooms = [stay.room for stay in departing_today]
        persons = get_persons(departing_today)
        data_today = (persons, rooms)
        persons = get_persons(stays) + get_persons(departing_today)
        days = get_departure_dates(hotel)
        if days:
            data = dict.fromkeys(days)
            for day in days:
                departing =  get_departing_stays(hotel, day)
                rooms = [stay.room for stay in departing]
                lpersons = get_persons(departing)
                data[day] = (lpersons, rooms)
        else:
            data = None
        mailer = Mailer()
        mailer.send_departure_mail(data=data, today=data_today, total=persons, address=mail)
        

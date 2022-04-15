#!/usr/bin/env python3
import csv
from curses import raw

import sys
import os
from unicodedata import name

import django
from datetime import date
from slugify import slugify
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serd.settings")
django.setup()


from django.contrib.auth.models import User
from serd.models import HousingRequest, Offer, Hotel
from serd.forms import isascii


def reformat_date(string):
    
    if not string:
        return date.today()
    raw = string.split()[0]
    try:
        day, month, year = raw.split(".")
    except:
            return date.today()
    if len(year) == 2:
        year = "20"+year
    if not year:
        year = "2022"
    return  "{year}-{month}-{day}".format(year=year, month=month, day=day)
    
def get_lang_list(string):
    string = string.upper()
    list = []
    if 'DEUTSCH' in string or 'GERMAN' in string:
        list.append('de')
    if 'ENGLISCH' in string or 'ENGLISH' in string:
        list.append('en')
    if 'UKRAINISCH' in string or 'UKRAINIAN' in string:
        list.append('uk')
    if 'RUSSISCH' in string or 'RUSSIAN' in string:
        list.append('ru')
    return list

def get_bool(string, default=False):
    if not string:
        return default
    string = string.upper()
    if 'JA' in string:
        return True
    return False

def get_Wohnung(string):
    if not string:
        return False
    string = string.upper()
    if 'EIGENE' in string:
        return False
    if 'FREIE' in string:
        return True
    raise ValueError("Could not parse appartment status of %s", string)

def get_living(string):
    if not string:
        return ''
    string = string.upper()
    if 'ALLEINE' in string:
        return  'single'
    if 'FAMILIE' in string or 'PARTNER' in string:
        return 'family'
    if 'FREUNDE' in string:
        return 'friends'
    raise ValueError('Could not parse living status of %s', string)

def get_pets(string):
    if not string:
        return ['none']
    string = string.upper()
    if 'KEINE' in string or 'NEIN' in string:
        return ['none']
    list = []
    if 'KATZE' in string:
        list.append('cat')
    if 'HUND' in string:
        list.append('dog')
    if 'KLEINTIER' or 'ANDERES' in string:
        list.append('small')
    if not list:
        list.append('none')
    return list

def get_State(string):
    if string == 'Neu':
        return 'new'
    if string == 'Kontakt hergestellt':
        return 'contacted'
    if string == 'Reserviert':
        return 'reserved'
    if string == 'Kontakt zu Gast vermittelt':
        return 'request_contact'
    if string == 'Gast in Unterkunft angekommen':
        return 'arrived'
    if string == 'Temporär nicht verfügbar':
        return 'stale'
    if string == 'wieder frei':
        return 'free'
    if string == 'nicht tragbar':
        return 'no'
    if not string:
        return 'new'
    raise ValueError("could not parse {}".format(string))

def get_housing(string):
    if not string:
        return 'none'
    if 'Ich habe keinen Schlafplatz' in string:
        return 'none'
    if 'Bei Freunden oder Verwandten' in string:
        return 'friends'
    if 'Staatliche Notunterkunft' in string:
        return 'shelter'
    if 'Hotel' in string:
        return 'hotel'
    return 'none'
    


def get_number(string):
    count = 0
    if not string:
        return 0
    try:
        count = int(string)
        return count
    except:
        pass
    for i in range(1, len(string)):
        try:
            count = int(string[:-i])
            return count
        except:
            continue
    return 0

def get_hotel(string):
    if 'Bischofshof' in string:
        return Hotel.objects.get(number=2)
    if 'Bohemian' in string:
        return Hotel.objects.get(number=3)
    if 'Greenspirit' in string:
        return Hotel.objects.get(number=5)
    if 'Includio' in string:
        return Hotel.objects.get(number=8)
    if 'Jugendherberge' in string:
        return Hotel.objects.get(number=9)
    if 'Akademie' in string:
        return Hotel.objects.get(number=10)
    if 'Weidenhof' in string:
        return Hotel.objects.get(number=14)
    return None

def get_request_state(string):
    if not string or 'Neu' in string:
        return 'new'
    if 'Kontakt hergestellt' in string:
        return 'contacted'
    if 'Kontakt zu Unterkunft vermittelt' in string:
        return 'housing_contact'
    if 'In Unterkunft untergekommen' in string:
        return 'arrived'
    if 'Gesuch nicht mehr aktuell' in string:
        return 'stale'
    if 'Nicht vermittelbar' in string:
        return 'no'
    raise ValueError('could not parse{}'.format(string))

def get_priority(string):
    if 'Ja' in string:
        return 'elevated'
    return 'normal'

def get_handler(string):
    return User.objects.get(username=string)

offer_file = open(sys.argv[1], 'r')
offers = csv.DictReader(offer_file)


for raw_offer in offers:
    offer = Offer()
    offer.number = get_number(raw_offer['Nr'])
    offer.created_at = reformat_date(raw_offer['Datum'])
    offer.last_name = raw_offer['Nachname']
    offer.given_name = raw_offer['Vorname']
    offer.plz = raw_offer['PLZ']
    offer.total_number = get_number(raw_offer['Persons'])
    offer.children_number = get_number(raw_offer['Kinder'])
    offer.street = raw_offer['Straße']
    offer.city = raw_offer['Ort']
    offer.phone = raw_offer['Tel']
    offer.mail = raw_offer['Mail']
    offer.language = get_lang_list(raw_offer['Sprachen'])
    offer.for_free = get_bool(raw_offer['Gratis'], True)
    if offer.for_free:
        offer.cost = 0
    else:
        offer.cost = 99999
    offer.spontan = get_bool(raw_offer['Spontan'])
    offer.available_from = reformat_date(raw_offer['Available_from'])
    offer.limited_availability = get_bool(raw_offer['begrenzt'])
    if offer.limited_availability:
        offer.available_until = reformat_date('Available_until')
    offer.seperate_appartment = get_Wohnung(raw_offer['seperate'])
    offer.accessability = get_bool(raw_offer['barrierefrei'])
    offer.public_transport = get_bool(raw_offer['ÖPNV'])
    offer.rooms = 0
    if not offer.seperate_appartment:
        offer.living_with = get_living(raw_offer['living_with'])
    offer.pets = get_pets(raw_offer['pets'])
    offer.state = get_State(raw_offer['Status'])
    offer.comment = raw_offer['Kommentar']
    offer.private_comment = raw_offer['Notizen']
    offer.by_municipality = get_bool(raw_offer['Stadt'])
    offer.save()
offer_file.close()

request_file = open(sys.argv[2],'r')
requests = csv.DictReader(request_file)
#handlers = set()
#for req in requests:
#    handlers.add(req['Sachbearbeiter'])
#for handler in handlers:
#    account = User(username=handler)
#    account.set_password('123')
#    account.save()



for raw_request in requests:
    request = HousingRequest()
    request.created_at = reformat_date(raw_request['Date'])
    request.number = get_number(raw_request['Nr'])
    request.last_name = raw_request['Nachname']
    request.given_name = raw_request['Vorname']
    if not isascii(request.last_name) or not isascii(request.given_name):
        request.name_slug = slugify(request.given_name)+" "+ slugify(request.last_name)
    request.phone = raw_request['Tel']
    request.mail = raw_request['Mail']
    request.representative = raw_request['STV']
    request.repr_phone = raw_request['STVTEL']
    request.repr_mail   = raw_request['STVMAIL']
    persons = get_number(raw_request['Persons'])
    children = get_number(raw_request['Kinder'])
    request.adults = persons -children
    if request.adults < 0:
        request.adults = 9999999
    request.children = children
    if request.children < 0:
        request.children = 999999
    request.who = raw_request['who']
    request.split = get_bool(raw_request['split'])
    request.current_housing = get_housing(raw_request['wo'])
    if request.current_housing == 'hotel':
        request.hotel = get_hotel(raw_request['wo'])
    request.arrival_date = reformat_date(raw_request['arrival'])
    request.arrival_location = raw_request['ankunf']
    request.pets = get_pets(raw_request['Haustiere'])
    if request.pets == ['none']:
        request.pet_number = 0
    else:
        request.pet_number = get_number(raw_request['Haustier_Anzahl'])
    request.car = get_bool(raw_request['Auto'])
    request.languages = get_lang_list(raw_request['Sprachen'])
    request.vaccination = get_bool(raw_request['COVID'])
    request.accessability_needs = get_bool(raw_request['barrierefrei'])
    request.state = get_request_state(raw_request['Status'])
    request.priority = get_priority(raw_request['Priorität'])
    request.placed_at = None
    request.private_comment = raw_request['Notizen']
    request.case_handler = get_handler(raw_request['Sachbearbeiter'])
    request.save()
    #print(raw_request.keys())
request_file.close()
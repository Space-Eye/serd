from datetime import datetime
from urllib import request
from django.test import TestCase
from django.contrib.auth.models import User
from serd.forms import RequestEditForm
from serd.models import HousingRequest, HotelStay, Hotel
def allStays():
    return HotelStay.objects.all()
def get_stay(number=1):
    return HotelStay.objects.get(number=number)
class stayCreation(TestCase):
    fixtures = ['test1']
    def assertStay(self, stay, arrival_date, departure_date, hotel, request, count=None):
        if count is not None:
            self.assertEqual(allStays().count(),count)
            self.assertEqual(stay.arrival_date, arrival_date)
            self.assertEqual(stay.departure_date, departure_date)
            self.assertEqual(stay.hotel, hotel)
            self.assertEqual(stay.request, request)
    def test_create_Request_empty_departure(self):
        stays = HotelStay.objects.all()
        self.assertEqual(0, stays.count(), "Bad fixture, there sould not be a HotelStay yet")
        hotel = Hotel.objects.get(number=1)
        arrival = datetime.strptime('22-04-2022', '%d-%m-%Y').date()
        data = {
            'given_name': 'test',
            'last_name': 'testb',
            'phone': '012345678',
            'mail': 'test@test.de',
            'adults': 3,
            'children': 1,
            'who': 'testgroup',
            'split': False,
            'current_housing': 'hotel',
            'can_pay': False,
            'arrival_date': arrival,
            'pets': ['none'],
            'pet_number': 0,
            'car': True,
            'languages': ['de'],
            'vaccination': True,
            'accessability_needs': False,
            'state' : 'new',
            'hotel': hotel

        }
        form = RequestEditForm(data)
        request = form.save()
        stays = HotelStay.objects.all()
        self.assertEqual(stays.count(), 1, "Should have created exactly one")
        stay = stays.first()
        self.assertEqual(stay.arrival_date, arrival)
        self.assertEqual(stay.departure_date , None)
        self.assertEqual(stay.request, request)
        self.assertEqual(stay.hotel, hotel)

    def test_create_Request_with_departure(self):
        stays = HotelStay.objects.all()
        self.assertEqual(0, stays.count(), "Bad fixture, there sould not be a HotelStay yet")
        hotel = Hotel.objects.get(number=1)
        arrival = datetime.strptime('22-04-2022', '%d-%m-%Y').date()
        departure = datetime.strptime('27-04-2022', '%d-%m-%Y').date()
        data = {
            'given_name': 'test',
            'last_name': 'testb',
            'phone': '012345678',
            'mail': 'test@test.de',
            'adults': 3,
            'children': 1,
            'who': 'testgroup',
            'split': False,
            'current_housing': 'hotel',
            'can_pay': False,
            'arrival_date': arrival,
            'pets': ['none'],
            'pet_number': 0,
            'car': True,
            'languages': ['de'],
            'vaccination': True,
            'accessability_needs': False,
            'state' : 'new',
            'hotel': hotel,
            'departure_date': departure

        }
        form = RequestEditForm(data)
        request = form.save()
        stays = HotelStay.objects.all()
        self.assertEqual(stays.count(), 1, "Should have created exactly one")
        stay = stays.first()
        self.assertEqual(stay.arrival_date, arrival)
        self.assertEqual(stay.departure_date , departure)
        self.assertEqual(stay.request, request)
        self.assertEqual(stay.hotel, hotel)
    
    def test_update_dates(self):
        stays = HotelStay.objects.all()
        self.assertEqual(0, stays.count(), "Bad fixture, there sould not be a HotelStay yet")
        hotel = Hotel.objects.get(number=1)
        arrival = datetime.strptime('22-04-2022', '%d-%m-%Y').date()
        
        data = {
            'given_name': 'test',
            'last_name': 'testb',
            'phone': '012345678',
            'mail': 'test@test.de',
            'adults': 3,
            'children': 1,
            'who': 'testgroup',
            'split': False,
            'current_housing': 'hotel',
            'can_pay': False,
            'arrival_date': arrival,
            'pets': ['none'],
            'pet_number': 0,
            'car': True,
            'languages': ['de'],
            'vaccination': True,
            'accessability_needs': False,
            'state' : 'new',
            'hotel': hotel

        }
        form = RequestEditForm(data)
        request: HousingRequest = form.save()
        stays = HotelStay.objects.all()
        self.assertEqual(stays.count(), 1, "Should have created exactly one")
        new_arrival = datetime.strptime('23-04-2022', '%d-%m-%Y').date()
        data['arrival_date'] = new_arrival
        form = RequestEditForm(data, instance=request)
        form.save()
        stay = allStays().first()
        self.assertEqual(stay.arrival_date, new_arrival)
        self.assertEqual(stay.departure_date , None)
        self.assertEqual(stay.request, request)
        self.assertEqual(stay.hotel, hotel)
        self.assertEqual(allStays().count(), 1)
        
        departure = datetime.strptime('25-04-2022', '%d-%m-%Y').date()
        data['departure_date'] = departure
        RequestEditForm(data, instance=request).save()

        self.assertEqual(allStays().count(), 1)
        stay = allStays().first()
        self.assertEqual(stay.arrival_date, new_arrival)
        self.assertEqual(stay.departure_date , departure)
        self.assertEqual(stay.request, request)
        self.assertEqual(stay.hotel, hotel)
        
        new_departure  = datetime.strptime('24-04-2022', '%d-%m-%Y').date()
        data['departure_date'] = new_departure
        RequestEditForm(data, instance=request).save()

        self.assertEqual(allStays().count(), 1)
        stay = allStays().first()
        self.assertEqual(stay.arrival_date, new_arrival)
        self.assertEqual(stay.departure_date , new_departure)
        self.assertEqual(stay.request, request)
        self.assertEqual(stay.hotel, hotel)
        
    def test_create_without_hotel(self):
        stays = HotelStay.objects.all()
        self.assertEqual(0, stays.count(), "Bad fixture, there sould not be a HotelStay yet")
        hotel = Hotel.objects.get(number=1)
        arrival = datetime.strptime('22-04-2022', '%d-%m-%Y').date()
        departure = datetime.strptime('22-04-2024', '%d-%m-%Y').date()
        data = {
            'given_name': 'test',
            'last_name': 'testb',
            'phone': '012345678',
            'mail': 'test@test.de',
            'adults': 3,
            'children': 1,
            'who': 'testgroup',
            'split': False,
            'current_housing': 'hotel',
            'can_pay': False,
            'arrival_date': arrival,
            'pets': ['none'],
            'pet_number': 0,
            'car': True,
            'languages': ['de'],
            'vaccination': True,
            'accessability_needs': False,
            'state' : 'new',
            'hotel': None,
            'departure_date': departure

        }
        
        request: HousingRequest = RequestEditForm(data).save()
        
        self.assertEqual(allStays().count(), 0)
        
        data['hotel'] = hotel
        RequestEditForm(data, instance=request).save()

        self.assertEqual(allStays().count(), 1)
        stay = allStays().first()
        self.assertEqual(stay.arrival_date, arrival)
        self.assertEqual(stay.departure_date , departure)
        self.assertEqual(stay.request, request)
        self.assertEqual(stay.hotel, hotel)


    def test_change_hotel_can_not_be_changed(self):
        hotel = Hotel.objects.get(number=1)
        arrival = datetime.strptime('22-04-2022', '%d-%m-%Y').date()
        departure = datetime.strptime('22-04-2024', '%d-%m-%Y').date()
        data = {
            'given_name': 'test',
            'last_name': 'testb',
            'phone': '012345678',
            'mail': 'test@test.de',
            'adults': 3,
            'children': 1,
            'who': 'testgroup',
            'split': False,
            'current_housing': 'hotel',
            'can_pay': False,
            'arrival_date': arrival,
            'pets': ['none'],
            'pet_number': 0,
            'car': True,
            'languages': ['de'],
            'vaccination': True,
            'accessability_needs': False,
            'state' : 'new',
            'hotel': hotel,
            'departure_date': departure

        }
        request = RequestEditForm(data).save()
        self.assertStay(stay=get_stay(), arrival_date=arrival, departure_date=departure, hotel=hotel, request=request, count=1)
        
        new_hotel = Hotel.objects.get(pk=2)
        data['hotel'] = new_hotel
        form: RequestEditForm = RequestEditForm(data, instance=request)
        self.assertFalse(form.is_valid())
        
        self.assertIn('kann nachträglich nur von Admin', form.errors.as_data()['hotel'][0].message)
        
    def test_changes_affect_first_stay(self):
        hotel = Hotel.objects.get(number=1)
        arrival = datetime.strptime('22-04-2022', '%d-%m-%Y').date()
        departure = datetime.strptime('22-04-2024', '%d-%m-%Y').date()
        data = {
            'given_name': 'test',
            'last_name': 'testb',
            'phone': '012345678',
            'mail': 'test@test.de',
            'adults': 3,
            'children': 1,
            'who': 'testgroup',
            'split': False,
            'current_housing': 'hotel',
            'can_pay': False,
            'arrival_date': arrival,
            'pets': ['none'],
            'pet_number': 0,
            'car': True,
            'languages': ['de'],
            'vaccination': True,
            'accessability_needs': False,
            'state' : 'new',
            'hotel': hotel,
            'departure_date': departure

        }

        request = RequestEditForm(data).save()
        self.assertStay(stay=get_stay(), arrival_date=arrival, departure_date=departure, hotel=hotel, request=request, count=1)
        
        stay = HotelStay()
        hotel2 = Hotel.objects.get(number=2)
        stay.hotel = hotel2 
        stay.request = request
        arrival_2 = datetime.strptime('22-04-2023', '%d-%m-%Y').date()
        departure_2 = datetime.strptime('22-04-2024', '%d-%m-%Y').date()
        stay.arrival_date = arrival_2
        stay.departure_date = departure_2
        stay.save()
        new_departure  = datetime.strptime('27-04-2024', '%d-%m-%Y').date()
        new_arrival  = datetime.strptime('17-04-2024', '%d-%m-%Y').date()
        data['departure_date'] = new_departure
        data['arrival_date'] = new_arrival
        RequestEditForm(data, instance=request).save()
        self.assertStay(get_stay(), new_arrival, new_departure, hotel, request, 2)
        self.assertStay(get_stay(2), arrival_2, departure_2, hotel2, request)
        request.hotel= hotel2
        request.save()
        self.assertStay(get_stay(), new_arrival, new_departure, hotel, request, 2)
        self.assertStay(get_stay(2), arrival_2, departure_2, hotel2, request)
        


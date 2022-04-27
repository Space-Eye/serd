from django.test import TestCase
from django.contrib.auth.models import User
from serd.forms import RequestEditForm
from serd.models import HousingRequest, HotelStay, Hotel
from django.utils import timezone

class stayCreation(TestCase):
    fixtures = ['test1']
    def test_create_Request(self):
        hotel = Hotel.objects.get(number=1)
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
            'arrival_date': timezone.localdate(),
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
        form.save()
        


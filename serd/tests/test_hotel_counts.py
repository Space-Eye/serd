from urllib import request
from django.test import TestCase
from serd.models import HousingRequest, Hotel

class HotelTests(TestCase):
    fixtures = ['test1']
    def testRemovefromHotel(self):
        hotel = Hotel.objects.get(pk=1)
        adults = hotel.adults_free
        children = hotel.children_free
        request = HousingRequest.objects.get(pk=2)
        adults_r = request.adults
        children_r = request.children
        request.hotel = None
        request.save()
        hotel.refresh_from_db()

        self.assertEqual(hotel.children_free, children + children_r)
        self.assertEqual(hotel.adults_free, adults + adults_r)

    def testSwitchHotel(self):
        hotel_old = Hotel.objects.get(pk=1)
        hotel_new = Hotel.objects.get(pk=2)
        adults_old = hotel_old.adults_free
        children_old = hotel_old.children_free
        adults_new = hotel_new.adults_free
        children_new = hotel_new.children_free

        request = HousingRequest.objects.get(pk=2)
        children_r = request.children
        adults_r = request.adults
        request.hotel = hotel_new
        request.save()
        hotel_old.refresh_from_db()
        hotel_new.refresh_from_db()
        self.assertEqual(hotel_old.adults_free, adults_old + adults_r)
        self.assertEqual(hotel_old.children_free, children_old + children_r)
        self.assertEqual(hotel_new.adults_free, adults_new - adults_r)
        self.assertEqual(hotel_new.children_free, children_new - children_r)

    def testDelteRequest(self):
        hotel = Hotel.objects.get(pk=1)
        adults = hotel.adults_free
        children = hotel.children_free
        request = HousingRequest.objects.get(pk=2)
        adults_r = request.adults
        children_r = request.children
        HousingRequest.objects.filter(pk=2).delete()
        hotel.refresh_from_db()
        self.assertEqual(hotel.children_free, children + children_r)
        self.assertEqual(hotel.adults_free, adults + adults_r)

    def testCreateRequest(self):
        
        hotel = Hotel.objects.get(pk=1)
        adults = hotel.adults_free
        children = hotel.children_free
        req = HousingRequest()
        req.adults = 5
        req.children = 7
        req.split= True
        req.can_pay = True
        req.car = True
        req.vaccination = False
        req.accessability_needs = False
        req.hotel = hotel
        req.save()
        hotel.refresh_from_db()
        self.assertEqual(hotel.adults_free, adults - req.adults)
        self.assertEqual(hotel.children_free, children - req.children)

    def testAddtoHotel(self):
        hotel = Hotel.objects.get(pk=1)
        adults = hotel.adults_free
        children = hotel.children_free
        request = HousingRequest.objects.get(pk=3)
        adults_r = request.adults
        children_r = request.children
        request.hotel = hotel
        request.save()
        hotel.refresh_from_db()

        self.assertEqual(hotel.children_free, children - children_r)
        self.assertEqual(hotel.adults_free, adults - adults_r)
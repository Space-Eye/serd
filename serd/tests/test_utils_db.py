from urllib import request
from django.test import TestCase
from serd.utils.db import get_arriving_stays, get_departing_stays, get_persons, get_requests, get_stays
from serd.models import Hotel, HotelStay, HousingRequest
from datetime import datetime, timedelta
def day(days):
    return  datetime.strptime("2022-04-15", "%Y-%m-%d").date()+  timedelta(days=days)

class HotelStayTests(TestCase):
    fixtures = ['admin', 'hotels', 'requests', 'stays']
    def test_get_persons(self):
        stays = HotelStay.objects.filter(number=1)
        self.assertEqual(get_persons(stays), 3)
        stays = HotelStay.objects.filter(number=7)
        self.assertEqual(get_persons(stays), 3)
        stays = HotelStay.objects.none()
        self.assertEqual(get_persons(stays), 0)
        stays = HotelStay.objects.filter(number__in= [2,3,4])
        self.assertEqual(get_persons(stays), 18)
        

    def test_get_stays(self):
        hotel = Hotel.objects.get(number=1)
        stay = HotelStay.objects.get(number=1)
        self.assertEqual(stay, get_stays(hotel, day(0)).first())
        self.assertEqual(1, len(get_stays(hotel, day(0))))
        for i in range(2,5):
            hotel = Hotel.objects.get(number=i)
            self.assertEqual(None, get_stays(hotel, day(0)).first())
        
        stay = HotelStay.objects.get(number=2)
        hotel = Hotel.objects.get(number=1)
        
        #16. 04.
        stays = get_stays(hotel, day(1)).order_by('number')

        self.assertEqual(stay, stays[0])
        stay = HotelStay.objects.get(number=3)
        self.assertEqual(stay, stays[1])
        
        stay = HotelStay.objects.get(number=4)
        self.assertEqual(stay, stays[2])
        self.assertEqual(3, len(stays))
        
        for i in range(2,5):
            hotel = Hotel.objects.get(number=i)
            self.assertEqual(0, len(get_stays(hotel, day(1))))
        

        #17.04
        hotel = Hotel.objects.get(number=1)
        stays = get_stays(hotel, day(2)).order_by('number')
        stay = HotelStay.objects.get(number=2)

        self.assertEqual(stay, stays[0])
        stay = HotelStay.objects.get(number=3)
        self.assertEqual(stay, stays[1])
        
        stay = HotelStay.objects.get(number=4)
        self.assertEqual(stay, stays[2])

        self.assertEqual(3, len(stays))
        for i in range(2,5):
            hotel = Hotel.objects.get(number=i)
            self.assertEqual(0, len(get_stays(hotel, day(2))))
        
        #18.04:
        hotel = Hotel.objects.get(number=2)
        stays = get_stays(hotel, day(3))
        stay = HotelStay.objects.get(number=5)
        self.assertEqual(1, len(stays))
        self.assertEqual(stay, stays.first())
        
        hotel = Hotel.objects.get(number=1)
        self.assertEqual(0, len(get_stays(hotel, day(3))))
        hotel = Hotel.objects.get(number=3)
        self.assertEqual(0, len(get_stays(hotel, day(3))))
        hotel = Hotel.objects.get(number=4)
        self.assertEqual(0, len(get_stays(hotel, day(3))))

        #19.04.
        for i in range(1,5):
            hotel = Hotel.objects.get(number=i)
            self.assertEqual(0, len(get_stays(hotel, day(4))))
        
        #20.04.
        hotel = Hotel.objects.get(number=1)
        self.assertEqual(0, len(get_stays(hotel, day(5))))
        hotel = Hotel.objects.get(number=2)
        self.assertEqual(0, len(get_stays(hotel, day(5))))
        hotel = Hotel.objects.get(number=4)
        self.assertEqual(0, len(get_stays(hotel, day(5))))

        hotel = Hotel.objects.get(number=3)
        stays = get_stays(hotel, day(5))
        self.assertEqual(1, len(stays))
        stay = HotelStay.objects.get(number=6)
        self.assertEqual(stay, stays.first())

        #21.04.
        hotel = Hotel.objects.get(number=1)
        self.assertEqual(0, len(get_stays(hotel, day(6))))
        hotel = Hotel.objects.get(number=2)
        self.assertEqual(0, len(get_stays(hotel, day(6))))
        hotel = Hotel.objects.get(number=4)
        self.assertEqual(0, len(get_stays(hotel, day(6))))

        hotel = Hotel.objects.get(number=3)
        stays = get_stays(hotel, day(6))
        self.assertEqual(1, len(stays))
        stay = HotelStay.objects.get(number=6)
        self.assertEqual(stay, stays.first())

        #22.04
        for i in range(1,5):
            hotel = Hotel.objects.get(number=i)
            self.assertEqual(0, len(get_stays(hotel, day(7))))
        #23.04
        for i in range(1,5):
            hotel = Hotel.objects.get(number=i)
            self.assertEqual(0, len(get_stays(hotel, day(8))))
        #24.04
        for i in range(1,4):
            hotel = Hotel.objects.get(number=i)
            self.assertEqual(0, len(get_stays(hotel, day(9))))
        hotel = Hotel.objects.get(number=4)
        stay = HotelStay.objects.get(number=7)
        stays = get_stays(hotel, day(9))
        self.assertEqual(stay, stays.first())
        self.assertEqual(1, len(stays))

        for i in range(1,4):
            hotel = Hotel.objects.get(number=i)
            self.assertEqual(0, len(get_stays(hotel, day(300))))
        hotel = Hotel.objects.get(number=4)
        stay = HotelStay.objects.get(number=7)
        stays = get_stays(hotel, day(300))
        self.assertEqual(stay, stays.first())
        self.assertEqual(1, len(stays))

        for i in range(1,4):
            hotel = Hotel.objects.get(number=i)
            self.assertEqual(0, len(get_stays(hotel, day(374))))
        hotel = Hotel.objects.get(number=4)
        stay = HotelStay.objects.get(number=7)
        stays = get_stays(hotel, day(374))
        self.assertEqual(stay, stays.first())
        self.assertEqual(1, len(stays))

    def test_get_requests(self):
        stays = HotelStay.objects.filter(number=1)
        requests = get_requests(stays)
        self.assertEqual(len(requests), 1)
        request = HousingRequest.objects.get(number=1)
        self.assertEqual(requests.first(), request)
        self.assertEqual(len(requests), 1)
        stays = HotelStay.objects.none()
        requests = get_requests(stays)
        self.assertEqual(0, len(requests))

        stays = HotelStay.objects.filter(number__in= [2,3,4])
        requests = get_requests(stays).order_by('number')
        self.assertEqual(3, len(requests))
        self.assertEqual(HousingRequest.objects.get(number=1), requests[0])
        self.assertEqual(HousingRequest.objects.get(number=2), requests[1])
        self.assertEqual(HousingRequest.objects.get(number=3), requests[2])
        
    def test_get_departing(self):
        for i in range(1,5):
            hotel = Hotel.objects.get(number = i)
            departing = get_departing_stays(hotel, day(0))
            self.assertEqual(len(departing), 0)

        hotel = Hotel.objects.get(number = 1)
        departing = get_departing_stays(hotel, day(1))
        self.assertEqual(1, len(departing))
        self.assertEqual(departing[0], HotelStay.objects.get(number=1))
        for i in range(2,5):
            hotel = Hotel.objects.get(number = i)
            departing = get_departing_stays(hotel, day(1))
            self.assertEqual(len(departing), 0)
        
        for i in range(1,5):
            hotel = Hotel.objects.get(number = i)
            departing = get_departing_stays(hotel, day(2))
            self.assertEqual(len(departing), 0)
        
        hotel = Hotel.objects.get(number= 1)
        departing = get_departing_stays(hotel, day(3)).order_by('number')
        self.assertEqual(len(departing), 3)
        self.assertEqual(departing[0], HotelStay.objects.get(number=2))
        self.assertEqual(departing[1], HotelStay.objects.get(number=3))
        self.assertEqual(departing[2], HotelStay.objects.get(number=4))

        for i in range(2,5):
            hotel = Hotel.objects.get(number = i)
            departing = get_departing_stays(hotel, day(3))
            self.assertEqual(len(departing), 0)

        hotel = Hotel.objects.get(number=2)
        departing = get_departing_stays(hotel, day(4)).order_by('number')
        self.assertEqual(len(departing), 1)
        self.assertEqual(departing[0], HotelStay.objects.get(number=5))

        for i in [1,3,4]:
            hotel = Hotel.objects.get(number = i)
            departing = get_departing_stays(hotel, day(4))
            self.assertEqual(len(departing), 0)
        for j in [5,6]:
            for i in range(1,5):
                hotel = Hotel.objects.get(number = i)
                departing = get_departing_stays(hotel, day(j))
                self.assertEqual(len(departing), 0)

    

    def test_arriving(self):
        hotel = Hotel.objects.get(number=1)
        stay = HotelStay.objects.get(number=1)
        stays = get_arriving_stays(hotel, day(0))
        self.assertEqual(len(stays), 1)
        self.assertEqual(stays.first(), stay)
        for i in range(2,5):
            hotel = Hotel.objects.get(number=i)
            stays = get_arriving_stays(hotel, day(0))
            self.assertEqual(len(stays), 0)
        
        hotel = Hotel.objects.get(number=1)
        correct = HotelStay.objects.filter(number__in=[2,3,4]).order_by('number')
        stays = get_arriving_stays(hotel, day(1)).order_by('number')
        self.assertEqual(len(stays), 3)
        self.assertListEqual(list(correct), list(stays))

        for i in range(2,5):
            hotel = Hotel.objects.get(number=i)
            stays = get_arriving_stays(hotel, day(1))
            self.assertEqual(len(stays), 0)
        
        for i in range(1,5):
            hotel = Hotel.objects.get(number=i)
            stays = get_arriving_stays(hotel, day(2))
            self.assertEqual(len(stays), 0)

        for i in [1,3,4]:
            hotel = Hotel.objects.get(number=i)
            stays = get_arriving_stays(hotel, day(3))
            self.assertEqual(len(stays), 0)
        hotel = Hotel.objects.get(number=2)
        stays = get_arriving_stays(hotel, day(3))
        self.assertEqual(len(stays), 1)
        self.assertAlmostEqual(stays.first(), HotelStay.objects.get(number=5))

        for i in range(1,5):
            hotel = Hotel.objects.get(number=i)
            stays = get_arriving_stays(hotel, day(4))
            self.assertEqual(len(stays), 0)


        for i in range(1,4):
            hotel = Hotel.objects.get(number=i)
            stays = get_arriving_stays(hotel, day(9))
            self.assertEqual(len(stays), 0)
        hotel = Hotel.objects.get(number=4)
        stays = get_arriving_stays(hotel, day(9))
        self.assertEqual(len(stays), 1)
        self.assertAlmostEqual(stays.first(), HotelStay.objects.get(number=7))

        for j in [30,31,364,365,366,1000,9999]:
            for i in range(1,5):
                hotel = Hotel.objects.get(number=i)
                stays = get_arriving_stays(hotel, day(j))
                self.assertEqual(len(stays), 0)
        



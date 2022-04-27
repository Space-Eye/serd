from asyncio.log import logger
import logging
from django.core.management.base import BaseCommand, CommandError
from serd.models import HotelStay, HousingRequest
from datetime import datetime

logger = logging.getLogger('default')
class Command(BaseCommand):
    help = 'Sets hotel to null for all requests that depart today.'

    def handle(self, *args, **options):
        today = datetime.now().date()
        logger.info("set_hotels_null executed at %s", str(datetime.now()))
        try:
            departing = HotelStay.objects.filter(departure_date=today)
        except Exception as e:
            logger.error("Error while getting departures from db: %s",e)
            return

        logger.info("Found %s departures", departing.count())
        for stay in departing:
            logger.info('deparing: %s', str(stay))
            stay.request.hotel = None
            stay.request.save()
            logger.info('done')
        logger.info("command done")

            



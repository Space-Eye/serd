from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField
from .choices import CURRENT_ACCOMODATION, LANGUAGE_CHOICE, LIVING_WITH, PRIORITY_CHOICE, LIVING_WITH, OFFER_STATE, PETS, REQUEST_STATE


class  HousingRequest(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=128)
    given_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=50)
    mail = models.CharField(max_length=256)
    representative = models.CharField(max_length=256)
    repr_phone = models.CharField(max_length=256)
    repr_mail = models.CharField(max_length=256)
    adults = models.PositiveSmallIntegerField()
    children = models.PositiveSmallIntegerField()
    who = models.CharField(max_length=256)
    split = models.BooleanField()
    current_housing = models.CharField(choices=CURRENT_ACCOMODATION, max_length=128)
    arrival_date = models.DateField()
    arrival_location = models.CharField(max_length=256)
    pets = MultiSelectField(choices=PETS)
    pet_number = models.PositiveSmallIntegerField()
    car = models.BooleanField()
    languages = MultiSelectField(choices=LANGUAGE_CHOICE)
    vaccination = models.BooleanField()
    accessability_needs = models.BooleanField()
    case_handler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(choices=PRIORITY_CHOICE, max_length=64)
    placed_at = models.ForeignKey('Offer', on_delete=models.SET_NULL, null=True)
    state = models.TextField(choices=REQUEST_STATE)
    private_comment = models.TextField(blank=True, null=True)
    def __str__(self):
        return "_".join([self.last_name, self.given_name,str(self.id)])


class Offer(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=128)
    given_name = models.CharField(max_length=128)
    plz = models.CharField(max_length=5)
    street = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    phone = models.CharField(max_length=50)
    mail = models.CharField(max_length=256)
    language = MultiSelectField(choices=LANGUAGE_CHOICE)
    cost = models.PositiveSmallIntegerField()
    spontan = models.BooleanField()
    available_from = models.DateField()
    limited_availability = models.BooleanField()
    available_until = models.DateField()
    accessability = models.BooleanField()
    public_transport = models.BooleanField()
    rooms = models.SmallIntegerField()
    seperate_appartment = models.BooleanField()
    living_with = models.CharField(choices=LIVING_WITH, max_length=64)
    pets = MultiSelectField(choices=PETS)
    state = models.CharField(choices=OFFER_STATE, max_length=64)
    comment = models.TextField(blank=True)
    private_comment = models.TextField(blank=True)
    def __str__(self):
        return "_".join([self.last_name, self.given_name,str(self.id)])
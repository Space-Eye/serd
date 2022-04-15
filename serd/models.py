from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from .choices import CURRENT_ACCOMODATION, FOOD_CHOICES, HOTEL_STATE, LANGUAGE_CHOICE, LIVING_WITH, PRIORITY_CHOICE, LIVING_WITH, OFFER_STATE, PETS, REQUEST_STATE
from .validators import validate_plz, validate_phone, validate_not_negative
from django.contrib.auth.models import User
class AnnotationManager(models.Manager):

    def __init__(self, **kwargs):
        super().__init__()
        self.annotations = kwargs

    def get_queryset(self):
        return super().get_queryset().annotate(**self.annotations)

class  HousingRequest(models.Model):
    number = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=128, verbose_name=_("Nachname"))
    given_name = models.CharField(max_length=128, verbose_name=_("Vorname"))
    name_slug = models.CharField(max_length=256, blank=True, default="")
    phone = models.CharField(max_length=50, validators=[validate_phone], verbose_name=_("Telephonnummer"))
    mail = models.CharField(max_length=256, validators=[validate_email],verbose_name=_("E-Mail Adresse"))
    representative = models.CharField(max_length=256, blank='true')
    repr_phone = models.CharField(max_length=256, blank='true', validators=[validate_phone])
    repr_mail = models.CharField(max_length=256, validators=[validate_email])
    adults = models.PositiveSmallIntegerField(verbose_name=_("Anzahl Erwachsener"), validators=[validate_not_negative])
    children = models.PositiveSmallIntegerField(verbose_name=_("Anzahl Kinder"), validators=[validate_not_negative])
    who = models.CharField(max_length=256, verbose_name=_("Kurze Beschreibung"))
    split = models.BooleanField(verbose_name=_("Gruppe darf geteilt werden"))
    current_housing = models.CharField(choices=CURRENT_ACCOMODATION, max_length=128, verbose_name=_("Aktuelle Unterbringung"))
    arrival_date = models.DateField(verbose_name=_("Ankunftstag"))
    arrival_location = models.CharField(max_length=256, verbose_name=("Ankunftsort"))
    pets = MultiSelectField(choices=PETS, verbose_name=_("Haustiere"))
    pet_number = models.PositiveSmallIntegerField(verbose_name=_("Anzahl der Haustiere"), null=True, validators=[validate_not_negative])
    car = models.BooleanField(verbose_name=_("Auto verfügbar"))
    languages = MultiSelectField(choices=LANGUAGE_CHOICE, verbose_name=_("Gesprochene Sprachen"))
    vaccination = models.BooleanField(verbose_name=_("Alle Personen vollständig geimpft"))
    accessability_needs = models.BooleanField(_("Barrierefreie Wohnung benötigt"))
    case_handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Sachbearbeiter:in"))
    priority = models.CharField(choices=PRIORITY_CHOICE, max_length=64, verbose_name=_("Priorität"))
    placed_at = models.ForeignKey('Offer', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Vermitttelt an"))
    hotel = models.ForeignKey('Hotel', on_delete=models.SET_NULL, null=True, verbose_name="Hotel", related_name='requests', blank=True)
    state = models.CharField(choices=REQUEST_STATE, verbose_name=_("Status"), default="new", max_length=64)
    private_comment = models.CharField(blank=True, null=True, verbose_name=_("Interner Kommentar"), default="", max_length=64)
    created_at = models.DateField(auto_now_add=True)

    _persons = None

    objects = AnnotationManager(persons=models.F('adults')+models.F('children'))
    def __str__(self):
        return "_".join([self.last_name, self.given_name,str(self.number)])
    class Meta:
        app_label ='serd'

class Offer(models.Model):
    number = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=128, verbose_name=_("Nachname"))
    given_name = models.CharField(max_length=128, verbose_name=_("Vorname"))
    plz = models.CharField(max_length=5, validators=[validate_plz], verbose_name=_("Postleitzahl"))
    total_number = models.PositiveSmallIntegerField(default=1, verbose_name=_("Gesamtanzahl der Personen"), validators=[validate_not_negative])
    children_number = models.PositiveSmallIntegerField(null=True, verbose_name=_("davon Kinder unter zwölf"), validators=[validate_not_negative])
    street = models.CharField(max_length=256, blank=True, verbose_name=_("Straße (optional"))
    city = models.CharField(max_length=256, verbose_name=_("Ort"))
    phone = models.CharField(max_length=50, validators=[validate_phone], verbose_name=_("Telephonnummer"))
    mail = models.CharField(max_length=256, validators=[validate_email], verbose_name=_("E-mail Adresse"))
    language = MultiSelectField(choices=LANGUAGE_CHOICE, verbose_name=_("Gesprochene Sprachen"),null=True)
    for_free = models.BooleanField(_("kostenfreie Unterkunft"))
    cost = models.PositiveSmallIntegerField( verbose_name=_("Monatsmiete"), null=True, validators=[validate_not_negative])
    spontan = models.BooleanField(verbose_name=_("Spontan Verfügbar"))
    available_from = models.DateField(verbose_name=_("Verfügbar Ab"))
    limited_availability = models.BooleanField(verbose_name=_("Nur vorrübergehend Verfügbar"))
    available_until = models.DateField( verbose_name=_("Verfügbar bis"), null=True)
    accessability = models.BooleanField( verbose_name=_("Barrierefrei"))
    public_transport = models.BooleanField(verbose_name=_("Mit ÖPNV Erreichbar"))
    rooms = models.SmallIntegerField(verbose_name=_("Anzahl Zimmer"))
    seperate_appartment = models.BooleanField(verbose_name=_("Unterkunft ist eine eigenständige Wohnung"))
    living_with = models.CharField(choices=LIVING_WITH, max_length=64, verbose_name=_("Meine Wohnsituation"), blank=True)
    pets = MultiSelectField(choices=PETS,verbose_name=_("Haustiere Erlaubt"))
    state = models.CharField(choices=OFFER_STATE, max_length=64, verbose_name=_("Status"),default="new")
    comment = models.CharField(blank=True, verbose_name=_("Kommentar"), max_length=512)
    private_comment = models.CharField(blank=True, verbose_name=("Interner Kommentar"), default="", max_length=512)
    by_municipality = models.BooleanField(default=False, verbose_name="Von Stadt Vermittelt")
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return "_".join([self.last_name, self.given_name,str(self.number)])
    class Meta:
        app_label ='serd'



class AnsprechpartnerHotel(models.Model):
    number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name="Name")
    tel = models.CharField(max_length=128, validators=[validate_phone], verbose_name="Telefonnummer", blank=True)
    mail = models.CharField(max_length=128, verbose_name="E-mail", validators=[validate_email], blank=True)
    hotel = models.ForeignKey('Hotel', on_delete=models.SET_NULL, null=True, related_name="ansprechpartner")
    def __str__(self) -> str:
        return "_".join([str(self.number), self.name])

    class Meta:
        app_label ='serd'

class Hotel(models.Model):
    number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name="Name")
    address = models.TextField(verbose_name="Adresse")
    state = models.CharField(max_length=64, choices=HOTEL_STATE, verbose_name="Status")
    responsible =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, 
                                    blank=True, verbose_name="Zuständig Meldung", related_name='responsible_for_hotel')
    team_gesamt = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Team gesamt", related_name='tem_for_hotel')
    food = models.CharField(choices=FOOD_CHOICES, max_length=64, verbose_name="Verpflegung", blank=True)
    cost = models.CharField(max_length=128, verbose_name="Kosten")
    beds_adults = models.PositiveSmallIntegerField(verbose_name="Betten Erwachsene", validators=[validate_not_negative])
    beds_children = models.PositiveSmallIntegerField(verbose_name="Betten Kinder", validators=[validate_not_negative])
    adults_free = models.IntegerField(null=True, blank=True, verbose_name="NICHTS EINTRAGEN, TECHNISCHES FELD, KOMMT BALD WEG")
    children_free = models.IntegerField(null=True, blank=True, verbose_name="NICHTS EINTRAGEN, TECHNISCHES FELD, KOMMT BALD WEG")
    info = models.TextField(verbose_name="Info", blank=True)
    def __str__(self) -> str:
        return "_".join([str(self.number), self.name])
    def save(self, *args, **kwargs):
        adults = 0
        children =0
        for request in self.requests.all():
            adults += request.adults
            children += request.children
        self.adults_free = self.beds_adults - adults
        self.children_free = self.beds_children -children
        super(Hotel, self).save(*args, **kwargs)
    class Meta:
        app_label ='serd'


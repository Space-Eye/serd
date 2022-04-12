from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from .choices import CURRENT_ACCOMODATION, LANGUAGE_CHOICE, LIVING_WITH, PRIORITY_CHOICE, LIVING_WITH, OFFER_STATE, PETS, REQUEST_STATE
from .validators import validate_plz, validate_phone

class AnnotationManager(models.Manager):

    def __init__(self, **kwargs):
        super().__init__()
        self.annotations = kwargs

    def get_queryset(self):
        return super().get_queryset().annotate(**self.annotations)

class  HousingRequest(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=128, verbose_name=_("Nachname"))
    given_name = models.CharField(max_length=128, verbose_name=_("Vorname"))
    name_slug = models.CharField(max_length=256, blank=True, default="")
    phone = models.CharField(max_length=50, validators=[validate_phone], verbose_name=_("Telephonnummer"))
    mail = models.CharField(max_length=256, validators=[validate_email],verbose_name=_("E-Mail Adresse"))
    representative = models.CharField(max_length=256, blank='true')
    repr_phone = models.CharField(max_length=256, blank='true', validators=[validate_phone])
    repr_mail = models.CharField(max_length=256, validators=[validate_email])
    adults = models.PositiveSmallIntegerField(verbose_name=_("Anzahl Erwachsener"))
    children = models.PositiveSmallIntegerField(verbose_name=_("Anzahl Kinder"))
    who = models.CharField(max_length=256, verbose_name=_("Kurze Beschreibung"))
    split = models.BooleanField(verbose_name=_("Gruppe darf geteilt werden"))
    current_housing = models.CharField(choices=CURRENT_ACCOMODATION, max_length=128, verbose_name=_("Aktuelle Unterbringung"))
    arrival_date = models.DateField(verbose_name=_("Ankunftstag"))
    arrival_location = models.CharField(max_length=256, verbose_name=("Ankunftsort"))
    pets = MultiSelectField(choices=PETS, verbose_name=_("Haustiere"))
    pet_number = models.PositiveSmallIntegerField(verbose_name=_("Anzahl der Haustiere"), null=True)
    car = models.BooleanField(verbose_name=_("Auto verfügbar"))
    languages = MultiSelectField(choices=LANGUAGE_CHOICE, verbose_name=_("Gesprochene Sprachen"))
    vaccination = models.BooleanField(verbose_name=_("Alle Personen vollständig geimpft"))
    accessability_needs = models.BooleanField(_("Barrierefreie Wohnung benötigt"))
    case_handler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Sachbearbeiter:in"))
    priority = models.CharField(choices=PRIORITY_CHOICE, max_length=64, verbose_name=_("Priorität"))
    placed_at = models.ForeignKey('Offer', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Vermitttelt an"))
    state = models.TextField(choices=REQUEST_STATE, verbose_name=_("Status"), default="new")
    private_comment = models.TextField(blank=True, null=True, verbose_name=_("Interner Kommentar"), default="")
    _persons = None

    objects = AnnotationManager(persons=models.F('adults')+models.F('children'))
    def __str__(self):
        return "_".join([self.last_name, self.given_name,str(self.id)])


class Offer(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=128, verbose_name=_("Nachname"))
    given_name = models.CharField(max_length=128, verbose_name=_("Vorname"))
    plz = models.CharField(max_length=5, validators=[validate_plz], verbose_name=_("Postleitzahl"))
    total_number = models.PositiveSmallIntegerField(default=1, verbose_name=_("Gesamtanzahl der Personen"))
    children_number = models.PositiveSmallIntegerField(null=True, verbose_name=_("davon Kinder unter zwölf"))
    street = models.CharField(max_length=256, blank=True, verbose_name=_("Straße (optional"))
    city = models.CharField(max_length=256, verbose_name=_("Ort"))#toDo Personenanzahl
    phone = models.CharField(max_length=50, validators=[validate_phone], verbose_name=_("Telephonnummer"))
    mail = models.CharField(max_length=256, validators=[validate_email], verbose_name=_("E-mail Adresse"))
    language = MultiSelectField(choices=LANGUAGE_CHOICE, verbose_name=_("Gesprochene Sprachen"))#toDo kostenfrei
    cost = models.PositiveSmallIntegerField( verbose_name=_("Monatsmiete"))
    spontan = models.BooleanField(verbose_name=_("Spontan Verfügbar"))
    available_from = models.DateField(verbose_name=_("Verfügbar Ab"))
    limited_availability = models.BooleanField(verbose_name=_("Nur vorrübergehend Verfügbar"))
    available_until = models.DateField( verbose_name=_("Verfügbar bis"))
    accessability = models.BooleanField( verbose_name=_("Barrierefrei"))
    public_transport = models.BooleanField(verbose_name=_("Mit ÖPNV Erreichbar"))
    rooms = models.SmallIntegerField(verbose_name=_("Anzahl Zimmer"))
    seperate_appartment = models.BooleanField(verbose_name=_("Unterkunft ist eine eigenständige Wohnung"))
    living_with = models.CharField(choices=LIVING_WITH, max_length=64, verbose_name=_("Meine Wohnsituation"), blank=True)
    pets = MultiSelectField(choices=PETS,verbose_name=_("Haustiere Erlaubt"))
    state = models.CharField(choices=OFFER_STATE, max_length=64, verbose_name=_("Status"),default="new")
    comment = models.TextField(blank=True, verbose_name=_("Kommentar"))
    private_comment = models.TextField(blank=True, verbose_name=("Interner Kommentar"), default="")
    def __str__(self):
        return "_".join([self.last_name, self.given_name,str(self.id)])
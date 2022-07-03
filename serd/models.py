from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .choices import CURRENT_ACCOMODATION, FOOD_CHOICES, HOTEL_STATE, LANGUAGE_CHOICE, LIVING_WITH, MENTOR_STATE, OFFER_SORT, PRIORITY_CHOICE, LIVING_WITH, OFFER_STATE, PETS, REQUEST_SORT, REQUEST_STATE, SORT_DIRECTION
from .validators import validate_not_empty, validate_plz, validate_phone, validate_not_negative



User = get_user_model()


class RequestFilter(models.Model):
    num_min = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Personen von")
    num_max = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Personen bis")
    split = models.BooleanField(null=True, verbose_name="Teilbar")
    current_housing = models.CharField(blank=True, choices=CURRENT_ACCOMODATION, verbose_name="Aktuelle Unterbringung", max_length=64)
    pets = MultiSelectField(choices=PETS, null=True, blank=True,  verbose_name="Haustiere")
    languages = MultiSelectField(choices=LANGUAGE_CHOICE, null=True, blank=True, verbose_name="Sprachen")
    accessability_needs = models.BooleanField(null=True,  verbose_name="Barrierefrei")
    priority = MultiSelectField(choices=PRIORITY_CHOICE, null=True, blank=True, verbose_name="Priorität")
    state = MultiSelectField(choices=REQUEST_STATE, null=True, blank=True, verbose_name="Status")
    no_handler = models.BooleanField(null=True, verbose_name="Kein Sachbearbeiter")
    case_handler = models.ForeignKey(to=User, on_delete=models.SET_NULL,  null=True, blank=True)
    sort = models.CharField(choices=REQUEST_SORT, default='number', verbose_name='Sortierung', max_length=64)
    sort_direction = models.CharField(choices=SORT_DIRECTION, default='asc', verbose_name='Auf/Absteigend', max_length=64)


class OfferFilter(models.Model):
    num_min = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Personen von")
    num_max = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Personen bis")
    PLZ = models.CharField(max_length=5, blank=True, verbose_name='PLZ')
    city = models.CharField(max_length=128, blank=True, verbose_name='Ort')
    cost_min = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Kosten von')
    cost_max = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Kosten bis')
    language = MultiSelectField(choices=LANGUAGE_CHOICE, blank=True, verbose_name="Sprachen")
    spontan = models.BooleanField(null=True,  verbose_name='Spontan')
    limited = models.BooleanField(null=True, verbose_name='Begrenzt verfügbar')
    appartment = models.BooleanField(null=True, verbose_name='Eigene Wohnung')
    pets = MultiSelectField(choices=PETS, null=True, blank=True, verbose_name='Haustiere')
    accessability = models.BooleanField(null=True, verbose_name="Barrierefrei")
    state = MultiSelectField(choices=OFFER_STATE, verbose_name='Status', null=True, blank=True)
    for_free = models.BooleanField(null=True, verbose_name='Gratis')
    sort = models.CharField(choices=OFFER_SORT, default='number', verbose_name='Sortierung', max_length=64)
    sort_direction = models.CharField(choices=SORT_DIRECTION, default='asc', verbose_name='Auf/Absteigend', max_length=64)

class Profile(models.Model):
    number = models.AutoField(primary_key=True)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Account")
    name = models.CharField(max_length=64, blank=True)
    mail = models.CharField(max_length=256, validators=[validate_email],verbose_name= "E-Mail-Adresse", blank=True)
    phone = models.CharField(max_length=50, validators=[validate_phone], verbose_name= "Telefonnummer", blank=True)
    telegram = models.CharField(max_length=64, verbose_name="Telegram", blank=True)
    threema = models.CharField(max_length=64, verbose_name="Threema", blank=True)
    whatsapp = models.BooleanField(verbose_name="Whatsapp")
    signal = models.BooleanField(verbose_name="Signal")
    languages = MultiSelectField(choices=LANGUAGE_CHOICE, verbose_name="Sprachkenntnisse", null=True, blank=True)
    comment = models.CharField(max_length=128, verbose_name="Kommentar", blank=True)
    request_filter = models.OneToOneField(to=RequestFilter, null=True, blank=True, on_delete=models.SET_NULL)
    offer_filter = models.OneToOneField(to=OfferFilter, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self) -> str:
        return self.account.username



class AnnotationManager(models.Manager):

    def __init__(self, **kwargs):
        super().__init__()
        self.annotations = kwargs

    def get_queryset(self):
        return super().get_queryset().annotate(**self.annotations)

class  HousingRequest(models.Model):
    number = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=128, verbose_name=_("Nachname"),blank=True)
    given_name = models.CharField(max_length=128, verbose_name=_("Vorname"), blank=True)
    name_slug = models.CharField(max_length=256, blank=True, default="")
    phone = models.CharField(max_length=50, validators=[validate_phone], verbose_name=_("Telefonnummer"), blank=True)
    mail = models.CharField(max_length=256, validators=[validate_email],verbose_name=_("E-Mail-Adresse"), blank=True)
    representative = models.CharField(max_length=256, blank=True, verbose_name=_("Name einer stellvertretenden Person"), help_text=_("falls zutreffend"))
    repr_phone = models.CharField(max_length=256, blank=True, validators=[validate_phone], verbose_name=_("Telefonnummer der stellvertretenden Person"))
    repr_mail = models.CharField(max_length=256, blank=True, validators=[validate_email], verbose_name=_("E-Mail-Adresse der stellvertretenden Person"))
    adults = models.PositiveSmallIntegerField(verbose_name=_("Anzahl der Erwachsenen und Kindern ab 12 Jahren"), validators=[validate_not_negative], blank=True)
    children = models.PositiveSmallIntegerField(verbose_name=_("Anzahl der Kinder unter 12"), validators=[validate_not_negative], blank=True)
    who = models.CharField(max_length=512, blank=True)
    split = models.BooleanField(verbose_name=_("Ab fünf Personen: Gruppe darf geteilt werden"), help_text=_("notfalls kann eine Unterbringung in zwei Unterkünften erfolgen"))
    current_housing = models.CharField(choices=CURRENT_ACCOMODATION, max_length=128, verbose_name=_("Wo sind Sie aktuell untergebracht?"), blank=True)
    arrival_date = models.DateField(verbose_name=_("Wann kommen Sie in Regensburg an oder seit wann sind Sie da?"), null=True)
    pets = MultiSelectField(choices=PETS, verbose_name=_("Welche Haustiere haben Sie?"), null=True)
    pet_number = models.PositiveSmallIntegerField(verbose_name=_("Wie viele Haustiere haben Sie?"), validators=[validate_not_negative], blank=True, null=True)
    car = models.BooleanField(verbose_name=_("Haben Sie ein Auto?"))
    languages = MultiSelectField(choices=LANGUAGE_CHOICE, verbose_name=_("Sprachkenntnisse"), null=True, blank=True)
    additional_languages = models.CharField(verbose_name=_("Weitere Sprachen"), max_length=64, blank=True)
    vaccination = models.BooleanField(verbose_name=_("Sind alle Personen in Ihrer Gruppe vollständig gegen COVID-19 geimpft?"))
    accessability_needs = models.BooleanField(_("Wird eine barrierefreie Wohnung benötigt?"))
    can_pay = models.BooleanField(verbose_name=_("Können Sie für Ihre Unterkunft zahlen?"), help_text=_("Keine Voraussetzung für die Vermittlung einer privaten Notunterkunft"))
    case_handler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Sachbearbeiter:in"))
    priority = models.CharField(choices=PRIORITY_CHOICE, max_length=64, verbose_name=_("Priorität"), blank=True)
    placed_at = models.ForeignKey('Offer', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Vermitttelt an"))
    state = models.CharField(choices=REQUEST_STATE, verbose_name=_("Status"), default="new", max_length=64)
    private_comment = models.CharField(blank=True, null=True,  default="", max_length=1024)
    created_at = models.DateField(auto_now_add=True)
    possible_hosts = models.ManyToManyField(to='Offer', related_name="possible_guests", blank=True, verbose_name="Mögliche Gastgeber")
    smoker = models.BooleanField(verbose_name=_("Raucht jemand aus Ihrer Gruppe?"))
    profession = models.CharField(verbose_name=_("Welchen Beruf üben Sie aus?"), max_length=64, null=True, blank=True)
    _persons = None

    objects = AnnotationManager(persons=models.F('adults')+models.F('children'))
    def __str__(self):
        return "_".join([str(self.number),self.last_name, self.given_name])
    class Meta:
        app_label ='serd'

class Offer(models.Model):
    number = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=128, verbose_name=_("Nachname"), blank=True, validators=[validate_not_empty])
    given_name = models.CharField(max_length=128, verbose_name=_("Vorname"), blank=True)
    plz = models.CharField(max_length=5, validators=[validate_plz], verbose_name=_("Postleitzahl"), blank=True)
    total_number = models.PositiveSmallIntegerField(verbose_name=_("Anzahl der Personen, die in dieser Wohnung eine Unterkunft finden können."), validators=[validate_not_negative], blank=True)
    children_number = models.PositiveSmallIntegerField(blank=True, verbose_name=_("Anzahl der zuvor genannten Plätze, die nur für Kinder unter 12 geeignet sind."), validators=[validate_not_negative])
    street = models.CharField(max_length=256, blank=True, verbose_name=_("Straße, Hausnummer (optional)"))
    city = models.CharField(max_length=256, verbose_name=_("Ort"), blank=True)
    mail = models.CharField(max_length=256, validators=[validate_email], verbose_name=_("E-Mail-Adresse"), blank=True)
    language = MultiSelectField(choices=LANGUAGE_CHOICE, verbose_name=_("Welche Sprachen sprechen Sie?"),  default=['de'], blank=True, null=True)
    additional_languages = models.CharField(verbose_name=_("Weitere Sprachen"), max_length=64, blank=True)
    for_free = models.BooleanField(verbose_name=_("Ich stelle die Unterkunft mindestens vorübergehend kostenlos zur Verfügung."))
    cost = models.PositiveSmallIntegerField(null=True, validators=[validate_not_negative])
    spontan = models.BooleanField(verbose_name=_("spontanes zur Verfügung stellen ist möglich"), help_text=_("innerhalb eines Tages"))
    available_from = models.DateField(verbose_name=_("Ab wann steht die Unterkunft zur Verfügung?"))
    limited_availability = models.BooleanField(verbose_name=_("Die Unterkunft wird nur zeitlich begrenzt zur Verfügung gestellt."))
    available_until = models.DateField(null=True)
    accessability = models.BooleanField( verbose_name=_("Ist die Unterkunft barrierefrei?"))
    public_transport = models.BooleanField(verbose_name=_("Ist die Unterkunft mit öffentlichen Verkehrsmitteln erreichbar? "))
    rooms = models.SmallIntegerField(verbose_name=_("Anzahl der zur Verfügung gestellten Zimmer"), blank=True)
    seperate_appartment = models.BooleanField(verbose_name=_("Unterkunft erfolgt in einer separaten Wohnung."))
    living_with = models.CharField(choices=LIVING_WITH, max_length=64, verbose_name=_("Bei Unterbringung in der eigenen Wohnung: Ich wohne"), blank=True)
    pets = MultiSelectField(choices=PETS,verbose_name=_("Folgende Haustiere sind erlaubt."))
    state = models.CharField(choices=OFFER_STATE, max_length=64, verbose_name=_("Status"),default="new")
    phone = models.CharField(max_length=128, validators=[validate_phone], verbose_name=_("Telefonnummer"), blank=True)
    mail = models.CharField(max_length=128, verbose_name=_("E-mail"), validators=[validate_email], blank=True)
    comment = models.TextField(blank=True)
    private_comment = models.CharField(blank=True, default="", max_length=512)
    by_municipality = models.BooleanField(default=False, verbose_name="Von Stadt Vermittelt")
    covid = models.BooleanField(default=False, verbose_name=_("Eine COVID-19-Impfung ist zwingend notwendig."))
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return "_".join([str(self.number),self.last_name, self.given_name])



class AnsprechpartnerHotel(models.Model):
    number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name="Name")
    tel = models.CharField(max_length=128, validators=[validate_phone], verbose_name="Telefonnummer", blank=True)
    mail = models.CharField(max_length=128, verbose_name="E-mail", validators=[validate_email], blank=True)
    hotel = models.ManyToManyField('Hotel',  related_name="ansprechpartner")
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
    beds = models.PositiveSmallIntegerField(verbose_name="Betten", validators=[validate_not_negative])
    info = models.TextField(verbose_name="Info", blank=True)
    visible = models.BooleanField(verbose_name="Sichtbar", default=True)
    def __str__(self) -> str:
        return "_".join([str(self.number), self.name])
    class Meta:
        app_label ='serd'


class NewsItem(models.Model):
    number = models.AutoField(primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    text = models.TextField()
    headline = models.CharField(max_length=128)
    class Meta:
        ordering = ('-number',)


class HotelStay(models.Model):
    number = models.AutoField(primary_key=True) 
    arrival_date = models.DateField(verbose_name="Ankunftstag")
    departure_date = models.DateField(verbose_name="Abreisetag", blank=True, null=True)
    room = models.CharField(blank=True, max_length=64)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='stays')
    request = models.ForeignKey(HousingRequest, on_delete=models.CASCADE, related_name='stays')
    def __str__(self) -> str:
        return "_".join([str(self.hotel), str(self.request)])

class Pate(models.Model):
    number = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=128, verbose_name=_("Nachname"), blank=True, validators=[validate_not_empty])
    given_name = models.CharField(max_length=128, verbose_name=_("Vorname"), blank=True)
    city = models.CharField(max_length=256, verbose_name=_("Wohnort"), blank=True)
    district = models.CharField(max_length=128, verbose_name=_('Stadtteil'), blank=True)
    languages = MultiSelectField(choices=LANGUAGE_CHOICE, verbose_name=_("Sprachkenntnisse"), null=True, blank=True)
    additional_languages = models.CharField(verbose_name=_("Weitere Sprachen"), max_length=64, blank=True)
    phone = models.CharField(max_length=50, validators=[validate_phone], verbose_name=_("Telefonnummer"), blank=True)
    mail = models.CharField(max_length=256, validators=[validate_email],verbose_name=_("E-Mail-Adresse"), blank=True)
    comment = models.TextField(blank=True, verbose_name=_('Kommentar'))
    state = models.CharField(choices=MENTOR_STATE, default='new', max_length=64)
    def __str__(self) -> str:
        return ' '.join([str(self.number), str(self.given_name), str(self.last_name)])
from django.utils.translation import gettext_lazy as _

REQUEST_STATE = (
    ('new','Neu'),
    ('contacted','Kontaktiert'),
    ('stale', 'nicht mehr aktuell'),
    ('housing_contact', 'Kontakt mit Unterkunft'),
    ('arrived','In Unterkunft angekommen')
)
LANGUAGE_CHOICE = (
    ('de', _('Deutsch')),
    ('uk', _('Ukrainisch')),
    ('ru', _('Russisch')),
    ('en', _('Englisch'))
)
LIVING_WITH = (
    ('single',_('alleine')),
    ('family',_('mit Familie')),
    ('friends', _('mit Freunden'))
)

OFFER_STATE = (
    ('new','Neu'),
    ('contacted', 'Kontaktiert'),
    ('request_contact', 'Kontakt zu Gast'),
    ('arrived', 'Gast ist Angekommen'),
    ('stale', 'Nicht mehr verfügbar'),
    ('free', 'Unterkunft wieder Verfügbar'),
    ('reserved', 'Reserviert')
)
PRIORITY_CHOICE = (
    ('normal','Normal'),
    ('elevated','Erhöht'),
    ('high','Hoch')
)
CURRENT_ACCOMODATION = (
    ('none', _('Ich habe keinen Schlafplatz')),
    ('friends', _('Bei Freunden oder Verwandten')),
    ('shelter', _('Staatliche Notunterkunft')),
    ('hotel', _('Im Hotel')),
)
PETS = (
    ('dog', _('Hund')),
    ('cat', _('Katze')),
    ('small', _('Kleintier')),
    ('none', _('Keine'))
)

HOTEL_STATE = (
    ('aktive', 'Aktiv'),
    ('open', 'offen'),
    ('full', 'Keine Kapaizitäten')
)
FOOD_CHOICES = (
    ('breakfast', 'Frühstück'),
    ('inclusive', 'Inklusive'),
    ('space-eye', 'Durch Space-Eye')
)
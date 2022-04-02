REQUEST_STATE = (
    ('new','Neu'),
    ('contacted','Kontaktiert'),
    ('stale', 'nicht mehr aktuell'),
    ('housing_contact', 'Kontakt mit Unterkunft'),
    ('arrived','In Unterkunft angekommen')
)
LANGUAGE_CHOICE = (
    ('de', 'Deutsch'),
    ('uk', 'Ukrainisch'),
    ('ru', 'Russisch'),
    ('en', 'Englisch')
)
LIVING_WITH = (
    ('single','alleine'),
    ('family','mit Familie'),
    ('friends', 'mit Freunden')
)

OFFER_STATE = (
    ('new','Neu'),
    ('contacted', 'Kontaktiert'),
    ('closed', 'Vermittelt' ),
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
    ('none', 'Ich habe keinen Schlafplatz'),
    ('friends', 'Bei Freunden oder Verwandten'),
    ('hotel', 'Hotel')
)
PETS = (
    ('dog', 'Hund'),
    ('cat', 'Katze'),
    ('small', 'Kleintier')
)